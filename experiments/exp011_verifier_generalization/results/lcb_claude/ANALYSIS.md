# exp011 ANALYSIS — lcb_claude (generated; do not hand-edit)

strong verifier: claude-sonnet-4-5
instrument @ 1a14ca82d; spend (global exp011) $173.22

## control
- oracle pass /30: [14, 15, 15, 15, 15] (mean 14.8)
- false accepts: 3.6 (runs [2, 5, 4, 4, 3])
- false rejects: 2.8 (runs [3, 3, 3, 2, 3]); verdict-error total: 6.4
- tests/run: 79.4 (canonical 75.0)

## strong_testgen
- oracle pass /30: [17, 16, 17, 17, 17] (mean 16.8)
- false accepts: 2.0 (runs [1, 3, 1, 1, 4])
- false rejects: 3.0 (runs [1, 4, 6, 2, 2]); verdict-error total: 5.0
- tests/run: 367.8 (canonical 75.0)
- vs control: {"FA": "d-1.6 p=1.0 -> within noise", "FR": "d0.2 -> within noise", "verdict_error": "d-1.4 -> within noise", "pass": "d2.0 p=0.5 -> within noise"}

## strong_judge
- oracle pass /30: [10, 18, 14, 16, 17] (mean 15.0)
- false accepts: 3.4 (runs [4, 4, 1, 3, 5])
- false rejects: 2.0 (runs [1, 3, 1, 3, 2]); verdict-error total: 5.4
- tests/run: 216.6 (canonical 75.0)
- vs control: {"FA": "d-0.2 p=1.0 -> within noise", "FR": "d-0.8 -> within noise", "verdict_error": "d-1.0 -> within noise", "pass": "d0.2 p=0.5 -> within noise"}

## strong_both
- oracle pass /30: [16, 15, 18, 18, 16] (mean 16.6)
- false accepts: 3.6 (runs [4, 4, 5, 2, 3])
- false rejects: 1.4 (runs [0, 0, 2, 4, 1]); verdict-error total: 5.0
- tests/run: 370.8 (canonical 75.0)
- vs control: {"FA": "d0.0 p=1.0 -> within noise", "FR": "d-1.4 -> within noise", "verdict_error": "d-1.4 -> within noise", "pass": "d1.8 p=0.5 -> within noise"}

Floors (pre-registered): {"pass": 4, "fa": 2, "fr": 2, "verdict_error": 3}. lcb30 = 19 easy + 11 medium LeetCode, post-2025 window; not benchmark rates.
