from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.classifier.qxn_classifier import QuestionClassifier
from backend.subsymbolic.gemini_api import GeminiAPI
from backend.symbolic.metta_reasoner import MettaReasoner
from backend.utils.config import GOOGLE_API_KEY
from backend.utils.logger import setup_logger
import uuid
import os


app = FastAPI(title="Law Expert System API")
logger = setup_logger()

gemini_api = GeminiAPI(api_key=GOOGLE_API_KEY)
logistic_classifier = QuestionClassifier(gemini_api=gemini_api)
metta_reasoner = MettaReasoner(gemini_api=gemini_api)


CUSTOM_FACTS_PATH = os.path.join(os.path.dirname(metta_reasoner.kb_path), "custom_facts.metta")

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def handle_query(request: QueryRequest):
    try:
        query = request.query.strip()
        logger.info(f"Received query: {query}")

        # Custom "clear facts" command
        if query.lower().strip() == "clear facts":
            metta_reasoner.load_default_kb()
            if os.path.exists(CUSTOM_FACTS_PATH):
                os.remove(CUSTOM_FACTS_PATH)
                logger.info("custom_facts.metta deleted. Default facts will be loaded.")
                return {"response": "All custom facts cleared. Default knowledge base loaded.", "source": "system"}
            else:
                logger.info("No custom_facts.metta to delete. Default facts already in use.")
                return {"response": "No custom facts to clear. Default knowledge base is already loaded.", "source": "system"}

        # Custom "add new facts"
        if query.lower().startswith("add new facts"):
            lines = [line.strip() for line in query.split('>')[1:] if line.strip()]
            added_facts = []
            with open(CUSTOM_FACTS_PATH, "w") as f:
                f.write("!(bind! &medical_kb (new-space))" + "\n")
                for info_text in lines:
                    info_id = f"FACT{uuid.uuid4().hex[:8]}"
                    metta_fact = parse_natural_fact_to_metta(info_text, gemini_api, info_id)
                    f.write(metta_fact + "\n")
                    added_facts.append(metta_fact)
            metta_reasoner.load_custome_kb()
            logger.info("Facts replaced:\n" + "\n".join(added_facts))
            return {"response": "Facts replaced:\n" + "\n".join(added_facts), "source": "system"}

        # Custom "add facts" command
        if query.lower().startswith("add facts"):
            lines = [line.strip() for line in query.split('>')[1:] if line.strip()]
            added_facts = []
            file_exists = os.path.exists(CUSTOM_FACTS_PATH)
            write_header = not file_exists or os.path.getsize(CUSTOM_FACTS_PATH) == 0
            with open(CUSTOM_FACTS_PATH, "a") as f:
                for info_text in lines:
                    info_id = f"FACT{uuid.uuid4().hex[:8]}"
                    metta_fact = parse_natural_fact_to_metta(info_text, gemini_api, info_id)
                    f.write(metta_fact + "\n")
                    added_facts.append(metta_fact)
            metta_reasoner.load_custome_kb()
            logger.info("Facts added:\n" + "\n".join(added_facts))
            return {"response": "Facts added:\n" + "\n".join(added_facts), "source": "system"}

        # Classify query
        confidence, is_symbolic = logistic_classifier.classify(query)

        # Route to appropriate AI
        if is_symbolic:
            response = metta_reasoner.process_query(query)
            source = "symbolic"
            logger.info("Query routed to symbolic AI")
        else:
            response = gemini_api.answer_query(query)
            source = "sub-symbolic"
            logger.info("Query routed to sub-symbolic AI")

        return {"response": response, "source": source}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def parse_natural_fact_to_metta(info_text, gemini_api, info_id):
    prompt = f"""
You are an expert in symbolic AI for medical expert systems.
Convert each clinical info below into MeTTa syntax for a respiratory disease diagnosis system.
Always use the format: !(add-atom &medical_kb (: <info type could be SYMPTOM, TEST, RISK, HISTORY>{{info_id}} (<Predicate> <Patient Name> <argument>)))
Choose the correct predicate and argument based on the meaning of the info type.
Do not add FACT after info type like SYMPTOMFACT0ee6b214, TESTFACTfe6e4ab1, RISKFACT024feb3b. 
It should be SYMPTOM0ee6b214, TESTfe6e4ab1, RISK024feb3b and such with different info_id.
Make sure it is wrraped by !(add-atom &medical_kb ) as the examples state
Use only the following predicates if possible: Presents, Shows, HasRiskFactor, HasMedicalHistory, HasPhysicalFinding.
Use snake_case for arguments. Output only the MeTTa info, no explanations or markdown.

Here are examples based on the knowledge base:

Input: The patient1 has a persistent cough.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 persistent_cough)))

Input: The patient1 has shortness of breath.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 shortness_of_breath)))

Input: The patient1 has chest pain.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 chest_pain)))

Input: The patient1 has wheezing.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 wheezing)))

Input: The patient1 has fever.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 fever)))

Input: The patient1 has night sweats.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 night_sweats)))

Input: The patient1 has weight loss.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 weight_loss)))

Input: The patient1 has fatigue.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 fatigue)))

Input: The patient1 has a productive cough.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 productive_cough)))

Input: The patient1 has hemoptysis.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 hemoptysis)))

Input: The patient1 has dyspnea.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 dyspnea)))

Input: The patient1 has chest tightness.
Output: !(add-atom &medical_kb (: SYMPTOM{info_id} (Presents patient1 chest_tightness)))

Input: The patient1's chest x-ray shows infiltrates.
Output: !(add-atom &medical_kb (: TEST{info_id} (Shows chest_xray patient1 infiltrates)))

Input: The patient1's CT chest shows pulmonary nodules.
Output: !(add-atom &medical_kb (: TEST{info_id} (Shows ct_chest patient1 pulmonary_nodules)))

Input: The patient1's spirometry shows an obstructive pattern.
Output: !(add-atom &medical_kb (: TEST{info_id} (Shows spirometry patient1 obstructive_pattern)))

Input: The patient1's peak flow is reduced.
Output: !(add-atom &medical_kb (: TEST{info_id} (Shows peak_flow patient1 reduced_values)))

Input: The patient1's pulse oximetry shows hypoxemia.
Output: !(add-atom &medical_kb (: TEST{info_id} (Shows pulse_oximetry patient1 hypoxemia)))

Input: The patient1's sputum culture shows bacterial growth.
Output: !(add-atom &medical_kb (: TEST{info_id} (Shows sputum_culture patient1 bacterial_growth)))

Input: The patient1 has the risk factor of tobacco use disorder.
Output: !(add-atom &medical_kb (: RISK{info_id} (HasRiskFactor patient1 tobacco_use_disorder)))

Input: The patient1 has a history of childhood asthma.
Output: !(add-atom &medical_kb (: HISTORY{info_id} (HasMedicalHistory patient1 childhood_asthma)))

Input: The patient1 has decreased breath sounds.
Output: !(add-atom &medical_kb (: HISTORY{info_id} (HasPhysicalFinding patient1 decreased_breath_sounds)))

Input: {info_text} and {info_id} is the unique identifier for this info.
Output:
"""
    metta_fact = gemini_api.llm.invoke(prompt)
    return metta_fact.strip()