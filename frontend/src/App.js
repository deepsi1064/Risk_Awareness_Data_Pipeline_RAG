import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [risks, setRisks] = useState([]);
  const [selected, setSelected] = useState(null);
  const [filtered,setfiltered] = useState([]);
  useEffect(() => {
    fetch("http://localhost:8080/api/risk/all")
      .then((res) => res.json())
      .then((data) => {
       setRisks(data);
       setfiltered(data);

      })
      .catch((err) => console.error(err));
  }, []);

  const getColor = (priority) => {
    if (priority === "HIGH") return "red";
    if (priority === "MEDIUM") return "orange";
    return "green";
  };
 
  
  const filterData = (type) => {
    if (type === "ALL") {
      setFiltered(risks);
    } else {
      setFiltered(risks.filter((r) => r.priority === type));
    }
  };

  const count = (type) =>
    risks.filter((r) => r.priority === type).length;
  return (
    <div className="container">
      <h1>🚨 Risk Dashboard</h1>
      <div className="cards">
        <div className="card">Total: {risks.length}</div>
        <div className="card high">High: {count("HIGH")}</div>
        <div className="card medium">Medium: {count("MEDIUM")}</div>
        <div className="card low">Low: {count("LOW")}</div>
      </div>
      {/* FILTER BUTTONS */}
      <div className="filters">
        <button onClick={() => filterData("ALL")}>All</button>
        <button onClick={() => filterData("HIGH")}>High</button>
        <button onClick={() => filterData("MEDIUM")}>Medium</button>
        <button onClick={() => filterData("LOW")}>Low</button>
      </div>
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