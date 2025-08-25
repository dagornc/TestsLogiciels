# intellitest_architect/main.py
from .logger import log
from .test_generator import TestGenerator
import sys

def main():
    """
    Point d'entrée principal de l'application IntelliTest-Architect.
    """
    try:
        # Le logger et la config sont déjà initialisés lors de leur importation.
        # Il suffit de créer et de lancer le générateur.
        generator = TestGenerator()
        generator.run()
    except Exception as e:
        # Capturer les erreurs critiques qui pourraient survenir lors de l'initialisation.
        log.error(f"Une erreur critique est survenue: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
