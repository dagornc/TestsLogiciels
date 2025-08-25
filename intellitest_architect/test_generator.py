# intellitest_architect/test_generator.py
from .logger import log
from .config_manager import config_manager
from .file_handler import FileHandler
from .llm_handler import LLMHandler

class TestGenerator:
    """
    Classe principale qui orchestre le processus de génération de tests.
    """
    def __init__(self):
        log.info("Initialisation du TestGenerator.")
        self.project_path = config_manager.get('project_path')
        self.documents_to_generate = config_manager.get('documents_to_generate', [])
        self.auto_correction_config = config_manager.get('auto_correction', {})

        self.file_handler = FileHandler(self.project_path)
        self.llm_handler = LLMHandler()

    def run(self):
        """
        Lance le processus complet de génération de tests.
        """
        log.info("="*50)
        log.info("Démarrage du processus de génération avec IntelliTest-Architect")
        log.info(f"Projet cible : {self.project_path}")
        log.info("="*50)

        # Gérer la sauvegarde si la correction auto est activée
        if self.auto_correction_config.get('enabled') and self.auto_correction_config.get('backup_before_correction'):
            self.file_handler.backup_project()
        
        # Obtenir le contexte du projet
        try:
            project_context = self.file_handler.get_project_context()
        except Exception as e:
            log.error(f"Impossible d'analyser le projet. Arrêt du processus. Erreur: {e}")
            return

        # Itérer sur les documents à générer
        for doc in self.documents_to_generate:
            if doc.get('enabled'):
                doc_name = doc.get('name', 'Document sans nom')
                log.info(f"--- Génération du document : {doc_name} ---")
                
                # Construire le prompt final
                final_prompt = f"Voici le contexte d'un projet logiciel :\n\n{project_context}\n\n"
                final_prompt += f"TACHE : {doc.get('prompt', '')}"
                
                # Appeler le LLM pour la génération
                generated_content = self.llm_handler.generate(final_prompt)
                
                # Sauvegarder le résultat
                if not generated_content.startswith("Erreur:"):
                    self.file_handler.save_generated_document(doc_name, generated_content)
                else:
                    log.error(f"La génération pour '{doc_name}' a échoué. Voir les logs précédents.")
            else:
                log.info(f"Le document '{doc.get('name')}' est désactivé, il est ignoré.")
        
        log.info("="*50)
        log.info("Processus de génération terminé.")
        log.info("="*50)
