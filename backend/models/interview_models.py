from pydantic import BaseModel


class StartInterviewRequest(BaseModel):
    role: str
    difficulty: str
    interview_type: str


class NextQuestionRequest(BaseModel):
    session_id: str
    previous_question: str
    previous_answer: str