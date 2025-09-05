import os
from hyperon import MeTTa
from backend.utils.logger import setup_logger
# from backend.symbolic.fcc_interpreter import FCCInterpreter

class MettaReasoner:
    def __init__(self, gemini_api):
        self.logger = setup_logger()
        self.gemini_api = gemini_api
        self.kb_path = os.path.join(os.path.dirname(__file__), "kb.metta")
        self.ai_path = os.path.join(os.path.dirname(__file__), "symbolic_ai.metta")
        self.rules_path = os.path.join(os.path.dirname(__file__), "rules.metta")
        self.load_default_kb()

    def load_default_kb(self):
        self.metta = MeTTa()
        with open(self.kb_path) as file:
            kb_str = file.read()
        self.logger.info("Loading facts from kb.metta")
        with open(self.rules_path) as file:
            rules_str = file.read()
        with open(self.ai_path) as file:
            ai_str = file.read()

        self.metta.run(kb_str)
        self.metta.run(rules_str)
        self.metta.run(ai_str)
    
    def load_custome_kb(self):

        custom_facts_path = os.path.join(os.path.dirname(self.kb_path), "custom_facts.metta")
        use_custom = os.path.exists(custom_facts_path) and os.path.getsize(custom_facts_path) > 0
        self.metta = MeTTa()
        if use_custom:
            with open(custom_facts_path) as file:
                kb_str = file.read()
            self.logger.info("Loading custom facts from custom_facts.metta")
        else:
            self.logger.info("No custom facts found. Using default knowledge base.")
            self.load_default_kb()
            return
        with open(self.rules_path) as file:
            rules_str = file.read()
        with open(self.ai_path) as file:
            ai_str = file.read()

        self.metta.run(kb_str)
        self.metta.run(rules_str)
        self.metta.run(ai_str)
    def convert_query_to_metta(self, query):
        prompt = f"""
                    You are an expert assistant for a symbolic AI medical diagnosis system using the MeTTa language. Your task is to convert natural language queries about respiratory illnesses into valid MeTTa function calls for reasoning.

                    Supported reasoning modes:
                    - Use **backward chaining (`bc`)** for queries about proving, checking, asking if someone is diagnosed, or who has an illness (e.g., "Who is sick with X?", "Prove that patient1 has X").
                    - Use **forward chaining (`fcc`)** for causal inference requests (e.g., "Infer who might have X", "Determine diagnoses", "Run inference on symptoms").

                    Variable usage:
                    - If no specific patient is mentioned, use `$patient`.
                    - If a patient is mentioned (e.g., "Prove that patient1 has asthma"), use the given patient ID directly (e.g., `patient1`).

                    If the illness is **not in the supported list**, output only:
                    **Illness not supported.**

                    ---

                    Supported illnesses and MeTTa calls:

                    asthma:
                    - bc:  !(bc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient asthma)))
                    - fcc: !(fcc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient asthma)))

                    copd:
                    - bc:  !(bc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient copd)))
                    - fcc: !(fcc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient copd)))

                    pulmonary_tuberculosis:
                    - bc:  !(bc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient pulmonary_tuberculosis)))
                    - fcc: !(fcc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient pulmonary_tuberculosis)))

                    lung_cancer:
                    - bc:  !(bc &medical_kb (fromNumber 7) (: $prf (DiagnosedWith $patient lung_cancer)))
                    - fcc: !(fcc &medical_kb (fromNumber 7) (: $prf (DiagnosedWith $patient lung_cancer)))

                    pulmonary_embolism:
                    - bc:  !(bc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient pulmonary_embolism)))
                    - fcc: !(fcc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient pulmonary_embolism)))

                    acute_bronchitis:
                    - bc:  !(bc &medical_kb (fromNumber 5) (: $prf (DiagnosedWith $patient acute_bronchitis)))
                    - fcc: !(fcc &medical_kb (fromNumber 5) (: $prf (DiagnosedWith $patient acute_bronchitis)))

                    pleural_effusion:
                    - bc:  !(bc &medical_kb (fromNumber 5) (: $prf (DiagnosedWith $patient pleural_effusion)))
                    - fcc: !(fcc &medical_kb (fromNumber 5) (: $prf (DiagnosedWith $patient pleural_effusion)))

                    allergic_asthma:
                    - bc:  !(bc &medical_kb (fromNumber 5) (: $prf (DiagnosedWith $patient allergic_asthma)))
                    - fcc: !(fcc &medical_kb (fromNumber 5) (: $prf (DiagnosedWith $patient allergic_asthma)))

                    pneumoconiosis:
                    - bc:  !(bc &medical_kb (fromNumber 5) (: $prf (DiagnosedWith $patient pneumoconiosis)))
                    - fcc: !(fcc &medical_kb (fromNumber 5) (: $prf (DiagnosedWith $patient pneumoconiosis)))

                    acute_respiratory_distress_syndrome:
                    - bc:  !(bc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient acute_respiratory_distress_syndrome)))
                    - fcc: !(fcc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient acute_respiratory_distress_syndrome)))

                    congestive_heart_failure_with_pulmonary_edema:
                    - bc:  !(bc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient congestive_heart_failure_with_pulmonary_edema)))
                    - fcc: !(fcc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient congestive_heart_failure_with_pulmonary_edema)))

                    laryngitis:
                    - bc:  !(bc &medical_kb (fromNumber 3) (: $prf (DiagnosedWith $patient laryngitis)))
                    - fcc: !(fcc &medical_kb (fromNumber 3) (: $prf (DiagnosedWith $patient laryngitis)))

                    pneumothorax:
                    - bc:  !(bc &medical_kb (fromNumber 4) (: $prf (DiagnosedWith $patient pneumothorax)))
                    - fcc: !(fcc &medical_kb (fromNumber 4) (: $prf (DiagnosedWith $patient pneumothorax)))

                    pneumonia:
                    - bc:  !(bc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient pneumonia)))
                    - fcc:  !(fcc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient pneumonia)))


                    supported treatments and metta calls:

                    beta2_agonist_bronchodilators:
                    - bc:  !(bc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient beta2_agonist_bronchodilators)))
                    - fcc:  !(fcc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient beta2_agonist_bronchodilators)))

                    long_acting_bronchodilators:
                    - (bc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient long_acting_bronchodilators)))
                    - (fcc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient long_acting_bronchodilators)))

                    broad_spectrum_antibiotics:
                    - bc:  !(bc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient broad_spectrum_antibiotics)))
                    - fcc:  !(fcc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient broad_spectrum_antibiotics)))

                    anti_tuberculosis_therapy:
                    - bc:  !(bc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient anti_tuberculosis_therapy)))
                    - fcc:  !(fcc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient anti_tuberculosis_therapy)))
                    anticoagulation_therapy
                    - bc:  !(bc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient anticoagulation_therapy)))
                    - fcc:  !(fcc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient anticoagulation_therapy)))

                    ---

                    Instructions:
                    1. Identify the illness or treatment from the query.
                    2. Choose `bc` if the query implies a question, proof, or diagnosis check.
                    3. Choose `fcc` if the query implies causal inference or symptom-based reasoning and also incudes specified person. perfer bc if no person is refered.
                    4. Replace `$patient` with an actual patient ID only if explicitly stated (e.g., patient1, person2).
                    5. Output the corresponding MeTTa function call only. No extra text.

                    ---

                    Examples:

                    Input: Who is sick with asthma?
                    Output: !(bc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith $patient asthma)))

                    Input: Who is recommended for beta2_agonist_bronchodilators?
                    Output: !(bc &medical_kb (fromNumber 7) (: $prf (IndicatedFor $patient beta2_agonist_bronchodilators)))

                    Input: What can be inferred if patient1 takes broad_spectrum_antibiotics?
                    Output: !(fcc &medical_kb (fromNumber 8) (: $prf (IndicatedFor patient1 broad_spectrum_antibiotics)))

                    Input: Prove that patient1 has copd.
                    Output: !(bc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith patient1 copd)))

                    Input: Infer if patient1 has pulmonary embolism.
                    Output: !(fcc &medical_kb (fromNumber 6) (: $prf (DiagnosedWith patient1 pulmonary_embolism)))

                    Input: Determine what can be known if patient1 have allergic asthma.
                    Output: !(fcc &medical_kb (fromNumber 5) (: $prf (DiagnosedWith patient1 allergic_asthma)))

                    Input: Is there any patient with pneumothorax?
                    Output: !(bc &medical_kb (fromNumber 4) (: $prf (DiagnosedWith $patient pneumothorax)))

                    Input: Diagnose personX with laryngitis.
                    Output: !(bc &medical_kb (fromNumber 3) (: $prf (DiagnosedWith personX laryngitis)))

                    Input: What is the diagnosis for patient1?
                    Output: Illness not supported.

                    Input: Who is sick with diabetes?
                    Output: Illness not supported.

                    Input: {query}
                    Output:
                    """

        try:
            response = self.gemini_api.llm.invoke(prompt)
            response = response.strip()
            self.logger.info(f"Converted query to MeTTa: {response}")
            if response[2] == "b":
                intent = "bc"
            elif response[2] == "f":
                intent = "fcc"
            return response, intent
        except Exception as e:
            self.logger.error(f"Error converting query to MeTTa: {str(e)}")
            return None
    
    def interpret_metta_response(self, intent, response):
        interpret_prompt = f"""
                You are a medical explanation interpreter for a symbolic respiratory diagnosis system. Given the raw MeTTa reasoning response and the user’s original query intent, convert the proof structure into a clear and informative natural language explanation suitable for a medical user or patient.

                The MeTTa response is a list of proof traces. Each proof includes a sequence of facts (e.g., SYMPTOM1, TEST3, RISK1) and applied rules (e.g., asthma_diagnosis_rule) that lead to a diagnostic conclusion (e.g., DiagnosedWith patient1 asthma).

                Your output should be a structured explanation containing:
                1. **Summary of Diagnosis**: State the diagnosis and the patient involved if intent is bc else state all symptoms and other conslusion arrived as the example states.
                2. **Symptoms, Test Results, and Risk Factors Used**: List the unique facts from the proof(s) that contributed to the diagnosis. Group them if relevant (e.g., symptoms, tests, risk factors).
                3. **Rules Applied**: List the unique diagnosis rules that were used to derive the conclusion.
                4. **Interpretation Note**: If multiple diagnoses or rule chains are involved, explain how they collectively contribute to the diagnosis.

                Avoid repeating the same fact or rule across multiple proofs. Format the explanation clearly with bullet points under each section.

                ---

                **Example**

                Question: Prove that patient1 has copd.
                intent: bc
                MeTTa Response: 
                [(: ((((((copd_diagnosis_rule SYMPTOM1) SYMPTOM11) SYMPTOM9) RISK1) TEST3) TEST10) (DiagnosedWith patient1 copd))]

                Output:

                **Diagnosis Summary**
                - Patient1 is diagnosed with COPD.

                **Evidence Used**
                - **Symptoms**:
                - SYMPTOM1
                - SYMPTOM11
                - SYMPTOM9
                - **Test Results**:
                - TEST3
                - TEST10
                - **Risk Factors**:
                - RISK1

                **Rules Applied**
                - copd_diagnosis_rule

                **Example 2**

                Question: Who has copd?
                intent: bc
                MeTTa Response: 
                [(: ((((((copd_diagnosis_rule SYMPTOM1) SYMPTOM11) SYMPTOM9) RISK1) TEST3) TEST10) (DiagnosedWith patient1 copd))]

                Output:

                **Diagnosis Summary**
                - Patient1 is diagnosed with copd.

                **Evidence Used**
                - **Symptoms**:
                - SYMPTOM1
                - SYMPTOM11
                - SYMPTOM9
                - **Test Results**:
                - TEST3
                - TEST10
                - **Risk Factors**:
                - RISK1

                **Rules Applied**
                - copd_diagnosis_rule

                **Example 3**

                Question: What can be infered if patient1 has asthma?
                intent: fcc
                MeTTa Response: 
                [(: ((((severe_respiratory_condition_rule SYMPTOM14) SYMPTOM13) TEST5) $prf) (ClassifiedAs patient1 asthma severe)), (: (beta_blocker_contraindication_rule $prf) (ContraindicatedFor patient1 beta_blockers)), (: (bronchodilator_indication_rule $prf) (IndicatedFor patient1 beta2_agonist_bronchodilators)), (: $prf (DiagnosedWith patient1 asthma))]
                Output:

                **Diagnosis Summary**
                - Patient1 Shows symptom SYMPTOM14 and SYMPTOM13, has taken TEST5, and is classified as asthma sever and contrained for beta_blocker and indicated for beta2_agonist_bronchodilators.

                **Evidence Used**
                **Rules Applied**
                - severe_respiratory_condition_rule
                - beta_blocker_contraindication_rule
                - bronchodilator_indication_rule

                ---

                Intent: {intent}
                MeTTa Response: {response}

                Output:
                """
        try:
            response = self.gemini_api.llm.invoke(interpret_prompt)
            self.logger.info(f"Interpreted MeTTa response: {response.strip()}")
            return response.strip()
        except Exception as e:  
            self.logger.error(f"Error interpreting MeTTa response: {str(e)}")
            return "Sorry, I couldn't interpret the response."

    def process_query(self, query):
        response, intent = self.convert_query_to_metta(query)
        if response == "Illness not supported.":
            return response
        metta_response = self.metta.run(response)
        self.logger.info(f"MeTTa response: {metta_response}")
        interpreted_response = self.interpret_metta_response(intent, metta_response)
        
        return interpreted_response