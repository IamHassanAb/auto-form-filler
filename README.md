# Auto Form Filler
<div align="center">
    <img src="https://github.com/IamHassanAb/auto-form-filler/raw/main/assets/demo.gif" alt="Description" style="width: 120%;">
    <br>
    DEMO
</div>


A project for automatically filling out forms using an LLM-powered Q&A workflow, with a real-time chat UI and Python FastAPI backend.

## Features

- **Real-time chat interface** for guided form filling
- **WebSocket communication** between frontend and backend
- **LLM-powered question generation and answer extraction** for form fields
- **Automatic validation** of user input
- **Extensible Python backend** using FastAPI and LangChain

## Project Structure

```
auto-form-filler/
│
├── auto-form-ui/           # Frontend (HTML, CSS, JS)
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── auto-form-py-api/       # Python FastAPI backend
│   ├── app.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── context/
│   ├── pds/
│   ├── prompts/
│   ├── states/
│   └── utils/
│
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js (for frontend development, optional)

### Backend Setup

1. **Install dependencies:**
    ```sh
    cd auto-form-py-api
    pip install -r requirements.txt
    ```

2. **Configure environment variables:**
    - Copy `.env.example` to `.env` and add your OpenAI API key.

3. **Run the FastAPI server:**
    ```sh
    uvicorn app:app --reload
    ```

### Frontend Setup

Open `auto-form-ui/index.html` in your browser.  
Make sure the backend server is running and accessible at `ws://localhost:8080/ws` (adjust port if needed).

## Usage

- Click **Auto Fill Form** to start the guided form filling session.
- Answer the questions in the chat interface.
- The form fields will be auto-filled based on your responses.

## Environment Variables

See [`auto-form-py-api/.env.example`](auto-form-py-api/.env.example) for required variables.

---

**Note:** This project uses OpenAI's API and requires a valid API key.
