# intellitest_architect/config_manager.py
import yaml
from .logger import log

class ConfigManager:
    """
    Une classe singleton pour charger, valider et fournir l'accès
    à la configuration de l'application à partir de config.yaml.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path='config.yaml'):
        # L'initialisation ne se produit qu'une seule fois.
        if not hasattr(self, 'initialized'):
            self.config_path = config_path
            self.config = None
            self.load_config()
            self.initialized = True

    def load_config(self):
        """Charge le fichier de configuration YAML."""
        log.info(f"Chargement de la configuration depuis : {self.config_path}")
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            log.info("Configuration chargée avec succès.")
            self._validate_config()
        except FileNotFoundError:
            log.error(f"Erreur: Le fichier de configuration '{self.config_path}' n'a pas été trouvé.")
            raise
        except yaml.YAMLError as e:
            log.error(f"Erreur lors du parsing du fichier YAML: {e}")
            raise

    def _validate_config(self):
        """Valide la présence des clés de configuration essentielles."""
        required_keys = ['project_path', 'llm_provider', 'documents_to_generate']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Clé de configuration manquante '{key}' dans {self.config_path}")
        
        provider = self.config['llm_provider']
        if provider not in ['ollama', 'hugging_face', 'api']:
             raise ValueError(f"Fournisseur LLM invalide: {provider}")
        if provider not in self.config:
            raise ValueError(f"La section de configuration pour le fournisseur '{provider}' est manquante.")
            
        log.info("La configuration a été validée.")

    def get(self, key, default=None):
        """Récupère une valeur de la configuration."""
        return self.config.get(key, default)

# Instance globale pour un accès facile
config_manager = ConfigManager()
