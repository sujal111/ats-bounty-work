import { useState } from "react";
import API from "../../api";

export default function Register({ onRegister }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = async () => {
    try {
      await API.post("/register", { username, password });
      setMessage("Registration successful! You can now login.");
      onRegister();
    } catch (e) {
      setMessage(e.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="container" style={{ maxWidth: "400px", margin: "5rem auto" }}>
      <h2>Register</h2>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button className="action" onClick={handleRegister}>Register</button>
      {message && <p>{message}</p>}
    </div>
  );
}
