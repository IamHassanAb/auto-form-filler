from pydantic import BaseModel, Field
from typing import List
from pds.ResponseDS import ResponseDS

class RequestDS(BaseModel):
    """
    Data Schema for RequestDS
    """

    field_name: str = Field(..., title="Field Name", description="The name of the field")
    field_description: str = Field(..., title="Field Description", description="The description of the field")
    question: str | None = Field(None, title="Question", description="The question related to the field")
    answer: str | None = Field(None, title="Answer", description="Answer to the question related to the field can be null")

    def __str__(self):
        return f"RequestDS(field_name={self.field_name}, field_description={self.field_description}, question={self.question}, answer={self.answer})"
    
    def __repr__(self):
        """ For Request Purposes """
        return f"RequestDS(field_name={self.field_name!r}, field_description={self.field_description!r}, question={self.question!r}, answer={self.answer!r})"