# exp006 ANALYSIS (generated; do not hand-edit)

instrument @ f02775d2e; spend $14.72

## control_rerun
- oracle pass /30: [22, 23, 24, 26, 25] (mean 24.0)
- false accepts base/plus: 3.0 / 4.0 (runs [5, 6, 3, 3, 3])
- false rejects: 5.4 (runs [4, 3, 5, 7, 8]); verdict-error total: 9.4
- tests/run: 84.0 (canonical 80.6)

## strong_testgen
- oracle pass /30: [24, 24, 26, 26, 26] (mean 25.2)
- false accepts base/plus: 2.2 / 3.2 (runs [5, 4, 2, 2, 3])
- false rejects: 3.6 (runs [3, 2, 6, 4, 3]); verdict-error total: 6.8
- tests/run: 89.4 (canonical 71.8)
- vs control: {"FA_plus": "\u0394-0.8 p=1.0 \u2192 within noise", "FR": "\u0394-1.8 \u2192 within noise", "verdict_error": "\u0394-2.6 \u2192 within noise", "pass": "\u03941.2 p=1.0 \u2192 within noise"}

## strong_judge
- oracle pass /30: [24, 25, 25, 25, 24] (mean 24.6)
- false accepts base/plus: 3.4 / 4.4 (runs [5, 4, 4, 4, 5])
- false rejects: 2.4 (runs [2, 3, 1, 4, 2]); verdict-error total: 6.8
- tests/run: 104.8 (canonical 79.4)
- vs control: {"FA_plus": "\u03940.4 p=1.0 \u2192 within noise", "FR": "\u0394-3.0 \u2192 beyond floor", "verdict_error": "\u0394-2.6 \u2192 within noise", "pass": "\u03940.6 p=1.0 \u2192 within noise"}

## strong_both
- oracle pass /30: [28, 25, 26, 26, 26] (mean 26.2)
- false accepts base/plus: 2.0 / 3.4 (runs [2, 6, 3, 4, 2])
- false rejects: 1.6 (runs [2, 2, 1, 2, 1]); verdict-error total: 5.0
- tests/run: 100.6 (canonical 72.0)
- vs control: {"FA_plus": "\u0394-0.6 p=1.0 \u2192 within noise", "FR": "\u0394-3.8 \u2192 beyond floor", "verdict_error": "\u0394-4.4 \u2192 beyond floor", "pass": "\u03942.2 p=1.0 \u2192 within noise"}

Floors (pre-registered): {"pass": 4, "fa": 2, "fr": 2, "verdict_error": 3}. Subset hardness-enriched; not benchmark rates.
