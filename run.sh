#!/bin/bash

# ==============================================================================
# Script d'exécution pour IntelliTest-Architect
# Ce script construit l'image Docker et lance le conteneur.
# ==============================================================================

# Variables
IMAGE_NAME="intellitest-architect"
CONTAINER_NAME="intellitest-architect-runner"
PROJECTS_DIR="/root/projets"

# Mettre fin au script en cas d'erreur
set -e

# Se placer dans le répertoire du script pour s'assurer que le contexte Docker est correct
cd "$(dirname "$0")"

echo "### Étape 1/3: Construction de l'image Docker '$IMAGE_NAME'..."
docker build -t $IMAGE_NAME .

echo "### Étape 2/3: Vérification du répertoire des projets..."
if [ ! -d "$PROJECTS_DIR" ]; then
    echo "AVERTISSEMENT: Le répertoire '$PROJECTS_DIR' n'existe pas sur l'hôte."
    echo "Création du répertoire..."
    mkdir -p "$PROJECTS_DIR"
    echo "Veuillez placer les projets que vous souhaitez analyser dans '$PROJECTS_DIR'."
    # Création d'un projet d'exemple pour démonstration
    echo "Création d'un projet d'exemple dans '$PROJECTS_DIR/sample_project'..."
    mkdir -p "$PROJECTS_DIR/sample_project"
    cat <<'EOT' > "$PROJECTS_DIR/sample_project/calculator.py"
# Un simple calculateur pour la démonstration
class Calculator:
    def add(self, a, b):
        return a + b
    def subtract(self, a, b):
        return a - b
EOT
fi

echo "### Étape 3/3: Lancement du conteneur Docker..."
docker run --name $CONTAINER_NAME -v "$PROJECTS_DIR:/root/projets" $IMAGE_NAME

echo "### Exécution terminée."
echo "Les résultats se trouvent dans le sous-répertoire 'tests_generes' de votre projet."
echo "Pour voir les logs, exécutez: docker logs $CONTAINER_NAME"
