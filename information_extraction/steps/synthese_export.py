import os
from typing import Dict, Any
from runner import Step
from collections import defaultdict
import csv

class Synthesis(Step):
    """
    Class to generate a synthesis from the structured documents generated before.
    """
    
    def __init__(self, **kwargs):
        super().__init__(input_keys=["structured_documents"], **kwargs)

    def run(self, input_data: Dict[str, Any], **runtime_args) -> Dict[str, Any]:
        self.validate_input(input_data)
        
        # retrieve the structured documents with the extracted infos
        documents = input_data.get("structured_documents", [])
        
        if not documents:
            return {"synthese_globale": "Pas de donnée disponible"}
        
        # retrieves information from the first document in the list
        infos_bien = documents[0].get("infos_bien", {})
        
        # puts together the critical points from all diagnostics
        points_critiques = []
        for doc in documents:
            points_critiques.extend(doc.get("points_critiques", []))
        
        # determine global risk based the critical points
        risque_global = self.evaluate_risk(points_critiques)
        
        #generate the synthesis
        synthese = f"""[ Synthèse générale du bien ]

Informations sur le bien
- Type de bien : {infos_bien.get('type_bien', 'Non spécifié')}
- Adresse : {infos_bien.get('adresse', 'Non spécifié')}
- Localisation : {infos_bien.get('localisation', 'Non spécifié')}
- Superficie : {infos_bien.get('superficie', 'Non spécifié')}
- Date de construction: {infos_bien.get('date_construction', 'Non spécifié')}
- Propriétaire: {infos_bien.get('propriétaire', 'Non spécifié')}

Points critiques principaux
{self.format_critic_points(points_critiques)}

Évaluation des risques
Risque global: {risque_global}

Recommandations
{self.get_recommandations(points_critiques)}
"""
        
        return {
            "synthese_globale": synthese,
            "infos_bien": infos_bien
        }
    
    def evaluate_risk(self, points_critiques):
        """
        Evaluates the global risk for a building based on the critical points found.
        """
        risques = defaultdict(int)
        for point in points_critiques:
            risque = point.get("niveau_risque", "Non spécifié")
            risques[risque] += 1

        if risques["élevé"] > 0:
            return "élevé"
        elif risques["moyen"] > 0:
            return "moyen"
        elif risques["faible"] > 0:
            return "faible"
        else:
            return "Non spécifié"
    
    def format_critic_points(self, points_critiques):
        """
        Formats te critical points to put them in the synthesis
        """
        if not points_critiques:
            return "Pas de point critique"
        
        formatted = []
        for point in points_critiques:
            formatted.append(f"- {point.get('catégorie')} (risque: {point.get('niveau_risque', 'N/C')}) : {point.get('description', 'Pas de description')}")
        
        return "\n".join(formatted)
    
    def get_recommandations(self, points_critiques):
        """
        Writes recommendations for high and medium critical points
        """
        recommandations = []
        
        for point in points_critiques:
            risque = point.get("niveau_risque", "Faible")
            if risque in ["moyen", "élevé"]:
                recommandations.append(f"- Faire une expertise pour: {point.get('catégorie')}")
        
        return "\n".join(recommandations) if recommandations else "Pas de recommandation"



class ExportDonnees(Step):
    """
    Class to expot the results of the synthesis and the infos on the building
    into txt and CSV files.
    """
    def __init__(self, **kwargs):
        """
        Initalizes the class with the input keys
        """
        super().__init__(input_keys=["synthese_globale", "infos_bien"], **kwargs)

    def run(self, input_data: Dict[str, Any], **runtime_args) -> Dict[str, Any]:
        """
        Exports the synthesis in a text file and the building informations
        in a CSV file.
        """
        self.validate_input(input_data)

        dossier_source = runtime_args.get("folder_path")
        dossier_name = os.path.basename(dossier_source)
        
        # create an ouptut in 'outputs'
        output_dir = os.path.join("outputs", dossier_name)
        os.makedirs(output_dir, exist_ok=True)
        
        # export the synthesis in .txt
        synthese_path = os.path.join(output_dir, "synthese_globale.txt")
        with open(synthese_path, "w", encoding="utf-8") as f:
            f.write(input_data["synthese_globale"])
        
        # export the building informations in CSV
        infos_bien = input_data["infos_bien"]
        infos_path = os.path.join(output_dir, "infos_bien.csv")
        
        with open(infos_path, mode='w', newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["type_bien", "adresse", "localisation", "superficie", "date_construction", "propriétaire"])
            writer.writeheader()
            writer.writerow(infos_bien)
        
        return {
            "synthese_path": synthese_path,
            "infos_path": infos_path
        }