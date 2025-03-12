import pandas as pd
from ml_model import RiskPredictor

# Load the CSV data
df = pd.read_csv('projects.csv')
descriptions = df['Description'].tolist()
labels = [row.split(',') for row in df['Risk_Types']]

# Initialize and train the model
model = RiskPredictor()
model.train(descriptions, labels)

# Save the trained model as a PKL file
model.save('risk_model.pkl')

print("Model trained and saved as 'risk_model.pkl'.")