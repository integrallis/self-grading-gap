# exp007 ANALYSIS (generated; do not hand-edit)

instrument @ f02775d2e; spend $37.32

## control
- oracle pass /30: [15, 16, 16, 13, 16] (mean 15.2)
- false accepts: 4.8 (runs [5, 6, 4, 5, 4])
- false rejects: 3.4 (runs [3, 5, 4, 1, 4]); verdict-error total: 8.2
- tests/run: 76.2 (canonical 75.0)

## strong_testgen
- oracle pass /30: [15, 16, 14, 18, 19] (mean 16.4)
- false accepts: 2.8 (runs [3, 4, 3, 2, 2])
- false rejects: 2.2 (runs [0, 2, 1, 3, 5]); verdict-error total: 5.0
- tests/run: 140.2 (canonical 75.0)
- vs control: {"FA": "\u0394-2.0 p=0.125 \u2192 within noise", "FR": "\u0394-1.2 \u2192 within noise", "verdict_error": "\u0394-3.2 \u2192 beyond floor", "pass": "\u03941.2 p=0.5 \u2192 within noise"}

## strong_judge
- oracle pass /30: [20, 21, 19, 20, 21] (mean 20.2)
- false accepts: 2.4 (runs [2, 2, 1, 2, 5])
- false rejects: 0.0 (runs [0, 0, 0, 0, 0]); verdict-error total: 2.4
- tests/run: 182.4 (canonical 75.0)
- vs control: {"FA": "\u0394-2.4 p=0.125 \u2192 within noise", "FR": "\u0394-3.4 \u2192 beyond floor", "verdict_error": "\u0394-5.8 \u2192 beyond floor", "pass": "\u03945.0 p=0.0312 \u2192 SIGNAL"}

## strong_both
- oracle pass /30: [21, 22, 22, 22, 20] (mean 21.4)
- false accepts: 3.0 (runs [4, 1, 2, 2, 6])
- false rejects: 0.0 (runs [0, 0, 0, 0, 0]); verdict-error total: 3.0
- tests/run: 193.6 (canonical 75.0)
- vs control: {"FA": "\u0394-1.8 p=0.375 \u2192 within noise", "FR": "\u0394-3.4 \u2192 beyond floor", "verdict_error": "\u0394-5.2 \u2192 beyond floor", "pass": "\u03946.2 p=0.0156 \u2192 SIGNAL"}

Floors (pre-registered): {"pass": 4, "fa": 2, "fr": 2, "verdict_error": 3}. lcb30 = 19 easy + 11 medium LeetCode, post-2025 window; not benchmark rates.
