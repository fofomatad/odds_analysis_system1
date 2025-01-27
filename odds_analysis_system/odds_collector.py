import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os
from config import DATA_DIR, ODDS_FILE
import time
import threading

logger = logging.getLogger(__name__)

class OddsCollector:
    def __init__(self):
        self.is_running = False
        self.collection_thread = None
        
    def start_collection(self):
        """Inicia a coleta de odds em uma thread separada"""
        if not self.is_running:
            self.is_running = True
            self.collection_thread = threading.Thread(target=self._collection_loop)
            self.collection_thread.daemon = True
            self.collection_thread.start()
            logger.info("Iniciou coleta de odds")
    
    def stop_collection(self):
        """Para a coleta de odds"""
        self.is_running = False
        if self.collection_thread:
            self.collection_thread.join()
            logger.info("Parou coleta de odds")
    
    def _collection_loop(self):
        """Loop principal de coleta"""
        while self.is_running:
            try:
                self.collect_odds()
                time.sleep(60)  # Coleta a cada minuto
            except Exception as e:
                logger.error(f"Erro no loop de coleta: {e}")
                time.sleep(5)
    
    def collect_odds(self):
        """Coleta odds das diferentes casas de apostas"""
        try:
            # Simulando coleta de dados
            odds_data = self._generate_sample_data()
            
            # Salva dados
            df = pd.DataFrame(odds_data)
            df.to_csv(ODDS_FILE, index=False)
            
            logger.info(f"Coletou odds de {len(odds_data)} jogos")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao coletar odds: {e}")
            return pd.DataFrame()
    
    def _generate_sample_data(self):
        """Gera dados de exemplo para teste"""
        games = [
            "Lakers vs Warriors",
            "Celtics vs Nets",
            "Bucks vs Heat"
        ]
        
        bookmakers = ["Bookmaker1", "Bookmaker2", "Bookmaker3"]
        
        data = []
        for game in games:
            for bookmaker in bookmakers:
                data.append({
                    'Match': game,
                    'Bookmaker': bookmaker,
                    'Home_Odds': np.random.uniform(1.5, 3.0),
                    'Away_Odds': np.random.uniform(1.5, 3.0),
                    'Timestamp': datetime.now()
                })
        
        return data
    
    def get_current_odds(self):
        """Retorna as odds mais recentes"""
        try:
            if os.path.exists(ODDS_FILE):
                return pd.read_csv(ODDS_FILE)
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Erro ao ler odds atuais: {e}")
            return pd.DataFrame()

    def get_game_data(self, game_id):
        """Retorna dados do jogo (implementar conforme necessário)"""
        return {
            'id': game_id,
            'home_team': 'Team A',
            'away_team': 'Team B',
            'start_time': datetime.now().strftime('%H:%M:%S')
        }
    
    def get_nba_games(self):
        """Retorna lista de jogos NBA disponíveis"""
        return [
            {
                'id': '1',
                'home_team': 'Lakers',
                'away_team': 'Warriors',
                'start_time': '19:30'
            },
            {
                'id': '2',
                'home_team': 'Celtics',
                'away_team': 'Nets',
                'start_time': '20:00'
            }
        ]

if __name__ == "__main__":
    collector = OddsCollector()
    collector.start_collection() 