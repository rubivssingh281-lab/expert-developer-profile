# Scikit-Learn & Google Machine Learning Foundations Reference

Synthesized from **Scikit-Learn Official User Guide** and **Google Machine Learning Foundational Courses**.

---

## 1. Google ML Foundational Principles & Feature Engineering

### A. Bucketing (Binning) & Outlier Mitigation
- **Concept**: Groups continuous numerical subranges into discrete categorical bins.
- **Why it matters**: Real-world features (e.g. house latitude, customer age, sensor voltage) rarely exhibit purely linear relationships with targets. Bucketing allows linear models or neural nets to learn independent weights for each subrange rather than fitting a single global linear slope.
- **Outlier Containment**: Extreme anomalous tail values are cleanly consolidated into minimum or maximum edge buckets, preventing outlier skew during loss minimization.

### B. Feature Crosses (Non-Linear Representation)
- **Concept**: Synthetic feature created by the Cartesian product of two or more categorical or bucketed features (e.g., `Bucket(Latitude) x Bucket(Longitude)` or `Bucket(WindSpeed) x Bucket(Temperature)`).
- **Engineering Value**: Enables linear models to learn complex non-linear combinations and interaction spaces without altering the underlying convex optimization algorithm.

### C. Data Leakage Vectors
Data leakage occurs when information from outside the training dataset is inadvertently used to create the model, producing artificially inflated validation scores that collapse in production:
1. **Global Preprocessing Trap**: Scaling, normalizing, or imputing missing values on the whole dataset before train/test splitting.
   - *Mitigation*: Strictly fit imputer/scaler on `X_train` only; use `pipeline.fit(X_train, y_train)` and `pipeline.predict(X_test)`.
2. **Temporal Leakage**: Random shuffling of time-series data allows future observations to predict past states.
   - *Mitigation*: Enforce `TimeSeriesSplit` where test indices are always strictly greater than train indices.
3. **Group Leakage**: Multiple observations from the same entity (e.g., patient, user, vehicle) appearing in both train and validation sets.
   - *Mitigation*: Enforce `GroupKFold` or `StratifiedGroupKFold`.

---

## 2. Advanced Evaluation Metrics & Class Imbalance

| Metric | When to Use | Failure Mode |
| :--- | :--- | :--- |
| **Accuracy** | Strictly balanced classes ($50/50$). | Useless on imbalanced data (predicting all negative achieves $99\%$ accuracy on $1\%$ fraud). |
| **ROC-AUC** | Ranking ability across all thresholds; balanced evaluation. | Can be overly optimistic on extreme class imbalance ($< 1\%$ positive rate). |
| **PR-AUC (Average Precision)** | **Gold standard for imbalanced classification** (fraud, disease detection). | Focuses specifically on the positive minority class without rewarding true negatives. |
| **Brier Score** | Evaluates calibration quality of probability estimates. | Sensitive to probabilistic accuracy. |

### Probability Calibration
Raw predicted probabilities from tree ensembles (RandomForest, XGBoost) are not well-calibrated probabilities. Calibrate before using thresholds:
```python
from sklearn.calibration import CalibratedClassifierCV

calibrated_clf = CalibratedClassifierCV(
    estimator=base_estimator,
    method="isotonic",    # or "sigmoid" (Platt scaling) for smaller datasets
    cv=5,
)
calibrated_clf.fit(X_train, y_train)
```

---

## 3. Custom Transformer Protocol (Scikit-Learn BaseEstimator)
Create leak-proof custom transformers compliant with Scikit-Learn API:

```python
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

class OutlierCapper(BaseEstimator, TransformerMixin):
    def __init__(self, lower_percentile=1.0, upper_percentile=99.0):
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile
        
    def fit(self, X, y=None):
        X_arr = np.asarray(X)
        self.lower_bound_ = np.percentile(X_arr, self.lower_percentile, axis=0)
        self.upper_bound_ = np.percentile(X_arr, self.upper_percentile, axis=0)
        return self
        
    def transform(self, X):
        X_arr = np.asarray(X)
        return np.clip(X_arr, self.lower_bound_, self.upper_bound_)
```
