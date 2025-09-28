from pydantic import BaseModel, Field
from typing import Optional

class ClassificationResponse(BaseModel):
    label: Optional[str] = Field(
        None,
        description="Classification of user's speech performance.",
        example="Advanced"
    )