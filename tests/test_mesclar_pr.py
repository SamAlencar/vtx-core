"""VTX-214: o script de merge não chama gh pr merge com check ruim ou sem veredito."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SCRIPT = RAIZ / "scripts" / "mesclar_pr.sh"
FIXTURES = RAIZ / "tests" / "fixtures" / "mesclar_pr"
CHECKS_PASS = json.loads((FIXTURES / "checks-pass-pr36.json").read_text(encoding="utf-8"))

# Campos reais de `gh pr checks --json` no gh 2.103.0 (ver checks-pass-pr36.meta.txt).
CAMPOS_PR_CHECKS = {
    "bucket",
    "completedAt",
    "description",
    "event",
    "link",
    "name",
    "startedAt",
    "state",
    "workflow",
}

SHA = "38fd0c8423704291106a24170169fc3c39bc6e83"
CURTO = SHA[:7]


def _check(*, name: str = "unittest", bucket: str, state: str) -> dict:
    return {"bucket": bucket, "name": name, "state": state}


def _gh_stub(dir_tmp: Path, *, checks, labels, comments, estado="OPEN") -> Path:
    binario = dir_tmp / "gh"
    payload = {
        "checks": checks,
        "labels": labels,
        "comments": comments,
        "estado": estado,
        "sha": SHA,
    }
    (dir_tmp / "payload.json").write_text(json.dumps(payload), encoding="utf-8")
    binario.write_text(
        f"""#!/usr/bin/env python3
import json, sys
from pathlib import Path
base = Path({str(dir_tmp)!r})
log = base / "gh.log"
payload = json.loads((base / "payload.json").read_text())
log.write_text((log.read_text() if log.exists() else "") + " ".join(sys.argv[1:]) + "\\n")
args = sys.argv[1:]
campos = {repr(sorted(CAMPOS_PR_CHECKS))}
if args[:2] == ["repo", "view"]:
    print(json.dumps({{"nameWithOwner": "SamAlencar/vtx-core"}}))
    sys.exit(0)
if args[:2] == ["pr", "view"]:
    labels = [{{"name": n}} for n in payload["labels"]]
    print(json.dumps({{
        "headRefOid": payload["sha"],
        "state": payload["estado"],
        "labels": labels,
        "url": "https://github.com/SamAlencar/vtx-core/pull/1",
    }}))
    sys.exit(0)
if args[:2] == ["pr", "checks"]:
    if "--json" not in args:
        sys.stderr.write("Specify one or more comma-separated fields for --json\\n")
        sys.exit(1)
    pedidas = args[args.index("--json") + 1].split(",")
    desconhecidos = [c for c in pedidas if c not in campos]
    if desconhecidos:
        sys.stderr.write('Unknown JSON field: "' + desconhecidos[0] + '"\\n')
        sys.stderr.write("Available fields:\\n")
        for c in campos:
            sys.stderr.write("  " + c + "\\n")
        sys.exit(1)
    filtrados = [{{k: item[k] for k in pedidas if k in item}} for item in payload["checks"]]
    print(json.dumps(filtrados, separators=(",", ":")))
    buckets = {{item.get("bucket") for item in payload["checks"]}}
    if "fail" in buckets or "cancel" in buckets:
        sys.exit(1)
    if "pending" in buckets:
        sys.exit(8)
    sys.exit(0)
if args[:1] == ["api"] and any("comments" in a for a in args):
    comments = payload["comments"]
    if "--paginate" not in args:
        comments = comments[:30]
    print(json.dumps(comments))
    sys.exit(0)
if args[:2] == ["pr", "merge"]:
    (base / "merged").write_text(" ".join(args) + "\\n")
    sys.exit(0)
