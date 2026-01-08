import React from "react";

function TodayCard({ data }) {
  if (!data) {
    return <div className="today-card">Loading...</div>;
  }

  const { medications, nextAppointment } = data;

  return (
    <div className="today-card">
      <h2 className="today-title">📋 Today's Plan</h2>

      {/* Medications */}
      <div className="today-section">
        <h3 className="section-title">💊 Medications</h3>
        {medications && medications.length > 0 ? (
          <ul className="med-list">
            {medications.map((med, idx) => (
              <li key={idx} className="med-item">
                <strong>{med.name}</strong>
                <br />
                {med.dose_quantity} × {med.dosage} — {med.frequency}
                {med.instructions && (
                  <>
                    <br />
                    <small className="instructions">{med.instructions}</small>
                  </>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p className="no-data">No medications scheduled for today.</p>
        )}
      </div>

      {/* Next Appointment */}
      <div className="today-section">
        <h3 className="section-title">📅 Next Appointment</h3>
        {nextAppointment ? (
          <div className="appt-box">
            <p>
              <strong>{nextAppointment.doctor_name}</strong>
              {nextAppointment.specialization && (
                <span className="spec"> ({nextAppointment.specialization})</span>
              )}
            </p>
            <p>{nextAppointment.date} at {nextAppointment.time}</p>
            {nextAppointment.location && (
              <p className="location">📍 {nextAppointment.location}</p>
            )}
          </div>
        ) : (
          <p className="no-data">No upcoming appointments scheduled.</p>
        )}
      </div>

      <div className="disclaimer-small">
        ℹ️ Ask your caregiver if you have questions about your medications or appointments.
      </div>
    </div>
  );
}

export default TodayCard;
