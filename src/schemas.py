# Schemas module defining structured output models.
# Uses Pydantic for type validation and structured responses.

from pydantic import BaseModel, Field


class ConceptExplanation(BaseModel):
    # Pydantic model for structured concept explanations
    topic: str = Field(description="The technical topic requested by the user.")
    difficulty_level: str = Field(
        description="The difficulty level of the explanation, such as beginner, intermediate, or advanced."
    )
    explanation: str = Field(
        description="A clear explanation of the topic in simple and practical language."
    )
    example: str = Field(
        description="A short example that helps the user understand the topic."
    )
    recommended_next_step: str = Field(
        description="A practical next step the user can take to keep learning."
    )
