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

SHA = "38fd0c8423704291106a24170169fc3c39bc6e83"
CURTO = SHA[:7]


def _gh_stub(dir_tmp: Path, *, checks, labels, comments, estado="OPEN") -> Path:
    binario = dir_tmp / "gh"
    log = dir_tmp / "gh.log"
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
log.write_text(log.read_text() + " ".join(sys.argv[1:]) + "\\n" if log.exists() else " ".join(sys.argv[1:]) + "\\n")
args = sys.argv[1:]
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
    print(json.dumps(payload["checks"]))
    sys.exit(0)
if args[:1] == ["api"] and "comments" in args[1]:
    print(json.dumps(payload["comments"]))
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
    return log


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
    def test_check_vermelho_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=[{"name": "unittest", "state": "COMPLETED", "conclusion": "FAILURE"}],
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
                checks=[{"name": "unittest", "state": "IN_PROGRESS", "conclusion": ""}],
                labels=[],
                comments=[_comentario("Aprovado")],
            )
            r = _rodar(d)
            self.assertNotEqual(r.returncode, 0, r.stderr)
            self.assertFalse((d / "merged").exists())
            self.assertIn("pendente", r.stderr)

    def test_sem_veredito_na_head_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=[{"name": "unittest", "state": "COMPLETED", "conclusion": "SUCCESS"}],
                labels=[],
                comments=[_comentario("Aprovado", sha="deadbee")],
            )
            r = _rodar(d)
            self.assertNotEqual(r.returncode, 0, r.stderr)
            self.assertFalse((d / "merged").exists())

    def test_sensivel_sem_aval_delegado_nao_mescla(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            _gh_stub(
                d,
                checks=[{"name": "unittest", "state": "COMPLETED", "conclusion": "SUCCESS"}],
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
                checks=[{"name": "unittest", "state": "COMPLETED", "conclusion": "SUCCESS"}],
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
                checks=[
                    {"name": "unittest", "state": "COMPLETED", "conclusion": "SUCCESS"},
                    {"name": "qualidade", "state": "SUCCESS", "conclusion": "SUCCESS"},
                ],
                labels=["precisa do Samuel"],
                comments=[_comentario("Aprovado (aval do Samuel delegado ao Tzu)")],
            )
            r = _rodar(d)
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            self.assertTrue((d / "merged").exists())


if __name__ == "__main__":
    unittest.main()
