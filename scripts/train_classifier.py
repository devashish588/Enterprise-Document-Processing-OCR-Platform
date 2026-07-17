from pathlib import Path
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import csv


ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((ROOT / "sample_data/classifier/training_data.csv").open()))
model = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression(max_iter=500))])
model.fit([row["text"] for row in rows], [row["label"] for row in rows])
out = ROOT / "backend/app/services/classifier.pkl"
with out.open("wb") as handle:
    pickle.dump(model, handle)
print(out)

