import React, { useState } from "react";

function MedicationForm({ seniorId, onAdded }) {
  const [form, setForm] = useState({
    name: "",
    dosage: "",
    dose_quantity: 1,
    frequency: "",
    instructions: "",
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
      const response = await fetch("/api/medications/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          senior_id: seniorId,
          ...form,
          dose_quantity: parseInt(form.dose_quantity),
        }),
      });

      if (response.ok) {
        setMessage("✓ Medication added successfully!");
        setForm({
          name: "",
          dosage: "",
          dose_quantity: 1,
          frequency: "",
          instructions: "",
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
        <label>Medication Name *</label>
        <input
          type="text"
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="e.g., Metformin"
          required
        />
      </div>

      <div className="form-group">
        <label>Dosage *</label>
        <input
          type="text"
          name="dosage"
          value={form.dosage}
          onChange={handleChange}
          placeholder="e.g., 500mg"
          required
        />
      </div>

      <div className="form-group">
        <label>How Many Units? *</label>
        <input
          type="number"
          name="dose_quantity"
          value={form.dose_quantity}
          onChange={handleChange}
          min="1"
          required
        />
      </div>

      <div className="form-group">
        <label>Frequency *</label>
        <select name="frequency" value={form.frequency} onChange={handleChange} required>
          <option value="">-- Select frequency --</option>
          <option value="Morning only">Morning only</option>
          <option value="Twice daily">Twice daily (morning & evening)</option>
          <option value="Three times daily">Three times daily</option>
          <option value="Once daily">Once daily (any time)</option>
          <option value="Every 12 hours">Every 12 hours</option>
          <option value="As needed">As needed</option>
        </select>
      </div>

      <div className="form-group">
        <label>Special Instructions</label>
        <textarea
          name="instructions"
          value={form.instructions}
          onChange={handleChange}
          placeholder="e.g., Take with food, do not crush"
          rows="3"
        />
      </div>

      {message && <div className="form-message">{message}</div>}

      <button type="submit" disabled={loading} className="btn-primary">
        {loading ? "Adding..." : "Add Medication"}
      </button>
    </form>
  );
}

export default MedicationForm;
