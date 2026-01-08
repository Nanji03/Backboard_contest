import React, { useState } from "react";
import SeniorProfileForm from "./SeniorProfileForm";
import MedicationList from "./MedicationList";
import MedicationForm from "./MedicationForm";
import AppointmentList from "./AppointmentList";
import AppointmentForm from "./AppointmentForm";
import "../../styles/caregiver.css";

function CaregiverDashboard({ seniorId, onSeniorIdChange }) {
  const [activeTab, setActiveTab] = useState("profile");
  const [refreshKey, setRefreshKey] = useState(0);

  const handleRefresh = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="caregiver-dashboard">
      <h2>Caregiver Dashboard</h2>

      {/* Tab navigation */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === "profile" ? "active" : ""}`}
          onClick={() => setActiveTab("profile")}
        >
          👤 Senior Profile
        </button>
        <button
          className={`tab ${activeTab === "medications" ? "active" : ""}`}
          onClick={() => setActiveTab("medications")}
        >
          💊 Medications
        </button>
        <button
          className={`tab ${activeTab === "appointments" ? "active" : ""}`}
          onClick={() => setActiveTab("appointments")}
        >
          📅 Appointments
        </button>
      </div>

      {/* Tab content */}
      <div className="tab-content">
        {activeTab === "profile" && (
          <SeniorProfileForm seniorId={seniorId} onSaved={handleRefresh} />
        )}

        {activeTab === "medications" && (
          <div className="two-column">
            <div className="column">
              <h3>Add New Medication</h3>
              <MedicationForm seniorId={seniorId} onAdded={handleRefresh} />
            </div>
            <div className="column">
              <h3>Current Medications</h3>
              <MedicationList key={refreshKey} seniorId={seniorId} />
            </div>
          </div>
        )}

        {activeTab === "appointments" && (
          <div className="two-column">
            <div className="column">
              <h3>Add New Appointment</h3>
              <AppointmentForm seniorId={seniorId} onAdded={handleRefresh} />
            </div>
            <div className="column">
              <h3>Upcoming Appointments</h3>
              <AppointmentList key={refreshKey} seniorId={seniorId} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default CaregiverDashboard;
