from langchain_google_genai import GoogleGenerativeAI
from backend.utils.logger import setup_logger

class GeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.logger = setup_logger()
        self.llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
        self.rag_context = """
        Respiratory Disease Context:
        - Patient1 presents with persistent cough, shortness of breath, chest pain, wheezing, fever, night sweats, weight loss, fatigue, productive cough, hemoptysis, dyspnea, chest tightness, tachypnea, cyanosis, hoarseness, orthopnea, and paroxysmal nocturnal dyspnea.
        - Test results: chest x-ray shows infiltrates, CT chest shows pulmonary nodules and emphysematous changes, spirometry shows obstructive pattern, peak flow shows reduced values, pulse oximetry shows hypoxemia, sputum culture shows bacterial growth, tuberculin skin test is positive, bronchoscopy shows malignant tissue, arterial blood gas shows respiratory acidosis, allergy panel shows environmental allergens, methacholine challenge shows bronchial hyperreactivity, chest x-ray shows pleural effusion and pneumothorax, CT pulmonary angiogram shows pulmonary embolus, echocardiogram shows left heart failure, D-dimer is elevated.
        - Risk factors: tobacco use disorder, occupational dust exposure, family history of atopy, advanced age, immunosuppression, recent travel history, allergen exposure, prolonged immobilization, cardiovascular comorbidity, previous pulmonary disease.
        - Medical history: childhood asthma, previous pneumonia, tuberculosis exposure, malignancy history, thromboembolic events.
        - Physical findings: decreased breath sounds, rales.
        """

    def answer_query(self, query):
        try:
            system_prompt = """
            You are a medical assistant specializing in respiratory diseases. Answer questions related to respiratory disease diagnosis, symptoms, risk factors, test results, and treatment. Use the provided context to ground responses for specific queries about the patient or findings mentioned in the context. For general questions, rely on your knowledge of respiratory medicine. If the query is unrelated to respiratory diseases, respond with: "This query is outside my expertise in respiratory diseases." Use clear, concise language suitable for a medical expert system.

            Context:
            {context}
            """
            prompt = f"{system_prompt.format(context=self.rag_context)}\nUser Query: {query}"
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            self.logger.error(f"Error answering query: {str(e)}")
            return "Sorry, I couldn't process that query."