import json
import time
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score,
    recall_score, roc_auc_score
)

start_total = time.time()

t0 = time.time()
df = pd.read_csv("creditcard.csv")
load_time = time.time() - t0

X = df.drop("Class", axis=1)
y = df["Class"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

train_data = lgb.Dataset(X_train, label=y_train)
params = {"objective": "binary", "metric": "auc", "verbosity": -1, "seed": 42}

t0 = time.time()
model = lgb.train(
    params, train_data, num_boost_round=200,
    valid_sets=[train_data], callbacks=[lgb.log_evaluation(50)]
)
train_time = time.time() - t0

y_pred_proba = model.predict(X_test)
y_pred = (y_pred_proba >= 0.5).astype(int)

results = {
    "load_data_seconds": round(load_time, 4),
    "training_seconds": round(train_time, 4),
    "best_iteration": model.best_iteration,
    "auc_roc": round(roc_auc_score(y_test, y_pred_proba), 4),
    "accuracy": round(accuracy_score(y_test, y_pred), 4),
    "f1_score": round(f1_score(y_test, y_pred), 4),
    "precision": round(precision_score(y_test, y_pred), 4),
    "recall": round(recall_score(y_test, y_pred), 4),
}

t0 = time.time()
model.predict(X_test.iloc[[0]])
results["inference_latency_1_row_ms"] = round((time.time() - t0) * 1000, 4)

t0 = time.time()
model.predict(X_test.iloc[:1000])
results["inference_throughput_1000_rows_ms"] = round((time.time() - t0) * 1000, 4)
results["total_seconds"] = round(time.time() - start_total, 4)

print("\n=== Benchmark Results (r5.2xlarge) ===")
for k, v in results.items():
    print(f"  {k}: {v}")

with open("benchmark_result.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved benchmark_result.json")
