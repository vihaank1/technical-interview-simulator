from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from models.interview_models import (
    StartInterviewRequest,
    NextQuestionRequest
)

from services.session_manager import (
    create_session,
    get_session,
    add_to_history,
    increment_round,
    add_score
)

from services.interviewer import (
    generate_question,
    evaluate_answer
)

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/start-interview")
def start_interview(req: StartInterviewRequest):

    session_id = create_session(
        req.role,
        req.difficulty,
        req.interview_type
    )

    question = generate_question(
        req.role,
        req.difficulty
    )

    return {
        "session_id": session_id,
        "question": question
    }


@app.post("/next-question")
def next_question(req: NextQuestionRequest):

    session = get_session(req.session_id)

    if not session:
        return {
            "error": "Session not found"
        }

    evaluation = evaluate_answer(
        req.previous_question,
        req.previous_answer
    )

    add_to_history(
        req.session_id,
        req.previous_question,
        req.previous_answer
    )

    add_score(
        req.session_id,
        evaluation["score"]
    )

    increment_round(req.session_id)

    next_q = generate_question(
        session["role"],
        session["difficulty"]
    )

    return {
        "evaluation": evaluation,
        "next_question": next_q,
        "round": session["round"]
    }