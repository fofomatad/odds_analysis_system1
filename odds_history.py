import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from config import DATA_DIR
import json
import logging

logger = logging.getLogger(__name__)

class OddsHistory:
    def __init__(self):
        self.history_file = os.path.join(DATA_DIR, 'odds_history.csv')
        self.max_history_days = 7  # Mantém histórico dos últimos 7 dias
        self._initialize_history()

    def _initialize_history(self):
        """Inicializa ou carrega o arquivo de histórico"""
        try:
            if not os.path.exists(self.history_file):
                self._create_empty_history()
            else:
                self._clean_old_records()
        except Exception as e:
            logger.error(f"Erro ao inicializar histórico: {e}")
            self._create_empty_history()

    def _create_empty_history(self):
        """Cria um arquivo de histórico vazio"""
        df = pd.DataFrame(columns=[
            'timestamp', 'match', 'side', 'odds', 'bookmaker'
        ])
        df.to_csv(self.history_file, index=False)

    def _clean_old_records(self):
        """Remove registros mais antigos que max_history_days"""
        try:
            df = pd.read_csv(self.history_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            cutoff_date = datetime.now() - timedelta(days=self.max_history_days)
            df = df[df['timestamp'] > cutoff_date]
            df.to_csv(self.history_file, index=False)
        except Exception as e:
            logger.error(f"Erro ao limpar registros antigos: {e}")

    def add_odds(self, match, side, odds, bookmaker):
        """Adiciona novo registro de odds ao histórico"""
        try:
            new_record = pd.DataFrame([{
                'timestamp': datetime.now(),
                'match': match,
                'side': side,
                'odds': odds,
                'bookmaker': bookmaker
            }])
            
            df = pd.read_csv(self.history_file)
            df = pd.concat([df, new_record], ignore_index=True)
            df.to_csv(self.history_file, index=False)
            
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar odds: {e}")
            return False

    def get_odds_history(self, match=None, hours=24):
        """Retorna histórico de odds com filtros opcionais"""
        try:
            df = pd.read_csv(self.history_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filtrar por período
            cutoff_time = datetime.now() - timedelta(hours=hours)
            df = df[df['timestamp'] > cutoff_time]
            
            # Filtrar por partida se especificado
            if match:
                df = df[df['match'] == match]
            
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Erro ao obter histórico: {e}")
            return []

    def get_trend_analysis(self, match):
        """Analisa tendência de odds para uma partida específica"""
        try:
            df = pd.read_csv(self.history_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            match_data = df[df['match'] == match].copy()
            
            if len(match_data) < 2:
                return None
            
            # Calcular métricas
            latest_odds = match_data['odds'].iloc[-1]
            oldest_odds = match_data['odds'].iloc[0]
            variation = (latest_odds - oldest_odds) / oldest_odds * 100
            volatility = match_data['odds'].std()
            
            return {
                'match': match,
                'current_odds': latest_odds,
                'variation_percent': variation,
                'volatility': volatility,
                'trend': 'up' if variation > 0 else 'down',
                'is_volatile': volatility > 0.1
            }
        except Exception as e:
            logger.error(f"Erro ao analisar tendência: {e}")
            return None
        
    def update_history(self, current_odds_df):
        """Atualiza o histórico de odds"""
        try:
            # Carrega histórico existente ou cria novo
            if os.path.exists(self.history_file):
                history_df = pd.read_csv(self.history_file)
                history_df['Timestamp'] = pd.to_datetime(history_df['Timestamp'])
            else:
                history_df = pd.DataFrame()
            
            # Adiciona odds atuais ao histórico
            if not current_odds_df.empty:
                current_odds_df['Timestamp'] = pd.to_datetime(current_odds_df['Timestamp'])
                history_df = pd.concat([history_df, current_odds_df])
            
            # Remove duplicatas e ordena
            history_df = history_df.drop_duplicates()
            history_df = history_df.sort_values('Timestamp')
            
            # Remove dados antigos (mais de 7 dias)
            cutoff_date = datetime.now() - timedelta(days=self.max_history_days)
            history_df = history_df[history_df['Timestamp'] > cutoff_date]
            
            # Salva histórico atualizado
            history_df.to_csv(self.history_file, index=False)
            return history_df
            
        except Exception as e:
            print(f"Erro ao atualizar histórico: {e}")
            return pd.DataFrame()
    
    def analyze_movements(self):
        """Analisa movimentações significativas nas odds"""
        try:
            if not os.path.exists(self.history_file):
                return pd.DataFrame()
                
            history_df = pd.read_csv(self.history_file)
            history_df['Timestamp'] = pd.to_datetime(history_df['Timestamp'])
            
            movements = []
            
            # Analisa cada jogo
            for match in history_df['Match'].unique():
                match_data = history_df[history_df['Match'] == match].copy()
                match_data = match_data.sort_values('Timestamp')
                
                # Calcula variação percentual nas odds
                for side in ['Home', 'Away']:
                    odds_col = f'{side}_Odds'
                    if len(match_data[odds_col]) > 1:
                        initial_odds = match_data[odds_col].iloc[0]
                        current_odds = match_data[odds_col].iloc[-1]
                        pct_change = ((current_odds - initial_odds) / initial_odds) * 100
                        
                        if abs(pct_change) >= 5:  # Movimento significativo (>5%)
                            movements.append({
                                'Match': match,
                                'Side': side,
                                'Initial_Odds': initial_odds,
                                'Current_Odds': current_odds,
                                'Change_Pct': pct_change,
                                'Start_Time': match_data['Timestamp'].iloc[0],
                                'Last_Update': match_data['Timestamp'].iloc[-1]
                            })
            
            return pd.DataFrame(movements)
            
        except Exception as e:
            print(f"Erro ao analisar movimentações: {e}")
            return pd.DataFrame()
    
    def get_trend_analysis(self):
        """Analisa tendências nas odds"""
        try:
            if not os.path.exists(self.history_file):
                return {}
                
            history_df = pd.read_csv(self.history_file)
            history_df['Timestamp'] = pd.to_datetime(history_df['Timestamp'])
            
            trends = {
                'increasing': [],  # Odds aumentando
                'decreasing': [],  # Odds diminuindo
                'volatile': []     # Odds instáveis
            }
            
            for match in history_df['Match'].unique():
                match_data = history_df[history_df['Match'] == match].copy()
                if len(match_data) < 3:  # Precisa de pelo menos 3 pontos
                    continue
                    
                for side in ['Home', 'Away']:
                    odds_col = f'{side}_Odds'
                    odds_series = match_data[odds_col]
                    
                    # Calcula volatilidade
                    volatility = odds_series.std() / odds_series.mean()
                    
                    # Determina tendência
                    slope = np.polyfit(range(len(odds_series)), odds_series, 1)[0]
                    
                    trend_info = {
                        'Match': match,
                        'Side': side,
                        'Current_Odds': odds_series.iloc[-1],
                        'Volatility': volatility
                    }
                    
                    if volatility > 0.1:  # Alta volatilidade
                        trends['volatile'].append(trend_info)
                    elif slope > 0.01:    # Tendência de alta
                        trends['increasing'].append(trend_info)
                    elif slope < -0.01:   # Tendência de baixa
                        trends['decreasing'].append(trend_info)
            
            return trends
            
        except Exception as e:
            print(f"Erro ao analisar tendências: {e}")
            return {} 