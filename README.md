# OMAS Safety Checker

A full-stack web application for:

- Parsing OMAS specifications
- Encoding OMAS into RBN
- Performing BFS-based safety verification
- Visualizing:
  - Parsing process
  - RBN encoding
  - BFS traversal
  - Reachable global states
  - Safety results

Built using:

- Frontend: React + Vite
- Backend: Flask (Python)

Because apparently staring at terminal logs for six hours became an accepted software engineering methodology.

---

# Features

## Parser Visualization

Displays:

- Parsed agent states
- Actions
- Protocols
- Agent transitions
- Environment transitions
- Initial and leave states

---

## RBN Encoding Visualization

Displays:

- RC transitions
- RL transitions
- Sigma messages
- Unsafe states
- Safety formulas

---

## BFS Safety Checking

Shows:

- BFS levels
- Current global state
- Broadcast transitions
- Tau transitions
- Reachable states
- Unsafe state detection

---

## File Upload Support

Upload OMAS specification files directly from browser.

Supported formats:

- `.txt`

---

# Project Structure

```bash
# Project Structure

```bash
FinalYearProject/
│
├── Code/
│   │
│   ├── Frontend/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── InputPanel.jsx
│   │   │   │   ├── ResultCard.jsx
│   │   │   │   ├── ReachableStates.jsx
│   │   │   │   ├── RBNViewer.jsx
│   │   │   │   └── LogsPanel.jsx
│   │   │   │
│   │   │   ├── services/
│   │   │   │   └── api.js
│   │   │   │
│   │   │   ├── App.jsx
│   │   │   ├── main.jsx
│   │   │   └── styles.css
│   │   │
│   │   ├── package.json
│   │   └── vite.config.js
│   │
│   ├── Backend/
│   │   ├── app.py
│   │   ├── parser.py
│   │   ├── encoder.py
│   │   ├── solver.py
│   │   ├── requirements.txt
│   │   └── test.txt
│   │
│   └── Inputs/
│       ├── input1.txt
│       ├── input2.txt
│       ├── input3.txt
│       ├── input4.txt
│       └── input5.txt
│
├── Presentation/
│
├── Reports/
│
├── Research Paper/
│
└── README.md
└── .gitignore
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/abhishek0628/FinalYearProject
cd FinalYearProject
```


---

# Backend Setup

## 1. Enter backend directory

```bash
cd Code/backend
```

## 2. Create virtual environment

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Flask server

```bash
python app.py
```

Backend runs on:

```txt
http://localhost:5001
```

---

# Frontend Setup

## 1. Enter frontend directory
```bash
open another terminal
```

```bash
cd Code/frontend
```

## 2. Install dependencies

```bash
npm install
```

## 3. Run frontend

```bash
npm run dev
```

Frontend runs on:

```txt
http://localhost:5173
```

---

# Backend Requirements

Create `requirements.txt`

```txt
flask
flask-cors
```

Install using:

```bash
pip install -r requirements.txt
```

---

# API Endpoint

## `POST /check`

Checks OMAS safety.

---

## Request

```json
{
  "input": "OMAS specification text"
}
```

---

## Response

```json
{
  "safe": true,
  "unsafe_reached": [],
  "reachable_states": [],
  "rbn": {},
  "logs": []
}
```

---

# Example OMAS Input

```txt
# agent information

l0: 1, l1: 1, l2: 1

a1, a2

l0: a1,a2
l1: a1,a2

l0,a1,b1,{a1},l0
l0,a2,b1,{a2},l0

l0,a1,b2,{a1,a2},l1
l0,a2,b2,{a1,a2},l1

l1,a1,b2,{a2},l1
l1,a2,b2,{a1},l1

l1,a1,b2,{a1,a2},l2
l1,a2,b2,{a1,a2},l2

l0
l0,l1,l2

# environment information

le0,le1

b1,b2

le0:b1,b2
le1:b2

le0

le0,b1,{a1},le0
le0,b1,{a2},le0

le0,b2,{a1,a2},le1
le1,b2,{a1,a2},le1
```

---

# Safety Semantics

The checker performs:

- Dynamic contributor spawning
- Contributor leaving
- Broadcast synchronization
- Simultaneous transitions
- BFS exploration of global states

Global state representation:

```txt
(AgentStateSet, EnvironmentState)
```

Example:

```txt
({sleep, l0, l1}, le0_a1)
```

---

# UI Components

## InputPanel

Features:

- Text input
- File upload
- Run verification button

---

## ResultCard

Displays:

- SAFE / UNSAFE result
- Unsafe states

---

## ReachableStates

Displays all reachable global states.

---

## RBNViewer

Displays:

- RC transitions
- RL transitions
- Sigma
- Safety formulas

---

## LogsPanel

Displays:

- Parsing logs
- Encoding logs
- BFS traversal logs

Basically every internal thought your verifier has while crawling through the state space like a caffeinated detective.

---

# Future Improvements

- Graph visualization
- State transition diagrams
- Petri net export
- Counterexample traces
- Temporal logic support
- Symbolic state compression
- Parallel BFS

Every formal verification project eventually becomes “accidentally building a research paper.”

---

# Author

**Abhishek Kumar**  
abhijnv124@gmail.com

---

# License

MIT License