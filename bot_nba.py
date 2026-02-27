import os
import requests
from nba_api.live.endpoints import scoreboard # <--- Cambio clave aquí
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def main():
    try:
        # Nueva forma de obtener los partidos
        games = scoreboard.ScoreBoard().get_dict()['scoreboard']['games']
        
        if not games:
            print("No hay partidos hoy.")
            return

        resumen = "\n".join([f"- {g['awayTeam']['teamName']} vs {g['homeTeam']['teamName']}" for g in games])
        
        # IA Analysis
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Analista de Blueeyestats-lab."},
                      {"role": "user", "content": f"Analiza estos partidos de NBA: {resumen}"}]
        )
        reporte = response.choices[0].message.content

        # Telegram
        token = os.getenv('TELEGRAM_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      data={'chat_id': chat_id, 'text': f"🏀 *BLUEEYESTATS-LAB*\n\n{reporte}", 'parse_mode': 'Markdown'})

        # Crear Web
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(f"<html><body style='background:#121212;color:white;padding:30px;'><h1>Blueeyestats-lab Activo</h1><p>{reporte.replace('\n', '<br>')}</p></body></html>")

    except Exception as e:
        print(f"Error detallado: {e}")

if __name__ == "__main__":
    main()
