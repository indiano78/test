# Utiliser l'image officielle Ubuntu pour la stabilité
FROM ubuntu:24.04

# Éviter les invites interactives lors de l'installation
ENV DEBIAN_FRONTEND=noninteractive

# 1. CORRECTION : Ajout de python3-flask + Correction du chemin /var/lib/apt/lists/
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3 \
    python3-pip \
    python3-flask \
    && rm -rf /var/lib/apt/lists/*

# Activer le module WSGI dans Apache
RUN a2enmod wsgi

# Définir le dossier de travail
WORKDIR /var/www/mon-app

# 2. CONFIGURATION : Copie des fichiers Flask et WSGI
# (Assurez-vous d'avoir renommé vos scripts en app.py et wsgi.py comme dans l'étape Flask)
COPY src/app.py /var/www/mon-app/app.py
COPY src/wsgi.py /var/www/mon-app/wsgi.py

# 3. AJOUT : Création du dossier d'upload et attribution des droits à Apache (www-data)
RUN mkdir -p /var/www/mon-app/uploads && \
    chown -R www-data:www-data /var/www/mon-app && \
    chmod -R 755 /var/www/mon-app

# 4. CORRECTION : Configuration Apache mise à jour pour pointer vers wsgi.py
RUN echo '<VirtualHost *:80>\n\
    WSGIScriptAlias / /var/www/mon-app/wsgi.py\n\
    <Directory /var/www/mon-app>\n\
        Require all granted\n\
    </Directory>\n\
    ErrorLog /dev/stderr\n\
    CustomLog /dev/stdout combined\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Exposer le port HTTP d'Apache
EXPOSE 80

# Lancer Apache au premier plan pour que le conteneur reste actif
CMD ["apachectl", "-D", "FOREGROUND"]

