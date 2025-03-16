import discord
from discord.ext import commands
import os
from dotenv import load_dotenv  # importar la libreria del .env, esto para mantener las KEYS privadas
import google.generativeai as genai  # importamos la API de Gemini

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Modelo cambiado aqui.

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name}")

# ----------------------Embeds del Bot (Meramente decorativo)--------------------------------


#Los embeds son sólo fragmentos de decoración, para que las respuestas queden ordenadas en un cuadro.

def create_embed(title, description, color_hex="#03fcd7"): #Acá #03fcd7 son el color Hex
    color_int = int(color_hex[1:], 16) #Con esto se construyen números hexadecimales a enteros porque solo se aceptan en formato int
    embed = discord.Embed(
        title=title,
        description=description,
        color=color_int
    )
    return embed


#----------------------BOT COMMANDS (para funcionalidad de respuestas)--------------------------------
@bot.command()
async def pregunta(ctx, *, pregunta):
    """Preguntas y respuestas en un embed"""
    try:
        response = model.generate_content(pregunta)
        if response and hasattr(response, "text"):
            embed = create_embed("Respuesta", response.text)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No se pudo obtener una respuesta válida de Gemini.")
            print(f"Respuesta inválida de Gemini: {response}")
    except Exception as e:
        await ctx.send(f"Ocurrió un error al procesar tu pregunta: {e}")
        print(f"Error de Gemini: {e}")



bot.run(DISCORD_TOKEN)


# Sección de pruebas de versiones de Gemini 
'''
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro') ## aca se cambio la version de la API de 'gemini-pro' a 'gemini-1.5-pro-latest'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name}")

@bot.command()
async def pregunta(ctx, *, pregunta):
    try:
        response = model.generate_content(pregunta)
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send(f"Ocurrió un error al procesar tu pregunta: {e}")
        print(f"Error de Gemini: {e}") #opcional, para ver el error en la consola.

bot.run(DISCORD_TOKEN)
'''