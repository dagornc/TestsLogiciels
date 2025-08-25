# intellitest_architect/logger.py
import logging
import sys

def setup_logger():
    """
    Configure et retourne un logger qui écrit à la fois dans un fichier et sur la console.
    """
    # Créer un logger
    logger = logging.getLogger('IntelliTestArchitect')
    logger.setLevel(logging.INFO)

    # Éviter d'ajouter plusieurs handlers si la fonction est appelée plusieurs fois
    if logger.hasHandlers():
        return logger

    # Formatter pour les logs
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler pour écrire dans le fichier de log (intellitest.log)
    file_handler = logging.FileHandler('intellitest.log', mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler pour écrire sur la console (stdout)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

# Instanciation globale du logger pour être importé dans d'autres modules
log = setup_logger()
