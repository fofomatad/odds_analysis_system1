import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from config import DATA_DIR
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

logger = logging.getLogger(__name__)

class HolzhauerNBAAnalyzer:
    def __init__(self):
        self.confidence_threshold = 0.8
        self.high_value_threshold = 5.0
        
    def analyze_quarter_patterns(self, game_data, current_quarter=1):
        """Analisa padrões por quarter"""
        patterns = {}
        for quarter in range(1, 5):
            patterns[f'q{quarter}'] = {
                'média': 0,
                'tendência': 'estável'
            }
        return patterns
        
    def identify_hot_streaks(self, player_data):
        """Identifica sequências positivas"""
        return {
            'current_streak': 0,
            'max_streak': 0,
            'is_hot': False
        }
        
    def find_prime_opportunities(self, player_stats, current_game_stats):
        """Encontra oportunidades prime baseadas na estratégia Holzhauer"""
        return []
        
    def generate_game_plan(self, player_stats, opponent_stats, game_situation):
        """Gera plano de jogo estilo Holzhauer"""
        return {
            'momentum': {
                'overall_factor': 1.0
            },
            'high_value_targets': []
        }
        
    def adjust_confidence_by_momentum(self, base_confidence, momentum_factor):
        """Ajusta confiança baseado no momento"""
        return min(base_confidence * momentum_factor, 1.0)
        
    def detect_momentum_shifts(self, player_stats, game_situation):
        """Detecta mudanças de momento"""
        return {
            'has_shift': False,
            'direction': 'neutral',
            'intensity': 0
        }
        
    def analyze_matchup_history(self, player_stats, opponent_stats, current_matchup):
        """Analisa histórico de confrontos"""
        return {
            'advantage': 'neutral',
            'confidence': 0.5
        }
        
    def analyze_player_mood(self, player_name, game_date, recent_events):
        """Analisa humor do jogador"""
        return {
            'mood_score': 0.5,
            'confidence_impact': 0
        }
        
    def _analyze_trend(self, data_series):
        """Analisa tendência de uma série de dados"""
        return 'estável'

