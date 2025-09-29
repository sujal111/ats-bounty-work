import { useState } from "react";
import DatasetTab from "./DatasetTab";
import EvaluateTab from "./EvaluateTab";
import PromptTab from "./PromptTab";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("dataset");

  return (
    <div>
      <div className="sidebar">
        <button className={activeTab === "dataset" ? "active" : ""} onClick={() => setActiveTab("dataset")}>Dataset</button>
        <button className={activeTab === "evaluate" ? "active" : ""} onClick={() => setActiveTab("evaluate")}>Evaluate</button>
        <button className={activeTab === "prompt" ? "active" : ""} onClick={() => setActiveTab("prompt")}>Prompts</button>
      </div>
      <div className="main">
        {activeTab === "dataset" && <DatasetTab />}
        {activeTab === "evaluate" && <EvaluateTab />}
        {activeTab === "prompt" && <PromptTab />}
      </div>
    </div>
  );
}
