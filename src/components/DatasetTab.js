import { useState } from "react";
import API from "../api";

export default function DatasetTab() {
  const [alias, setAlias] = useState("");
  const [goldens, setGoldens] = useState([{ id: "", input: "", expected_output: "" }]);
  const [message, setMessage] = useState("");

  const handleGoldenChange = (index, field, value) => {
    const newGoldens = [...goldens];
    newGoldens[index][field] = value;
    setGoldens(newGoldens);
  };

  const addGolden = () => setGoldens([...goldens, { id: "", input: "", expected_output: "" }]);

  const createDataset = async () => {
    try {
      const resp = await API.post("/dataset/create", { alias, goldens });
      setMessage(`Dataset created: ${resp.data.alias}`);
      setAlias("");
      setGoldens([{ id: "", input: "", expected_output: "" }]);
    } catch (e) {
      setMessage(e.response?.data?.detail || "Error creating dataset");
    }
  };

  return (
    <div className="container">
      <h2>Create Dataset</h2>
      <input placeholder="Dataset Alias" value={alias} onChange={(e) => setAlias(e.target.value)} />
      {goldens.map((g, i) => (
        <div key={i} className="card">
          <input placeholder="ID" value={g.id} onChange={(e) => handleGoldenChange(i, "id", e.target.value)} />
          <input placeholder="Input" value={g.input} onChange={(e) => handleGoldenChange(i, "input", e.target.value)} />
          <input placeholder="Expected Output" value={g.expected_output} onChange={(e) => handleGoldenChange(i, "expected_output", e.target.value)} />
        </div>
      ))}
      <button className="action" onClick={addGolden}>Add More</button>
      <button className="action" onClick={createDataset}>Create Dataset</button>
      {message && <p>{message}</p>}
    </div>
  );
}
