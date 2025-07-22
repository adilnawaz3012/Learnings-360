from datetime import datetime
from uuid import uuid4
from ..models.database_models import PresentationDB
from ..models.schemas import PresentationConfig

async def create_presentation_record(config: PresentationConfig, user):
    presentation_id = str(uuid4())
    presentation = PresentationDB(
        id=presentation_id,
        title=config.title,
        owner_id=user.id,
        config=config.dict(),
        status="processing",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(presentation)
    db.commit()
    return presentation

async def get_presentation_record(presentation_id, user_id):
    presentation = db.query(PresentationDB).filter(
        PresentationDB.id == presentation_id,
        PresentationDB.owner_id == user_id
    ).first()
    if not presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")
    return presentation

async def update_presentation_config(presentation_id, user_id, config_update):
    presentation = await get_presentation_record(presentation_id, user_id)
    # Update logic here
    return presentation