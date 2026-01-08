Elderly Care Companion is a web-based AI assistant that helps elderly users and their caregivers manage daily health tasks in a simple, safe way.  
The **goal** is to reduce missed medications and forgotten appointments, while making health information easier to understand for non‑technical, older adults.

Core objectives:
- Let a caregiver enter and update the senior’s medication schedule and upcoming appointments.
- Give the senior a simple chat interface to:
  - Ask “What do I take this morning?” or “When is my next doctor visit?”.
  - Receive friendly reminders at the right times.
- Allow pasting text from medical reports (e.g., blood test summary) and get a **plain‑language explanation** plus a reminder to discuss details with their doctor, not to replace medical advice.[1][2]

How it uses Backboard.io (for judging):
- Uses **Backboard memory** to store each user’s medications, appointments, preferences, and conversational context across sessions.[3][4]
- Optionally uses **Backboard RAG** to attach and recall prior report texts so the assistant can say things like “In your last blood test, your cholesterol was high.” without manual re-upload.[4]
- Uses Backboard’s **LLM routing/stateful API** to keep conversations consistent and configurable across models.[3][4]

## 2. Recommended tech stack

Pick one of these two variants (both are viable for 6 days):

### Option A: Flask + React (more polished UI)

- **Frontend (React)**
  - React + Vite or Create React App for quick setup.
  - UI pages:
    - Caregiver dashboard:
      - Forms to add/edit medications (name, dosage, schedule, instructions).
      - Forms to add/edit appointments (date, time, doctor, location, notes).
      - Text area to paste medical report text and “attach” it to the user.
    - Senior view:
      - Very simple chat page with:
        - Large text chat bubbles.
        - Input box (optionally microphone button if you add speech later).
  - HTTP calls to Flask backend for:
    - `/api/chat`
    - `/api/medications`
    - `/api/appointments`
    - `/api/reports`

- **Backend (Flask, Python)**
  - Flask for REST API endpoints.
  - Backboard Python/HTTP client to:
    - Store and retrieve per‑user memory (meds, appointments, preferences).[4]
    - Run chat completions with the right system prompt and memory context.
    - (Optional) Use RAG over stored report texts.
  - Simple in‑memory or SQLite/Postgres store for:
    - User accounts / roles (caregiver vs senior).
    - Mapping userId ↔ Backboard memory keys.
  - Lightweight scheduler:
    - For hackathon, can simulate reminders on demand (e.g., “show next reminders” button) or run a background thread that checks every minute and logs reminders.
    - Real notifications (email/SMS) are optional nice‑to‑have.

### Option B: Pure Flask (simpler, faster)

If you want maximum speed, you can do everything server‑rendered:

- **Frontend**
  - Flask templates (Jinja2) for:
    - Caregiver forms for meds/appointments.
    - Chat page that uses AJAX or fetch to `/api/chat`.
  - Basic Bootstrap or Tailwind CSS for quick styling.

- **Backend**
  - Same as above: Flask + Backboard integration for memory and chat logic.[3][4]

Given your comfort with Flask and React, **Option A** is better if you can set up React quickly; **Option B** is safer on time.

## 3. Example project structure

For Flask + React:

```text
eldercare-companion/
  backend/
    app.py
    models.py
    backboard_client.py
    scheduler.py
    requirements.txt
  frontend/
    package.json
    src/
      main.jsx
      App.jsx
      components/
        Chat.jsx
        CaregiverDashboard.jsx
        MedForm.jsx
        AppointmentForm.jsx
        ReportForm.jsx
  README.md
```

Key backend pieces:

- `backboard_client.py`
  - Functions:
    - `create_or_get_thread(user_id)`
    - `store_memory(user_id, meds, appointments, preferences)`
    - `chat_with_user(user_id, message, mode="senior"|"caregiver")`
    - `add_report_document(user_id, text)`
- `app.py`
  - Routes:
    - `POST /api/chat` – takes `userId`, `message`, returns assistant response.
    - `POST /api/medications` – add/update meds for that user.
    - `POST /api/appointments` – add/update appointments.
    - `POST /api/reports` – store pasted report text in RAG.
    - `GET /api/summary` – return “today’s meds” and “next appointment”.

## 4. Example README template text

You can adapt this directly:

> **Project Name:** ElderCare Companion – Backboard.io x McHacks 13  
>  
> **Purpose**  
> ElderCare Companion is an AI‑powered assistant that helps older adults and their caregivers manage medications and medical appointments, and better understand written health information. It reduces missed doses and forgotten visits by combining structured schedules with a conversational interface that remembers each user over time.  
>  
> **Why it matters**  
> Many seniors rely on complex medication plans and frequent appointments, which can be hard to track and understand. Caregivers often juggle multiple responsibilities and cannot always be present. ElderCare Companion provides a simple chat‑based interface tailored to elderly users, while giving caregivers a clear dashboard to configure what the assistant should remind and explain.  
>  
> **Backboard.io integration**  
> - Uses Backboard **stateful memory** to store per‑user medication schedules, appointment calendars, and conversational context, so the assistant “remembers” the senior’s routine and preferences across sessions.[4][3]
> - Uses Backboard **RAG** to attach and query previous report texts, enabling grounded explanations like “In your last blood test, your glucose was high” instead of generic answers.[4]
> - Uses Backboard’s LLM routing to stay flexible on model choice and future scaling.[3]
>  
> **Scope & safety**  
> ElderCare Companion is an educational and reminder tool. It does **not** diagnose conditions, change dosages, or make treatment decisions. For any medical concerns, users are instructed to consult their physician.[2][5]

## 5. How to position this for the judges

In your 3–5 minute video, emphasize:

- Problem: Medication adherence and appointment tracking are hard for seniors and caregivers.
- Solution: Simple chat + caregiver dashboard with persistent memory.
- Backboard focus:
  - Show how changing models or restarting the app does not lose the senior’s schedule because it lives in Backboard memory.[3][4]
  - Show asking about a previously pasted report (“What was my last cholesterol result?”) and how the assistant answers using the stored document.