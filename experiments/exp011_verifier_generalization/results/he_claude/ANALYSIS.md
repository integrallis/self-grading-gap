# exp011 ANALYSIS — he_claude (generated; do not hand-edit)

strong verifier: claude-sonnet-4-5
instrument @ 1a14ca82d; spend (global exp011) $65.23

## control
- oracle pass /30: [25, 23, 22, 24, 25] (mean 23.8)
- false accepts base/plus: 2.8 / 3.8 (runs [3, 5, 3, 5, 3])
- false rejects: 4.8 (runs [5, 5, 2, 6, 6]); verdict-error total: 8.6
- tests/run: 85.6 (canonical 79.8)

## strong_testgen
- oracle pass /30: [26, 25, 25, 27, 27] (mean 26.0)
- false accepts base/plus: 1.6 / 2.8 (runs [3, 3, 2, 3, 3])
- false rejects: 4.0 (runs [4, 3, 5, 4, 4]); verdict-error total: 6.8
- tests/run: 343.0 (canonical 71.6)
- vs control: {"FA_plus": "d-1.0 p=1.0 -> within noise", "FR": "d-0.8 -> within noise", "verdict_error": "d-1.8 -> within noise", "pass": "d2.2 p=0.5 -> within noise"}

## strong_judge
- oracle pass /30: [25, 26, 23, 24, 25] (mean 24.6)
- false accepts base/plus: 2.8 / 3.4 (runs [2, 1, 6, 5, 3])
- false rejects: 2.2 (runs [2, 2, 3, 2, 2]); verdict-error total: 5.6
- tests/run: 137.4 (canonical 72.8)
- vs control: {"FA_plus": "d-0.4 p=1.0 -> within noise", "FR": "d-2.6 -> beyond floor", "verdict_error": "d-3.0 -> within noise", "pass": "d0.8 p=1.0 -> within noise"}

## strong_both
- oracle pass /30: [26, 24, 28, 25, 27] (mean 26.0)
- false accepts base/plus: 2.6 / 4.2 (runs [2, 6, 4, 5, 4])
- false rejects: 1.4 (runs [3, 0, 1, 1, 2]); verdict-error total: 5.6
- tests/run: 343.6 (canonical 72.0)
- vs control: {"FA_plus": "d0.4 p=1.0 -> within noise", "FR": "d-3.4 -> beyond floor", "verdict_error": "d-3.0 -> within noise", "pass": "d2.2 p=0.25 -> within noise"}

Floors (pre-registered): {"pass": 4, "fa": 2, "fr": 2, "verdict_error": 3}. Subset hardness-enriched; not benchmark rates.
