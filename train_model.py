import pandas as pd

from ml_model import RiskPredictor

df = pd.read_csv('projects.csv')
descriptions = df['Description'].tolist()
labels = [row.split(',') for row in df['Risk_Types']]

model = RiskPredictor()
model.train(descriptions, labels)

model.save('risk_model.pkl')

print("Model trained and saved as 'risk_model.pkl'.")
