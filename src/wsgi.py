import sys
# On s'assure que le dossier de l'application est dans le chemin Python
sys.path.insert(0, '/var/www/mon-app')

# On importe l'instance de l'application Flask
from app import app as application
