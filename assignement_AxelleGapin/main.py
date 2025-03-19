from runner import Runner
from steps.read_files import ReadDossier
from steps.extract_info import Extract
from steps.synthese_export import Synthesis, ExportDonnees

if __name__ == "__main__":
    
    # define the folder to process
    dossier_a_traiter = "data/Dossier3"

    runner = Runner()

    # defines a global parameter for the folder path
    runner.set_global_param("folder_path", dossier_a_traiter)

    # configuration of the pipeline step order
    runner.add(ReadDossier(description="Read the files"))
    runner.add(Extract(description="Extract informations from the documents"))
    runner.add(Synthesis(description="Generate a global synthesis"))
    runner.add(ExportDonnees(description="Export the data"))

    # run the pipeline
    result = runner.run(
        initial_input={
            "path": dossier_a_traiter
        },
    )
    
    print(result)