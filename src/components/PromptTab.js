import { useState } from "react";
import API from "../api";

export default function PromptTab() {
  const [alias, setAlias] = useState("");
  const [version, setVersion] = useState("");
  const [type, setType] = useState("text");
  const [content, setContent] = useState("");
  const [variables, setVariables] = useState({});
  const [rendered, setRendered] = useState("");

  const createVersion = async () => {
    try {
      await API.post("/prompts/create-version", { alias, version, type, content });
      alert("Prompt version created!");
    } catch (e) {
      alert(e.response?.data?.detail || "Error creating prompt");
    }
  };

  const renderPrompt = async () => {
    try {
      const resp = await API.post("/prompts/render", { alias, version, variables });
      setRendered(resp.data.rendered_prompt);
    } catch (e) {
      alert(e.response?.data?.detail || "Error rendering prompt");
    }
  };

  return (
    <div className="container">
      <h2>Prompt Manager</h2>
      <input placeholder="Alias" value={alias} onChange={(e) => setAlias(e.target.value)} />
      <input placeholder="Version" value={version} onChange={(e) => setVersion(e.target.value)} />
      <select value={type} onChange={(e) => setType(e.target.value)}>
        <option value="text">Text</option>
        <option value="messages">Messages</option>
      </select>
      <textarea placeholder="Content" rows={4} value={content} onChange={(e) => setContent(e.target.value)} />
      <button className="action" onClick={createVersion}>Create Prompt Version</button>
      <hr />
      <h3>Render Prompt</h3>
      <textarea placeholder="Variables JSON" rows={2} value={JSON.stringify(variables)} onChange={(e) => setVariables(JSON.parse(e.target.value))} />
      <button className="action" onClick={renderPrompt}>Render</button>
      {rendered && <div className="card"><b>Rendered Prompt:</b> <pre>{rendered}</pre></div>}
    </div>
  );
}
