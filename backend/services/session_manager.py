import uuid

sessions = {}


def create_session(role, difficulty, interview_type):

    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "role": role,
        "difficulty": difficulty,
        "interview_type": interview_type,
        "history": [],
        "round": 1,
        "score": 0
    }

    return session_id


def get_session(session_id):
    return sessions.get(session_id)


def add_to_history(session_id, question, answer):

    sessions[session_id]["history"].append({
        "question": question,
        "answer": answer
    })


def increment_round(session_id):
    sessions[session_id]["round"] += 1


def add_score(session_id, score):
    sessions[session_id]["score"] += score