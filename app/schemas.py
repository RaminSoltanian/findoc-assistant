from typing import Literal
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)

class Answer(BaseModel):
    answer: str
    confidence: Literal["high", "medium", "low"]
    topic: Literal["mortgage", "regulation", "banking", "out_of_scope"]
    needs_source_document: bool = Field(
        description="True if a reliable answer needs the bank's own documents")