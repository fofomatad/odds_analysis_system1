from flask import Flask, render_template, jsonify, request
import pandas as pd
from config import ODDS_FILE, OPPORTUNITIES_FILE
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json
from odds_history import OddsHistory
from alerts import AlertSystem
from player_stats import PlayerStatsAnalyzer
from player_behavior_tracker import PlayerBehaviorTracker
import config
import logging
import os
from datetime import datetime
import threading
from odds_collector import OddsCollector
from monitoring import SystemMonitor
from holzhauer_strategy import HolzhauerStrategy
from nba_analyzer import NBAAnalyzer
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy

# Criar a aplicação Flask
app = Flask(__name__)

# Configurar SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///odds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Criar diretórios necessários
os.makedirs(config.DATA_DIR, exist_ok=True)
os.makedirs(config.LOGS_DIR, exist_ok=True)

# Configuração de logging
logging.basicConfig(
    filename=os.path.join(config.LOGS_DIR, 'app.log'),
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Inicializar componentes
odds_history = OddsHistory()
alert_system = AlertSystem()
player_stats = PlayerStatsAnalyzer()
player_behavior = PlayerBehaviorTracker()
system_monitor = SystemMonitor()
holzhauer = HolzhauerStrategy()
nba_analyzer = NBAAnalyzer()

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para o dashboard de jogadores
@app.route('/player-dashboard')
def player_dashboard():
    return render_template('player_dashboard.html')

# API para registrar observações
@app.route('/api/observation', methods=['POST'])
def register_observation():
    data = request.json
    player_behavior.add_observation(data)
    return jsonify({"status": "success"})

# API para registrar interações
@app.route('/api/interaction', methods=['POST'])
def register_interaction():
    data = request.json
    player_behavior.add_interaction(data)
    return jsonify({"status": "success"})

# API para obter estados emocionais
@app.route('/api/emotional-states')
def get_emotional_states():
    states = player_behavior.get_emotional_states()
    return jsonify(states)

# API para análise de sequências
@app.route('/api/sequence-analysis')
def get_sequence_analysis():
    analysis = player_behavior.analyze_sequences()
    return jsonify(analysis)

# API para análise de correlações
@app.route('/api/correlation-analysis')
def get_correlation_analysis():
    analysis = player_behavior.analyze_correlations()
    return jsonify(analysis)

# API para histórico de comportamento
@app.route('/api/behavior-history')
def get_behavior_history():
    history = player_behavior.get_history()
    return jsonify(history)

# API para oportunidades
@app.route('/api/opportunities')
def get_opportunities():
    opportunities = odds_history.get_opportunities()
    return jsonify(opportunities)

# API para estatísticas de jogadores
@app.route('/api/player-stats/<player_id>')
def get_player_stats(player_id):
    stats = player_stats.get_stats(player_id)
    return jsonify(stats)

# API para jogos ao vivo
@app.route('/api/live-games')
def get_live_games():
    games = nba_analyzer.get_live_games()
    return jsonify(games)

# API para próximos jogos
@app.route('/api/upcoming-games')
def get_upcoming_games():
    games = nba_analyzer.get_upcoming_games()
    return jsonify(games)

# Rota para análise de jogo
@app.route('/game/<game_id>')
def game_analysis(game_id):
    return render_template('game_analysis.html', game_id=game_id)

# Rota para análise pré-jogo
@app.route('/pregame/<game_id>')
def pregame_analysis(game_id):
    return render_template('pregame_analysis.html', game_id=game_id)

# API para dados do jogo
@app.route('/api/game-data/<game_id>')
def get_game_data(game_id):
    data = nba_analyzer.get_game_data(game_id)
    return jsonify(data)

# API para análise de jogadores
@app.route('/api/player-analysis/<game_id>')
def get_player_analysis(game_id):
    analysis = player_stats.analyze_game_players(game_id)
    return jsonify(analysis)

# API para previsões
@app.route('/api/predictions/<game_id>')
def get_game_predictions(game_id):
    predictions = holzhauer.analyze_game(game_id)
    return jsonify(predictions)

# API para atualizar gráficos
@app.route('/api/update-charts')
def update_charts():
    charts = {
        'odds_history': odds_history.create_chart(),
        'player_performance': player_stats.create_chart(),
        'behavior_trends': player_behavior.create_chart()
    }
    return jsonify(charts)

# API para tendências
@app.route('/api/trends')
def get_trends():
    trends = {
        'odds': odds_history.analyze_trends(),
        'players': player_stats.analyze_trends(),
        'behavior': player_behavior.analyze_trends()
    }
    return jsonify(trends)

# API para saúde do sistema
@app.route('/api/health')
def system_health():
    health = system_monitor.get_health()
    return jsonify(health)

# API para estatísticas do sistema
@app.route('/api/system-stats')
def system_stats():
    stats = system_monitor.get_stats()
    return jsonify(stats)

# API para análise de oportunidade
@app.route('/api/analyze-opportunity/<match_id>')
def analyze_opportunity(match_id):
    analysis = holzhauer.analyze_opportunity(match_id)
    return jsonify(analysis)

# API para análise de jogo NBA
@app.route('/api/analyze-nba/<game_id>')
def analyze_nba_game(game_id):
    analysis = nba_analyzer.analyze_game(game_id)
    return jsonify(analysis)

# API para jogos NBA
@app.route('/api/nba-games')
def get_nba_games():
    games = nba_analyzer.get_games()
    return jsonify(games)

# Rota para dashboard NBA
@app.route('/nba-dashboard')
def nba_dashboard():
    return render_template('nba_dashboard.html')

# API para registrar emoção
@app.route('/api/emotion', methods=['POST'])
def register_emotion():
    data = request.json
    player_behavior.register_emotion(data)
    return jsonify({"status": "success"})

# API para disparar alerta
@app.route('/api/alert', methods=['POST'])
def trigger_alert():
    data = request.json
    alert_system.trigger_alert(data)
    return jsonify({"status": "success"})

# API para adicionar nota
@app.route('/api/note', methods=['POST'])
def add_note():
    data = request.json
    player_behavior.add_note(data)
    return jsonify({"status": "success"})

# Rota para análise Holzhauer
@app.route('/holzhauer')
def holzhauer_analysis():
    return render_template('holzhauer.html')

# API para análise por quarter
@app.route('/api/quarter-analysis/<game_id>')
def get_quarter_analysis(game_id):
    analysis = nba_analyzer.analyze_quarters(game_id)
    return jsonify(analysis)

# API para props com valor
@app.route('/api/value-props/<game_id>')
def get_value_props(game_id):
    props = holzhauer.analyze_props(game_id)
    return jsonify(props)

# Tratamento de erros
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Iniciar sistema de alertas
def start_alert_system():
    alert_system.start()
    threading.Thread(target=alert_system.run).start()

# Health check para o Render
@app.route('/healthz')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    # Criar diretórios necessários
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.LOGS_DIR, exist_ok=True)
    
    # Iniciar sistema de alertas
    start_alert_system()
    
    # Iniciar scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_charts, trigger="interval", minutes=5)
    scheduler.start()
    
    # Iniciar aplicação
    app.run(debug=True)
