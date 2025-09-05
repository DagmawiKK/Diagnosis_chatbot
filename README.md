# Diagnosis

This project is a NeuroSymbolic Expert System for respiratory disease diagnosis. It combines symbolic reasoning (using MeTTa and a medical knowledge base) with sub-symbolic (LLM/Gemini) capabilities to answer both logical and descriptive medical queries.

---

## Features

- **Symbolic Reasoning:**  
  Uses a curated knowledge base (`kb.metta`) and medical rules (`rules.metta`) to perform logical diagnosis, inference, and treatment recommendations for respiratory diseases.

- **Sub-symbolic Reasoning:**  
  Integrates Google Gemini LLM for general medical questions, explanations, and context-aware answers.

- **Natural Language Interface:**  
  Accepts user queries in plain English and classifies them as symbolic (reasoning) or sub-symbolic (descriptive).

- **Fact Management:**  
  Supports adding, clearing, and listing patient facts via the API or frontend.

- **Interactive Frontend:**  
  Streamlit-based chat interface with sidebar for browsing available facts and rules.

---

## Project Structure

```
backend/
    main.py                # FastAPI backend server
    classifier/            # Query classifier (symbolic vs sub-symbolic)
    subsymbolic/           # Gemini LLM API integration
    symbolic/
        kb.metta           # Medical facts (knowledge base)
        rules.metta        # Medical diagnosis and treatment rules
        metta_reasoner.py  # Symbolic reasoning engine (MeTTa)
        symbolic_ai.metta  # MeTTa logic definitions
    utils/
        config.py          # API key and config loader
        logger.py          # Logging setup
    .env                   # API keys (not tracked by git)
frontend/
    app.py                 # Streamlit chat UI
```

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd Respiratory_Disease_Diagnosis_NeuroSymbolic_AI
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up API keys

Create a `.env` file in the `backend/` directory with your Google API key:

```
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Run the backend server

```bash
cd backend
uvicorn main:app --reload
```

### 6. Run the frontend

In a new terminal:

```bash
cd frontend
streamlit run app.py
```

---

## Usage

- **Ask diagnosis or inference questions** (e.g., "Who has asthma?", "Prove patient1 has COPD", "What can be inferred if patient1 has pneumonia?")
- **Ask descriptive questions** (e.g., "What is asthma?", "Explain the difference between asthma and COPD")
- **Add new facts** using the chat:  
  ```
  add new facts> Abebe presents with wheezing> Abebe presents with chest_tightness> ...
  ```
- **Clear facts** using the chat:  
  ```
  clear facts
  ```

---

## Customization

- **Knowledge Base:**  
  Edit `backend/symbolic/kb.metta` to add or modify patient facts.
- **Rules:**  
  Edit `backend/symbolic/rules.metta` to add or modify diagnosis and treatment rules.
- **Frontend Sidebar:**  
  The sidebar displays all available facts and rules in human-readable format.

---

## Troubleshooting

- **Port already in use:**  
  Kill the process using the port (default 8000) or run on a different port.
- **No diagnosis made:**  
  Ensure facts and rule arguments match exactly (including spelling and underscores).
- **API key errors:**  
  Make sure your `.env` file is present and contains a valid Google API key.

---

## License

MIT License

---

## Acknowledgements

- [Hyperon/MeTTa](https://github.com/trueagi-io/hyperon-experimental) for symbolic reasoning
- [Google Gemini](https://ai.google.dev/) for LLM
