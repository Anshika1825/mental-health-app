import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

print("🔄 Starting model training...")

# Load dataset
data = pd.read_csv("mental_health.csv")
print("✅ Dataset loaded")

# Select PHQ columns
data = data[['phq1','phq2','phq3','phq4','phq5','phq6','phq7','phq8','phq9']]

# Handle missing values
data = data.fillna(0)

print("✅ Data cleaned")

# Create score
data['score'] = data.sum(axis=1)

# Create output (0 = Normal, 1 = Depression risk)
data['Outcome'] = data['score'].apply(lambda x: 1 if x > 10 else 0)

# Features and target
X = data[['phq1','phq2','phq3','phq4','phq5','phq6','phq7','phq8','phq9']]
y = data['Outcome']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("✅ Data split done")

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print("✅ Model trained")

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("🎉 Model saved as model.pkl")