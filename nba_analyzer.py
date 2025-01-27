import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from config import DATA_DIR
import os

logger = logging.getLogger(__name__)

class NBAAnalyzer:
    def __init__(self):
        self.quarter_patterns = {
            'Q1': {'weight': 0.3, 'variance': 0.2},
            'Q2': {'weight': 0.2, 'variance': 0.15},
            'Q3': {'weight': 0.2, 'variance': 0.25},
            'Q4': {'weight': 0.3, 'variance': 0.3}
        }
        
        self.player_impact = {
            'superstar': 0.25,
            'star': 0.15,
            'starter': 0.1,
            'rotation': 0.05
        }
        
        self.situation_factors = {
            'home_court': 1.1,
            'back_to_back': 0.9,
            'rest_advantage': 1.15,
            'playoff': 1.2
        }
        
    def analyze_game(self, game_data, player_stats, team_stats):
        """Análise completa do jogo usando estratégia Holzhauer"""
        try:
            analysis = {
                'quarter_analysis': self._analyze_quarters(game_data),
                'player_analysis': self._analyze_key_players(player_stats),
                'matchup_analysis': self._analyze_matchups(team_stats),
                'situation_analysis': self._analyze_situation(game_data),
                'momentum_factors': self._analyze_momentum(game_data)
            }
            
            # Calcula score final
            analysis['holzhauer_score'] = self._calculate_holzhauer_score(analysis)
            
            # Gera recomendações
            analysis['recommendations'] = self._generate_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro na análise do jogo: {e}")
            return None
            
    def _analyze_quarters(self, game_data):
        """Analisa padrões por quarter"""
        try:
            quarter_stats = {}
            
            for quarter, params in self.quarter_patterns.items():
                stats = {
                    'avg_points': np.mean(game_data[f'{quarter}_points']),
                    'variance': np.std(game_data[f'{quarter}_points']),
                    'trend': self._calculate_trend(game_data[f'{quarter}_points']),
                    'weight': params['weight']
                }
                
                # Identifica padrões específicos
                stats['patterns'] = {
                    'slow_start': stats['avg_points'] < 25,
                    'strong_finish': stats['avg_points'] > 30,
                    'consistent': stats['variance'] < params['variance']
                }
                
                quarter_stats[quarter] = stats
                
            return quarter_stats
            
        except Exception as e:
            logger.error(f"Erro na análise de quarters: {e}")
            return {}
            
    def _analyze_key_players(self, player_stats):
        """Analisa desempenho dos jogadores chave"""
        try:
            player_analysis = {}
            
            for player, stats in player_stats.items():
                # Calcula impacto do jogador
                impact_category = self._determine_player_impact(stats)
                impact_factor = self.player_impact[impact_category]
                
                analysis = {
                    'impact_category': impact_category,
                    'impact_factor': impact_factor,
                    'form_rating': self._calculate_form(stats),
                    'matchup_advantage': self._calculate_matchup_advantage(stats),
                    'fatigue_factor': self._calculate_fatigue(stats)
                }
                
                player_analysis[player] = analysis
                
            return player_analysis
            
        except Exception as e:
            logger.error(f"Erro na análise de jogadores: {e}")
            return {}
            
    def _analyze_matchups(self, team_stats):
        """Analisa confrontos específicos"""
        try:
            return {
                'pace_advantage': self._calculate_pace_advantage(team_stats),
                'style_matchup': self._analyze_style_matchup(team_stats),
                'historical_matchup': self._analyze_historical_matchup(team_stats),
                'key_battles': self._identify_key_battles(team_stats)
            }
        except Exception as e:
            logger.error(f"Erro na análise de confrontos: {e}")
            return {}
            
    def _analyze_situation(self, game_data):
        """Analisa fatores situacionais"""
        try:
            situation = {}
            
            # Analisa vantagem de casa
            if game_data['is_home']:
                situation['home_factor'] = self.situation_factors['home_court']
            
            # Analisa calendário
            if game_data['back_to_back']:
                situation['schedule_factor'] = self.situation_factors['back_to_back']
            elif game_data['rest_days'] >= 2:
                situation['schedule_factor'] = self.situation_factors['rest_advantage']
            
            # Analisa importância do jogo
            if game_data['is_playoff']:
                situation['importance_factor'] = self.situation_factors['playoff']
            
            return situation
            
        except Exception as e:
            logger.error(f"Erro na análise situacional: {e}")
            return {}
            
    def _analyze_momentum(self, game_data):
        """Analisa fatores de momentum"""
        try:
            return {
                'team_momentum': self._calculate_team_momentum(game_data),
                'player_momentum': self._calculate_player_momentum(game_data),
                'recent_performance': self._analyze_recent_games(game_data),
                'momentum_shifts': self._identify_momentum_shifts(game_data)
            }
        except Exception as e:
            logger.error(f"Erro na análise de momentum: {e}")
            return {}
            
    def _calculate_holzhauer_score(self, analysis):
        """Calcula score final baseado na estratégia Holzhauer"""
        try:
            score = 0
            weights = {
                'quarters': 0.2,
                'players': 0.3,
                'matchups': 0.2,
                'situation': 0.15,
                'momentum': 0.15
            }
            
            # Pontuação por quarters
            quarter_score = np.mean([q['avg_points'] * q['weight'] 
                                   for q in analysis['quarter_analysis'].values()])
            score += quarter_score * weights['quarters']
            
            # Pontuação por jogadores
            player_score = np.mean([p['impact_factor'] * p['form_rating']
                                  for p in analysis['player_analysis'].values()])
            score += player_score * weights['players']
            
            # Outros fatores
            situation_score = np.mean(list(analysis['situation_analysis'].values()))
            momentum_score = np.mean(list(analysis['momentum_factors'].values()))
            
            score += situation_score * weights['situation']
            score += momentum_score * weights['momentum']
            
            return score
            
        except Exception as e:
            logger.error(f"Erro no cálculo do score Holzhauer: {e}")
            return 0
            
    def _generate_recommendations(self, analysis):
        """Gera recomendações baseadas na análise"""
        try:
            recommendations = []
            
            # Recomendações baseadas no score
            if analysis['holzhauer_score'] > 0.7:
                recommendations.append({
                    'type': 'strong_bet',
                    'confidence': 'high',
                    'description': 'Condições muito favoráveis para aposta'
                })
            
            # Recomendações baseadas em quarters
            for quarter, stats in analysis['quarter_analysis'].items():
                if stats['patterns']['strong_finish']:
                    recommendations.append({
                        'type': 'quarter_bet',
                        'quarter': quarter,
                        'confidence': 'medium',
                        'description': f'Oportunidade de over no {quarter}'
                    })
            
            # Recomendações baseadas em jogadores
            for player, stats in analysis['player_analysis'].items():
                if stats['form_rating'] > 0.8 and stats['matchup_advantage'] > 0:
                    recommendations.append({
                        'type': 'player_prop',
                        'player': player,
                        'confidence': 'high',
                        'description': 'Boa oportunidade em props do jogador'
                    })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Erro ao gerar recomendações: {e}")
            return []

    def _calculate_trend(self, data_series):
        """Calcula tendência de uma série de dados"""
        try:
            if len(data_series) < 2:
                return {'direction': 'neutral', 'strength': 0}
            
            # Calcula inclinação da linha de tendência
            x = np.arange(len(data_series))
            slope, _ = np.polyfit(x, data_series, 1)
            
            # Determina força e direção
            strength = abs(slope)
            direction = 'up' if slope > 0 else 'down' if slope < 0 else 'neutral'
            
            return {
                'direction': direction,
                'strength': strength,
                'slope': slope
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular tendência: {e}")
            return {'direction': 'neutral', 'strength': 0}

    def _determine_player_impact(self, stats):
        """Determina categoria de impacto do jogador"""
        try:
            impact_score = (
                stats['pts_per_game'] * 0.4 +
                stats['min_per_game'] * 0.2 +
                stats['plus_minus'] * 0.2 +
                stats['usage_rate'] * 0.2
            )
            
            if impact_score > 25:
                return 'superstar'
            elif impact_score > 20:
                return 'star'
            elif impact_score > 15:
                return 'starter'
            else:
                return 'rotation'
            
        except Exception as e:
            logger.error(f"Erro ao determinar impacto: {e}")
            return 'rotation'

    def _calculate_form(self, stats):
        """Calcula rating de forma atual"""
        try:
            # Pesos para diferentes fatores
            weights = {
                'recent_games': 0.4,
                'season_avg': 0.3,
                'vs_opponent': 0.3
            }
            
            form_score = (
                stats['last_5_games_rating'] * weights['recent_games'] +
                stats['season_rating'] * weights['season_avg'] +
                stats['vs_opponent_rating'] * weights['vs_opponent']
            )
            
            return min(max(form_score, 0), 1)  # Normaliza entre 0 e 1
            
        except Exception as e:
            logger.error(f"Erro ao calcular forma: {e}")
            return 0.5

    def _calculate_matchup_advantage(self, stats):
        """Calcula vantagem no confronto direto"""
        try:
            # Analisa estatísticas contra defensor
            advantage_factors = {
                'height_diff': stats.get('height_advantage', 0) * 0.2,
                'speed_diff': stats.get('speed_advantage', 0) * 0.2,
                'historical': stats.get('historical_advantage', 0) * 0.3,
                'style': stats.get('style_advantage', 0) * 0.3
            }
            
            return sum(advantage_factors.values())
            
        except Exception as e:
            logger.error(f"Erro ao calcular vantagem: {e}")
            return 0

    def _calculate_fatigue(self, stats):
        """Calcula fator de fadiga"""
        try:
            fatigue_factors = {
                'minutes_last_game': -0.1 if stats['minutes_last_game'] > 35 else 0,
                'back_to_back': -0.2 if stats['is_back_to_back'] else 0,
                'recent_workload': -0.1 if stats['last_5_games_minutes'] > 175 else 0,
                'rest_days': 0.1 if stats['days_rest'] >= 2 else 0
            }
            
            return 1 + sum(fatigue_factors.values())
            
        except Exception as e:
            logger.error(f"Erro ao calcular fadiga: {e}")
            return 1

    def _calculate_pace_advantage(self, team_stats):
        """Calcula vantagem no ritmo de jogo"""
        try:
            home_pace = team_stats['home_team']['pace']
            away_pace = team_stats['away_team']['pace']
            
            pace_diff = home_pace - away_pace
            return {
                'difference': pace_diff,
                'advantage': 'home' if pace_diff > 2 else 'away' if pace_diff < -2 else 'neutral',
                'magnitude': abs(pace_diff)
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular vantagem de pace: {e}")
            return {'advantage': 'neutral', 'magnitude': 0}

    def _analyze_style_matchup(self, team_stats):
        """Analisa compatibilidade de estilos de jogo"""
        try:
            style_factors = {
                'three_point_rate': abs(team_stats['home_team']['three_rate'] - 
                                      team_stats['away_team']['three_rate']),
                'paint_points': abs(team_stats['home_team']['paint_points'] - 
                                  team_stats['away_team']['paint_points']),
                'fast_break': abs(team_stats['home_team']['fast_break_points'] - 
                                team_stats['away_team']['fast_break_points'])
            }
            
            return {
                'style_difference': np.mean(list(style_factors.values())),
                'factors': style_factors
            }
            
        except Exception as e:
            logger.error(f"Erro ao analisar estilos: {e}")
            return {'style_difference': 0}

    def _analyze_historical_matchup(self, team_stats):
        """Analisa histórico de confrontos"""
        try:
            h2h_stats = team_stats['head_to_head']
            
            return {
                'total_games': len(h2h_stats),
                'home_wins': sum(1 for game in h2h_stats if game['winner'] == 'home'),
                'avg_point_diff': np.mean([game['point_diff'] for game in h2h_stats]),
                'recent_trend': self._calculate_trend([game['point_diff'] 
                                                     for game in h2h_stats[-5:]])
            }
            
        except Exception as e:
            logger.error(f"Erro ao analisar histórico: {e}")
            return {}

    def _identify_key_battles(self, team_stats):
        """Identifica confrontos chave"""
        try:
            key_matchups = []
            
            for position in ['PG', 'SG', 'SF', 'PF', 'C']:
                home_player = team_stats['home_team']['starters'][position]
                away_player = team_stats['away_team']['starters'][position]
                
                advantage = self._calculate_matchup_advantage({
                    'home_player': home_player,
                    'away_player': away_player
                })
                
                if abs(advantage) > 0.1:
                    key_matchups.append({
                        'position': position,
                        'advantage_team': 'home' if advantage > 0 else 'away',
                        'magnitude': abs(advantage)
                    })
            
            return sorted(key_matchups, key=lambda x: x['magnitude'], reverse=True)
            
        except Exception as e:
            logger.error(f"Erro ao identificar confrontos chave: {e}")
            return []

    def _calculate_team_momentum(self, game_data):
        """Calcula momentum da equipe"""
        try:
            recent_games = game_data['last_10_games']
            
            momentum_score = sum([
                game['win'] * (1.1 ** (10 - i))  # Jogos mais recentes têm mais peso
                for i, game in enumerate(recent_games)
            ]) / len(recent_games)
            
            return momentum_score
            
        except Exception as e:
            logger.error(f"Erro ao calcular momentum da equipe: {e}")
            return 0

    def _calculate_player_momentum(self, game_data):
        """Calcula momentum dos jogadores"""
        try:
            player_scores = {}
            
            for player, stats in game_data['player_stats'].items():
                recent_performance = stats['last_5_games']
                baseline = stats['season_average']
                
                # Calcula desvio do baseline
                momentum = sum([
                    (game['pts'] - baseline['pts']) / baseline['pts']
                    for game in recent_performance
                ]) / len(recent_performance)
                
                player_scores[player] = momentum
            
            return player_scores
            
        except Exception as e:
            logger.error(f"Erro ao calcular momentum dos jogadores: {e}")
            return {}

    def _analyze_recent_games(self, game_data):
        """Analisa jogos recentes"""
        try:
            recent_stats = {
                'wins': sum(1 for game in game_data['last_5_games'] if game['win']),
                'avg_points': np.mean([game['points'] for game in game_data['last_5_games']]),
                'avg_margin': np.mean([game['margin'] for game in game_data['last_5_games']]),
                'trend': self._calculate_trend([game['points'] 
                                              for game in game_data['last_5_games']])
            }
            
            return recent_stats
            
        except Exception as e:
            logger.error(f"Erro ao analisar jogos recentes: {e}")
            return {}

    def _identify_momentum_shifts(self, game_data):
        """Identifica mudanças de momentum"""
        try:
            shifts = []
            
            for game in game_data['last_5_games']:
                quarter_scores = [game[f'Q{i}_points'] for i in range(1, 5)]
                
                for i in range(len(quarter_scores) - 1):
                    diff = quarter_scores[i+1] - quarter_scores[i]
                    if abs(diff) > 10:
                        shifts.append({
                            'game_id': game['id'],
                            'quarter': i + 1,
                            'magnitude': abs(diff),
                            'direction': 'up' if diff > 0 else 'down'
                        })
            
            return shifts
            
        except Exception as e:
            logger.error(f"Erro ao identificar mudanças de momentum: {e}")
            return [] 