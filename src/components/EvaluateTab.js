import { useState } from "react";
import API from "../api";

export default function EvaluateTab() {
  const [alias, setAlias] = useState("");
  const [promptAlias, setPromptAlias] = useState("");
  const [promptVersion, setPromptVersion] = useState("");
  const [variables, setVariables] = useState({});
  const [results, setResults] = useState(null);

  const runEvaluation = async () => {
    try {
      const resp = await API.post(`/evaluate/${alias}`, { prompt_alias: promptAlias, prompt_version: promptVersion, variables });
      setResults(resp.data);
    } catch (e) {
      setResults({ error: e.response?.data?.detail || "Error evaluating" });
    }
  };

  return (
    <div className="container">
      <h2>Evaluate Dataset</h2>
      <input placeholder="Dataset Alias" value={alias} onChange={(e) => setAlias(e.target.value)} />
      <input placeholder="Prompt Alias (optional)" value={promptAlias} onChange={(e) => setPromptAlias(e.target.value)} />
      <input placeholder="Prompt Version (optional)" value={promptVersion} onChange={(e) => setPromptVersion(e.target.value)} />
      <textarea placeholder="Variables JSON" rows={2} value={JSON.stringify(variables)} onChange={(e) => setVariables(JSON.parse(e.target.value))} />
      <button className="action" onClick={runEvaluation}>Run Evaluation</button>

      {results && (
        <div>
          <h3>Results:</h3>
          {results.results?.map((r) => (
            <div key={r.id} className="card">
              <b>ID:</b> {r.id} <br />
              <b>Input:</b> {r.input} <br />
              <b>Expected:</b> {r.expected_output} <br />
              <b>Actual:</b> {r.actual_output} <br />
              <b>Passed:</b> {r.passed ? "✅" : "❌"} <br />
              <b>Score:</b> {r.score}
            </div>
          ))}
          {results.summary && (
            <div>
              <b>Total Cases:</b> {results.summary.total_cases} <br />
              <b>Pass Rate:</b> {results.summary.pass_rate}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
