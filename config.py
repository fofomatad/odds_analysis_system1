import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Criar diretórios se não existirem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Arquivos
ODDS_FILE = os.path.join(DATA_DIR, 'odds.csv')
OPPORTUNITIES_FILE = os.path.join(DATA_DIR, 'opportunities.csv')
PLAYER_STATS_FILE = os.path.join(DATA_DIR, 'player_stats.csv')
PLAYER_PROPS_FILE = os.path.join(DATA_DIR, 'player_props.csv')
PLAYER_TRENDS_FILE = os.path.join(DATA_DIR, 'player_trends.csv')

# Configurações do servidor
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Configurações de coleta
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 30))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', 5))

# Thresholds
ALERT_THRESHOLDS = {
    'odds_movement': float(os.getenv('ODDS_MOVEMENT_THRESHOLD', 5.0)),
    'volatility': float(os.getenv('VOLATILITY_THRESHOLD', 0.1)),
    'min_ev': float(os.getenv('MIN_EV_THRESHOLD', 5.0))
}

# Configurações de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.path.join(LOGS_DIR, 'app.log')

# Configurações de atualização
ALERT_CHECK_INTERVAL = int(os.getenv('ALERT_CHECK_INTERVAL', 60))

# Configurações da estratégia Holzhauer
CONFIDENCE_THRESHOLD = int(os.getenv('CONFIDENCE_THRESHOLD', 75))
VALUE_THRESHOLD = int(os.getenv('VALUE_THRESHOLD', 5))
QUARTER_ANALYSIS_WINDOW = int(os.getenv('QUARTER_ANALYSIS_WINDOW', 10))
TREND_ANALYSIS_WINDOW = int(os.getenv('TREND_ANALYSIS_WINDOW', 5)) 