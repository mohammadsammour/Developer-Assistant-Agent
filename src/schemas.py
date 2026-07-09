from pydantic import BaseModel,Field
from typing import Literal

class PotentialBug(BaseModel):
    bug : str = Field(default_factory=None, description= "The Suspected Bug or issue.")
    explanation : str = Field(default_factory=None, description="Why this might be a bug and how it affects the code.")
class DeveloperTaskReport(BaseModel):
    task_type: Literal[
        "code_explanation",
        "debugging",
        "feature_planning",
        "general_question",
    ] = Field(description="What kind of developer task this is.")

    difficulty: Literal["easy", "medium", "hard"] = Field(
        description="Estimated difficulty of the task."
    )

    risk_level: Literal["low", "medium", "high"] = Field(
        description="How risky it would be to act on this without review."
    )

    summary: str = Field(
        description="A short, plain-language summary of the analysis."
    )

    key_points: list[str] = Field(
        description="Important observations about the code or request."
    )

    potential_bugs : list[PotentialBug] = Field(
        default_factory=list,
        description="Potential Bugs Found in the code with descriptions"
    )

    next_steps: list[str] = Field(
        description="Concrete, actionable next steps for the developer."
    )

    needs_human_review: bool = Field(
        description="True if a human should double-check this before acting on it."
    )


