"""Medição da camada de objetos em Postgres local (VTX-152, parte 1).

Uso: python medir_objetos.py 2000   (precisa de initdb/pg_ctl/psql do PostgreSQL no PATH ou em /usr/lib/postgresql/*/bin)
Gera modelo sintético (10 andares, 5 tipos, 10 grupos), extrai objetos, carrega em jsonb,
mede consultas/edições/diff em SQL e a volta ao IFC com `objetos.aplicar`.
"""
import glob, json, os, random, re, subprocess, sys, tempfile, time
import importlib.util
import ifcopenshell, ifcopenshell.api

AQUI = os.path.dirname(os.path.abspath(__file__))
def mod(n):
    sys.path.insert(0, AQUI); s = importlib.util.spec_from_file_location(n, os.path.join(AQUI, f"{n}.py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
r, o = mod("receitas"), mod("objetos")
BIN = next(iter(sorted(glob.glob("/usr/lib/postgresql/*/bin"))), "")
pg = lambda c: os.path.join(BIN, c) if BIN else c
N = int(sys.argv[1]); random.seed(1); api = ifcopenshell.api
t0 = time.time(); f = r.criar_modelo(); predio = f.by_type("IfcBuilding")[0]
andares = [f.by_type("IfcBuildingStorey")[0]]
for i in range(2, 11):
    a = api.root.create_entity(f, ifc_class="IfcBuildingStorey", name=f"Pav {i}")
    api.aggregate.assign_object(f, products=[a], relating_object=predio); andares.append(a)
tipos = [api.root.create_entity(f, ifc_class="IfcWallType", name=f"Tipo {i}") for i in range(5)]
grupos = [api.group.add_group(f, name=f"Grupo {i}") for i in range(10)]
por_andar, por_tipo, por_grupo = {}, {}, {}
for i in range(N):
    w = r.criar_parede(f, f"P{i}", random.uniform(1, 6), 0.15, 3.0, {"Pset_WallCommon": {"IsExternal": i % 3 == 0}})
    por_andar.setdefault(i % 10, []).append(w); por_tipo.setdefault(i % 5, []).append(w); por_grupo.setdefault(i % 10, []).append(w)
for k, ws in por_andar.items(): api.spatial.assign_container(f, products=ws, relating_structure=andares[k])
for k, ws in por_tipo.items(): api.type.assign_type(f, related_objects=ws, relating_type=tipos[k])
for k, ws in por_grupo.items(): api.group.assign_group(f, products=ws, group=grupos[k])
d = tempfile.mkdtemp(); base = os.path.join(d, "v1.ifc"); f.write(base)
print(f"modelo {N} paredes: {time.time()-t0:.1f} s, {os.path.getsize(base)/1e6:.1f} MB")
t = time.time(); f = ifcopenshell.open(base); print(f"abrir IFC: {time.time()-t:.2f} s")
t = time.time(); objs = o.extrair(f); print(f"extrair objetos: {time.time()-t:.2f} s")
# v2: 1% editado pela "IA"
v2 = json.loads(json.dumps(objs))
for x in random.sample(v2, max(1, N // 100)): x["psets"]["Pset_WallCommon"]["IsExternal"] = not x["psets"]["Pset_WallCommon"]["IsExternal"]
dados = os.path.join(d, "pg"); sock = d
subprocess.run([pg("initdb"), "-D", dados, "-A", "trust", "-U", "vtx", "-E", "UTF8"], check=True, capture_output=True)
subprocess.run([pg("pg_ctl"), "-D", dados, "-o", f"-k {sock} -p 54329 -c listen_addresses=''", "-l", os.path.join(d, "log"), "-w", "start"], check=True, capture_output=True)
try:
    linhas = os.path.join(d, "o.tsv")
    with open(linhas, "w") as fh:
        for v, lista in ((1, objs), (2, v2)):
            for x in lista: fh.write(f"{v}\t{x['globalid']}\t{json.dumps(x, ensure_ascii=False).replace(chr(92), chr(92)*2)}\n")
    alvo = v2[N // 2]["globalid"]
    filtro = json.dumps({"classe": "IfcWall", "andar": {"nome": "Pav 2"}, "psets": {"Pset_WallCommon": {"IsExternal": True}}})
    sql = f"""\\timing on
CREATE TABLE objetos(versao int, globalid text, dados jsonb, PRIMARY KEY(versao, globalid));
\\copy objetos FROM '{linhas}'
CREATE INDEX ON objetos USING gin (dados jsonb_path_ops);
ANALYZE objetos;
SELECT count(*) FROM objetos WHERE versao=2 AND dados @> '{filtro}';
SELECT dados->'andar'->>'nome', count(*) FROM objetos WHERE versao=2 GROUP BY 1 ORDER BY 1 LIMIT 3;
SELECT dados->>'nome' FROM objetos WHERE versao=2 AND globalid='{alvo}';
UPDATE objetos SET dados=jsonb_set(dados,'{{psets,Pset_WallCommon,LoadBearing}}','true') WHERE versao=2 AND globalid='{alvo}';
UPDATE objetos SET dados=jsonb_set(dados,'{{nome}}','"lote"') WHERE versao=2 AND globalid IN (SELECT globalid FROM objetos WHERE versao=2 ORDER BY globalid LIMIT 100);
SELECT count(*) FROM objetos a JOIN objetos b USING (globalid) WHERE a.versao=1 AND b.versao=2 AND a.dados<>b.dados;
SELECT pg_size_pretty(pg_total_relation_size('objetos'));
"""
    out = subprocess.run([pg("psql"), "-h", sock, "-p", "54329", "-U", "vtx", "-d", "postgres", "-At", "-v", "ON_ERROR_STOP=1"],
                         input=sql, text=True, capture_output=True, check=True).stdout
    rot = ["criar tabela", "carga COPY (2 versões)", "índice GIN", "analyze", "consulta paredes externas Pav 2",
           "contagem por andar", "busca por GlobalId", "editar 1 objeto", "editar 100 objetos", "diff v1×v2 em SQL", "tamanho"]
    tempos = re.findall(r"Time: ([\d.]+) ms", out)
    for nome, ms in zip(rot, tempos): print(f"{nome}: {float(ms):.1f} ms")
    print("saídas:", [l for l in out.splitlines() if l and not l.startswith(("Time", "Timing", "CREATE", "COPY", "ANALYZE", "UPDATE"))])
    t = time.time()
    exp = subprocess.run([pg("psql"), "-h", sock, "-p", "54329", "-U", "vtx", "-d", "postgres", "-At", "-c",
                          "SELECT dados FROM objetos WHERE versao=2"], text=True, capture_output=True, check=True).stdout
    editados = [json.loads(l) for l in exp.splitlines()]
    res = o.aplicar(f, editados); f.write(os.path.join(d, "v2.ifc"))
    print(f"volta ao IFC (ler {len(editados)} + aplicar + gravar): {time.time()-t:.2f} s, alterados {res['alterados']}, erros {len(res['erros'])}")
    t = time.time(); dd = r.diff_por_globalid(ifcopenshell.open(base), ifcopenshell.open(os.path.join(d, "v2.ifc")))
    print(f"diff IFC v1×v2 por GlobalId: {time.time()-t:.2f} s, alterados {len(dd['alterados'])}")
finally:
    subprocess.run([pg("pg_ctl"), "-D", dados, "-m", "fast", "stop"], capture_output=True)
