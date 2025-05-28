from pydantic import BaseModel, Field
from typing import List

class ResponseDS(BaseModel):
    """
    Data Schema for ResponseDS
    """

    field_value: str = Field(..., title="Field Value", description="The value to be filled in the field")

    def __str__(self):
        return f"ResponseDS(field_value={self.field_value})"
    
    def __repr__(self):
        return f"ResponseDS(field_value={self.field_value!r})"