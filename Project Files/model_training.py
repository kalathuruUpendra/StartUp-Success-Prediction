import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("startup data.csv")

TARGET = "status"

df[TARGET] = df[TARGET].map({
    "operating": 1,
    "acquired": 1,
    "closed": 0
})

df = df.dropna(subset=[TARGET])

# ==========================
# ONLY FEATURES USED IN UI
# ==========================
FEATURES = [
    "age_first_funding_year",
    "age_last_funding_year",
    "age_first_milestone_year",
    "age_last_milestone_year",
    "relationships",
    "funding_rounds",
    "funding_total_usd",
    "milestones",
    "avg_participants"
]

X = df[FEATURES]
y = df[TARGET]

X = X.fillna(X.median())

# ==========================
# Train Test Split
# ==========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ==========================
# Model
# ==========================
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=2,
    min_samples_leaf=2,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================
# Evaluation
# ==========================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)
print(classification_report(y_test, y_pred))

# ==========================
# Save Model
# ==========================
with open("random_forest_model.pkl", "wb") as f:
    pickle.dump((model, FEATURES, accuracy), f)

print("✅ Model saved correctly")
