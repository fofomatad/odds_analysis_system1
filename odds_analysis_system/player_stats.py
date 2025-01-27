import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import os
from config import DATA_DIR
from holzhauer_strategy import HolzhauerNBAAnalyzer

class PlayerStatsAnalyzer:
    def __init__(self):
        self.stats_file = os.path.join(DATA_DIR, 'player_stats.csv')
        self.props_file = os.path.join(DATA_DIR, 'player_props.csv')
        self.trends_file = os.path.join(DATA_DIR, 'player_trends.csv')
        self.holzhauer = HolzhauerNBAAnalyzer()
        
    def get_player_stats(self, player_name):
        """Retorna estatísticas do jogador"""
        try:
            df = pd.read_csv(self.stats_file)
            player_stats = df[df['player_name'] == player_name].copy()
            
            if player_stats.empty:
                return None
                
            return player_stats.to_dict('records')
            
        except Exception as e:
            print(f"Erro ao obter estatísticas do jogador: {e}")
            return None
        
    def analyze_player_trends(self, player_name, stat_type):
        """Analisa tendências de um jogador para uma estatística específica"""
        try:
            df = pd.read_csv(self.stats_file)
            player_stats = df[df['player_name'] == player_name].copy()
            
            if player_stats.empty:
                return None
                
            # Análise básica
            recent_games = player_stats.sort_values('game_date').tail(10)
            
            analysis = {
                'média_últimos_10': recent_games[stat_type].mean(),
                'tendência': self.holzhauer._analyze_trend(recent_games[stat_type]),
                'média_casa': recent_games[recent_games['is_home']][stat_type].mean(),
                'média_fora': recent_games[~recent_games['is_home']][stat_type].mean(),
                'consistência': recent_games[stat_type].std(),
                'máximo_10_jogos': recent_games[stat_type].max(),
                'mínimo_10_jogos': recent_games[stat_type].min()
            }
            
            # Análise por quarter (estilo Holzhauer)
            quarters_analysis = self.holzhauer.analyze_quarter_patterns(
                recent_games,
                current_quarter=1  # Default para análise inicial
            )
            analysis['quarters'] = quarters_analysis
            
            # Análise de hot streaks
            streaks = self.holzhauer.identify_hot_streaks(recent_games)
            analysis['streaks'] = streaks
            
            return analysis
            
        except Exception as e:
            print(f"Erro ao analisar tendências do jogador: {e}")
            return None
    
    def find_value_props(self, live_odds):
        """Encontra props com valor baseado nas tendências e estratégia Holzhauer"""
        try:
            props_df = pd.read_csv(self.props_file)
            value_props = []
            
            for _, prop in props_df.iterrows():
                player_name = prop['player_name']
                stat_type = prop['stat_type']
                line = prop['line']
                
                # Análise do jogador
                analysis = self.analyze_player_trends(player_name, stat_type)
                if not analysis:
                    continue
                
                # Análise Holzhauer de oportunidades prime
                current_game_stats = {
                    'current_quarter': 1,  # Atualizar com dados reais
                    f'current_{stat_type}': 0,  # Atualizar com dados reais
                    'last_3_minutes': {
                        'points': [],  # Últimos 3 minutos de pontuação
                    },
                    'current_pace': 0,  # Ritmo atual
                    'average_pace': 0,  # Ritmo médio
                    'time_remaining': 0,  # Tempo restante
                    'quarter': 1  # Quarter atual
                }
                
                # Atualiza estatísticas do jogo atual se disponíveis
                if live_odds and live_odds.get('game_stats'):
                    game_stats = live_odds['game_stats']
                    current_game_stats.update({
                        'current_quarter': game_stats.get('quarter', 1),
                        f'current_{stat_type}': game_stats.get(f'current_{stat_type}', 0),
                        'last_3_minutes': game_stats.get('last_3_minutes', {'points': []}),
                        'current_pace': game_stats.get('current_pace', 0),
                        'average_pace': game_stats.get('average_pace', 0),
                        'time_remaining': game_stats.get('time_remaining', 0),
                        'quarter': game_stats.get('quarter', 1)
                    })
                
                prime_opps = self.holzhauer.find_prime_opportunities(
                    player_stats=pd.read_csv(self.stats_file),
                    current_game_stats=current_game_stats
                )
                
                # Combina análises tradicionais com estratégia Holzhauer
                for opp in prime_opps:
                    if opp['stat_type'] == stat_type:
                        # Análise de momento
                        game_plan = self.holzhauer.generate_game_plan(
                            player_stats=pd.read_csv(self.stats_file),
                            opponent_stats=None,
                            game_situation=current_game_stats
                        )
                        
                        # Ajusta confiança baseado no momento
                        base_confidence = opp['confidence']
                        momentum_factor = game_plan['momentum']['overall_factor']
                        adjusted_confidence = self.holzhauer.adjust_confidence_by_momentum(
                            base_confidence,
                            momentum_factor
                        )
                        
                        # Analisa possibilidade de explosão de pontuação
                        momentum_shift = self.holzhauer.detect_momentum_shifts(
                            player_stats=pd.read_csv(self.stats_file),
                            game_situation={
                                **current_game_stats,
                                'last_points': self._get_recent_points(player_name)
                            }
                        )
                        
                        # Analisa matchup com defensor
                        if live_odds and live_odds.get('defender_stats'):
                            matchup_analysis = self.holzhauer.analyze_matchup_history(
                                player_stats=pd.read_csv(self.stats_file),
                                opponent_stats=live_odds['defender_stats'],
                                current_matchup={
                                    'defender_id': live_odds['defender_stats']['player_id'],
                                    'game_situation': current_game_stats
                                }
                            )
                        else:
                            matchup_analysis = None
                            
                        # Analisa humor e fatores emocionais
                        if live_odds and live_odds.get('player_events'):
                            mood_analysis = self.holzhauer.analyze_player_mood(
                                player_name=player_name,
                                game_date=datetime.now(),
                                recent_events=live_odds['player_events']
                            )
                        else:
                            mood_analysis = None
                        
                        value_props.append({
                            'player_name': player_name,
                            'stat_type': stat_type,
                            'line': line,
                            'odds': prop['odds'],
                            'análise': analysis,
                            'confiança': adjusted_confidence,
                            'momento': game_plan['momentum'],
                            'momentum_shift': momentum_shift,
                            'matchup_analysis': matchup_analysis,
                            'mood_analysis': mood_analysis,
                            'recomendação': 'over' if line < opp['expected_value'] else 'under',
                            'estratégia': opp['recommendation']
                        })
            
            # Ordena por confiança (estilo Holzhauer)
            return sorted(value_props, key=lambda x: x['confiança'], reverse=True)
            
        except Exception as e:
            print(f"Erro ao encontrar props com valor: {e}")
            return []
    
    def get_live_stats(self, game_id):
        """Obtém estatísticas ao vivo do jogo"""
        # Aqui você implementaria a conexão com uma API de stats ao vivo
        # Por exemplo: NBA API, SportRadar, etc.
        pass
    
    def update_player_stats(self, stats_data):
        """Atualiza o arquivo de estatísticas dos jogadores"""
        try:
            if os.path.exists(self.stats_file):
                current_stats = pd.read_csv(self.stats_file)
            else:
                current_stats = pd.DataFrame()
            
            new_stats = pd.DataFrame(stats_data)
            updated_stats = pd.concat([current_stats, new_stats]).drop_duplicates()
            updated_stats.to_csv(self.stats_file, index=False)
            
        except Exception as e:
            print(f"Erro ao atualizar estatísticas: {e}")
    
    def get_quarter_predictions(self, player_name, current_stats):
        """Prevê estatísticas para os próximos quarters usando estratégia Holzhauer"""
        try:
            # Análise básica
            analysis = self.analyze_player_trends(player_name, 'points')
            if not analysis or not analysis['quarters']:
                return None
                
            # Gera plano de jogo Holzhauer
            player_stats = pd.read_csv(self.stats_file)
            game_plan = self.holzhauer.generate_game_plan(
                player_stats=player_stats[player_stats['player_name'] == player_name],
                opponent_stats=None,  # Implementar análise de oponente
                game_situation=current_stats
            )
            
            predictions = {}
            remaining_quarters = range(current_stats['current_quarter'] + 1, 5)
            
            for quarter in remaining_quarters:
                # Previsão base
                q_avg = analysis['quarters'][f'q{quarter}']['média']
                q_trend = analysis['quarters'][f'q{quarter}']['tendência']
                
                # Ajuste Holzhauer
                is_high_value = any(
                    target['quarter'] == str(quarter)
                    for target in game_plan['high_value_targets']
                )
                
                # Ajusta previsão baseado no ritmo e estratégia
                current_pace = current_stats['current_points'] / current_stats['current_quarter']
                pace_factor = current_pace / analysis['média_últimos_10']
                
                predicted_value = q_avg * pace_factor
                if is_high_value:
                    predicted_value *= 1.2  # Bônus para quarters de alto valor
                
                predictions[f'q{quarter}'] = {
                    'previsão': predicted_value,
                    'tendência': q_trend,
                    'confiança': self._calculate_quarter_confidence(
                        current_stats, analysis, quarter
                    ),
                    'estratégia': 'aggressive' if is_high_value else 'conservative'
                }
            
            return predictions
            
        except Exception as e:
            print(f"Erro ao fazer previsões por quarter: {e}")
            return None
    
    def _calculate_quarter_confidence(self, current_stats, analysis, quarter):
        """Calcula confiança na previsão do quarter usando métricas Holzhauer"""
        confidence = 0.5
        
        # Ajusta baseado na consistência histórica
        if analysis['consistência'] < 5:  # Muito consistente
            confidence += 0.2
        elif analysis['consistência'] > 10:  # Inconsistente
            confidence -= 0.1
            
        # Ajusta baseado no momento do jogo
        if quarter == 4 and current_stats['current_points'] > analysis['média_últimos_10']:
            confidence += 0.15  # Jogador "quente"
            
        # Ajusta baseado na pressão do jogo
        if quarter == 4 and abs(current_stats.get('score_difference', 0)) < 10:
            confidence -= 0.1  # Jogo apertado = mais pressão
            
        return min(max(confidence, 0), 1)  # Limita entre 0 e 1
    
    def _get_recent_points(self, player_name):
        """Obtém pontos recentes do jogador"""
        try:
            df = pd.read_csv(self.stats_file)
            player_stats = df[df['player_name'] == player_name].copy()
            
            if player_stats.empty:
                return []
                
            return player_stats.sort_values('game_date').tail(3)['points'].tolist()
            
        except Exception as e:
            print(f"Erro ao obter pontos recentes: {e}")
            return []

    def get_total_bets(self):
        """Retorna o total de apostas realizadas"""
        try:
            df = pd.read_csv(self.stats_file)
            return len(df)
        except Exception as e:
            print(f"Erro ao obter total de apostas: {e}")
            return 0

    def get_win_rate(self):
        """Retorna a taxa de vitória das apostas"""
        try:
            df = pd.read_csv(self.stats_file)
            if len(df) == 0:
                return 0
            wins = len(df[df['result'] == 'win'])
            return round((wins / len(df)) * 100, 1)
        except Exception as e:
            print(f"Erro ao calcular taxa de vitória: {e}")
            return 0

    def get_current_streak(self):
        """Retorna a sequência atual de resultados"""
        try:
            df = pd.read_csv(self.stats_file)
            if len(df) == 0:
                return 0
            
            # Ordena por data e pega os resultados mais recentes
            df = df.sort_values('game_date', ascending=False)
            results = df['result'].tolist()
            
            streak = 0
            current_result = results[0]
            
            for result in results:
                if result == current_result:
                    if result == 'win':
                        streak += 1
                    else:
                        streak -= 1
                else:
                    break
                    
            return streak
        except Exception as e:
            print(f"Erro ao calcular sequência atual: {e}")
            return 0 