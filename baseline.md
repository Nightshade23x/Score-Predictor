## Baseline v1 – Differentials-only Logistic Regression

**Setup**
- Model: Logistic Regression (C = 0.3)
- Features:
  - form_points_diff
  - form_goal_diff_diff
  - season_strength_diff
  - h2h_points_diff
- Backtest: season-by-season (train < test)

**Results**
| Test Season | Accuracy | Log Loss |
|------------|----------|----------|
| 19–20 | 0.495 | 1.013 |
| 20–21 | 0.468 | 1.065 |
| 21–22 | 0.505 | 0.988 |
| 22–23 | 0.476 | 1.041 |
| 23–24 | 0.539 | 0.975 |
| 24–25 | 0.463 | 1.043 |
| 25–26 | 0.476 | 1.037 |

**Summary**
- Mean accuracy ≈ **0.489**
- Mean log loss ≈ **1.023**


### Ablation – form_points_diff only
- Mean accuracy ≈ 0.47
- Mean log loss ≈ 1.05


### Ablation – form_goal_diff_diff only
- Mean accuracy ≈ 0.46
- Mean log loss ≈ 1.05

### Ablation – season_strength_diff only
- Mean accuracy ≈ 0.51
- Mean log loss ≈ 1.03

### Ablation – h2h_points_diff only
- Mean accuracy ≈ 0.47
- Mean log loss ≈ 1.05

**Ablation conclusion:**  
Season-long strength is the strongest standalone signal. Other
features provide complementary value and improve calibration when
combined.

### Ablation – season_strength_diff + form_points_diff
- Mean accuracy ≈ 0.51–0.52 (peak ≈ 0.56)
- Mean log loss ≈ 1.01 (best ≈ 0.96)


### Ablation – season_strength_diff + form_goal_diff_diff
- Mean accuracy ≈ 0.50
- Mean log loss ≈ 1.03


### Ablation – season_strength_diff + form_points_diff + form_goal_diff_diff
- Mean accuracy ≈ 0.50
- Mean log loss ≈ 1.02

**Ablation conclusion:**  
Season-long strength is the strongest standalone signal. Points-based
recent form provides consistent complementary value. Goal-difference
form does not improve performance when added alongside points-based
form and is excluded from the final feature set.

**Final feature set:**  
`season_strength_diff`, `form_points_diff`

## Final Model v1 – Evaluation

**Model**
- Logistic Regression (C = 0.3)
- Standardized features
- Rolling season-by-season backtest (train < test)

**Final Feature Set**
- season_strength_diff
- form_points_diff

**Results**
- Mean accuracy ≈ 0.51
- Mean log loss ≈ 1.01
- Best season (2023–24): Accuracy = 0.563, Log loss = 0.957

**Notes**
The final model outperforms a broader differentials-based baseline,
demonstrating that a small, carefully selected feature set yields better
generalization and probability calibration.


## v2 – season_strength_diff + form_points_diff + home_advantage
- Mean accuracy ≈ 0.51
- Mean log loss ≈ 1.03

## v2.1 – season_strength_diff + home_points_lastN + away_points_lastN
- Mean accuracy ≈ 0.51
- Mean log loss ≈ 1.03
- Home and away form show asymmetric effects, but overall performance remains similar to v2.0.


## v3 – Gradient Boosting (non-linear)
- Mean accuracy ≈ 0.46–0.47
- Mean log loss ≈ 1.09

- Initial non-linear model underperforms linear baselines without tuning.


## v3.1 – Gradient Boosting (tuned)
- Mean accuracy ≈ 0.47
- Mean log loss ≈ 1.05

## v3.2 – Gradient Boosting + form_asymmetry
- Mean accuracy ≈ 0.48
- Mean log loss ≈ 1.04



