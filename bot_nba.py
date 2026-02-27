import os
import requests
from datetime import datetime
from nba_api.stats.endpoints import scoreboardv3
from openai import OpenAI

# Configuración Blueeyestats-lab
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
URL_WEB = "https://blueeyestats.com"

def analizar_con_ia(datos_partidos):
    prompt = f"Analista de Blueeyestats-lab: Procesa estos partidos de la NBA, da probabilidades matemáticas y correcciones por lesiones: {datos_partidos}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Experto en NBA."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    try:
        sb = scoreboardv3.ScoreboardV3().get_dict()
        games = sb['scoreBoard']['games']
        if not games:
            return
        
        resumen = "\n".join([f"- {g['awayTeam']['teamName']} vs {g['homeTeam']['teamName']}" for g in games])
        reporte = analizar_con_ia(resumen)

        # Telegram
        token = os.getenv('TELEGRAM_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      data={'chat_id': chat_id, 'text': f"🏀 *BLUEEYESTATS-LAB*\n\n{reporte}\n\n🌐 {URL_WEB}", 'parse_mode': 'Markdown'})

        # Web
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(f"<html><body style='background:#121212;color:white;padding:30px;'><h1>BLUEEYESTATS-LAB</h1><p>{reporte.replace('\n', '<br>')}</p></body></html>")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
