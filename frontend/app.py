import streamlit as st
import requests
import os
import re

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# API endpoint
API_URL = "http://localhost:8001/query"

def metta_fact_to_human_readable(line):
    # Simple parser for the most common fact patterns
    if "Presents" in line:
        match = re.search(r"\(Presents (\w+) ([\w_]+)\)", line)
        if match:
            return f"{match.group(1).capitalize()} presents with {match.group(2).replace('_', ' ')}."
    if "Shows" in line:
        match = re.search(r"\(Shows ([\w_]+) (\w+) ([\w_]+)\)", line)
        if match:
            return f"{match.group(2).capitalize()}'s {match.group(1).replace('_', ' ')} shows {match.group(3).replace('_', ' ')}."
    if "HasRiskFactor" in line:
        match = re.search(r"\(HasRiskFactor (\w+) ([\w_]+)\)", line)
        if match:
            return f"{match.group(1).capitalize()} has risk factor: {match.group(2).replace('_', ' ')}."
    if "HasMedicalHistory" in line:
        match = re.search(r"\(HasMedicalHistory (\w+) ([\w_]+)\)", line)
        if match:
            return f"{match.group(1).capitalize()} has medical history of {match.group(2).replace('_', ' ')}."
    if "HasPhysicalFinding" in line:
        match = re.search(r"\(HasPhysicalFinding (\w+) ([\w_]+)\)", line)
        if match:
            return f"{match.group(1).capitalize()} has physical finding: {match.group(2).replace('_', ' ')}."
    return line.strip()

def load_facts():
    kb_path = os.path.join(os.path.dirname(__file__), "../backend/symbolic/kb.metta")
    facts = []
    if os.path.exists(kb_path):
        with open(kb_path) as f:
            for line in f:
                label_match = re.search(r"\(:\s*([A-Z0-9_]+)\s+\(", line)
                label = label_match.group(1) if label_match else None
                if "(Presents" in line or "(Shows" in line or "(HasRiskFactor" in line or "(HasMedicalHistory" in line or "(HasPhysicalFinding" in line:
                    fact_text = metta_fact_to_human_readable(line)
                    if label:
                        facts.append(f"**{label}**: {fact_text}")
                    else:
                        facts.append(fact_text)
    return facts

def metta_rule_to_human_readable(line):
    import re
    diag_match = re.search(r"\(: (\w+)_diagnosis_rule\s+\(->(.+)\(DiagnosedWith \$patient ([\w_]+)\)\)+", line.replace("\n", " "))
    if diag_match:
        disease = diag_match.group(3).replace('_', ' ')
        factors = re.findall(r"\(Presents \$patient ([\w_]+)\)", line)
        factors += re.findall(r"\(Shows ([\w_]+) \$patient ([\w_]+)\)", line)
        factors += re.findall(r"\(HasRiskFactor \$patient ([\w_]+)\)", line)
        factors += re.findall(r"\(HasMedicalHistory \$patient ([\w_]+)\)", line)
        factors += re.findall(r"\(HasPhysicalFinding \$patient ([\w_]+)\)", line)
        readable_factors = []
        for f in factors:
            if isinstance(f, tuple):
                readable_factors.append(f"{f[0].replace('_', ' ')}: {f[1].replace('_', ' ')}")
            else:
                readable_factors.append(f.replace('_', ' '))
        if readable_factors:
            return f"Diagnose {disease} if patient has: " + ", ".join(readable_factors)
        else:
            return f"Diagnose {disease} (see rule details)"
    treat_match = re.search(r"\(: (\w+)_indication_rule\s+\(-> \(DiagnosedWith \$patient ([\w_]+)\)\s+\(IndicatedFor \$patient ([\w_]+)\)\)\)", line.replace("\n", " "))
    if treat_match:
        return f"If diagnosed with {treat_match.group(2).replace('_', ' ')}, indicate treatment: {treat_match.group(3).replace('_', ' ')}"
    contra_match = re.search(r"\(: (\w+)_contraindication_rule\s+\(-> \(DiagnosedWith \$patient ([\w_]+)\)\s+\(ContraindicatedFor \$patient ([\w_]+)\)\)\)", line.replace("\n", " "))
    if contra_match:
        return f"If diagnosed with {contra_match.group(2).replace('_', ' ')}, contraindicated: {contra_match.group(3).replace('_', ' ')}"
    prog_match = re.search(r"\(: (\w+)_prognosis_rule\s+\(-> \(DiagnosedWith \$patient ([\w_]+)\)\s+\(-> \(ClassifiedAs \$patient [\w_]+ [\w_]+\)\s+\(HasPrognosis \$patient ([\w_]+)\)\)\)\)", line.replace("\n", " "))
    if prog_match:
        return f"If diagnosed with {prog_match.group(2).replace('_', ' ')} and classified as advanced stage, prognosis: {prog_match.group(3).replace('_', ' ')}"
    follow_match = re.search(r"\(: (\w+)_requirement_rule\s+\(-> \(DiagnosedWith \$patient ([\w_]+)\)\s+\(RequiresFollowUp \$patient ([\w_]+)\)\)\)", line.replace("\n", " "))
    if follow_match:
        return f"If diagnosed with {follow_match.group(2).replace('_', ' ')}, requires follow-up: {follow_match.group(3).replace('_', ' ')}"
    return None

def load_rules():
    rules_path = os.path.join(os.path.dirname(__file__), "../backend/symbolic/rules.metta")
    rules = []
    if os.path.exists(rules_path):
        with open(rules_path) as f:
            collecting = False
            rule_lines = []
            for line in f:
                if line.strip().startswith("!(add-reduct &medical_kb (:"):
                    collecting = True
                    rule_lines = [line]
                elif collecting:
                    rule_lines.append(line)
                    if line.strip().endswith(")))") or line.strip().endswith("))))") or line.strip().endswith(")))))"):
                        collecting = False
                        rule_str = "".join(rule_lines)
                        readable = metta_rule_to_human_readable(rule_str)
                        if readable:
                            rules.append(readable)
    return rules

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 350px;
            max-width: 400px;
            width: 350px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar.expander("Show available facts"):
    facts = load_facts()
    if facts:
        st.markdown("\n".join([f"- {fact}" for fact in facts]))
    else:
        st.write("No facts available.")

with st.sidebar.expander("Show diagnosis & treatment rules"):
    rules = load_rules()
    if rules:
        st.markdown("\n".join([f"- {rule}" for rule in rules]))
    else:
        st.write("No rules available.")

st.title("Respiratory Disease Diagnosis System")
st.write("Ask questions about Respiratory Disease Diagnosis. Responses are labeled as 'Symbolic' (reasoning-based) or 'Sub-symbolic' (descriptive).")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            st.markdown(f"_{message['source']} AI_")

if prompt := st.chat_input("Enter your query (e.g., what can we infer if patient1 has pneumonia or What is a pneumonia?)"):
    st.session_state.messages.append({"role": "user", "content": prompt, "source": None})
    
    with st.spinner("Processing your query..."):
        try:
            response = requests.post(API_URL, json={"query": prompt})
            response.raise_for_status()
            result = response.json()
            answer = result.get("response", "No response received")
            source = result.get("source", "Unknown")
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "source": source.capitalize()
            })
            
            st.rerun()
        except requests.RequestException as e:
            st.error(f"Error: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: {str(e)}",
                "source": "Error"
            })
            st.rerun()