import os
import requests
from datetime import datetime

def generar_web(filas_partidos):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Blueeyestats Lab - Dashboard</title>
        <style>
            body {{ font-family: 'Montserrat', sans-serif; background-color: #1a1a1a; color: #f4f4f4; text-align: center; padding: 50px; }}
            .container {{ max-width: 800px; margin: auto; background: #2d2d2d; padding: 30px; border-radius: 15px; border-left: 5px solid #c0c0c0; }}
            h1 {{ color: #ffffff; text-transform: uppercase; letter-spacing: 2px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 15px; border-bottom: 1px solid #444; text-align: left; }}
            th {{ color: #c0c0c0; }}
            .footer {{ margin-top: 20px; font-size: 0.8em; color: #888; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>BLUEEYESTATS LAB</h1>
            <p>Branding: Blueeyestats-lab | Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <table>
                <tr><th>Evento</th><th>Predicción</th><th>Confianza</th></tr>
                {filas_partidos}
            </table>
            <div class="footer">Sistema de análisis automatizado para NBA</div>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def enviar_telegram(mensaje):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    requests.get(url)

# Simulación de datos para estrenar la web
partidos_hoy = "<tr><td>Ejemplo: Lakers vs Celtics</td><td>Gana Lakers</td><td>75%</td></tr>"

# Ejecutamos ambas funciones
generar_web(partidos_hoy)
enviar_telegram("🏀 Blueeyestats: Reporte diario generado y Dashboard actualizado.")


