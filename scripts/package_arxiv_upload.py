"""Create an arXiv ZIP from the reviewed source manifest without changing the paper."""

import hashlib
import json
from pathlib import Path
import zipfile


REPO = Path(__file__).resolve().parent.parent
PAPER = REPO / "paper"
RELEASE = REPO / "release"


def main():
    manifest = json.loads((RELEASE / "manifest.json").read_text())
    sources = {}
    for name, expected_hash in manifest["source_sha256"].items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit(f"Invalid source path: {name}")
        data = (PAPER / relative).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected_hash:
            raise SystemExit(f"Reviewed source has changed: {name}; rebuild and package first.")
        sources[name] = data
    if b"\\documentclass{article}" not in sources.get("main.tex", b""):
        raise SystemExit("The reviewed main.tex is missing its document class.")

    # Explicit instructions for the exceptional case where Check Files fails to
    # identify the main source. Schema: https://info.arxiv.org/help/00README.html
    config = {
        "spec_version": 1,
        "process": {"compiler": "pdflatex"},
        "sources": [{"filename": "main.tex", "usage": "toplevel"}],
    }
    sources["00README.json"] = (json.dumps(config, indent=2) + "\n").encode()
    output = RELEASE / "self-grading-gap-arxiv.zip"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sources.items():
            # Fixed metadata avoids platform-specific archive attributes and
            # makes repeated packaging of identical inputs reproducible.
            info = zipfile.ZipInfo(name)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise SystemExit("ZIP integrity check failed.")
        for name, data in sources.items():
            if archive.read(name) != data:
                raise SystemExit(f"ZIP content mismatch: {name}")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(".zip.sha256").write_text(f"{digest}  {output.name}\n")
    print(f"Prepared {output}: {len(sources) - 1} unchanged source files and 00README.json.")
    print("Top-level file: main.tex; processor: pdflatex. No uploads performed.")


if __name__ == "__main__":
    main()
