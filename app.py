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
