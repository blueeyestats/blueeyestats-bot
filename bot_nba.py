import os
import requests
from datetime import datetime
from nba_api.stats.endpoints import scoreboardv3
from openai import OpenAI

# Configuración Blueeyestats-lab
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
URL_WEB = "https://blueeyestats.com"

def analizar_con_ia(datos_partidos):
    prompt = f"""
    Eres el analista jefe de Blueeyestats-lab. Analiza estos partidos:
    {datos_partidos}
    Calcula probabilidades matemáticas reales, menciona correcciones por bajas/lesiones 
    y da una predicción final con porcentaje de confianza.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Analista experto en NBA."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    try:
        # Obtener datos de la NBA
        sb = scoreboardv3.ScoreboardV3().get_dict()
        games = sb['scoreBoard']['games']
        
        if not games:
            print("No hay partidos hoy.")
            return

        resumen = ""
        for g in games:
            resumen += f"- {g['awayTeam']['teamName']} vs {g['homeTeam']['teamName']}\n"

        # Generar reporte detallado con IA
        reporte = analizar_con_ia(resumen)

        # Enviar a Telegram
        token = os.getenv('TELEGRAM_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        mensaje = f"🏀 *BLUEEYESTATS-LAB: ANÁLISIS*\n\n{reporte}\n\n🌐 {URL_WEB}"
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      data={'chat_id': chat_id, 'text': mensaje, 'parse_mode': 'Markdown'})

        # Crear archivo para la Web
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(f"<html><body style='background:#121212;color:white;font-family:sans-serif;padding:30px;'>")
            f.write(f"<h1>BLUEEYESTATS-LAB</h1><hr><p>{reporte.replace('\n', '<br>')}</p></body></html>")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    main()