sys.stderr.write("gh stub: comando inesperado: " + " ".join(args) + "\\n")
sys.exit(2)
""",
        encoding="utf-8",
    )
    binario.chmod(binario.stat().st_mode | stat.S_IEXEC)
    return dir_tmp / "gh.log"


def _rodar(dir_tmp: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = f"{dir_tmp}:{env['PATH']}"
    env["GH_CONFIG_DIR"] = str(dir_tmp / "ghconfig")
    return subprocess.run(
        ["bash", str(SCRIPT), "1"],
        cwd=str(RAIZ),
        env=env,
        text=True,
        capture_output=True,
    )


def _comentario(veredito: str, sha: str = CURTO) -> dict:
    return {"body": f"**Veredito: {veredito}** (HEAD `{sha}`)\n\nTexto."}


class TestMesclarPr(unittest.TestCase):
    def test_fixture_real_usa_campos_do_gh(self) -> None:
        self.assertGreater(len(CHECKS_PASS), 0)
        for item in CHECKS_PASS:
            self.assertNotIn("conclusion", item)
            self.assertEqual(set(item), {"bucket", "name", "state"})
            self.assertIn(item["bucket"], {"pass", "fail", "pending", "skipping", "cancel"})
            self.assertIn(item["state"], {"SUCCESS", "FAILURE", "IN_PROGRESS", "CANCELLED", "SKIPPED"})

    def test_stub_recusa_campo_conclusion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(d, checks=CHECKS_PASS, labels=[], comments=[])
            r = subprocess.run(
                [str(d / "gh"), "pr", "checks", "1", "--json", "name,state,conclusion"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("Unknown JSON field", r.stderr)
            self.assertIn("conclusion", r.stderr)

    def test_check_vermelho_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=[_check(bucket="fail", state="FAILURE")],
                labels=[],
                comments=[_comentario("Aprovado")],
            )
            r = _rodar(d)
            self.assertNotEqual(r.returncode, 0, r.stderr)
            self.assertFalse((d / "merged").exists())
            self.assertIn("vermelho", r.stderr)

    def test_check_pendente_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=[_check(bucket="pending", state="IN_PROGRESS")],
                labels=[],
                comments=[_comentario("Aprovado")],
            )
            r = _rodar(d)
            self.assertNotEqual(r.returncode, 0, r.stderr)
            self.assertFalse((d / "merged").exists())
            self.assertIn("pendente", r.stderr)

    def test_check_cancel_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=[_check(bucket="cancel", state="CANCELLED")],
                labels=[],
                comments=[_comentario("Aprovado")],
            )
            r = _rodar(d)
            self.assertNotEqual(r.returncode, 0, r.stderr)
            self.assertFalse((d / "merged").exists())
            self.assertIn("vermelho", r.stderr)

    def test_check_skipping_com_pass_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=[
                    _check(name="qualidade", bucket="skipping", state="SKIPPED"),
                    _check(name="unittest", bucket="pass", state="SUCCESS"),
                ],
                labels=[],
                comments=[_comentario("Aprovado")],
            )
            r = _rodar(d)
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            self.assertTrue((d / "merged").exists())

    def test_sem_veredito_na_head_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=CHECKS_PASS,
                labels=[],
                comments=[_comentario("Aprovado", sha="deadbee")],
            )
            r = _rodar(d)
            self.assertNotEqual(r.returncode, 0, r.stderr)
            self.assertFalse((d / "merged").exists())

    def test_aprovado_sem_cabecalho_veredito_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=CHECKS_PASS,
                labels=[],
                comments=[{"body": f"Aprovado na HEAD `{CURTO}`. Sem o cabeçalho do revisor."}],
            )
            r = _rodar(d)
            self.assertNotEqual(r.returncode, 0, r.stderr)
            self.assertFalse((d / "merged").exists())
            self.assertIn("formato", r.stderr)

    def test_aprovado_com_ressalvas_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=CHECKS_PASS,
                labels=[],
                comments=[_comentario("Aprovado com ressalvas")],
            )
            r = _rodar(d)
            self.assertNotEqual(r.returncode, 0, r.stderr)
            self.assertFalse((d / "merged").exists())
            self.assertIn("ressalvas", r.stderr)

    def test_sensivel_sem_aval_delegado_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=CHECKS_PASS,
                labels=["precisa do Samuel"],
                comments=[_comentario("Aprovado")],
            )
            r = _rodar(d)
            self.assertNotEqual(r.returncode, 0, r.stderr)
            self.assertFalse((d / "merged").exists())
            self.assertIn("delegado", r.stderr)

    def test_verde_com_aprovado_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=CHECKS_PASS,
                labels=[],
                comments=[_comentario("Aprovado")],
            )
            r = _rodar(d)
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            merged = (d / "merged").read_text()
            self.assertIn("pr merge 1 --squash --match-head-commit " + SHA, merged)

    def test_sensivel_com_aval_delegado_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=CHECKS_PASS,
                labels=["precisa do Samuel"],
                comments=[_comentario("Aprovado (aval do Samuel delegado ao Tzu)")],
            )
            r = _rodar(d)
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            self.assertTrue((d / "merged").exists())

    def test_veredito_depois_de_30_comentarios_exige_paginate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            antigos = [{"body": f"comentario {i}"} for i in range(30)]
            _gh_stub(
                d,
                checks=CHECKS_PASS,
                labels=[],
                comments=[*antigos, _comentario("Aprovado")],
            )
            r = _rodar(d)
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            self.assertTrue((d / "merged").exists())
            self.assertIn("--paginate", (d / "gh.log").read_text())

    def test_pr_fechado_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=CHECKS_PASS,
                labels=[],
                comments=[_comentario("Aprovado")],
                estado="MERGED",
            )
            r = _rodar(d)
            self.assertNotEqual(r.returncode, 0, r.stderr)
            self.assertFalse((d / "merged").exists())
            self.assertIn("não está aberto", r.stderr)


if __name__ == "__main__":
    unittest.main()
