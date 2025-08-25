# Étape 1: Utiliser une image de base Python 3.12 slim
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
# --no-cache-dir pour réduire la taille de l'image
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY ./intellitest_architect /app/intellitest_architect

# Copier le fichier de configuration par défaut
COPY config.yaml .

# Spécifier la commande à exécuter lorsque le conteneur démarre
# Le volume /root/projets de l'hôte devra être monté sur /root/projets dans le conteneur
# pour que l'application puisse accéder au code à analyser.
CMD ["python3", "-u", "-m", "intellitest_architect.main"]
