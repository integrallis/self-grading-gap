#!/usr/bin/env python3
"""Stage and compile a venue wrapper against shared, provenance-checked inputs."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("venue", choices=["se4agenticai-2026", "vst-2027"])
    parser.add_argument("--full", action="store_true", help="Compile the unabridged reflow baseline, including appendices.")
    args = parser.parse_args()
    shared = ROOT / "_shared"
    manifest = json.loads((shared / "source-manifest.json").read_text())
    for name, digest in manifest["inputs_sha256"].items():
        if hashlib.sha256((REPO / name).read_bytes()).hexdigest() != digest:
            raise SystemExit(f"Shared source is stale: {name}; review changes and run submissions/prepare.py.")
    venue = ROOT / args.venue
    edition = "full-length" if args.full else "review"
    build = venue / "build" / edition
    build.mkdir(parents=True, exist_ok=True)
    for path in (ROOT / "_templates" / "ieee").glob("*"):
        if path.suffix in {".cls", ".bst"}:
            shutil.copy2(path, build / path.name)
    for path in shared.rglob("*.tex"):
        target = build / path.relative_to(shared)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    for path in venue.glob("*.tex"):
        shutil.copy2(path, build / path.name)
    for name in ["audit_numbers.tex", "refs.bib", "algpseudocode.sty", "algorithmicx.sty"]:
        shutil.copy2(REPO / "paper" / name, build / name)
    for name in manifest["inputs_sha256"]:
        if name.startswith("paper/figures/"):
            target = build / Path(name).relative_to("paper")
            target.parent.mkdir(exist_ok=True)
            shutil.copy2(REPO / name, target)
    body = shared / "full-body.tex" if args.full else venue / "content.tex"
    if not body.exists():
        raise SystemExit(f"Review text not prepared: {body}. Use --full for the reflow baseline.")
    shutil.copy2(body, build / "manuscript.tex")
    wrapper = (venue / "main.tex").read_text()
    if args.full:
        wrapper = "\\def\\IncludeFullAppendices{1}\n" + wrapper
    (build / "main.tex").write_text(wrapper)
    engine = shutil.which("tectonic")
    if not engine:
        raise SystemExit("Install Tectonic to build these local drafts.")
    with (build / "build.log").open("w") as log:
        result = subprocess.run([engine, "--untrusted", "--keep-logs", "--keep-intermediates", "main.tex"],
                                cwd=build, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        print((build / "build.log").read_text()[-10000:])
        raise SystemExit(result.returncode)
    output = venue / f"{edition}.pdf"
    shutil.copy2(build / "main.pdf", output)
    info = subprocess.run(["pdfinfo", str(output)], check=True, capture_output=True, text=True).stdout
    pages = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    limit = 10 if args.venue == "se4agenticai-2026" else 8
    texlog = (build / "main.log").read_text(errors="replace")
    errors = re.findall(r"[^\n]*(?:undefined references|Citation .+ undefined|Reference .+ undefined)[^\n]*", texlog)
    overfull = re.findall(r"Overfull \\[hv]box[^\n]*", texlog)
    report = {"venue": args.venue, "edition": edition, "pdf": str(output.relative_to(REPO)),
              "pages": pages, "page_limit": limit, "within_page_limit": pages <= limit,
              "undefined_references": errors, "overfull_boxes": overfull,
              "pdf_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
              "upload_ready": False,
              "note": "Local author draft. Venue-specific checks and exact-PDF author approval remain required."}
    (venue / f"{edition}-checks.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
