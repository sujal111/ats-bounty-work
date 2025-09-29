import { useState } from "react";
import API from "../../api";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const form = new URLSearchParams();
      form.append("username", username);
      form.append("password", password);
      const resp = await API.post("/token", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      localStorage.setItem("token", resp.data.access_token);
      onLogin();
    } catch (e) {
      setError(e.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="container" style={{ maxWidth: "400px", margin: "5rem auto" }}>
      <h2>Login</h2>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button className="action" onClick={handleLogin}>Login</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
