import os
import requests
import feedparser
from datetime import datetime
from nba_api.stats.endpoints import scoreboardv3, leaguestandings
from openai import OpenAI

# --- CONFIGURACIÓN DE SEGURIDAD (GitHub Secrets) ---
# No ponemos las llaves aquí por seguridad; GitHub las inyectará solas
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

client = OpenAI()

MAPEO_EQUIPOS = {
    1610612737: 'Atlanta Hawks', 1610612738: 'Boston Celtics', 1610612739: 'Cleveland Cavaliers',
    1610612740: 'New Orleans Pelicans', 1610612741: 'Chicago Bulls', 1610612742: 'Dallas Mavericks',
    1610612743: 'Denver Nuggets', 1610612744: 'Golden State Warriors', 1610612745: 'Houston Rockets',
    1610612746: 'LA Clippers', 1610612747: 'Los Angeles Lakers', 1610612748: 'Miami Heat',
    1610612749: 'Milwaukee Bucks', 1610612750: 'Minnesota Timberwolves', 1610612751: 'Brooklyn Nets',
    1610612752: 'New York Knicks', 1610612753: 'Orlando Magic', 1610612754: 'Indiana Pacers',
    1610612755: 'Philadelphia 76ers', 1610612756: 'Phoenix Suns', 1610612757: 'Portland Trail Blazers',
    1610612758: 'Sacramento Kings', 1610612759: 'San Antonio Spurs', 1610612760: 'Oklahoma City Thunder',
    1610612761: 'Toronto Raptors', 1610612762: 'Utah Jazz', 1610612763: 'Memphis Grizzlies',
    1610612764: 'Washington Wizards', 1610612765: 'Detroit Pistons', 1610612766: 'Charlotte Hornets'
}

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

try:
    df_stats = leaguestandings.LeagueStandings().get_data_frames()[0]
    db = {row['TeamName']: {'win_pct': row['WinPCT']} for _, row in df_stats.iterrows()}
    
    hoy = datetime.now().strftime('%Y-%m-%d')
    partidos_raw = scoreboardv3.ScoreboardV3(game_date=hoy).get_data_frames()[0]

    feed = feedparser.parse("https://www.espn.com/espn/rss/nba/news")
    noticias = [e.title for e in feed.entries[:10]]
    
    reporte = "🏀 *BLUEEYESTATS-LAB: INSIGHTS*\n" + "="*25 + "\n\n"
    encontrados = False

    for _, p in partidos_raw.iterrows():
        id_l = p.get('homeTeamId', p.get('HOME_TEAM_ID'))
        id_v = p.get('awayTeamId', p.get('VISITOR_TEAM_ID'))
        nom_l, nom_v = MAPEO_EQUIPOS.get(id_l), MAPEO_EQUIPOS.get(id_v)
        
        if nom_l and nom_v and nom_l in db and nom_v in db:
            encontrados = True
            prob_base = (db[nom_l]['win_pct'] / (db[nom_l]['win_pct'] + db[nom_v]['win_pct'])) * 100
            prompt = f"Analiza: {nom_l} vs {nom_v}. Noticias: {noticias}. Dame ajuste (-10 a 10) y razón corta."
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
            reporte += f"📍 *{nom_l} vs {nom_v}*\n📊 Base: {prob_base:.1f}%\n🤖 {res.choices[0].message.content}\n\n"

    if encontrados:
        enviar_telegram(reporte)
except Exception as e:
    print(f"Error: {e}")
