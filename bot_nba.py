import os
import requests
from nba_api.live.endpoints import scoreboard # <--- Esta es la solución al error
from openai import OpenAI

# Configuración profesional Blueeyestats-lab
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def main():
    try:
        # Obtenemos los partidos del nuevo endpoint 'live'
        board = scoreboard.ScoreBoard()
        games = board.get_dict()['scoreboard']['games']
        
        if not games:
            print("No hay partidos programados.")
            return

        lista_partidos = "\n".join([f"- {g['awayTeam']['teamName']} vs {g['homeTeam']['teamName']}" for g in games])
        
        # Le pedimos a la IA que haga su magia
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Eres el analista jefe de Blueeyestats-lab. Genera probabilidades y correcciones por bajas."},
                      {"role": "user", "content": f"Analiza estos partidos de NBA: {lista_partidos}"}]
        )
        reporte = response.choices[0].message.content

        # Enviamos a Telegram
        token = os.getenv('TELEGRAM_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      data={'chat_id': chat_id, 'text': f"🏀 *REPORTE BLUEEYESTATS-LAB*\n\n{reporte}", 'parse_mode': 'Markdown'})

        # Actualizamos la Web
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(f"<html><body style='background:#121212;color:white;font-family:sans-serif;padding:30px;'>")
            f.write(f"<h1>BLUEEYESTATS-LAB ACTIVO</h1><hr><p>{reporte.replace('\n', '<br>')}</p></body></html>")

    except Exception as e:
        print(f"Error detectado: {e}")

if __name__ == "__main__":
    main()
