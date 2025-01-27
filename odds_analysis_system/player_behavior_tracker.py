import pandas as pd
from datetime import datetime
import numpy as np

class PlayerBehaviorTracker:
    def __init__(self):
        self.behavior_log = []
        self.emotional_states = {}
        self.interaction_history = []
        
    def register_observation(self, player_name, timestamp, observation_type, details):
        """Registra uma observação sobre o comportamento do jogador"""
        observation = {
            'jogador': player_name,
            'timestamp': timestamp,
            'tipo': observation_type,
            'detalhes': details,
            'quarter': self._get_current_quarter(timestamp),
            'impacto_emocional': self._calculate_emotional_impact(observation_type, details)
        }
        
        self.behavior_log.append(observation)
        self._update_emotional_state(player_name, observation)
        return observation
        
    def register_interaction(self, player1, player2, interaction_type, details):
        """Registra uma interação entre jogadores"""
        interaction = {
            'jogador1': player1,
            'jogador2': player2,
            'tipo': interaction_type,
            'detalhes': details,
            'timestamp': datetime.now(),
            'impacto': self._calculate_interaction_impact(interaction_type)
        }
        
        self.interaction_history.append(interaction)
        return interaction
        
    def get_player_emotional_state(self, player_name):
        """Retorna o estado emocional atual do jogador"""
        if player_name not in self.emotional_states:
            return {
                'estado': 'neutro',
                'intensidade': 0.5,
                'tendência': 'estável',
                'fatores_influência': []
            }
        return self.emotional_states[player_name]
        
    def analyze_behavior_pattern(self, player_name, time_window_minutes=10):
        """Analisa padrões de comportamento recentes"""
        recent_observations = self._get_recent_observations(player_name, time_window_minutes)
        
        return {
            'padrão_dominante': self._identify_dominant_pattern(recent_observations),
            'nível_pressão': self._calculate_pressure_level(recent_observations),
            'sinais_importantes': self._identify_key_signals(recent_observations),
            'previsão_comportamento': self._predict_behavior(recent_observations)
        }
        
    def _update_emotional_state(self, player_name, observation):
        """Atualiza o estado emocional do jogador"""
        current_state = self.emotional_states.get(player_name, {
            'estado': 'neutro',
            'intensidade': 0.5,
            'tendência': 'estável',
            'fatores_influência': []
        })
        
        # Atualiza baseado na nova observação
        impact = observation['impacto_emocional']
        new_state = {
            'estado': self._determine_emotional_state(current_state, impact),
            'intensidade': self._calculate_new_intensity(current_state['intensidade'], impact),
            'tendência': self._determine_trend(current_state, impact),
            'fatores_influência': self._update_influence_factors(
                current_state['fatores_influência'],
                observation
            )
        }
        
        self.emotional_states[player_name] = new_state
        
    def _calculate_emotional_impact(self, observation_type, details):
        """Calcula o impacto emocional de uma observação"""
        impact_weights = {
            # Reações Emocionais
            'frustração': -0.3,
            'celebração': 0.4,
            'discussão_arbitragem': -0.2,
            'irritação_companheiro': -0.25,
            'motivação_time': 0.35,
            
            # Linguagem Corporal
            'cabeça_baixa': -0.3,
            'gestos_confiança': 0.3,
            'isolamento_time': -0.4,
            'comunicação_ativa': 0.25,
            
            # Momentos do Jogo
            'erro_crucial': -0.4,
            'jogada_decisiva': 0.5,
            'lance_livre_pressão': -0.15,
            'clutch_moment': 0.45,
            'momento_decisivo': 0.4,
            
            # Interações
            'interação_positiva': 0.2,
            'interação_negativa': -0.2,
            'apoio_companheiros': 0.3,
            'conflito_adversário': -0.35,
            'provocação_recebida': -0.25,
            
            # Fatores Físicos
            'lesão': -0.6,
            'fadiga_visível': -0.3,
            'recuperação_lesão': 0.2,
            'desconforto_físico': -0.25,
            
            # Fatores Externos
            'reação_torcida': 0.2,
            'pressão_placar': -0.3,
            'timeout': 0.1,
            'substituição': -0.1,
            
            # Sinais de Confiança
            'pedido_bola': 0.25,
            'liderança_quadra': 0.35,
            'hesitação': -0.3,
            'postura_dominante': 0.4,
            
            # Concentração
            'foco_intenso': 0.35,
            'distração': -0.3,
            'rotina_préjogo': 0.2,
            'ansiedade_visível': -0.35
        }
        
        base_impact = impact_weights.get(observation_type, 0)
        
        # Ajusta impacto baseado nos detalhes
        if details:
            if 'muito' in details.lower() or 'extremamente' in details.lower():
                base_impact *= 1.5
            if 'pouco' in details.lower() or 'levemente' in details.lower():
                base_impact *= 0.5
                
        return base_impact
        
    def _calculate_interaction_impact(self, interaction_type):
        """Calcula o impacto de uma interação entre jogadores"""
        impact_weights = {
            # Interações Positivas
            'celebração_conjunta': 0.3,
            'apoio_mútuo': 0.35,
            'comunicação_estratégica': 0.25,
            'motivação_companheiro': 0.4,
            'liderança_positiva': 0.45,
            
            # Interações Negativas
            'confronto': -0.4,
            'discussão': -0.2,
            'provocação': -0.3,
            'crítica_pública': -0.35,
            'isolamento_grupo': -0.4,
            
            # Interações Técnicas
            'ajuste_tático': 0.2,
            'correção_técnica': 0.15,
            'orientação_jogo': 0.25,
            
            # Interações Emocionais
            'compartilhamento_frustração': -0.25,
            'celebração_emocional': 0.4,
            'suporte_emocional': 0.3
        }
        
        return impact_weights.get(interaction_type, 0)
        
    def _get_recent_observations(self, player_name, time_window_minutes):
        """Obtém observações recentes de um jogador"""
        current_time = datetime.now()
        return [
            obs for obs in self.behavior_log
            if obs['jogador'] == player_name and
            (current_time - obs['timestamp']).total_seconds() <= time_window_minutes * 60
        ]
        
    def _identify_dominant_pattern(self, observations):
        """Identifica o padrão dominante nas observações"""
        if not observations:
            return None
            
        pattern_counts = {}
        for obs in observations:
            if obs['tipo'] not in pattern_counts:
                pattern_counts[obs['tipo']] = 0
            pattern_counts[obs['tipo']] += 1
            
        return max(pattern_counts.items(), key=lambda x: x[1])[0]
        
    def _calculate_pressure_level(self, observations):
        """Calcula o nível de pressão baseado nas observações"""
        if not observations:
            return 0.5
            
        pressure_factors = {
            'erro_crucial': 0.3,
            'jogada_decisiva': 0.2,
            'discussão_arbitragem': 0.15,
            'lesão': 0.25,
            'timeout': -0.1
        }
        
        total_pressure = 0.5  # Nível base
        for obs in observations:
            total_pressure += pressure_factors.get(obs['tipo'], 0)
            
        return min(max(total_pressure, 0), 1)
        
    def _identify_key_signals(self, observations):
        """Identifica sinais importantes nas observações"""
        signals = []
        
        if not observations:
            return signals
            
        # Analisa sequência de eventos
        for i in range(len(observations) - 1):
            current = observations[i]
            next_obs = observations[i + 1]
            
            if current['impacto_emocional'] * next_obs['impacto_emocional'] < 0:
                signals.append({
                    'tipo': 'mudança_emocional',
                    'momento': current['timestamp'],
                    'intensidade': abs(next_obs['impacto_emocional'])
                })
                
        return signals
        
    def _predict_behavior(self, observations):
        """Prevê comportamento futuro baseado nas observações"""
        if not observations:
            return {
                'tendência': 'estável',
                'confiança': 0.5,
                'alertas': []
            }
            
        # Analisa tendência recente
        recent_impact = sum(obs['impacto_emocional'] for obs in observations[-3:]) / 3
        
        prediction = {
            'tendência': 'positiva' if recent_impact > 0.1 else 'negativa' if recent_impact < -0.1 else 'estável',
            'confiança': min(0.5 + abs(recent_impact), 0.9),
            'alertas': []
        }
        
        # Identifica possíveis alertas
        if abs(recent_impact) > 0.3:
            prediction['alertas'].append({
                'tipo': 'mudança_comportamental_iminente',
                'probabilidade': abs(recent_impact),
                'direção': 'positiva' if recent_impact > 0 else 'negativa'
            })
            
        return prediction
        
    def _determine_emotional_state(self, current_state, impact):
        """Determina novo estado emocional"""
        states = {
            'muito_positivo': (0.7, 1.0),
            'positivo': (0.3, 0.7),
            'neutro': (-0.3, 0.3),
            'negativo': (-0.7, -0.3),
            'muito_negativo': (-1.0, -0.7)
        }
        
        new_value = current_state['intensidade'] + impact
        
        for state, (min_val, max_val) in states.items():
            if min_val <= new_value <= max_val:
                return state
                
        return 'neutro'
        
    def _calculate_new_intensity(self, current_intensity, impact):
        """Calcula nova intensidade emocional"""
        new_intensity = current_intensity + impact
        return min(max(new_intensity, 0), 1)
        
    def _determine_trend(self, current_state, impact):
        """Determina tendência emocional"""
        if abs(impact) < 0.1:
            return 'estável'
        return 'ascendente' if impact > 0 else 'descendente'
        
    def _update_influence_factors(self, current_factors, new_observation):
        """Atualiza fatores de influência"""
        # Mantém apenas os 5 fatores mais recentes
        factors = current_factors[-4:] + [{
            'tipo': new_observation['tipo'],
            'impacto': new_observation['impacto_emocional'],
            'timestamp': new_observation['timestamp']
        }]
        
        return factors
        
    def _get_current_quarter(self, timestamp):
        """Determina o quarter atual baseado no timestamp"""
        # Implementar lógica para determinar quarter baseado no tempo de jogo
        return 1  # Placeholder 

    def analyze_pressure_response(self, player_name, game_situation):
        """Analisa como o jogador responde à pressão do momento"""
        recent_obs = self._get_recent_observations(player_name, 5)  # últimos 5 minutos
        
        pressure_analysis = {
            'nível_pressão': self._calculate_pressure_level(recent_obs),
            'sinais_pressão': [],
            'resposta_atual': 'neutra',
            'histórico_resposta': [],
            'recomendações': []
        }
        
        # Analisa sinais de pressão
        for obs in recent_obs:
            if obs['tipo'] in ['hesitação', 'ansiedade_visível', 'erro_crucial']:
                pressure_analysis['sinais_pressão'].append({
                    'tipo': obs['tipo'],
                    'momento': obs['timestamp'],
                    'intensidade': abs(obs['impacto_emocional'])
                })
        
        # Determina resposta atual
        if pressure_analysis['sinais_pressão']:
            recent_responses = [s['intensidade'] for s in pressure_analysis['sinais_pressão']]
            avg_response = sum(recent_responses) / len(recent_responses)
            
            if avg_response > 0.7:
                pressure_analysis['resposta_atual'] = 'muito_afetado'
            elif avg_response > 0.4:
                pressure_analysis['resposta_atual'] = 'moderadamente_afetado'
            elif avg_response > 0.2:
                pressure_analysis['resposta_atual'] = 'levemente_afetado'
            else:
                pressure_analysis['resposta_atual'] = 'resiliente'
        
        return pressure_analysis 

    def analyze_sequence_patterns(self, player_name, time_window_minutes=15):
        """Analisa padrões de sequência de eventos e seu impacto no desempenho"""
        sequence_analysis = {
            'padrões_identificados': [],
            'sequência_atual': None,
            'probabilidade_explosão': 0.0,
            'probabilidade_queda': 0.0,
            'gatilhos_ativos': [],
            'previsão_próximos_minutos': None
        }
        
        try:
            # Obtém observações recentes
            recent_obs = self._get_recent_observations(player_name, time_window_minutes)
            
            if recent_obs:
                # Identifica padrões de sequência
                patterns = self._identify_sequence_patterns(recent_obs)
                sequence_analysis['padrões_identificados'] = patterns
                
                # Analisa sequência atual
                current_sequence = self._analyze_current_sequence(recent_obs)
                sequence_analysis['sequência_atual'] = current_sequence
                
                # Calcula probabilidades
                explosion_prob = self._calculate_explosion_probability(patterns, current_sequence)
                sequence_analysis['probabilidade_explosão'] = explosion_prob
                
                decline_prob = self._calculate_decline_probability(patterns, current_sequence)
                sequence_analysis['probabilidade_queda'] = decline_prob
                
                # Identifica gatilhos ativos
                active_triggers = self._identify_active_triggers(current_sequence)
                sequence_analysis['gatilhos_ativos'] = active_triggers
                
                # Gera previsão
                prediction = self._generate_sequence_prediction(
                    patterns,
                    current_sequence,
                    active_triggers
                )
                sequence_analysis['previsão_próximos_minutos'] = prediction
                
        except Exception as e:
            print(f"Erro ao analisar padrões de sequência: {e}")
            
        return sequence_analysis
    
    def _identify_sequence_patterns(self, observations):
        """Identifica padrões nas sequências de eventos"""
        patterns = []
        
        try:
            # Analisa sequências de 3 eventos
            for i in range(len(observations) - 2):
                sequence = observations[i:i+3]
                pattern = {
                    'eventos': [obs['tipo'] for obs in sequence],
                    'impactos': [obs['impacto_emocional'] for obs in sequence],
                    'duração': (sequence[-1]['timestamp'] - sequence[0]['timestamp']).total_seconds(),
                    'resultado': self._determine_sequence_result(sequence)
                }
                
                if self._is_significant_pattern(pattern):
                    patterns.append(pattern)
            
            # Agrupa padrões similares
            grouped_patterns = self._group_similar_patterns(patterns)
            
            # Calcula confiabilidade dos padrões
            for pattern in grouped_patterns:
                pattern['confiabilidade'] = self._calculate_pattern_reliability(pattern)
                
        except Exception as e:
            print(f"Erro ao identificar padrões de sequência: {e}")
            
        return grouped_patterns
    
    def _analyze_current_sequence(self, observations):
        """Analisa a sequência atual de eventos"""
        try:
            # Pega os últimos 3 eventos
            recent_sequence = observations[-3:]
            
            if len(recent_sequence) < 3:
                return None
                
            return {
                'eventos': [obs['tipo'] for obs in recent_sequence],
                'impactos': [obs['impacto_emocional'] for obs in recent_sequence],
                'tendência': self._calculate_sequence_trend(recent_sequence),
                'intensidade': self._calculate_sequence_intensity(recent_sequence),
                'momento': recent_sequence[-1]['timestamp']
            }
            
        except Exception as e:
            print(f"Erro ao analisar sequência atual: {e}")
            return None
    
    def _calculate_explosion_probability(self, patterns, current_sequence):
        """Calcula probabilidade de explosão de desempenho"""
        try:
            if not current_sequence:
                return 0.0
                
            base_prob = 0.3  # Probabilidade base
            
            # Ajusta baseado nos padrões históricos
            for pattern in patterns:
                if self._is_similar_sequence(pattern['eventos'], current_sequence['eventos']):
                    if pattern['resultado'] == 'explosão':
                        base_prob *= (1 + pattern['confiabilidade'])
                        
            # Ajusta baseado na tendência atual
            if current_sequence['tendência'] == 'ascendente':
                base_prob *= 1.3
            elif current_sequence['tendência'] == 'descendente':
                base_prob *= 0.7
                
            # Ajusta baseado na intensidade
            base_prob *= (1 + current_sequence['intensidade'] * 0.5)
            
            return min(max(base_prob, 0), 1)
            
        except Exception as e:
            print(f"Erro ao calcular probabilidade de explosão: {e}")
            return 0.0
    
    def _calculate_decline_probability(self, patterns, current_sequence):
        """Calcula probabilidade de queda de desempenho"""
        try:
            if not current_sequence:
                return 0.0
                
            base_prob = 0.3  # Probabilidade base
            
            # Ajusta baseado nos padrões históricos
            for pattern in patterns:
                if self._is_similar_sequence(pattern['eventos'], current_sequence['eventos']):
                    if pattern['resultado'] == 'queda':
                        base_prob *= (1 + pattern['confiabilidade'])
                        
            # Ajusta baseado na tendência atual
            if current_sequence['tendência'] == 'descendente':
                base_prob *= 1.3
            elif current_sequence['tendência'] == 'ascendente':
                base_prob *= 0.7
                
            # Ajusta baseado na intensidade
            base_prob *= (1 + current_sequence['intensidade'] * 0.5)
            
            return min(max(base_prob, 0), 1)
            
        except Exception as e:
            print(f"Erro ao calcular probabilidade de queda: {e}")
            return 0.0
    
    def _identify_active_triggers(self, current_sequence):
        """Identifica gatilhos ativos na sequência atual"""
        triggers = []
        
        try:
            if not current_sequence:
                return triggers
                
            # Analisa eventos recentes
            for evento, impacto in zip(current_sequence['eventos'], current_sequence['impactos']):
                # Gatilhos positivos
                if evento in ['jogada_decisiva', 'clutch_moment'] and impacto > 0.3:
                    triggers.append({
                        'tipo': 'momento_decisivo',
                        'força': abs(impacto),
                        'natureza': 'positivo'
                    })
                    
                # Gatilhos negativos
                if evento in ['erro_crucial', 'frustração'] and impacto < -0.3:
                    triggers.append({
                        'tipo': 'pressão_negativa',
                        'força': abs(impacto),
                        'natureza': 'negativo'
                    })
                    
                # Gatilhos de momentum
                if evento in ['celebração', 'gestos_confiança'] and impacto > 0.2:
                    triggers.append({
                        'tipo': 'momentum_positivo',
                        'força': abs(impacto),
                        'natureza': 'positivo'
                    })
                    
        except Exception as e:
            print(f"Erro ao identificar gatilhos ativos: {e}")
            
        return triggers
    
    def _generate_sequence_prediction(self, patterns, current_sequence, active_triggers):
        """Gera previsão baseada na sequência atual"""
        try:
            if not current_sequence:
                return None
                
            # Encontra padrões similares
            similar_patterns = [
                p for p in patterns
                if self._is_similar_sequence(p['eventos'], current_sequence['eventos'])
            ]
            
            if not similar_patterns:
                return None
                
            # Calcula tendência provável
            positive_outcomes = sum(1 for p in similar_patterns if p['resultado'] == 'explosão')
            negative_outcomes = sum(1 for p in similar_patterns if p['resultado'] == 'queda')
            
            total_patterns = len(similar_patterns)
            if total_patterns == 0:
                return None
                
            prediction = {
                'tendência_provável': 'explosão' if positive_outcomes > negative_outcomes else 'queda',
                'confiança': max(positive_outcomes, negative_outcomes) / total_patterns,
                'janela_tempo': '5-10 minutos',
                'intensidade_esperada': self._calculate_expected_intensity(
                    similar_patterns,
                    active_triggers
                )
            }
            
            return prediction
            
        except Exception as e:
            print(f"Erro ao gerar previsão de sequência: {e}")
            return None
    
    def _determine_sequence_result(self, sequence):
        """Determina o resultado de uma sequência de eventos"""
        try:
            # Calcula impacto total
            total_impact = sum(obs['impacto_emocional'] for obs in sequence)
            
            if total_impact > 0.5:
                return 'explosão'
            elif total_impact < -0.5:
                return 'queda'
            else:
                return 'neutro'
                
        except Exception as e:
            print(f"Erro ao determinar resultado da sequência: {e}")
            return 'neutro'
    
    def _is_significant_pattern(self, pattern):
        """Verifica se um padrão é significativo"""
        try:
            # Verifica duração
            if pattern['duração'] > 900:  # 15 minutos
                return False
                
            # Verifica impacto total
            total_impact = sum(pattern['impactos'])
            if abs(total_impact) < 0.5:
                return False
                
            return True
            
        except Exception as e:
            print(f"Erro ao verificar significância do padrão: {e}")
            return False
    
    def _group_similar_patterns(self, patterns):
        """Agrupa padrões similares"""
        grouped = []
        
        try:
            for pattern in patterns:
                found_group = False
                for group in grouped:
                    if self._is_similar_sequence(group['eventos'], pattern['eventos']):
                        # Atualiza estatísticas do grupo
                        group['ocorrências'] = group.get('ocorrências', 1) + 1
                        group['impacto_médio'] = (
                            group.get('impacto_médio', sum(group['impactos'])) +
                            sum(pattern['impactos'])
                        ) / 2
                        found_group = True
                        break
                        
                if not found_group:
                    pattern['ocorrências'] = 1
                    pattern['impacto_médio'] = sum(pattern['impactos'])
                    grouped.append(pattern)
                    
        except Exception as e:
            print(f"Erro ao agrupar padrões similares: {e}")
            
        return grouped
    
    def _calculate_pattern_reliability(self, pattern):
        """Calcula a confiabilidade de um padrão"""
        try:
            # Fatores de confiabilidade
            occurrence_factor = min(pattern.get('ocorrências', 1) / 5, 1)  # Máximo após 5 ocorrências
            impact_factor = min(abs(pattern.get('impacto_médio', 0)), 1)
            
            return (occurrence_factor * 0.6 + impact_factor * 0.4)
            
        except Exception as e:
            print(f"Erro ao calcular confiabilidade do padrão: {e}")
            return 0.5
    
    def _calculate_sequence_trend(self, sequence):
        """Calcula a tendência de uma sequência"""
        try:
            impacts = [obs['impacto_emocional'] for obs in sequence]
            
            if len(impacts) < 2:
                return 'estável'
                
            # Calcula diferenças entre impactos consecutivos
            differences = [impacts[i+1] - impacts[i] for i in range(len(impacts)-1)]
            avg_diff = sum(differences) / len(differences)
            
            if avg_diff > 0.1:
                return 'ascendente'
            elif avg_diff < -0.1:
                return 'descendente'
            else:
                return 'estável'
                
        except Exception as e:
            print(f"Erro ao calcular tendência da sequência: {e}")
            return 'estável'
    
    def _calculate_sequence_intensity(self, sequence):
        """Calcula a intensidade de uma sequência"""
        try:
            impacts = [abs(obs['impacto_emocional']) for obs in sequence]
            return sum(impacts) / len(impacts)
            
        except Exception as e:
            print(f"Erro ao calcular intensidade da sequência: {e}")
            return 0.0
    
    def _is_similar_sequence(self, seq1, seq2):
        """Verifica se duas sequências são similares"""
        try:
            if len(seq1) != len(seq2):
                return False
                
            # Conta eventos similares
            similar_count = sum(1 for e1, e2 in zip(seq1, seq2) if e1 == e2)
            
            # Considera similar se pelo menos 2 eventos são iguais
            return similar_count >= 2
            
        except Exception as e:
            print(f"Erro ao comparar sequências: {e}")
            return False
    
    def _calculate_expected_intensity(self, similar_patterns, active_triggers):
        """Calcula a intensidade esperada baseada em padrões similares e gatilhos ativos"""
        try:
            if not similar_patterns:
                return 0.5
                
            # Média de impactos dos padrões similares
            base_intensity = sum(p.get('impacto_médio', 0) for p in similar_patterns) / len(similar_patterns)
            
            # Ajusta baseado nos gatilhos ativos
            trigger_modifier = 1.0
            for trigger in active_triggers:
                if trigger['natureza'] == 'positivo':
                    trigger_modifier *= (1 + trigger['força'] * 0.2)
                else:
                    trigger_modifier *= (1 - trigger['força'] * 0.2)
                    
            return base_intensity * trigger_modifier
            
        except Exception as e:
            print(f"Erro ao calcular intensidade esperada: {e}")
            return 0.5

    def analyze_event_correlations(self, player_name, time_window_minutes=30):
        """Analisa correlações entre eventos e seu impacto combinado no desempenho"""
        correlation_analysis = {
            'correlações_identificadas': [],
            'fatores_multiplicadores': {},
            'confiança_geral': 0.0,
            'recomendações': []
        }
        
        try:
            # Obtém observações recentes
            recent_obs = self._get_recent_observations(player_name, time_window_minutes)
            
            if len(recent_obs) < 3:
                return correlation_analysis
                
            # Identifica correlações
            correlations = self._identify_event_correlations(recent_obs)
            correlation_analysis['correlações_identificadas'] = correlations
            
            # Calcula multiplicadores
            multipliers = self._calculate_correlation_multipliers(correlations)
            correlation_analysis['fatores_multiplicadores'] = multipliers
            
            # Calcula confiança geral
            confidence = self._calculate_correlation_confidence(correlations)
            correlation_analysis['confiança_geral'] = confidence
            
            # Gera recomendações
            recommendations = self._generate_correlation_recommendations(
                correlations,
                multipliers,
                confidence
            )
            correlation_analysis['recomendações'] = recommendations
            
        except Exception as e:
            print(f"Erro ao analisar correlações de eventos: {e}")
            
        return correlation_analysis
    
    def _identify_event_correlations(self, observations):
        """Identifica correlações entre eventos"""
        correlations = []
        
        try:
            # Analisa pares de eventos
            for i in range(len(observations) - 1):
                for j in range(i + 1, min(i + 3, len(observations))):
                    event1 = observations[i]
                    event2 = observations[j]
                    
                    correlation = {
                        'eventos': [event1['tipo'], event2['tipo']],
                        'impacto_combinado': self._calculate_combined_impact(event1, event2),
                        'tempo_entre': (event2['timestamp'] - event1['timestamp']).total_seconds(),
                        'força_correlação': self._calculate_correlation_strength(event1, event2)
                    }
                    
                    if correlation['força_correlação'] > 0.3:  # Correlação significativa
                        correlations.append(correlation)
                        
            # Ordena por força de correlação
            correlations.sort(key=lambda x: x['força_correlação'], reverse=True)
            
        except Exception as e:
            print(f"Erro ao identificar correlações: {e}")
            
        return correlations
    
    def _calculate_combined_impact(self, event1, event2):
        """Calcula o impacto combinado de dois eventos"""
        try:
            base_impact = event1['impacto_emocional'] + event2['impacto_emocional']
            
            # Fatores de amplificação
            time_factor = 1.0
            time_diff = (event2['timestamp'] - event1['timestamp']).total_seconds()
            
            if time_diff <= 60:  # Eventos em 1 minuto
                time_factor = 1.5
            elif time_diff <= 180:  # Eventos em 3 minutos
                time_factor = 1.2
                
            # Verifica sinergia de eventos
            if self._are_events_synergistic(event1['tipo'], event2['tipo']):
                base_impact *= 1.3
                
            return base_impact * time_factor
            
        except Exception as e:
            print(f"Erro ao calcular impacto combinado: {e}")
            return 0.0
    
    def _calculate_correlation_strength(self, event1, event2):
        """Calcula a força da correlação entre dois eventos"""
        try:
            # Fatores base
            impact_correlation = abs(event1['impacto_emocional'] * event2['impacto_emocional'])
            time_proximity = 1.0 - min((event2['timestamp'] - event1['timestamp']).total_seconds() / 300, 1)
            
            # Fatores de tipo
            type_synergy = 1.0
            if self._are_events_synergistic(event1['tipo'], event2['tipo']):
                type_synergy = 1.5
            elif self._are_events_antagonistic(event1['tipo'], event2['tipo']):
                type_synergy = 0.5
                
            return (impact_correlation * 0.4 + time_proximity * 0.3 + type_synergy * 0.3)
            
        except Exception as e:
            print(f"Erro ao calcular força da correlação: {e}")
            return 0.0
    
    def _are_events_synergistic(self, type1, type2):
        """Verifica se dois tipos de eventos são sinérgicos"""
        synergistic_pairs = {
            ('jogada_decisiva', 'celebração'),
            ('erro_crucial', 'frustração'),
            ('clutch_moment', 'foco_intenso'),
            ('motivação_time', 'gestos_confiança'),
            ('fadiga_visível', 'erro_crucial'),
            ('pressão_placar', 'ansiedade_visível')
        }
        
        return (type1, type2) in synergistic_pairs or (type2, type1) in synergistic_pairs
    
    def _are_events_antagonistic(self, type1, type2):
        """Verifica se dois tipos de eventos são antagonísticos"""
        antagonistic_pairs = {
            ('celebração', 'frustração'),
            ('foco_intenso', 'distração'),
            ('gestos_confiança', 'hesitação'),
            ('motivação_time', 'isolamento_time'),
            ('jogada_decisiva', 'erro_crucial')
        }
        
        return (type1, type2) in antagonistic_pairs or (type2, type1) in antagonistic_pairs
    
    def _calculate_correlation_multipliers(self, correlations):
        """Calcula multiplicadores baseados nas correlações"""
        multipliers = {
            'impacto_emocional': 1.0,
            'confiança_previsão': 1.0,
            'janela_tempo': 1.0
        }
        
        try:
            if not correlations:
                return multipliers
                
            # Média das forças de correlação
            avg_strength = sum(c['força_correlação'] for c in correlations) / len(correlations)
            
            # Ajusta multiplicadores
            multipliers['impacto_emocional'] = 1 + (avg_strength * 0.5)
            multipliers['confiança_previsão'] = 1 + (avg_strength * 0.3)
            
            # Ajusta janela de tempo baseado na proximidade dos eventos
            avg_time = sum(c['tempo_entre'] for c in correlations) / len(correlations)
            if avg_time < 120:  # Eventos muito próximos
                multipliers['janela_tempo'] = 0.7  # Janela menor
            elif avg_time > 600:  # Eventos distantes
                multipliers['janela_tempo'] = 1.3  # Janela maior
                
        except Exception as e:
            print(f"Erro ao calcular multiplicadores: {e}")
            
        return multipliers
    
    def _calculate_correlation_confidence(self, correlations):
        """Calcula a confiança geral baseada nas correlações identificadas"""
        try:
            if not correlations:
                return 0.5
                
            # Fatores de confiança
            correlation_count = len(correlations)
            avg_strength = sum(c['força_correlação'] for c in correlations) / correlation_count
            
            # Penaliza se houver poucos dados
            if correlation_count < 3:
                avg_strength *= 0.7
                
            # Ajusta baseado na consistência das correlações
            strength_variance = np.var([c['força_correlação'] for c in correlations])
            consistency_factor = 1 - min(strength_variance, 0.5)
            
            return min(avg_strength * consistency_factor, 1.0)
            
        except Exception as e:
            print(f"Erro ao calcular confiança das correlações: {e}")
            return 0.5
    
    def _generate_correlation_recommendations(self, correlations, multipliers, confidence):
        """Gera recomendações baseadas nas correlações identificadas"""
        recommendations = []
        
        try:
            if not correlations:
                return recommendations
                
            # Analisa correlações mais fortes
            strong_correlations = [c for c in correlations if c['força_correlação'] > 0.6]
            
            for correlation in strong_correlations:
                if correlation['impacto_combinado'] > 0:
                    recommendations.append({
                        'tipo': 'oportunidade',
                        'descrição': f"Padrão positivo identificado: {correlation['eventos'][0]} seguido de {correlation['eventos'][1]}",
                        'confiança': correlation['força_correlação'],
                        'janela_tempo': f"{int(correlation['tempo_entre'])} segundos"
                    })
                else:
                    recommendations.append({
                        'tipo': 'alerta',
                        'descrição': f"Padrão negativo identificado: {correlation['eventos'][0]} seguido de {correlation['eventos'][1]}",
                        'confiança': correlation['força_correlação'],
                        'janela_tempo': f"{int(correlation['tempo_entre'])} segundos"
                    })
                    
            # Recomendações gerais
            if confidence > 0.7:
                recommendations.append({
                    'tipo': 'estratégia',
                    'descrição': "Alta confiabilidade nas correlações - considerar ajustes mais agressivos",
                    'confiança': confidence
                })
            elif confidence < 0.4:
                recommendations.append({
                    'tipo': 'cautela',
                    'descrição': "Baixa confiabilidade nas correlações - manter abordagem conservadora",
                    'confiança': confidence
                })
                
        except Exception as e:
            print(f"Erro ao gerar recomendações: {e}")
            
        return recommendations 

    def register_emotion(self, emotion):
        """Registra uma emoção direta do jogador"""
        timestamp = datetime.now()
        return self.register_observation(
            player_name='current_player',  # Assumindo jogador atual
            timestamp=timestamp,
            observation_type=emotion,
            details=f'Emoção registrada diretamente pelo jogador: {emotion}'
        )

    def add_note(self, note):
        """Adiciona uma nota de observação"""
        timestamp = datetime.now()
        return self.register_observation(
            player_name='current_player',  # Assumindo jogador atual
            timestamp=timestamp,
            observation_type='nota_manual',
            details=note
        )

    def get_current_emotional_state(self):
        """Retorna o estado emocional atual do jogador"""
        return self.get_player_emotional_state('current_player')  # Assumindo jogador atual

    def get_recent_history(self, time_window_minutes=30):
        """Retorna o histórico recente de comportamento"""
        observations = self._get_recent_observations('current_player', time_window_minutes)
        return [{
            'timestamp': obs['timestamp'].isoformat(),
            'type': obs['tipo'],
            'description': obs['detalhes']
        } for obs in observations] 