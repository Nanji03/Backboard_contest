import React, { useState } from "react";
import "./styles/globals.css";
import Header from "./components/layout/Header";
import TabSwitcher from "./components/layout/TabSwitcher";
import CaregiverDashboard from "./components/caregiver/CaregiverDashboard";
import SeniorAssistant from "./components/senior/SeniorAssistant";

function App() {
  const [role, setRole] = useState("senior"); // "senior" or "caregiver"
  const [seniorId, setSeniorId] = useState("demo-senior-001");

  return (
    <div className="app">
      <Header />
      <TabSwitcher role={role} onRoleChange={setRole} />
      
      <main className="main-content">
        {role === "senior" ? (
          <SeniorAssistant seniorId={seniorId} />
        ) : (
          <CaregiverDashboard seniorId={seniorId} onSeniorIdChange={setSeniorId} />
        )}
      </main>
    </div>
  );
}

export default App;
