**🔑 42LAN OAuth**
Système d'authentification automatisé pour serveurs Discord utilisant l'API Intra de 42.

**🌟 Fonctionnalités**
Vérification 42 : Authentification sécurisée via OAuth2.

Mise à jour automatique : Change le pseudonyme en Prénom (login) et attribue un rôle dédié.

Interface simple : Bouton d'authentification persistant dans le salon choisi.

**🛠️ Configuration Rapide**
Variables d'environnement : Créez un fichier .env basé sur .env.example avec vos accès Discord et 42.

Lancement via Docker :

docker-compose -f docker-compose.dev.yml up -d
Cette commande lance simultanément le bot et le serveur de callback.
**
📂 Structure**
discord_bot.py : Gestion du bot et des interactions.

flask_server.py : Serveur web pour le traitement de l'authentification.

**📜 Licence**
Distribué sous licence GNU GPL v3.
