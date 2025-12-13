import discord
from discord.ext import commands
from discord import ui
import urllib.parse
from config import *

intents = discord.Intents.default()
intents.members = True
class AuthButton(ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None) 
        self.bot = bot

    @ui.button(label="🔑 S'authentifier via 42", style=discord.ButtonStyle.primary, custom_id="persistent_auth_button")
    async def auth_callback(self, interaction: discord.Interaction, button: ui.Button):
        user_id = str(interaction.user.id) 

        params = {
            'client_id': CLIENT_ID_42,
            'redirect_uri': REDIRECT_URI,
            'response_type': 'code',
            'scope': 'public', 
            'state': user_id
        }
        
        auth_url = 'https://api.intra.42.fr/oauth/authorize?' + urllib.parse.urlencode(params)

        ephemeral_message_content = (
            f"Bonjour {interaction.user.name},\n\n"
            f"**⚠️ ATTENTION :** Ne partagez ce lien avec personne.\n\n"
            f"Cliquez sur le lien ci-dessous pour vous connecter avec votre compte 42 :\n\n"
            f"**{auth_url}**\n\n"
            "Une fois connecté, votre pseudonyme sur le serveur sera mis à jour."
        )
        
        try:
            await interaction.response.send_message(
                ephemeral_message_content, 
                ephemeral=True
            )
            
        except discord.Forbidden:
            await interaction.response.send_message("Je ne peux pas vous envoyer de message privé. Veuillez autoriser les DMs sur ce serveur.", ephemeral=True)


intents = discord.Intents.all()
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    
    activity = discord.Game(name="Rocket League",)
    await bot.change_presence(status=discord.Status.online, activity=activity)

    channel = bot.get_channel(AUTH_CHANNEL_ID)
    if channel:
        try:
            auth_message_content_key = "Cliquez sur le bouton ci-dessous."
            
            history = [msg async for msg in channel.history(limit=5)] 
            
            if not any(auth_message_content_key in m.content for m in history if m.author == bot.user):
                await channel.send(
                    auth_message_content_key + " Vous recevrez un lien pour vous connecter grace à l'Intra de 42.", 
                    view=AuthButton(bot)
                )
            else:
                 print("Message d'authentification déjà trouvé, saut de l'envoi.")

        except Exception as e:
            print(f"ERREUR: Impossible d'envoyer le message d'authentification : {e}")

    else:
        print(f"ERREUR: Canal d'authentification avec l'ID {AUTH_CHANNEL_ID} non trouvé.")
    
    print(f'{bot.user} est connecté à Discord ! Statut: En ligne.')

# --- Lancement du Bot ---
if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)