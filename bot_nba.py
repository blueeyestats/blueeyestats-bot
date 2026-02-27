import os
import requests
from datetime import datetime
from nba_api.stats.endpoints import scoreboardv3, leaguestandings
from openai import OpenAI

# Configuración del Laboratorio
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
URL_WEB = "https://blueeyestats.com"

def obtener_analisis_ia(resumen_partidos):
    prompt = f"""
    Eres el analista jefe de Blueeyestats-lab. Procesa estos partidos de la NBA:
    {resumen_partidos}
    
    Genera un reporte detallado con:
    1. Probabilidades matemáticas basadas en estadísticas.
    2. Correcciones del bot (lesiones, rachas, cansancio).
    3. Predicción final con porcentaje de confianza.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Analista senior de NBA."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def ejecutar_bot():
    try:
        # Obtener partidos de hoy
        sb = scoreboardv3.ScoreboardV3().get_dict()
        games = sb['scoreBoard']['games']
        
        if not games:
            print("No hay partidos hoy.")
            return

        texto_partidos = ""
        for g in games:
            texto_partidos += f"- {g['awayTeam']['teamName']} vs {g['homeTeam']['teamName']}\n"

        # Análisis con la API de OpenAI
        reporte_ia = obtener_analisis_ia(texto_partidos)

        # Enviar a Telegram
        token = os.getenv('TELEGRAM_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        mensaje_telegram = f"🏀 *BLUEEYESTATS-LAB: REPORTE DIARIO*\n\n{reporte_ia}\n\n🌐 Dashboard: {URL_WEB}"
        
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      data={'chat_id': chat_id, 'text': mensaje_telegram, 'parse_mode': 'Markdown'})

        # Actualizar la Web (index.html)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(f"<html><body style='background:#1a1a1a;color:white;font-family:sans-serif;padding:40px;'>")
            f.write(f"<h1 style='color:silver;'>BLUEEYESTATS-LAB</h1>")
            f.write(f"<div style='border:1px solid #444;padding:20px;'>{reporte_ia.replace('\n', '<br>')}</div>")
            f.write(f"</body></html>")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar_bot()
