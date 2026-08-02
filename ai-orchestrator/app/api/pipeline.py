from fastapi import APIRouter

from app.models.incident import Incident
from app.services.pipeline_service import PipelineService

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])


@router.post("/run")
def run_pipeline(incident: Incident):

    return PipelineService.execute(incident.model_dump())