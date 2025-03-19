import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer


class RiskPredictor:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultiOutputClassifier(RandomForestClassifier()))
        ])
        self.mlb = MultiLabelBinarizer()

    def train(self, descriptions, labels):
        y = self.mlb.fit_transform(labels)
        self.pipeline.fit(descriptions, y)

    def save(self, filename):
        joblib.dump({'pipeline': self.pipeline, 'mlb': self.mlb}, filename)

    def load(self, filename):
        loaded = joblib.load(filename)
        self.pipeline = loaded['pipeline']
        self.mlb = loaded['mlb']

    def predict(self, description):
        if isinstance(description, str):
            description = [description]
        predictions = self.pipeline.predict(description)
        return self.mlb.inverse_transform(predictions)[0]
