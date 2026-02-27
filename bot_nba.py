import os
import requests
from nba_api.live.endpoints import scoreboard
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def main():
    try:
        board = scoreboard.ScoreBoard()
        games = board.get_dict()['scoreboard']['games']
        
        if not games:
            print("No hay partidos programados.")
            return

        lista_partidos = "\n".join([f"- {g['awayTeam']['teamName']} vs {g['homeTeam']['teamName']}" for g in games])
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Analista jefe de Blueeyestats-lab."},
                      {"role": "user", "content": "Analiza estos partidos: " + lista_partidos}]
        )
        reporte = response.choices[0].message.content

        # Telegram
        token = os.getenv('TELEGRAM_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        requests.post("https://api.telegram.org/bot" + token + "/sendMessage", 
                      data={'chat_id': chat_id, 'text': "🏀 BLUEEYESTATS-LAB\n\n" + reporte})

        # Web (Solución al SyntaxError de la barra invertida)
        contenido_html = "<html><body style='background:#121212;color:white;padding:30px;'>"
        contenido_html += "<h1>BLUEEYESTATS-LAB ACTIVO</h1><hr><p>"
        contenido_html += reporte.replace('\n', '<br>')
        contenido_html += "</p></body></html>"
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(contenido_html)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
