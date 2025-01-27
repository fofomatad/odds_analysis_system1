import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Arquivos
ODDS_FILE = os.path.join(DATA_DIR, 'odds.csv')
OPPORTUNITIES_FILE = os.path.join(DATA_DIR, 'opportunities.csv')

# Configurações do Telegram (valores padrão)
TELEGRAM_TOKEN = "7953335517:AAGlj_iB6McgohVtC0Tf9w9uy_hlG3mznEg"
TELEGRAM_CHAT_ID = "5860229978"

# Thresholds e configurações
ALERT_THRESHOLDS = {
    'odds_movement': float(os.getenv('ODDS_MOVEMENT_THRESHOLD', 5.0)),
    'volatility': float(os.getenv('VOLATILITY_THRESHOLD', 0.1)),
    'min_ev': float(os.getenv('MIN_EV_THRESHOLD', 5.0))
}

# Logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
