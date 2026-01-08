import React, { useState } from "react";

function SeniorProfileForm({ seniorId, onSaved }) {
  const [form, setForm] = useState({
    name: "",
    age: "",
    contact_phone: "",
    doctor_contact: "",
    caregiver_name: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setMessage("✓ Profile saved (local storage only for now)");
    // In production, this would POST to `/api/profile/`
    localStorage.setItem(`senior_${seniorId}`, JSON.stringify(form));
    onSaved();
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <div className="form-group">
        <label>Senior's Name *</label>
        <input
          type="text"
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="e.g., Margaret Johnson"
          required
        />
      </div>

      <div className="form-group">
        <label>Age</label>
        <input
          type="number"
          name="age"
          value={form.age}
          onChange={handleChange}
          min="18"
        />
      </div>

      <div className="form-group">
        <label>Senior's Contact Phone</label>
        <input
          type="tel"
          name="contact_phone"
          value={form.contact_phone}
          onChange={handleChange}
          placeholder="e.g., +1-555-0123"
        />
      </div>

      <div className="form-group">
        <label>Primary Doctor Contact</label>
        <input
          type="text"
          name="doctor_contact"
          value={form.doctor_contact}
          onChange={handleChange}
          placeholder="e.g., Dr. Smith, 555-9999"
        />
      </div>

      <div className="form-group">
        <label>Caregiver Name (You)</label>
        <input
          type="text"
          name="caregiver_name"
          value={form.caregiver_name}
          onChange={handleChange}
          placeholder="Your name"
        />
      </div>

      {message && <div className="form-message">{message}</div>}

      <button type="submit" className="btn-primary">
        Save Profile
      </button>
    </form>
  );
}

export default SeniorProfileForm;
