import React, { useEffect, useRef, useState } from "react";
import axios from "axios";

const API = "http://localhost:5000/api";

export default function App() {
  const [questions, setQuestions] = useState([]);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [recording, setRecording] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  useEffect(() => {
    axios.get(`${API}/questions`).then((r) => setQuestions(r.data.questions));
  }, []);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    chunksRef.current = [];
    recorder.ondataavailable = (e) => chunksRef.current.push(e.data);
    recorder.onstop = submitRecording;
    recorder.start();
    mediaRecorderRef.current = recorder;
    setRecording(true);
    setResult(null);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  };

  const submitRecording = async () => {
    setLoading(true);
    const blob = new Blob(chunksRef.current, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio", blob, "answer.webm");

    try {
      const res = await axios.post(`${API}/evaluate-answer`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>EchoMind</h1>
        <p>AI mock interview coach -- practice out loud, get delivery feedback</p>
      </header>

      <div className="question-card">
        <span className="q-label">Question {questionIndex + 1} of {questions.length}</span>
        <h2>{questions[questionIndex]}</h2>
        <div className="q-nav">
          <button onClick={() => setQuestionIndex((i) => Math.max(0, i - 1))}>Previous</button>
          <button onClick={() => setQuestionIndex((i) => Math.min(questions.length - 1, i + 1))}>Next</button>
        </div>
      </div>

      <div className="record-panel">
        {!recording ? (
          <button className="record-btn" onClick={startRecording}>Start Answer</button>
        ) : (
          <button className="stop-btn" onClick={stopRecording}>Stop &amp; Analyze</button>
        )}
        {loading && <p>Transcribing and analyzing...</p>}
      </div>

      {result && (
        <div className="feedback-panel">
          <div className="confidence-score">Confidence Score: {result.confidence_score}/100</div>
          <p className="transcript"><strong>Transcript:</strong> {result.transcript}</p>
          <div className="metrics">
            <div><span>Speaking Pace</span><strong>{result.speaking_pace_wpm} wpm</strong></div>
            <div><span>Filler Rate</span><strong>{result.filler_rate_pct}%</strong></div>
            <div><span>Hedging Phrases</span><strong>{result.hedge_phrase_count}</strong></div>
          </div>
          <h3>Feedback</h3>
          <ul>{result.feedback.map((f, i) => <li key={i}>{f}</li>)}</ul>
        </div>
      )}
    </div>
  );
}
