from fastapi import APIRouter
from app.models.agent_models import AgentConfigRead

router = APIRouter(prefix="/agent-config", tags=["agent-config"])

@router.get("/", response_model=list[AgentConfigRead])
def list_agent_configs():
    # Dummy response for boilerplate
    return []