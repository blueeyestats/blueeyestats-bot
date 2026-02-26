import os
import requests

def enviar_test():
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    mensaje = "🚀 ¡Conexión exitosa! Blueeyestats está listo para enviarte datos."
    
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    response = requests.get(url)
    print(f"Respuesta de Telegram: {response.status_code}")

if __name__ == "__main__":
    enviar_test()
