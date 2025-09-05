from backend.utils.logger import setup_logger

class QuestionClassifier:
    def __init__(self, gemini_api):
        self.gemini_api = gemini_api
        self.logger = setup_logger()
        self.classification_prompt = """
        You are a classifier for a respiratory disease diagnosis expert system. Your task is to classify a user query as either 'symbolic' (requiring logical reasoning, deduction, or inference using medical rules and facts, such as diagnosis, treatment indication, or severity classification) or 'sub-symbolic' (general, descriptive, or ambiguous questions about respiratory diseases, such as definitions, explanations, or broad overviews). Respond only with 'symbolic' or 'sub-symbolic'.

        Examples:
        - Query: "Is the patient diagnosed with asthma?" -> symbolic
        - Query: "what can we infer if someone has asthma?" -> symbolic
        - Query: "What respiratory disease is the patient diagnosed with?" -> symbolic
        - Query: "What symptoms does the patient present with?" -> symbolic
        - Query: "What treatment is indicated for the patient?" -> symbolic
        - Query: "Does the patient have risk factors for tuberculosis?" -> symbolic
        - Query: "Does the chest x-ray show infiltrates?" -> symbolic
        - Query: "Is there evidence of pulmonary embolism based on the CT pulmonary angiogram?" -> symbolic
        - Query: "Does the patient have a history of childhood asthma?" -> symbolic
        - Query: "What physical findings are present in the patient?" -> symbolic
        - Query: "Is the patient at risk due to tobacco use disorder?" -> symbolic
        - Query: "What is asthma?" -> sub-symbolic
        - Query: "Explain the difference between asthma and COPD." -> sub-symbolic
        - Query: "What are the risk factors for pneumonia?" -> sub-symbolic
        - Query: "Describe the symptoms of tuberculosis." -> sub-symbolic
        - Query: "What is a chest x-ray?" -> sub-symbolic
        - Query: "How does spirometry work?" -> sub-symbolic
        - Query: "What is the significance of hypoxemia?" -> sub-symbolic
        - Query: "What are common respiratory diseases?" -> sub-symbolic

        Query: {query}
        """

    def classify(self, query):
        try:
            response = self.gemini_api.llm.invoke(self.classification_prompt.format(query=query))
            classification = response.strip().lower()
            if classification not in ['symbolic', 'sub-symbolic']:
                self.logger.warning(f"Invalid classification response: {classification}, defaulting to sub-symbolic")
                return 0.5, False
            is_symbolic = classification == 'symbolic'
            confidence = 0.9 if classification in ['symbolic', 'sub-symbolic'] else 0.5 
            self.logger.info(f"Classified query '{query}' as {classification}")
            return confidence, is_symbolic
        except Exception as e:
            self.logger.error(f"Error classifying query: {str(e)}")
            return 0.0, False