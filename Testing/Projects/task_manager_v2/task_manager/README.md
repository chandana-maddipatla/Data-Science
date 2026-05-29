# Task Manager Pro v2.0

Full-stack task management app with FastAPI backend, React frontend, and RTM + STLC testing documents.

---

## Quick Start

### 1. Backend (FastAPI)

```bash
cd task_manager/backend
pip install -r requirements.txt
py -m uvicorn app.main:app --reload --port 8000
```

- API live at: http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

### 2. Frontend (React + Vite)

```bash
cd task_manager/frontend
npm create vite@latest . -- --template react-ts
# Select: "Ignore files and continue"
npm install
```

Replace `src/App.tsx` with the one from this zip, and `src/index.css` with:
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0f172a; }
select option { background: #1e293b; }
```

Then:
```bash
npm run dev
```

- App: http://localhost:5173

### 3. Login

| Field | Value |
|-------|-------|
| Username | admin |
| Password | password |

---

## Testing Files

Open directly in Excel (no setup needed):

- `testing/RTM/RTM_Task_Manager.xlsx` — 15 TCs mapped to 9 requirements + defect log + coverage summary
- `testing/STLC/STLC_Document.xlsx` — All 6 STLC phases + test plan + execution log

To regenerate:
```bash
python testing/RTM/generate_rtm.py
python testing/STLC/generate_stlc.py
```

---

## Project Structure

```
task_manager/
├── backend/
│   ├── app/
│   │   └── main.py          ← FastAPI app
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.tsx           ← React UI
│       └── index.css
├── testing/
│   ├── RTM/
│   │   ├── RTM_Task_Manager.xlsx
│   │   └── generate_rtm.py
│   └── STLC/
│       ├── STLC_Document.xlsx
│       └── generate_stlc.py
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/login | Get JWT token |
| GET | /tasks | List tasks (filterable) |
| POST | /tasks | Create task |
| GET | /tasks/stats/summary | Dashboard counts |
| GET | /tasks/{id} | Get single task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |

---

## Requirements

- Python 3.9+
- Node.js 18+
- Both servers running simultaneously
