# IntelliTest-Architect 🤖

**IntelliTest-Architect** est un système backend intelligent qui automatise la génération d'artefacts de test logiciel en utilisant la puissance des grands modèles de langage (LLM). Il analyse votre code source et produit des plans de test, des scénarios d'intégration et des tests unitaires, vous faisant gagner un temps précieux et améliorant la qualité de vos projets.

---

### ✨ Description pour les Débutants

Imaginez que vous ayez un assistant expert en tests qui peut lire votre code et écrire tous les documents de test ennuyeux pour vous. C'est exactement ce que fait **IntelliTest-Architect** ! Vous lui donnez le chemin de votre projet, vous choisissez le "cerveau" (un modèle IA comme Gemma ou Llama) qu'il doit utiliser, et il génère automatiquement des documents clairs qui vous expliquent comment tester votre application. C'est un gain de temps énorme et un excellent moyen d'apprendre les bonnes pratiques de test !

---

### 🚀 Description Technique pour les Experts

**IntelliTest-Architect** est un outil d'ingénierie logicielle assistée par IA, conçu pour s'intégrer dans des flux de travail de développement modernes. Il est écrit en Python 3.12 et entièrement conteneurisé avec Docker pour une portabilité et une reproductibilité maximales.

**Architecture :**
Le système est construit sur une architecture modulaire et découplée, facilitant son extension et sa maintenance.
* **`ConfigManager` (`config_manager.py`) :** Un singleton responsable du chargement, de la validation et de la fourniture de la configuration à partir du fichier `config.yaml`. Il assure que l'ensemble de l'application partage une configuration unique et cohérente.
* **`LLMHandler` (`llm_handler.py`) :** Le cœur de l'interaction avec l'IA. Cette classe abstraite la complexité de la communication avec différents fournisseurs de LLM. En utilisant un design pattern "Strategy", elle peut basculer de manière transparente entre :
    * **Ollama :** Pour les modèles auto-hébergés, via des requêtes HTTP simples.
    * **Hugging Face :** Pour l'exécution locale de modèles open-source (comme Gemma, Mistral) via la bibliothèque `transformers` de Hugging Face et `torch`. Elle gère le chargement du modèle et du tokenizer.
    * **API Externe :** Pour les services compatibles avec l'API OpenAI (OpenRouter, Perplexity, etc.), en utilisant des requêtes HTTP authentifiées.
* **`TestGenerator` (`test_generator.py`) :** Contient la logique métier principale. Il orchestre le processus :
    1.  Lecture de la structure du projet cible.
    2.  Itération sur les documents à générer définis dans la configuration.
    3.  Construction de prompts spécifiques pour chaque tâche.
    4.  Invocation du `LLMHandler` pour obtenir les générations.
    5.  Sauvegarde des artefacts produits dans le répertoire de sortie.
* **`FileHandler` (`file_handler.py`) :** Fournit des utilitaires robustes pour toutes les opérations sur les fichiers (lecture, écriture, création de sauvegardes ZIP), en utilisant `pathlib` pour une gestion moderne des chemins.
* **`main.py` :** Le point d'entrée qui initialise les services (logger, config) et lance le `TestGenerator`.

**Flux d'Exécution :**
1.  Au lancement, `main.py` initialise le logger et charge la configuration.
2.  Le `TestGenerator` est instancié avec la configuration chargée.
3.  Il analyse le `project_path` pour rassembler le contexte du code source.
4.  Pour chaque document activé dans `documents_to_generate`, il formate un prompt détaillé incluant le contexte du code et la tâche demandée.
5.  Le prompt est envoyé au `LLMHandler` qui, en fonction du `llm_provider` configuré, interagit avec le LLM approprié.
6.  La réponse du LLM est reçue, nettoyée et sauvegardée dans un fichier Markdown dans le répertoire de sortie.
7.  Des logs détaillés sont émis à chaque étape pour un monitoring complet.

### 🛠️ Installation et Utilisation

**Prérequis :**
* Docker
* (Optionnel) Ollama si vous souhaitez utiliser un modèle local.

**Lancement :**
1.  **Configurez :** Modifiez le fichier `config.yaml` pour pointer vers votre projet (`project_path`) et choisir votre fournisseur de LLM.
2.  **Exécutez le script :** Lancez le script `run.sh` :
    ```bash
    bash run.sh
    ```
    Ce script va automatiquement :
    * Construire l'image Docker `intellitest-architect`.
    * Lancer un conteneur en montant votre répertoire `/root/projets` pour que l'application puisse y accéder.
3.  **Vérifiez les résultats :** Les documents de test générés apparaîtront dans le sous-répertoire `tests_generes` de votre projet. Les logs seront disponibles dans `intellitest.log`.
