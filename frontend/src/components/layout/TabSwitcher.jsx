import React from "react";

function TabSwitcher({ role, onRoleChange }) {
  return (
    <div className="tab-switcher">
      <button
        className={`tab-button ${role === "senior" ? "active" : ""}`}
        onClick={() => onRoleChange("senior")}
        style={{ fontSize: "18px", padding: "12px 24px" }}
      >
        👴 For Seniors
      </button>
      <button
        className={`tab-button ${role === "caregiver" ? "active" : ""}`}
        onClick={() => onRoleChange("caregiver")}
        style={{ fontSize: "18px", padding: "12px 24px" }}
      >
        💼 For Caregivers
      </button>
    </div>
  );
}

export default TabSwitcher;
