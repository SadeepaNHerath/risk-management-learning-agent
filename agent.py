import os
import sqlite3
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel

from ml_model import RiskPredictor

load_dotenv()

@dataclass
class AgentDependencies:
    ml_model: 'RiskPredictor'

class AgentResponse(BaseModel):
    response_type: str = Field(description="Type of response: 'prediction' or 'log'")
    predicted_risks: Optional[list[str]] = Field(None, description="List of predicted risks")
    suggestions: Optional[list[str]] = Field(None, description="List of suggestions for risk management")
    log_message: Optional[str] = Field(None, description="Confirmation message for logging incident")

agent = Agent(
    GroqModel(
        model_name='llama-3.3-70b-versatile',
        api_key=os.getenv("GROQ_API_KEY")
    ),
    deps_type=AgentDependencies,
    result_type=AgentResponse,
    system_prompt=(
        "You are a risk management assistant for construction projects. "
        "When the user provides a new project description, follow these steps: "
        "1. Use the predict_risks tool to get a list of potential risks based on the description. "
        "2. For each predicted risk, provide specific suggestions for managing that risk. "
        "3. Return the response with response_type='prediction', and include the list of predicted_risks and the corresponding suggestions. "
        "When the user reports an incident, use the log_new_incident tool to record it, "
        "then return a confirmation message with response_type='log' and log_message."
    )
)

@agent.tool
def predict_risks(ctx: RunContext[AgentDependencies], description: str) -> list[str]:
    """Predict potential risks for a new project description using the ML model."""
    return ctx.deps.ml_model.predict(description)

@agent.tool
def log_new_incident(ctx: RunContext[AgentDependencies], project_id: int, incident_type: str, description: str,
                     severity: str, mitigation: str, outcome: str) -> str:
    """Log a new incident into the database."""
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute("INSERT INTO incidents (project_id, incident_type, description, severity, mitigation_actions, outcome) "
              "VALUES (?, ?, ?, ?, ?, ?)", (project_id, incident_type, description, severity, mitigation, outcome))
    conn.commit()
    conn.close()
    return "Incident logged successfully."