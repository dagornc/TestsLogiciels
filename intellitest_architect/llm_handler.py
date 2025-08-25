# intellitest_architect/llm_handler.py
import os
import requests
import json
from .logger import log
from .config_manager import config_manager

class LLMHandler:
    """
    Classe de base pour gérer les interactions avec les LLM.
    Utilise une approche de type 'Strategy' pour sélectionner le bon fournisseur.
    """
    def __init__(self):
        self.provider_name = config_manager.get('llm_provider')
        self.config = config_manager.get(self.provider_name)
        self.generation_config = config_manager.get('generation_config')
        
        if not self.config:
            raise ValueError(f"Configuration manquante pour le fournisseur LLM : {self.provider_name}")
            
        log.info(f"Initialisation du LLMHandler avec le fournisseur : {self.provider_name}")

    def generate(self, prompt: str) -> str:
        """Méthode de génération principale qui délègue au bon fournisseur."""
        if self.provider_name == 'ollama':
            return self._generate_with_ollama(prompt)
        elif self.provider_name == 'hugging_face':
            return self._generate_with_hugging_face(prompt)
        elif self.provider_name == 'api':
            return self._generate_with_api(prompt)
        else:
            log.error(f"Fournisseur LLM non supporté : {self.provider_name}")
            raise ValueError(f"Fournisseur LLM non supporté : {self.provider_name}")

    def _generate_with_ollama(self, prompt: str) -> str:
        """Génération via l'API locale d'Ollama."""
        url = f"{self.config['base_url']}/api/generate"
        payload = {
            "model": self.config['model_name'],
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.generation_config.get('temperature', 0.7)
            }
        }
        log.info(f"Envoi de la requête à Ollama (modèle: {self.config['model_name']})...")
        try:
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            # La réponse d'Ollama est une chaîne de JSON objets, nous prenons la dernière.
            full_response = json.loads(response.text)
            log.info("Réponse reçue d'Ollama.")
            return full_response.get('response', '')
        except requests.exceptions.RequestException as e:
            log.error(f"Erreur de communication avec l'API Ollama: {e}")
            return f"Erreur: Impossible de contacter Ollama à {url}."

    def _generate_with_hugging_face(self, prompt: str) -> str:
        """Génération via un modèle local Hugging Face."""
        # Pour éviter une dépendance lourde, nous vérifions l'import au moment de l'exécution
        try:
            import torch
            from transformers import pipeline
        except ImportError:
            log.error("Les bibliothèques 'torch' et 'transformers' sont nécessaires pour utiliser Hugging Face.")
            log.error("Veuillez les installer avec : pip install torch transformers accelerate")
            return "Erreur: Dépendances Hugging Face non installées."

        model_id = self.config['model_id']
        log.info(f"Chargement du pipeline Hugging Face pour le modèle : {model_id}")
        try:
            # Utiliser 'text-generation' qui est le pipeline standard
            pipe = pipeline(
                "text-generation",
                model=model_id,
                torch_dtype=torch.bfloat16,
                device_map="auto" # 'auto' pour utiliser le CPU si pas de GPU
            )
            
            log.info("Génération de texte avec le modèle Hugging Face...")
            outputs = pipe(
                prompt,
                max_new_tokens=self.generation_config.get('max_new_tokens', 1024),
                do_sample=True,
                temperature=self.generation_config.get('temperature', 0.7),
                top_p=0.95
            )
            log.info("Réponse reçue du modèle Hugging Face.")
            # La sortie est une liste de dictionnaires, nous extrayons le texte généré
            generated_text = outputs[0]['generated_text']
            # Retirer le prompt initial de la réponse
            if generated_text.startswith(prompt):
                 return generated_text[len(prompt):].strip()
            return generated_text.strip()
            
        except Exception as e:
            log.error(f"Erreur lors de la génération avec Hugging Face : {e}")
            return f"Erreur: Échec de la génération avec le modèle {model_id}."


    def _generate_with_api(self, prompt: str) -> str:
        """Génération via une API externe compatible OpenAI."""
        api_key = os.getenv('API_KEY', self.config.get('api_key'))
        if not api_key:
            log.error("Clé API non trouvée. Veuillez la définir dans config.yaml ou via la variable d'environnement API_KEY.")
            return "Erreur: Clé API manquante."
            
        url = f"{self.config['base_url']}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.config['model_name'],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.generation_config.get('temperature', 0.7),
            "max_tokens": self.generation_config.get('max_new_tokens', 1024)
        }
        log.info(f"Envoi de la requête à l'API externe (modèle: {self.config['model_name']})...")
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            log.info("Réponse reçue de l'API.")
            return data['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            log.error(f"Erreur de communication avec l'API externe: {e}")
            return f"Erreur: Impossible de contacter l'API à {url}."
        except (KeyError, IndexError) as e:
            log.error(f"Réponse inattendue de l'API: {response.text}")
            return f"Erreur: Le format de la réponse de l'API est invalide."