class HolzhauerStrategy:
    def __init__(self):
        self.model_file = os.path.join(DATA_DIR, 'holzhauer_model.joblib')
        self.scaler_file = os.path.join(DATA_DIR, 'holzhauer_scaler.joblib')
        self.min_confidence = 0.75
        self.model = self._load_model()
        self.scaler = self._load_scaler()
        
        # Parâmetros da estratégia Holzhauer
        self.momentum_window = 10  # Janela para análise de momentum
        self.volatility_threshold = 0.1
        self.efficiency_threshold = 0.02
        self.value_threshold = 0.1
        
    def analyze_opportunity(self, match_data):
        """Analisa uma oportunidade usando a estratégia Holzhauer"""
        try:
            # Extrai features
            features = self._extract_features(match_data)
            if features is None:
                return None
                
            # Normaliza features
            features_scaled = self.scaler.transform([features])
            
            # Predição
            confidence = self.model.predict_proba(features_scaled)[0][1]
            
            # Análise detalhada
            analysis = {
                'confidence': confidence,
                'recommended': confidence >= self.min_confidence,
                'momentum': self._analyze_momentum(match_data),
                'market_efficiency': self._analyze_market_efficiency(match_data),
                'value_opportunities': self._find_value_opportunities(match_data),
                'risk_assessment': self._assess_risk(match_data)
            }
            
            # Adiciona insights
            analysis['insights'] = self._generate_insights(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro ao analisar oportunidade: {e}")
            return None
            
    def _analyze_momentum(self, match_data):
        """Analisa momentum do mercado"""
        try:
            odds_series = match_data['Home_Odds'].values
            if len(odds_series) < 2:
                return {'trend': 'neutral', 'strength': 0}
                
            # Calcula variação percentual
            momentum = (odds_series[-1] - odds_series[0]) / odds_series[0]
            
            # Determina força e direção
            strength = abs(momentum)
            trend = 'up' if momentum > 0 else 'down'
            
            return {
                'trend': trend,
                'strength': strength,
                'recent_change': momentum
            }
            
        except Exception as e:
            logger.error(f"Erro ao analisar momentum: {e}")
            return {'trend': 'neutral', 'strength': 0}
            
    def _analyze_market_efficiency(self, match_data):
        """Analisa eficiência do mercado"""
        try:
            # Calcula spread entre casas
            home_spread = match_data['Home_Odds'].max() - match_data['Home_Odds'].min()
            away_spread = match_data['Away_Odds'].max() - match_data['Away_Odds'].min()
            
            # Calcula eficiência
            efficiency = 1 - (home_spread + away_spread) / 2
            
            return {
                'efficiency_score': efficiency,
                'home_spread': home_spread,
                'away_spread': away_spread,
                'is_efficient': efficiency > self.efficiency_threshold
            }
            
        except Exception as e:
            logger.error(f"Erro ao analisar eficiência: {e}")
            return {'efficiency_score': 0, 'is_efficient': False}
            
    def _find_value_opportunities(self, match_data):
        """Encontra oportunidades de valor"""
        try:
            opportunities = []
            
            # Analisa cada casa de apostas
            for _, row in match_data.iterrows():
                # Calcula valor esperado
                home_ev = self._calculate_ev(row['Home_Odds'], 'home')
                away_ev = self._calculate_ev(row['Away_Odds'], 'away')
                
                if home_ev > self.value_threshold:
                    opportunities.append({
                        'type': 'home',
                        'odds': row['Home_Odds'],
                        'ev': home_ev,
                        'bookmaker': row['Bookmaker']
                    })
                    
                if away_ev > self.value_threshold:
                    opportunities.append({
                        'type': 'away',
                        'odds': row['Away_Odds'],
                        'ev': away_ev,
                        'bookmaker': row['Bookmaker']
                    })
                    
            return sorted(opportunities, key=lambda x: x['ev'], reverse=True)
            
        except Exception as e:
            logger.error(f"Erro ao encontrar oportunidades: {e}")
            return []
            
    def _assess_risk(self, match_data):
        """Avalia risco da operação"""
        try:
            # Calcula volatilidade
            volatility = match_data['Home_Odds'].std()
            
            # Analisa liquidez
            liquidity = len(match_data)  # Número de casas oferecendo odds
            
            # Calcula score de risco
            risk_score = (volatility * 0.6) + ((1/liquidity) * 0.4)
            
            return {
                'risk_score': risk_score,
                'volatility': volatility,
                'liquidity': liquidity,
                'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.3 else 'low'
            }
            
        except Exception as e:
            logger.error(f"Erro ao avaliar risco: {e}")
            return {'risk_level': 'unknown'}
            
    def _generate_insights(self, analysis):
        """Gera insights baseados na análise"""
        insights = []
        
        # Analisa momentum
        if analysis['momentum']['strength'] > 0.05:
            insights.append({
                'type': 'momentum',
                'message': f"Forte momentum {analysis['momentum']['trend']}",
                'importance': 'high'
            })
            
        # Analisa eficiência
        if analysis['market_efficiency']['is_efficient']:
            insights.append({
                'type': 'efficiency',
                'message': "Mercado eficiente, odds confiáveis",
                'importance': 'medium'
            })
            
        # Analisa valor
        if analysis['value_opportunities']:
            best_opp = analysis['value_opportunities'][0]
            insights.append({
                'type': 'value',
                'message': f"Melhor oportunidade: {best_opp['ev']:.1f}% EV",
                'importance': 'high'
            })
            
        # Analisa risco
        risk = analysis['risk_assessment']
        insights.append({
            'type': 'risk',
            'message': f"Nível de risco: {risk['risk_level']}",
            'importance': 'high' if risk['risk_level'] == 'high' else 'medium'
        })
        
        return insights
            
    def _calculate_ev(self, odds, side):
        """Calcula valor esperado"""
        try:
            # Implementar cálculo real de probabilidade
            if side == 'home':
                true_prob = 0.55  # Exemplo
            else:
                true_prob = 0.45  # Exemplo
                
            return (true_prob * odds - 1) * 100
            
        except Exception as e:
            logger.error(f"Erro ao calcular EV: {e}")
            return 0
            
    def _load_model(self):
        """Carrega ou cria novo modelo"""
        try:
            if os.path.exists(self.model_file):
                return joblib.load(self.model_file)
            return RandomForestClassifier(n_estimators=100, max_depth=10)
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            return RandomForestClassifier(n_estimators=100, max_depth=10)
            
    def _load_scaler(self):
        """Carrega ou cria novo scaler"""
        try:
            if os.path.exists(self.scaler_file):
                return joblib.load(self.scaler_file)
            return StandardScaler()
        except Exception as e:
            logger.error(f"Erro ao carregar scaler: {e}")
            return StandardScaler()

    def _extract_features(self, match_data):
        """Extrai features relevantes para análise"""
        try:
            # Valor das odds
            odds_value = match_data['Home_Odds'].values[-1]
            
            # Eficiência do mercado (spread entre casas)
            market_efficiency = self._analyze_market_efficiency(match_data)
            
            # Volatilidade histórica
            volatility = self._calculate_volatility(match_data)
            
            # Momentum do mercado
            momentum = self._analyze_momentum(match_data)
            
            # Ratio valor/probabilidade
            value_ratio = self._calculate_value_ratio(match_data)
            
            return [odds_value, market_efficiency['efficiency_score'], volatility, momentum['strength'], value_ratio]
            
        except Exception as e:
            logger.error(f"Erro ao extrair features: {e}")
            return None
    
    def _calculate_volatility(self, match_data):
        """Calcula volatilidade histórica"""
        try:
            return match_data['Home_Odds'].std()
        except:
            return 0
    
    def _calculate_value_ratio(self, match_data):
        """Calcula ratio valor/probabilidade"""
        try:
            implied_prob = 1 / match_data['Home_Odds'].values[-1]
            fair_odds = 1 / match_data['Home_Odds'].values[-1]
            return (fair_odds / match_data['Home_Odds'].values[-1]) - 1
        except:
            return 0
    
    def train_model(self, training_data):
        """Treina o modelo com novos dados"""
        try:
            X = training_data[['odds_value', 'market_efficiency', 'volatility', 
                             'momentum', 'value_ratio']]
            y = training_data['result']
            
            # Atualiza scaler
            self.scaler.fit(X)
            X_scaled = self.scaler.transform(X)
            
            # Treina modelo
            self.model.fit(X_scaled, y)
            
            # Salva modelo e scaler
            joblib.dump(self.model, self.model_file)
            joblib.dump(self.scaler, self.scaler_file)
            
            logger.info("Modelo treinado e salvo com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao treinar modelo: {e}")
            return False
    
    def get_strategy_insights(self, opportunity):
        """Gera insights detalhados sobre a oportunidade"""
        try:
            analysis = self.analyze_opportunity(opportunity['match_data'])
            
            if not analysis:
                return None
            
            insights = {
                'match': opportunity['match'],
                'confidence': analysis['confidence'],
                'recommendation': 'Apostar' if analysis['recommended'] else 'Não apostar',
                'key_factors': []
            }
            
            # Analisa fatores chave
            features = analysis['features']
            
            if features['market_efficiency'] < 0.02:
                insights['key_factors'].append({
                    'factor': 'Mercado Eficiente',
                    'impact': 'Positivo',
                    'description': 'Baixa dispersão entre odds indica mercado eficiente'
                })
            
            if features['volatility'] > 0.1:
                insights['key_factors'].append({
                    'factor': 'Alta Volatilidade',
                    'impact': 'Negativo',
                    'description': 'Mercado instável aumenta risco'
                })
            
            if features['momentum'] > 0.05:
                insights['key_factors'].append({
                    'factor': 'Momentum Positivo',
                    'impact': 'Positivo',
                    'description': 'Tendência de alta nas odds'
                })
            
            if features['value_ratio'] > 0.1:
                insights['key_factors'].append({
                    'factor': 'Valor Encontrado',
                    'impact': 'Positivo',
                    'description': 'Odds acima do valor justo estimado'
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Erro ao gerar insights: {e}")
            return None 