import os
from typing import Dict, Any
from runner import Step

class ReadDossier(Step):
    def __init__(self, **kwargs):
        super().__init__(input_keys=["path"], **kwargs)
    
    def run(self, input_data: Dict[str, Any] = None, **runtime_args) -> Dict[str, Any]:
        """ 
        Main function that reads the files from a specific folder 
        """
        folder_path = runtime_args.get('folder_path') or input_data.get('path')
        
        if not folder_path:
            raise ValueError("Aucun dossier")
        if not os.path.exists(folder_path):
            raise ValueError(f"Le dossier {folder_path} n'existe pas.")
        
        splitted_path = os.path.join(folder_path, 'Splitted')
        
        #initialize a list to store the read documents
        documents = []

        # checks every txt file in the folder and store its content in documents
        for filename in os.listdir(splitted_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(splitted_path, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
                    documents.append({
                        "filename": filename,
                        "text": text
                    })
        return {
            "documents": documents,
            "path": folder_path 
        }