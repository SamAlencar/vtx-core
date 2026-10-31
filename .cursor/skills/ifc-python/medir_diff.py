"""Medição de diff/armazenamento entre duas versões IFC (VTX-151). Uso: python medir_diff.py 2000 (grava v1.ifc, v2.ifc no diretório atual)."""
import sys, time, gzip, difflib, importlib.util, os, random
import ifcopenshell, ifcopenshell.guid, ifcopenshell.api.geometry
spec=importlib.util.spec_from_file_location("r",__import__("os").path.join(__import__("os").path.dirname(__file__),"receitas.py"));r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
N=int(sys.argv[1]); random.seed(1)
t=time.time(); a=r.criar_modelo()
for i in range(N): r.criar_parede(a,f"P{i}",random.uniform(1,6),0.15,3.0,{"Pset_WallCommon":{"IsExternal":i%2==0}})
a.write("v1.ifc"); print("gerar",N,round(time.time()-t,1),"s")
b=ifcopenshell.open("v1.ifc"); ws=b.by_type("IfcWall")
for w in ws[:10]: r.definir_pset(b,w,{"Pset_WallCommon":{"IsExternal":not r.ler_psets(w)["Pset_WallCommon"]["IsExternal"]}})
for w in ws[10:15]: w.Name=w.Name+"-ren"
for w in ws[15:25]: ifcopenshell.api.run("root.remove_product",b,product=w)
for i in range(20): r.criar_parede(b,f"N{i}",2,0.15,3.0)
b.write("v2.ifc")
c=ifcopenshell.open("v2.ifc")
for e in c.by_type("IfcRoot"): e.GlobalId=ifcopenshell.guid.new()
c.write("v2_reexport.ifc")
A=ifcopenshell.open("v1.ifc");B=ifcopenshell.open("v2.ifc");C=ifcopenshell.open("v2_reexport.ifc")
t=time.time(); d=r.diff_por_globalid(A,B); print("diff_globalid",{k:len(v) for k,v in d.items()},round(time.time()-t,2),"s")
t=time.time(); d=r.diff_por_globalid(A,C); print("diff_reexport",{k:len(v) for k,v in d.items()},round(time.time()-t,2),"s")
import ifcdiff
t=time.time(); x=ifcdiff.IfcDiff(A,B,relationships=["attributes","property"]); x.diff(); print("ifcdiff attr+prop",len(x.added_elements),len(x.deleted_elements),len(x.change_register),round(time.time()-t,2),"s")
t=time.time(); x=ifcdiff.IfcDiff(A,B,relationships=["geometry"]); x.diff(); print("ifcdiff geom",len(x.added_elements),len(x.deleted_elements),len(x.change_register),round(time.time()-t,2),"s")
s1=os.path.getsize("v1.ifc"); s2=os.path.getsize("v2.ifc")
g1=len(gzip.compress(open("v1.ifc","rb").read())); g2=len(gzip.compress(open("v2.ifc","rb").read()))
l1=open("v1.ifc").read().splitlines(); l2=open("v2.ifc").read().splitlines()
delta="\n".join(difflib.unified_diff(l1,l2,lineterm="",n=0)).encode()
print("bytes v1",s1,"v2",s2,"gz v1",g1,"gz v2",g2,"delta texto",len(delta),"delta gz",len(gzip.compress(delta)))
