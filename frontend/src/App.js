import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [risks, setRisks] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8080/api/risk/all")
      .then((res) => res.json())
      .then((data) => setRisks(data))
      .catch((err) => console.error(err));
  }, []);

  const getColor = (priority) => {
    if (priority === "HIGH") return "red";
    if (priority === "MEDIUM") return "orange";
    return "green";
  };

  return (
    <div className="container">
      <h1>🚨 Risk Dashboard</h1>

      <table>
        <thead>
          <tr>
            <th>Transaction</th>
            <th>Risks</th>
            <th>Score</th>
            <th>Priority</th>
          </tr>
        </thead>

        <tbody>
          {risks.map((r) => (
            <tr key={r.transactionId} onClick={() => setSelected(r)}>
              <td>{r.transactionId}</td>
              <td>{r.risks}</td>
              <td>{r.score}</td>
              <td style={{ color: getColor(r.priority) }}>
                {r.priority}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selected && (
        <div className="details">
          <h2>🔍 Details</h2>
          <p><b>ID:</b> {selected.transactionId}</p>
          <p><b>Risks:</b> {selected.risks}</p>
          <p><b>Score:</b> {selected.score}</p>
          <p><b>Priority:</b> {selected.priority}</p>
        </div>
      )}
    </div>
  );
}

export default App;