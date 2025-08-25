# intellitest_architect/file_handler.py
import os
import shutil
from pathlib import Path
from .logger import log

class FileHandler:
    """Gère toutes les opérations liées aux fichiers et aux répertoires."""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        if not self.project_path.is_dir():
            log.error(f"Le chemin du projet '{project_path}' n'existe pas ou n'est pas un répertoire.")
            raise FileNotFoundError(f"Le chemin du projet '{project_path}' est invalide.")

    def get_project_context(self) -> str:
        """
        Lit la structure et le contenu des fichiers du projet pour fournir un contexte au LLM.
        Pour la simplicité, nous allons lister les fichiers et lire le contenu des fichiers Python.
        """
        log.info(f"Analyse du contexte du projet : {self.project_path}")
        context = f"Structure du projet à l'adresse '{self.project_path}':\n\n"
        file_contents = ""

        for path in sorted(self.project_path.rglob('*')):
            if path.is_dir():
                continue
            
            relative_path = path.relative_to(self.project_path)
            context += f"- {relative_path}\n"

            # Lire le contenu des fichiers pertinents (ex: .py, .js, .txt)
            if path.suffix in ['.py', '.js', '.txt', '.md', 'Dockerfile']:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        file_contents += f"\n--- Contenu de {relative_path} ---\n"
                        file_contents += content
                        file_contents += "\n--- Fin du contenu ---\n"
                except Exception as e:
                    log.warning(f"Impossible de lire le fichier {path}: {e}")
        
        return context + file_contents

    def save_generated_document(self, doc_name: str, content: str):
        """
        Sauvegarde un document généré dans le sous-répertoire 'tests_generes'.
        """
        output_dir = self.project_path / "tests_generes"
        output_dir.mkdir(exist_ok=True)
        
        # Nettoyer le nom du fichier
        filename = doc_name.replace(" ", "_").lower() + ".md"
        output_path = output_dir / filename
        
        log.info(f"Sauvegarde du document généré : {output_path}")
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            log.info(f"Document '{doc_name}' sauvegardé avec succès.")
        except IOError as e:
            log.error(f"Impossible d'écrire le fichier {output_path}: {e}")

    def backup_project(self):
        """Crée une archive ZIP du répertoire du projet."""
        backup_dir = self.project_path.parent
        backup_name = backup_dir / f"{self.project_path.name}_backup_{os.urandom(4).hex()}"
        
        log.info(f"Création de la sauvegarde du projet à l'adresse : {backup_name}.zip")
        try:
            shutil.make_archive(str(backup_name), 'zip', str(self.project_path))
            log.info("Sauvegarde terminée avec succès.")
        except Exception as e:
            log.error(f"La création de la sauvegarde a échoué : {e}")
            raise
