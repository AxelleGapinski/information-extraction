import openai
from dotenv import load_dotenv
import json
from runner import Step

load_dotenv()

class Extract(Step):
    
    """
    Step to extract informations from the diagnostic files 
    """

    def __init__(self, **kwargs):
        super().__init__(input_keys=["documents"], **kwargs)

        self.system_prompt = """
        
        Tu es un expert en diagnostics immobiliers. Extrait les informations suivantes de manière concise:
        - Type de diagnostic
        - Détails du bien (type, adresse exacte, superficie, date de construction, propriétaire)
        - Points critiques et évaluation globale
        - Si tu ne trouves pas une information, note 'N/C'
        
        """
        self.user_prompt = """
        
        Type du diagnostic: {diagnostic_type}
        Texte du diagnostic: {diagnostic_text}
        Réponse en JSON :
        {{
            "type": "{diagnostic_type}",
            "infos_bien": {{
                "type_bien": "type de bien",
                "adresse": "adresse",
                "localisation": "Etage",
                "superficie": "Superficie en m²",
                "date_construction": "date de construction",
                "propriétaire": "Propriétaire"
            }},
            "points_critiques": [
                {{
                    "catégorie": "Catégorie",
                    "description": "Description détaillée",
                    "niveau_risque": "faible/moyen/élevé"
                }}
            ],
            "évaluation": "Évaluation globale"
        }}
        """

    def run(self, input_data, **runtime_args):
        
        """ 
        This function goes through the documents, it detects the type of diagnostic, 
        extracts infos and gives a structured output
        """
        
        self.validate_input(input_data)
        structured_documents, infos_bien = [], None

        for document in input_data["documents"]:
            text = document.get("text", "")
            if not text:
                continue
            
            # gets the diagnostic type
            diagnostic_type = self.get_diagnostic_type(text)
            
            # calls the openai API to extract data
            extracted_data = self.call_openai(text, diagnostic_type)

            if extracted_data and infos_bien is None:
                infos_bien = extracted_data.get("infos_bien")
            
            # adds the extracted info in structured_documents
            if extracted_data:
                structured_documents.append({
                    **extracted_data,
                    "infos_bien": infos_bien or extracted_data.get("infos_bien")
                })

        return {"structured_documents": structured_documents}

    def call_openai(self, text, diagnostic_type):
        """ 
        Calls the openai API for extraction 
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_prompt.format(
                        diagnostic_type=diagnostic_type,
                        diagnostic_text=text
                    )}
                ],
                max_tokens=2000,
                temperature=0.3 
            )
            return self.process_json(response.choices[0].message.content)
        except Exception as e:
            print(f"Error extracting : {e}")
            return {}

    def process_json(self, response_text):
        """ Cleans and process the JSON """
        try:
            json_data = response_text.strip().removeprefix("```json").removesuffix("```")
            return json.loads(json_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file {e}")
            return {}

    def get_diagnostic_type(self, text):
        """ Get the diagnostic type among a predefined list """
        types = ["Amiante", "Électricité", "Plomb", "DPE", "Gaz", "Termites", "Pollution", "Nuisances"]
        return next((t for t in types if t.lower() in text.lower()), "Autre")
