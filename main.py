import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import agent, AgentDependencies, AgentResponse
from database import create_database, insert_sample_data, get_training_data
from ml_model import RiskPredictor

ml_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    yield
    print("Shutting down application.")


app = FastAPI(
    title="Risk Management Agent API",
    description="API for predicting and managing risks in construction projects",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve UI files
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str


def get_agent_deps():
    return AgentDependencies(ml_model=ml_model)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Redirect to UI."""
    return RedirectResponse(url="/static/index.html")


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


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring systems."""
    return {"status": "healthy", "model_loaded": ml_model is not None}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"Starting server on {host}:{port}")
    print(f"Visit http://localhost:{port} to access the UI")
    uvicorn.run(app, host=host, port=port, reload=debug)
