import React, { useState, useEffect } from "react";
import TodayCard from "./TodayCard";
import ChatWindow from "./ChatWindow";
import "../../styles/senior.css";

function SeniorAssistant({ seniorId }) {
  const [todayData, setTodayData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch today's medications and next appointment
    const fetchTodayData = async () => {
      try {
        const [medsRes, apptRes] = await Promise.all([
          fetch(`/api/medications/${seniorId}/today`),
          fetch(`/api/appointments/${seniorId}/next`),
        ]);

        const meds = await medsRes.json();
        const appt = await apptRes.json();

        setTodayData({
          medications: meds.today_medications || [],
          nextAppointment: appt.next_appointment,
        });
      } catch (error) {
        console.error("Error fetching today data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTodayData();
  }, [seniorId]);

  return (
    <div className="senior-assistant">
      <div className="senior-layout">
        {/* Left panel: Today's info */}
        <aside className="senior-sidebar">
          {loading ? (
            <p>Loading...</p>
          ) : (
            <TodayCard data={todayData} />
          )}
        </aside>

        {/* Right panel: Chat */}
        <section className="senior-chat-section">
          <ChatWindow seniorId={seniorId} role="senior" />
        </section>
      </div>
    </div>
  );
}

export default SeniorAssistant;
