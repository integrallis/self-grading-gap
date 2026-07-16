"""LCB pilot stage 2 — generate gpt-4o-mini completions for the selected slice.

Runs in the vgap venv (ChatLiteLLM + repo .env keys). LCB leaderboard settings are
temperature 0.2, top_p 0.95, n=10 for pass@1; the pilot uses n=3 per problem (recorded
deviation — this is a feasibility pilot, not a leaderboard entry). Raw model outputs are
saved unextracted; extraction happens in stage 3 with the harness's own extractor.
"""

import asyncio
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_litellm import ChatLiteLLM

HERE = Path(__file__).parent
RESULTS = HERE / "results"
MODEL = "gpt-4o-mini"
N_SAMPLES = 3
CONCURRENCY = 6


async def sample_problem(llm: ChatLiteLLM, row: dict, sem: asyncio.Semaphore) -> dict:
    outputs = []
    usage = {"input_tokens": 0, "output_tokens": 0}
    for _ in range(N_SAMPLES):
        async with sem:
            resp = await llm.ainvoke([
                SystemMessage(content=row["system"]),
                HumanMessage(content=row["user"]),
            ])
        outputs.append(resp.content if isinstance(resp.content, str) else str(resp.content))
        u = (resp.usage_metadata or {})
        usage["input_tokens"] += u.get("input_tokens", 0)
        usage["output_tokens"] += u.get("output_tokens", 0)
    print(f"  {row['question_id']:>10}  {row['difficulty']:<6} done")
    return {"question_id": row["question_id"], "outputs": outputs, "usage": usage}


async def main() -> None:
    load_dotenv(HERE.parent.parent.parent / ".env")
    rows = json.loads((RESULTS / "problems.json").read_text())
    llm = ChatLiteLLM(model=MODEL, temperature=0.2, top_p=0.95, max_tokens=4096)
    sem = asyncio.Semaphore(CONCURRENCY)

    t0 = time.time()
    results = await asyncio.gather(*(sample_problem(llm, r, sem) for r in rows))
    wall = time.time() - t0

    out = {
        "model": MODEL, "temperature": 0.2, "top_p": 0.95, "n_samples": N_SAMPLES,
        "wall_time_s": round(wall, 1),
        "total_input_tokens": sum(r["usage"]["input_tokens"] for r in results),
        "total_output_tokens": sum(r["usage"]["output_tokens"] for r in results),
        "generations": results,
    }
    path = RESULTS / "raw_outputs.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"{len(results)} problems x {N_SAMPLES} samples in {wall:.0f}s -> {path}")
    print(f"tokens: {out['total_input_tokens']} in / {out['total_output_tokens']} out")


if __name__ == "__main__":
    asyncio.run(main())
