# exp011 ANALYSIS — lcb_gemini (generated; do not hand-edit)

strong verifier: vertex_ai/gemini-2.5-pro
instrument @ 1a14ca82d; spend (global exp011) $303.89

## control
- oracle pass /30: [14, 15, 16, 15, 16] (mean 15.2)
- false accepts: 3.8 (runs [4, 6, 3, 3, 3])
- false rejects: 2.6 (runs [1, 4, 2, 1, 5]); verdict-error total: 6.4
- tests/run: 76.4 (canonical 75.0)

## strong_testgen
- oracle pass /30: [18, 17, 20, 18, 21] (mean 18.8)
- false accepts: 1.8 (runs [2, 0, 2, 3, 2])
- false rejects: 1.4 (runs [1, 3, 1, 1, 1]); verdict-error total: 3.2
- tests/run: 299.2 (canonical 75.0)
- vs control: {"FA": "d-2.0 p=0.5 -> within noise", "FR": "d-1.2 -> within noise", "verdict_error": "d-3.2 -> beyond floor", "pass": "d3.6 p=0.625 -> within noise"}

## strong_judge
- oracle pass /30: [18, 17, 15, 15, 15] (mean 16.0)
- false accepts: 3.4 (runs [2, 1, 4, 5, 5])
- false rejects: 3.4 (runs [4, 3, 3, 5, 2]); verdict-error total: 6.8
- tests/run: 177.8 (canonical 74.0)
- vs control: {"FA": "d-0.4 p=0.5 -> within noise", "FR": "d0.8 -> within noise", "verdict_error": "d0.4 -> within noise", "pass": "d0.8 p=1.0 -> within noise"}

## strong_both
- oracle pass /30: [23, 22, 19, 21, 23] (mean 21.6)
- false accepts: 2.6 (runs [2, 2, 5, 2, 2])
- false rejects: 0.4 (runs [1, 1, 0, 0, 0]); verdict-error total: 3.0
- tests/run: 320.4 (canonical 75.0)
- vs control: {"FA": "d-1.2 p=1.0 -> within noise", "FR": "d-2.2 -> beyond floor", "verdict_error": "d-3.4 -> beyond floor", "pass": "d6.4 p=0.0156 -> SIGNAL"}

Floors (pre-registered): {"pass": 4, "fa": 2, "fr": 2, "verdict_error": 3}. lcb30 = 19 easy + 11 medium LeetCode, post-2025 window; not benchmark rates.
