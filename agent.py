import os
import sqlite3
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel

load_dotenv()


@dataclass
class AgentDependencies:
    pass

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
    result_type=AgentResponse,
    system_prompt=(
        "You are a risk management assistant for construction projects. "
        "When the user provides a new project description, use the get_relevant_incidents tool to retrieve relevant past incidents, "
        "then analyze them to predict potential risks and suggest management strategies. "
        "Return the response with response_type='prediction', and include predicted_risks and suggestions. "
        "When the user reports an incident, use the log_new_incident tool to record it, "
        "then return a confirmation message with response_type='log' and log_message."
    )
)


@agent.tool
def get_relevant_incidents(ctx: RunContext[AgentDependencies], description: str) -> list[dict]:
    """Retrieve incidents from projects with similar descriptions."""
    conn = sqlite3.connect('projects.db')  # Create a new connection
    c = conn.cursor()
    c.execute("SELECT i.* FROM incidents i JOIN projects p ON i.project_id = p.project_id WHERE p.description LIKE ?",
              (f"%{description}%",))
    incidents = c.fetchall()
    conn.close()  # Close the connection
    return [dict(zip([column[0] for column in c.description], row)) for row in incidents]

# Tool to log a new incident
@agent.tool
def log_new_incident(ctx: RunContext[AgentDependencies], project_id: int, incident_type: str, description: str,
                     severity: str, mitigation: str, outcome: str) -> str:
    """Log a new incident into the database."""
    conn = sqlite3.connect('projects.db')  # Create a new connection
    c = conn.cursor()
    c.execute("INSERT INTO incidents (project_id, incident_type, description, severity, mitigation_actions, outcome) "
              "VALUES (?, ?, ?, ?, ?, ?)", (project_id, incident_type, description, severity, mitigation, outcome))
    conn.commit()  # Save changes
    conn.close()   # Close the connection
    return "Incident logged successfully."