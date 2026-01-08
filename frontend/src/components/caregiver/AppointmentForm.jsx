import React, { useState } from "react";

function AppointmentForm({ seniorId, onAdded }) {
  const [form, setForm] = useState({
    date: "",
    time: "",
    doctor_name: "",
    specialization: "",
    location: "",
    notes: "",
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("/api/appointments/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          senior_id: seniorId,
          ...form,
        }),
      });

      if (response.ok) {
        setMessage("✓ Appointment added successfully!");
        setForm({
          date: "",
          time: "",
          doctor_name: "",
          specialization: "",
          location: "",
          notes: "",
        });
        onAdded();
      } else {
        const error = await response.json();
        setMessage(`✗ Error: ${error.error}`);
      }
    } catch (error) {
      setMessage("✗ Connection error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <div className="form-group">
        <label>Date *</label>
        <input
          type="date"
          name="date"
          value={form.date}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Time *</label>
        <input
          type="time"
          name="time"
          value={form.time}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Doctor Name *</label>
        <input
          type="text"
          name="doctor_name"
          value={form.doctor_name}
          onChange={handleChange}
          placeholder="e.g., Dr. John Smith"
          required
        />
      </div>

      <div className="form-group">
        <label>Specialization</label>
        <input
          type="text"
          name="specialization"
          value={form.specialization}
          onChange={handleChange}
          placeholder="e.g., Cardiologist, General Practice"
        />
      </div>

      <div className="form-group">
        <label>Location</label>
        <input
          type="text"
          name="location"
          value={form.location}
          onChange={handleChange}
          placeholder="e.g., Hospital Name or Address"
        />
      </div>

      <div className="form-group">
        <label>Notes / Preparation</label>
        <textarea
          name="notes"
          value={form.notes}
          onChange={handleChange}
          placeholder="e.g., Bring recent blood test results, fast before appointment"
          rows="3"
        />
      </div>

      {message && <div className="form-message">{message}</div>}

      <button type="submit" disabled={loading} className="btn-primary">
        {loading ? "Adding..." : "Add Appointment"}
      </button>
    </form>
  );
}

export default AppointmentForm;
