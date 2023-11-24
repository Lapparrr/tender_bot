from pydantic import BaseModel, ConfigDict

from models.db_model import TenderOrm





class TenderName(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    tender: TenderOrm
    text: str
