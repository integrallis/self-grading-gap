"""Prepare a local author-preprint packet from an already-built paper. No uploads."""

from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile

REPO = Path(__file__).resolve().parent.parent
PAPER = REPO / "paper"
OUT = REPO / "release"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = (PAPER / "main.tex").read_text()
    figures = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source)
    names = ["main.tex", "refs.bib", "audit_numbers.tex", "main.bbl"]
    names += [p.name for p in sorted(PAPER.glob("*.sty"))] + figures
    files = [PAPER / n for n in names]
    for path in [*files, PAPER / "main.pdf"]:
        if not path.is_file():
            raise SystemExit(f"Missing {path}; regenerate analyses/figures and build the paper first.")
    if any(p.stat().st_mtime > (PAPER / "main.pdf").stat().st_mtime
           for p in files if p.suffix != ".bbl"):
        raise SystemExit("The PDF is older than a source input; rebuild before packaging.")
    pdfinfo = subprocess.run(["pdfinfo", str(PAPER / "main.pdf")], check=True,
                             capture_output=True, text=True).stdout
    pages = int(re.search(r"^Pages:\s+(\d+)", pdfinfo, re.M)[1])
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, check=True,
                              capture_output=True, text=True).stdout.strip()
    diff = subprocess.run(["git", "diff", "--binary", "HEAD"], cwd=REPO, check=True,
                          capture_output=True).stdout
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, check=True,
                           capture_output=True, text=True).stdout.strip()
    OUT.mkdir(exist_ok=True)
    archive = OUT / "self-grading-gap-reviewed-source.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for path in files:
            tar.add(path, arcname=str(path.relative_to(PAPER)), recursive=False)
        readme = ("Author-preprint revision prepared locally; not uploaded.\n"
                  "Build: latexmk -pdf main.tex\n"
                  "Alternative: tectonic --untrusted main.tex\n"
                  "Generated audit_numbers.tex and all referenced figures are included.\n"
                  "Audit: https://github.com/integrallis/self-grading-gap\n").encode()
        info = tarfile.TarInfo("README.txt")
        info.size = len(readme)
        tar.addfile(info, io.BytesIO(readme))
    pdf = OUT / "self-grading-gap-reviewed.pdf"
    shutil.copyfile(PAPER / "main.pdf", pdf)
    abstract = source.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0]
    for name, value in re.findall(r"\\newcommand\{\\(\w+)\}\{([^{}]*)\}",
                                  (PAPER / "audit_numbers.tex").read_text()):
        abstract = abstract.replace("\\" + name, value)
    abstract = re.sub(r"\\(?:emph|texttt|textbf)\{([^{}]*)\}", r"\1", abstract)
    abstract = " ".join(abstract.replace(r"\%", "%").replace("$", "").split())
    (OUT / "abstract.txt").write_text(abstract + "\n")
    tables = len(re.findall(r"\\begin\{table\}", source))
    comments = (f"{pages} pages, {len(figures)} figures, {tables} tables. "
                "Code, retained data, prompts, protocols, and post hoc review analyses: "
                "https://github.com/integrallis/self-grading-gap "
                "RGRBench: https://github.com/integrallis/rgrbench")
    (OUT / "submission-comments.txt").write_text(comments + "\n")
    manifest = {"status": "local author-preprint revision; not uploaded",
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "existing_submission": "submit/7939730", "pages": pages,
                "figures": len(figures), "tables": tables,
                "base_revision": revision, "working_tree_dirty": bool(dirty),
                "tracked_diff_sha256": hashlib.sha256(diff).hexdigest(),
                "source_sha256": {str(p.relative_to(PAPER)): sha256(p) for p in files},
                "pdf_sha256": sha256(pdf)}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    artifacts = [pdf, archive, OUT / "abstract.txt", OUT / "submission-comments.txt", OUT / "manifest.json"]
    (OUT / "SHA256SUMS").write_text("".join(f"{sha256(p)}  {p.name}\n" for p in artifacts))
    print(f"Prepared {OUT}: {pages} pages, {len(figures)} figures, {tables} tables. No uploads.")


if __name__ == "__main__":
    main()
