from fastapi import APIRouter
from app.models.tool_models import ToolConfigRead

router = APIRouter(prefix="/tool-config", tags=["tool-config"])

@router.get("/", response_model=list[ToolConfigRead])
def list_tool_configs():
    # Dummy response for boilerplate
    return []