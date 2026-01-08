import React, { useState, useEffect } from "react";

function AppointmentList({ seniorId }) {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await fetch(`/api/appointments/${seniorId}`);
        const data = await response.json();
        setAppointments(data.appointments || []);
      } catch (error) {
        console.error("Error fetching appointments:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAppointments();
  }, [seniorId]);

  if (loading) return <p>Loading appointments...</p>;

  if (appointments.length === 0) {
    return <p className="empty-state">No appointments scheduled.</p>;
  }

  return (
    <div className="list">
      {appointments.map((appt, idx) => (
        <div key={idx} className="list-item">
          <div className="item-header">
            <h4>{appt.doctor_name}</h4>
            <span className="date">
              {appt.date} at {appt.time}
            </span>
          </div>
          <div className="item-details">
            {appt.specialization && (
              <p>
                <strong>Type:</strong> {appt.specialization}
              </p>
            )}
            {appt.location && (
              <p>
                <strong>Location:</strong> {appt.location}
              </p>
            )}
            {appt.notes && (
              <p>
                <strong>Notes:</strong> {appt.notes}
              </p>
            )}
            <p className="status">
              Status: <strong>{appt.status}</strong>
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default AppointmentList;
