"""Avaliação holdout final."""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

_ROOT = Path(__file__).resolve().parent.parent
DATA = _ROOT / "data" / "processed.csv"
MODEL = _ROOT / "models" / "model.pkl"
METRICS = _ROOT / "metrics" / "eval.json"

df = pd.read_csv(DATA)
X = df[["x1", "x2", "x3"]]
y = df["y"]
_, X_te, _, y_te = train_test_split(X, y, test_size=0.2, random_state=0)

model = joblib.load(MODEL)
proba = model.predict_proba(X_te)[:, 1]
pred = (proba >= 0.5).astype(int)

metrics = {
    "auc": float(roc_auc_score(y_te, proba)),
    "accuracy": float(accuracy_score(y_te, pred)),
    "f1": float(f1_score(y_te, pred)),
}
METRICS.write_text(json.dumps(metrics, indent=2))
print(metrics)
