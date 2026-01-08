import React from "react";

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">ElderCare Companion</h1>
        <p className="header-subtitle">
          Medication reminders & health information helper
        </p>
        <p className="disclaimer">
          ⚠️ Educational tool. Not a substitute for medical advice. Always consult your doctor.
        </p>
      </div>
    </header>
  );
}

export default Header;
