"""SWT-Bench pilot — gpt-4o-mini on 5 SWT-Bench Lite instances, ZeroShotPlus format.

Runs in the vgap venv. Prompts come from the benchmark's published dataset
(nmuendler/SWT-Bench_Lite_bm25_27k_zsp: issue + BM25-retrieved 27k-token context, ZSP
custom-diff instructions baked in). Raw model output goes into `model_patch` verbatim; the
SWT-Bench harness extracts the patch itself when run with --patch_types custom fuzzy.
Instance selection is deterministic: first 5 by instance_id.
"""

import asyncio
import json
import time
from pathlib import Path

from datasets import load_dataset
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_litellm import ChatLiteLLM

HERE = Path(__file__).parent
RESULTS = HERE / "results"
MODEL = "gpt-4o-mini"
N_INSTANCES = 5


async def main() -> None:
    load_dotenv(HERE.parent.parent.parent / ".env")
    RESULTS.mkdir(exist_ok=True)

    ds = load_dataset("nmuendler/SWT-Bench_Lite_bm25_27k_zsp", split="test")
    rows = sorted(ds, key=lambda r: r["instance_id"])[:N_INSTANCES]
    print(f"instances: {[r['instance_id'] for r in rows]}")

    llm = ChatLiteLLM(model=MODEL, temperature=0.0, max_tokens=4096)

    async def gen(row):
        resp = await llm.ainvoke([HumanMessage(content=row["text"])])
        content = resp.content if isinstance(resp.content, str) else str(resp.content)
        u = resp.usage_metadata or {}
        print(f"  {row['instance_id']}: {u.get('input_tokens', '?')} in / {u.get('output_tokens', '?')} out")
        return {
            "instance_id": row["instance_id"],
            "model_name_or_path": f"{MODEL}-zsp-pilot",
            "model_patch": content,
            "full_output": content,
            "usage": u and {"input_tokens": u.get("input_tokens"), "output_tokens": u.get("output_tokens")},
        }

    t0 = time.time()
    preds = await asyncio.gather(*(gen(r) for r in rows))
    print(f"{len(preds)} generations in {time.time()-t0:.0f}s")

    path = RESULTS / "predictions.jsonl"
    with path.open("w") as f:
        for p in preds:
            f.write(json.dumps({k: v for k, v in p.items() if k != "usage"}) + "\n")
    (RESULTS / "usage.json").write_text(json.dumps([{**{"instance_id": p["instance_id"]}, **(p["usage"] or {})} for p in preds], indent=2))
    print(f"-> {path}")


if __name__ == "__main__":
    asyncio.run(main())
