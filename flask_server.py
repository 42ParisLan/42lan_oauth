from flask import Flask, request, redirect, jsonify
import requests
import urllib.parse
from config import *
app = Flask(__name__)

API_42_URL = 'https://api.intra.42.fr'

@app.route('/authcallback', methods=['GET'])
def auth_callback():
    code = request.args.get('code')
    user_id = request.args.get('state')
    

    if not code or not user_id:
        return "Erreur: Paramètres 'code' ou 'state' manquants.", 400

    print(f"Authentification reçue pour l'utilisateur Discord ID: {user_id}")

    token_url = f'{API_42_URL}/oauth/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID_42,
        'client_secret': CLIENT_SECRET_42,
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    
    try:
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        access_token_42 = token_response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'échange de jeton 42 : {e}")
        return "Erreur d'authentification 42. Veuillez réessayer.", 500

    me_url = f'{API_42_URL}/v2/me'
    headers_42 = {'Authorization': f'Bearer {access_token_42}'}

    try:
        me_response = requests.get(me_url, headers=headers_42)
        me_response.raise_for_status()
        # print(me_response.json()) 
        login_42 = me_response.json().get('login')
        ususal_first_name = me_response.json().get('usual_first_name')
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des infos /v2/me : {e}")
        return "Erreur lors de la récupération de votre login 42.", 500

    print(f"Login 42 récupéré: {login_42}")

    
    discord_api_url = f'https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}'
    headers_discord = {
        'Authorization': f'Bot {DISCORD_TOKEN}',
        'Content-Type': 'application/json'
    }
    nickname = ususal_first_name + ' (' + login_42 + ')'
    payload = {'nick': nickname}

    try:
        discord_response = requests.patch(discord_api_url, headers=headers_discord, json=payload)
        discord_response.raise_for_status()
        print(f"Pseudonyme de l'utilisateur {user_id} changé pour {nickname} !")

        # add le role
        role_url = f'{discord_api_url}/roles/{VERIFIED_ROLE_ID}'
        role_response = requests.put(role_url, headers=headers_discord)
        role_response.raise_for_status()
        print(f"Rôle {VERIFIED_ROLE_ID} ajouté à l'utilisateur {user_id} !")
        
        return f"Connexion 42 réussie ! Votre pseudonyme Discord a été mis à jour à **{nickname}**."
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            error_message = "Erreur de permission Discord. Le bot n'a pas la permission de modifier les pseudonymes (ou ne peut pas modifier un administrateur)."
        else:
            error_message = f"Erreur lors de la modification du pseudonyme Discord: {e}"
        print(error_message)
        return f"Erreur critique: {error_message}. Contactez un admin.", 500
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API Discord : {e}")
        return "Erreur de connexion à l'API Discord.", 500

# Flask
if __name__ == '__main__':
    app.run(debug=True, port=8484)