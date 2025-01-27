import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple

class HolzhauerIntegratedAnalysis:
    def __init__(self):
        self.confidence_threshold = 0.85  # 85% mínimo para recomendações
        self.momentum_weight = 0.3
        self.pattern_weight = 0.25
        self.emotional_weight = 0.2
        self.physical_weight = 0.15
        self.context_weight = 0.1
        
    def analyze_opportunity(self, player_data: Dict, game_context: Dict) -> Dict:
        """Análise integrada Holzhauer para identificar oportunidades de alto valor"""
        try:
            # 1. Análise de Momento (30%)
            momentum_score = self._analyze_momentum(player_data, game_context)
            
            # 2. Análise de Padrões (25%)
            pattern_score = self._analyze_patterns(player_data)
            
            # 3. Análise Emocional (20%)
            emotional_score = self._analyze_emotional_state(player_data)
            
            # 4. Análise Física (15%)
            physical_score = self._analyze_physical_condition(player_data)
            
            # 5. Análise de Contexto (10%)
            context_score = self._analyze_game_context(game_context)
            
            # Cálculo da pontuação final ponderada
            final_score = (
                momentum_score * self.momentum_weight +
                pattern_score * self.pattern_weight +
                emotional_score * self.emotional_weight +
                physical_score * self.physical_weight +
                context_score * self.context_weight
            )
            
            # Identificação de fatores amplificadores
            amplifiers = self._identify_amplifiers(player_data, game_context)
            
            # Ajuste final com base nos amplificadores
            final_confidence = self._adjust_confidence(final_score, amplifiers)
            
            return {
                'confidence': final_confidence,
                'factors': {
                    'momentum': momentum_score,
                    'patterns': pattern_score,
                    'emotional': emotional_score,
                    'physical': physical_score,
                    'context': context_score
                },
                'amplifiers': amplifiers,
                'recommendation': self._generate_recommendation(final_confidence)
            }
            
        except Exception as e:
            logging.error(f"Erro na análise Holzhauer: {e}")
            return None
            
    def _analyze_momentum(self, player_data: Dict, game_context: Dict) -> float:
        """Análise detalhada do momento do jogador"""
        recent_performance = self._calculate_recent_performance(player_data)
        game_flow = self._analyze_game_flow(game_context)
        hot_streaks = self._identify_hot_streaks(player_data)
        
        return np.mean([recent_performance, game_flow, hot_streaks])
        
    def _analyze_patterns(self, player_data: Dict) -> float:
        """Análise de padrões específicos de performance"""
        quarter_patterns = self._analyze_quarter_patterns(player_data)
        matchup_patterns = self._analyze_matchup_patterns(player_data)
        situation_patterns = self._analyze_situation_patterns(player_data)
        
        return np.mean([quarter_patterns, matchup_patterns, situation_patterns])
        
    def _analyze_emotional_state(self, player_data: Dict) -> float:
        """Análise do estado emocional e impacto na performance"""
        confidence_level = self._assess_confidence_level(player_data)
        pressure_handling = self._assess_pressure_handling(player_data)
        recent_interactions = self._analyze_recent_interactions(player_data)
        
        return np.mean([confidence_level, pressure_handling, recent_interactions])
        
    def _analyze_physical_condition(self, player_data: Dict) -> float:
        """Análise da condição física e energia"""
        rest_factor = self._calculate_rest_factor(player_data)
        injury_impact = self._assess_injury_impact(player_data)
        stamina_level = self._assess_stamina_level(player_data)
        
        return np.mean([rest_factor, 1 - injury_impact, stamina_level])
        
    def _analyze_game_context(self, game_context: Dict) -> float:
        """Análise do contexto do jogo e situações específicas"""
        game_importance = self._assess_game_importance(game_context)
        matchup_advantage = self._calculate_matchup_advantage(game_context)
        tactical_situation = self._analyze_tactical_situation(game_context)
        
        return np.mean([game_importance, matchup_advantage, tactical_situation])
        
    def _identify_amplifiers(self, player_data: Dict, game_context: Dict) -> List[Dict]:
        """Identifica fatores que podem amplificar a confiança na previsão"""
        amplifiers = []
        
        # Sequência positiva excepcional
        if self._has_exceptional_streak(player_data):
            amplifiers.append({
                'type': 'hot_streak',
                'impact': 0.15,
                'description': 'Sequência excepcional nas últimas jogadas'
            })
            
        # Vantagem específica no confronto
        if self._has_matchup_advantage(player_data, game_context):
            amplifiers.append({
                'type': 'matchup',
                'impact': 0.12,
                'description': 'Vantagem histórica significativa neste confronto'
            })
            
        # Momento decisivo do jogo
        if self._is_clutch_situation(game_context):
            amplifiers.append({
                'type': 'clutch',
                'impact': 0.18,
                'description': 'Momento decisivo do jogo'
            })
            
        return amplifiers
        
    def _adjust_confidence(self, base_score: float, amplifiers: List[Dict]) -> float:
        """Ajusta a confiança base considerando os amplificadores"""
        adjusted_score = base_score
        
        for amplifier in amplifiers:
            adjusted_score *= (1 + amplifier['impact'])
            
        return min(adjusted_score, 1.0)  # Limita a 100%
        
    def _generate_recommendation(self, confidence: float) -> Dict:
        """Gera recomendação baseada na confiança final"""
        if confidence >= self.confidence_threshold:
            return {
                'action': 'FORTE',
                'confidence_level': confidence,
                'description': 'Oportunidade de alto valor confirmada'
            }
        elif confidence >= 0.75:
            return {
                'action': 'MODERADA',
                'confidence_level': confidence,
                'description': 'Oportunidade com valor potencial'
            }
        else:
            return {
                'action': 'AGUARDAR',
                'confidence_level': confidence,
                'description': 'Confiança insuficiente para recomendação'
            } 

    def _calculate_recent_performance(self, player_data: Dict) -> float:
        """Calcula performance recente com peso maior para últimas ações"""
        try:
            recent_actions = player_data.get('recent_actions', [])
            if not recent_actions:
                return 0.5
                
            weights = np.exp(np.linspace(0, 1, len(recent_actions)))
            weights = weights / weights.sum()
            
            scores = [self._score_action(action) for action in recent_actions]
            return np.average(scores, weights=weights)
        except Exception as e:
            logging.error(f"Erro ao calcular performance recente: {e}")
            return 0.5
            
    def _analyze_game_flow(self, game_context: Dict) -> float:
        """Analisa o fluxo do jogo e seu impacto no jogador"""
        try:
            pace = game_context.get('pace', 100)
            score_margin = abs(game_context.get('score_margin', 0))
            time_pressure = self._calculate_time_pressure(game_context)
            
            # Normaliza fatores
            pace_score = self._normalize_pace(pace)
            margin_score = self._normalize_margin(score_margin)
            pressure_score = time_pressure
            
            return np.mean([pace_score, margin_score, pressure_score])
        except Exception as e:
            logging.error(f"Erro ao analisar fluxo do jogo: {e}")
            return 0.5
            
    def _identify_hot_streaks(self, player_data: Dict) -> float:
        """Identifica e avalia sequências positivas"""
        try:
            actions = player_data.get('recent_actions', [])
            if len(actions) < 3:
                return 0.5
                
            # Analisa últimas 3 ações
            recent_success = sum(1 for action in actions[-3:] 
                               if action.get('result') == 'success')
            
            if recent_success == 3:
                return 1.0
            elif recent_success == 2:
                return 0.8
            elif recent_success == 1:
                return 0.5
            else:
                return 0.3
        except Exception as e:
            logging.error(f"Erro ao identificar hot streaks: {e}")
            return 0.5
            
    def _analyze_quarter_patterns(self, player_data: Dict) -> float:
        """Analisa padrões de performance por quarter"""
        try:
            quarter_stats = player_data.get('quarter_stats', {})
            current_quarter = player_data.get('current_quarter', 1)
            
            if not quarter_stats:
                return 0.5
                
            # Analisa tendência histórica no quarter atual
            quarter_avg = quarter_stats.get(f'q{current_quarter}_avg', 0)
            quarter_std = quarter_stats.get(f'q{current_quarter}_std', 0)
            
            if quarter_avg > 0:
                normalized_avg = min(quarter_avg / (quarter_avg + quarter_std), 1)
                return normalized_avg
            return 0.5
        except Exception as e:
            logging.error(f"Erro ao analisar padrões por quarter: {e}")
            return 0.5
            
    def _analyze_matchup_patterns(self, player_data: Dict) -> float:
        """Analisa padrões contra adversário específico"""
        try:
            matchup_stats = player_data.get('matchup_stats', {})
            if not matchup_stats:
                return 0.5
                
            success_rate = matchup_stats.get('success_rate', 0)
            games_played = matchup_stats.get('games_played', 0)
            
            # Ajusta confiança baseado no histórico
            confidence = min(games_played / 10, 1)  # Máximo após 10 jogos
            return success_rate * confidence
        except Exception as e:
            logging.error(f"Erro ao analisar padrões de confronto: {e}")
            return 0.5
            
    def _analyze_situation_patterns(self, player_data: Dict) -> float:
        """Analisa padrões em situações específicas"""
        try:
            situation_stats = player_data.get('situation_stats', {})
            current_situation = player_data.get('current_situation', {})
            
            if not situation_stats or not current_situation:
                return 0.5
                
            relevant_situations = self._find_relevant_situations(
                situation_stats, current_situation)
                
            if not relevant_situations:
                return 0.5
                
            return np.mean([s.get('success_rate', 0) for s in relevant_situations])
        except Exception as e:
            logging.error(f"Erro ao analisar padrões situacionais: {e}")
            return 0.5
            
    def _assess_confidence_level(self, player_data: Dict) -> float:
        """Avalia nível de confiança do jogador"""
        try:
            recent_success = player_data.get('recent_success_rate', 0)
            body_language = player_data.get('body_language_score', 0)
            interaction_score = player_data.get('interaction_score', 0)
            
            return np.mean([recent_success, body_language, interaction_score])
        except Exception as e:
            logging.error(f"Erro ao avaliar nível de confiança: {e}")
            return 0.5
            
    def _assess_pressure_handling(self, player_data: Dict) -> float:
        """Avalia como o jogador lida com pressão"""
        try:
            clutch_stats = player_data.get('clutch_stats', {})
            if not clutch_stats:
                return 0.5
                
            success_rate = clutch_stats.get('success_rate', 0)
            sample_size = clutch_stats.get('sample_size', 0)
            
            confidence = min(sample_size / 20, 1)  # Máximo após 20 situações
            return success_rate * confidence
        except Exception as e:
            logging.error(f"Erro ao avaliar resposta à pressão: {e}")
            return 0.5
            
    def _analyze_recent_interactions(self, player_data: Dict) -> float:
        """Analisa interações recentes e seu impacto"""
        try:
            interactions = player_data.get('recent_interactions', [])
            if not interactions:
                return 0.5
                
            scores = []
            for interaction in interactions:
                if interaction['type'] == 'positive':
                    scores.append(0.8)
                elif interaction['type'] == 'negative':
                    scores.append(0.2)
                else:
                    scores.append(0.5)
                    
            return np.mean(scores)
        except Exception as e:
            logging.error(f"Erro ao analisar interações recentes: {e}")
            return 0.5
            
    def _calculate_rest_factor(self, player_data: Dict) -> float:
        """Calcula fator de descanso/fadiga"""
        try:
            minutes_played = player_data.get('minutes_played', 0)
            days_rest = player_data.get('days_rest', 0)
            
            # Normaliza minutos jogados (assume máximo de 48 minutos)
            fatigue = minutes_played / 48
            
            # Normaliza dias de descanso (assume ótimo de 3 dias)
            rest = min(days_rest / 3, 1)
            
            return (1 - fatigue) * rest
        except Exception as e:
            logging.error(f"Erro ao calcular fator de descanso: {e}")
            return 0.5
            
    def _assess_injury_impact(self, player_data: Dict) -> float:
        """Avalia impacto de lesões recentes"""
        try:
            injury_status = player_data.get('injury_status', {})
            if not injury_status:
                return 0
                
            severity = injury_status.get('severity', 0)
            recovery = injury_status.get('recovery_progress', 100)
            
            impact = severity * (1 - recovery/100)
            return min(impact, 1)
        except Exception as e:
            logging.error(f"Erro ao avaliar impacto de lesões: {e}")
            return 0.5
            
    def _assess_stamina_level(self, player_data: Dict) -> float:
        """Avalia nível de energia/resistência"""
        try:
            current_stamina = player_data.get('current_stamina', 100)
            average_stamina = player_data.get('average_stamina', 100)
            
            return current_stamina / average_stamina
        except Exception as e:
            logging.error(f"Erro ao avaliar nível de energia: {e}")
            return 0.5
            
    def _assess_game_importance(self, game_context: Dict) -> float:
        """Avalia importância do jogo"""
        try:
            factors = [
                game_context.get('playoff_implications', 0),
                game_context.get('rivalry_factor', 0),
                game_context.get('standings_impact', 0)
            ]
            return np.mean(factors)
        except Exception as e:
            logging.error(f"Erro ao avaliar importância do jogo: {e}")
            return 0.5
            
    def _calculate_matchup_advantage(self, game_context: Dict) -> float:
        """Calcula vantagem no confronto específico"""
        try:
            matchup_stats = game_context.get('matchup_stats', {})
            if not matchup_stats:
                return 0.5
                
            win_rate = matchup_stats.get('win_rate', 0.5)
            performance_ratio = matchup_stats.get('performance_ratio', 1.0)
            
            return np.mean([win_rate, performance_ratio - 0.5])
        except Exception as e:
            logging.error(f"Erro ao calcular vantagem no confronto: {e}")
            return 0.5
            
    def _analyze_tactical_situation(self, game_context: Dict) -> float:
        """Analisa situação tática atual"""
        try:
            tactics = game_context.get('tactical_analysis', {})
            if not tactics:
                return 0.5
                
            factors = [
                tactics.get('formation_advantage', 0),
                tactics.get('matchup_exploitation', 0),
                tactics.get('strategy_effectiveness', 0)
            ]
            return np.mean(factors)
        except Exception as e:
            logging.error(f"Erro ao analisar situação tática: {e}")
            return 0.5
            
    def _has_exceptional_streak(self, player_data: Dict) -> bool:
        """Verifica se existe uma sequência excepcional"""
        try:
            streak_data = player_data.get('current_streak', {})
            if not streak_data:
                return False
                
            streak_length = streak_data.get('length', 0)
            streak_quality = streak_data.get('quality', 0)
            
            return streak_length >= 3 and streak_quality >= 0.8
        except Exception as e:
            logging.error(f"Erro ao verificar sequência excepcional: {e}")
            return False
            
    def _has_matchup_advantage(self, player_data: Dict, game_context: Dict) -> bool:
        """Verifica se existe vantagem significativa no confronto"""
        try:
            matchup_stats = player_data.get('matchup_stats', {})
            if not matchup_stats:
                return False
                
            advantage_score = matchup_stats.get('advantage_score', 0)
            games_played = matchup_stats.get('games_played', 0)
            
            return advantage_score >= 0.7 and games_played >= 5
        except Exception as e:
            logging.error(f"Erro ao verificar vantagem no confronto: {e}")
            return False
            
    def _is_clutch_situation(self, game_context: Dict) -> bool:
        """Verifica se é um momento decisivo do jogo"""
        try:
            time_remaining = game_context.get('time_remaining', 1000)
            score_difference = abs(game_context.get('score_difference', 100))
            quarter = game_context.get('quarter', 1)
            
            return (quarter >= 4 and 
                    time_remaining <= 300 and  # últimos 5 minutos
                    score_difference <= 10)
        except Exception as e:
            logging.error(f"Erro ao verificar situação decisiva: {e}")
            return False
            
    def _score_action(self, action: Dict) -> float:
        """Pontua uma ação específica"""
        try:
            result = action.get('result', '')
            importance = action.get('importance', 1.0)
            
            if result == 'success':
                return min(0.8 * importance, 1.0)
            elif result == 'partial':
                return min(0.5 * importance, 0.8)
            else:
                return max(0.2 * importance, 0)
        except Exception as e:
            logging.error(f"Erro ao pontuar ação: {e}")
            return 0.5
            
    def _normalize_pace(self, pace: float) -> float:
        """Normaliza o ritmo do jogo para score entre 0 e 1"""
        try:
            # Assume ritmo médio de 100 possessões
            min_pace = 90
            max_pace = 110
            
            normalized = (pace - min_pace) / (max_pace - min_pace)
            return max(0, min(normalized, 1))
        except Exception as e:
            logging.error(f"Erro ao normalizar ritmo: {e}")
            return 0.5
            
    def _normalize_margin(self, margin: float) -> float:
        """Normaliza margem de pontos para score entre 0 e 1"""
        try:
            # Considera margem de 20 pontos como máximo relevante
            max_margin = 20
            
            normalized = 1 - (margin / max_margin)
            return max(0, min(normalized, 1))
        except Exception as e:
            logging.error(f"Erro ao normalizar margem: {e}")
            return 0.5
            
    def _calculate_time_pressure(self, game_context: Dict) -> float:
        """Calcula pressão do tempo no momento"""
        try:
            quarter = game_context.get('quarter', 1)
            time_remaining = game_context.get('time_remaining', 720)  # segundos
            
            # Aumenta pressão nos últimos quartos
            quarter_factor = quarter / 4
            
            # Aumenta pressão com menos tempo
            time_factor = 1 - (time_remaining / 720)
            
            return np.mean([quarter_factor, time_factor])
        except Exception as e:
            logging.error(f"Erro ao calcular pressão do tempo: {e}")
            return 0.5
            
    def _find_relevant_situations(self, situation_stats: Dict, current_situation: Dict) -> List[Dict]:
        """Encontra situações históricas relevantes para o momento atual"""
        try:
            relevant = []
            
            for situation in situation_stats.values():
                similarity = self._calculate_situation_similarity(
                    situation, current_situation)
                    
                if similarity >= 0.7:  # 70% de similaridade mínima
                    relevant.append(situation)
                    
            return relevant
        except Exception as e:
            logging.error(f"Erro ao encontrar situações relevantes: {e}")
            return []
            
    def _calculate_situation_similarity(self, hist_situation: Dict, curr_situation: Dict) -> float:
        """Calcula similaridade entre duas situações"""
        try:
            factors = [
                'score_difference',
                'time_remaining',
                'quarter',
                'pace',
                'opponent_strength'
            ]
            
            similarities = []
            for factor in factors:
                hist_val = hist_situation.get(factor, 0)
                curr_val = curr_situation.get(factor, 0)
                
                if factor == 'quarter':
                    similarities.append(1.0 if hist_val == curr_val else 0.0)
                else:
                    max_diff = self._get_max_difference(factor)
                    diff = abs(hist_val - curr_val)
                    similarities.append(max(0, 1 - diff/max_diff))
                    
            return np.mean(similarities)
        except Exception as e:
            logging.error(f"Erro ao calcular similaridade de situações: {e}")
            return 0
            
    def _get_max_difference(self, factor: str) -> float:
        """Retorna diferença máxima aceitável para cada fator"""
        max_differences = {
            'score_difference': 20,
            'time_remaining': 720,
            'pace': 20,
            'opponent_strength': 1
        }
        return max_differences.get(factor, 1) 