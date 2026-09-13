# exp011 ANALYSIS — he_gemini (generated; do not hand-edit)

strong verifier: vertex_ai/gemini-2.5-pro
instrument @ f02775d2e; spend (global exp011) $303.89

## control
- oracle pass /30: [24, 23, 24, 23, 24] (mean 23.6)
- false accepts base/plus: 3.8 / 4.8 (runs [5, 5, 5, 5, 4])
- false rejects: 4.0 (runs [5, 4, 4, 2, 5]); verdict-error total: 8.8
- tests/run: 81.8 (canonical 77.6)

## strong_testgen
- oracle pass /30: [27, 26, 27, 25, 27] (mean 26.4)
- false accepts base/plus: 1.2 / 3.2 (runs [3, 4, 3, 3, 3])
- false rejects: 4.4 (runs [4, 5, 5, 4, 4]); verdict-error total: 7.6
- tests/run: 238.8 (canonical 71.6)
- vs control: {"FA_plus": "d-1.6 p=0.625 -> within noise", "FR": "d0.4 -> within noise", "verdict_error": "d-1.2 -> within noise", "pass": "d2.8 p=0.125 -> within noise"}

## strong_judge
- oracle pass /30: [23, 22, 24, 25, 24] (mean 23.6)
- false accepts base/plus: 2.8 / 4.0 (runs [3, 5, 4, 5, 3])
- false rejects: 2.8 (runs [4, 4, 4, 1, 1]); verdict-error total: 6.8
- tests/run: 136.8 (canonical 78.8)
- vs control: {"FA_plus": "d-0.8 p=1.0 -> within noise", "FR": "d-1.2 -> within noise", "verdict_error": "d-2.0 -> within noise", "pass": "d0.0 p=0.5 -> within noise"}

## strong_both
- oracle pass /30: [26, 26, 26, 26, 24] (mean 25.6)
- false accepts base/plus: 3.8 / 4.8 (runs [6, 4, 6, 4, 4])
- false rejects: 2.2 (runs [2, 2, 3, 4, 0]); verdict-error total: 7.0
- tests/run: 241.8 (canonical 72.0)
- vs control: {"FA_plus": "d0.0 p=1.0 -> within noise", "FR": "d-1.8 -> within noise", "verdict_error": "d-1.8 -> within noise", "pass": "d2.0 p=0.375 -> within noise"}

Floors (pre-registered): {"pass": 4, "fa": 2, "fr": 2, "verdict_error": 3}. Subset hardness-enriched; not benchmark rates.
