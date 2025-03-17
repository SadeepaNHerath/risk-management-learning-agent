import os
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from agent import agent, AgentDependencies, AgentResponse
from ml_model import RiskPredictor
from database import create_database, insert_sample_data, get_training_data

# Create FastAPI application
app = FastAPI()

# Global variable for the ML model
ml_model = None


@app.on_event("startup")
def startup_event():
    """Initialize the database and load or train the ML model on startup."""
    global ml_model
    create_database()
    insert_sample_data()

    ml_model = RiskPredictor()
    pkl_path = 'risk_model.pkl'
    if os.path.exists(pkl_path):
        print("Loading pre-trained model from", pkl_path)
        ml_model.load(pkl_path)
    else:
        print("No pre-trained model found. Training with database data...")
        data = get_training_data()
        if data:
            descriptions, labels = zip(*data)
            ml_model.train(descriptions, labels)
            ml_model.save(pkl_path)
            print(f"Model trained and saved as {pkl_path}")
        else:
            print("No training data available. Starting with an untrained model.")


# Define the request model for the chat endpoint
class ChatRequest(BaseModel):
    message: str


# Dependency to provide agent dependencies
def get_agent_deps():
    return AgentDependencies(ml_model=ml_model)


@app.post("/chat", response_model=AgentResponse)
def chat(request: ChatRequest, deps: AgentDependencies = Depends(get_agent_deps)):
    """Process the user's message and return the agent's response."""
    result = agent.run_sync(request.message, deps=deps)
    return result.data


@app.get("/info")
def get_info():
    """Provide information about the Risk Management Agent system."""
    return {
        "description": "This is a Risk Management Agent for construction projects. It uses a machine learning model to predict potential risks based on project descriptions and allows logging of incidents for record-keeping and model improvement.",
        "features": [
            "Predict risks for new project descriptions with tailored suggestions.",
            "Log incidents with details such as project ID, type, severity, and outcome."
        ],
        "version": "1.0",
        "author": "Sadeepa Herath",
        "api_documentation": "Visit /docs for interactive API documentation."
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)