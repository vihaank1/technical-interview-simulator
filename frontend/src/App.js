import { useState } from "react";
import API from "./services/Api";
import "./App.css";

function App() {

  const [role, setRole] = useState("Software Engineer");
  const [difficulty, setDifficulty] = useState("Medium");

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [sessionId, setSessionId] = useState("");
  const [evaluation, setEvaluation] = useState(null);

  const [loading, setLoading] = useState(false);

  async function startInterview() {

    setLoading(true);

    const res = await API.post("/start-interview", {
      role,
      difficulty,
      interview_type: "Technical"
    });

    setSessionId(res.data.session_id);
    setQuestion(res.data.question);

    setLoading(false);
  }

  async function submitAnswer() {

    setLoading(true);

    const res = await API.post("/next-question", {
      session_id: sessionId,
      previous_question: question,
      previous_answer: answer
    });

    setEvaluation(res.data.evaluation);

    setQuestion(res.data.next_question);

    setAnswer("");

    setLoading(false);
  }

  return (
    <div className="app">

      <div className="sidebar">
        <h2>AI Interviewer</h2>

        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          <option>Software Engineer</option>
          <option>Frontend Engineer</option>
          <option>Backend Engineer</option>
          <option>ML Engineer</option>
          <option>Product Manager</option>
        </select>

        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
        >
          <option>Easy</option>
          <option>Medium</option>
          <option>Hard</option>
        </select>

        <button onClick={startInterview}>
          Start Interview
        </button>
      </div>

      <div className="main">

        <div className="chat">

          {question && (
            <div className="message interviewer">
              {question}
            </div>
          )}

          {evaluation && (
            <div className="score-card">

              <h3>
                Score: {evaluation.score}/10
              </h3>

              <div>
                <h4>Strengths</h4>
                <ul>
                  {evaluation?.strengths?.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h4>Weaknesses</h4>
                <ul>
                  {evaluation?.weaknesses?.map((w, i) => (
                    <li key={i}>{w}</li>
                  ))}
                </ul>
              </div>

            </div>
          )}

          {loading && (
            <div className="loading">
              AI Interviewer is thinking...
            </div>
          )}

        </div>

        {question && (
          <div className="answer-box">

            <textarea
              placeholder="Type your answer..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />

            <button onClick={submitAnswer}>
              Submit Answer
            </button>

          </div>
        )}

      </div>

    </div>
  );
}

export default App;