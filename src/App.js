import { useState, useEffect } from "react";
import "./styles.css";
import Dashboard from "./components/Dashboard";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) setLoggedIn(true);
  }, []);

  if (!loggedIn) {
    return showRegister ? (
      <div>
        <Register onRegister={() => setShowRegister(false)} />
        <p style={{ textAlign: "center" }}>
          Already have an account? <button className="action" onClick={() => setShowRegister(false)}>Login</button>
        </p>
      </div>
    ) : (
      <div>
        <Login onLogin={() => setLoggedIn(true)} />
        <p style={{ textAlign: "center" }}>
          Don't have an account? <button className="action" onClick={() => setShowRegister(true)}>Register</button>
        </p>
      </div>
    );
  }

  return (
    <div>
      <header>
        LLM Evaluation Platform
        <button
          style={{ float: "right", background: "#7d00e0", color: "white", border: "none", padding: "0.5rem 1rem", borderRadius: "8px", cursor: "pointer" }}
          onClick={() => {
            localStorage.removeItem("token");
            window.location.reload();
          }}
        >
          Logout
        </button>
      </header>
      <Dashboard />
    </div>
  );
}

export default App;
