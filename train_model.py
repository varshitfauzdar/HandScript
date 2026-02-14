import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Dummy training data (you can later replace with real dataset)
X = np.array([
    [1,0,0,0,0],
    [1,1,0,0,0],
    [1,1,1,1,1]
])

y = np.array([
    "draw",
    "erase",
    "clear"
])

model = RandomForestClassifier()
model.fit(X, y)

with open("gesture_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as gesture_model.pkl")
