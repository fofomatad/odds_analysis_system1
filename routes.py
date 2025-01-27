from flask import Blueprint, jsonify
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from models import db, Game, Player, Strategy, Result
from utils.analysis import calculate_ev, analyze_opportunity
from utils.stats import calculate_player_stats, get_game_stats
from config import ODDS_MOVEMENT_THRESHOLD, VOLATILITY_THRESHOLD, MIN_EV_THRESHOLD

# Criar Blueprint
api = Blueprint('api', __name__)

# Rotas para o Player Dashboard
@api.route('/api/player-stats')
def get_player_stats():
    players = Player.query.all()
    return jsonify([{
        'id': player.id,
        'name': player.name,
        'position': player.position,
        'stats': {
            'points': player.avg_points,
            'assists': player.avg_assists,
            'rebounds': player.avg_rebounds
        }
    } for player in players])

@api.route('/api/player-stats/<int:player_id>')
def get_player_details(player_id):
    player = Player.query.get_or_404(player_id)
    stats = calculate_player_stats(player)
    
    return jsonify({
        'performance_chart': {
            'data': [{
                'x': stats['dates'],
                'y': stats['points'],
                'type': 'scatter',
                'name': 'Pontos'
            }],
            'layout': {
                'title': 'Performance do Jogador'
            }
        },
        'consistency_chart': {
            'data': [{
                'values': stats['consistency'],
                'labels': ['Alta', 'Média', 'Baixa'],
                'type': 'pie'
            }],
            'layout': {
                'title': 'Consistência'
            }
        },
        'notes': stats['notes']
    })

@api.route('/api/player-analysis/overview')
def get_player_overview():
    players = Player.query.all()
    stats = pd.DataFrame([{
        'name': p.name,
        'points': p.avg_points,
        'efficiency': p.efficiency
    } for p in players])
    
    return jsonify({
        'chart': {
            'data': [{
                'x': stats['points'],
                'y': stats['efficiency'],
                'mode': 'markers',
                'type': 'scatter',
                'text': stats['name']
            }],
            'layout': {
                'title': 'Pontos vs Eficiência',
                'xaxis': {'title': 'Pontos'},
                'yaxis': {'title': 'Eficiência'}
            }
        }
    })

# Rotas para o NBA Dashboard
@api.route('/api/live-games')
def get_live_games():
    games = Game.query.filter_by(status='live').all()
    return jsonify([{
        'id': game.id,
        'team1': {
            'name': game.team1_name,
            'score': game.team1_score,
            'logo': game.team1_logo
        },
        'team2': {
            'name': game.team2_name,
            'score': game.team2_score,
            'logo': game.team2_logo
        },
        'quarter': game.current_quarter,
        'time': game.current_time,
        'ev': calculate_ev(game)
    } for game in games])

@api.route('/api/nba-games')
def get_nba_stats():
    games = Game.query.all()
    stats = get_game_stats(games)
    
    return jsonify({
        'points_distribution': {
            'data': [{
                'x': stats['total_points'],
                'type': 'histogram',
                'nbinsx': 20
            }],
            'layout': {
                'title': 'Distribuição de Pontos'
            }
        },
        'ev_trends': {
            'data': [{
                'x': stats['dates'],
                'y': stats['ev_values'],
                'type': 'scatter'
            }],
            'layout': {
                'title': 'Tendências de EV'
            }
        }
    })

@api.route('/api/upcoming-games')
def get_upcoming_games():
    future = datetime.now() + timedelta(days=7)
    games = Game.query.filter(
        Game.date <= future,
        Game.status == 'scheduled'
    ).all()
    
    return jsonify([{
        'id': game.id,
        'datetime': game.date.strftime('%Y-%m-%d %H:%M'),
        'team1': {
            'name': game.team1_name,
            'logo': game.team1_logo
        },
        'team2': {
            'name': game.team2_name,
            'logo': game.team2_logo
        },
        'odds': game.odds,
        'predicted_ev': calculate_ev(game),
        'confidence': game.confidence
    } for game in games])

# Rotas para o Holzhauer Dashboard
@api.route('/api/system-stats')
def get_system_stats():
    results = Result.query.all()
    strategies = Strategy.query.filter_by(status='active').all()
    
    success_rate = len([r for r in results if r.profit > 0]) / len(results) * 100
    avg_ev = np.mean([r.predicted_ev for r in results])
    total_profit = sum([r.profit for r in results])
    
    return jsonify({
        'success_rate': round(success_rate, 2),
        'avg_ev': round(avg_ev, 2),
        'total_profit': round(total_profit, 2),
        'active_strategies': len(strategies)
    })

@api.route('/api/value-props/overall')
def get_value_props():
    results = Result.query.all()
    df = pd.DataFrame([{
        'date': r.date,
        'profit': r.profit,
        'ev': r.predicted_ev
    } for r in results])
    
    return jsonify({
        'performance_chart': {
            'data': [{
                'x': df['date'],
                'y': df['profit'].cumsum(),
                'type': 'scatter',
                'name': 'Lucro Acumulado'
            }],
            'layout': {
                'title': 'Performance da Estratégia'
            }
        },
        'distribution_chart': {
            'data': [{
                'x': df['profit'],
                'type': 'histogram',
                'nbinsx': 20
            }],
            'layout': {
                'title': 'Distribuição de Resultados'
            }
        }
    })

@api.route('/api/analyze-nba/active')
def get_active_strategies():
    strategies = Strategy.query.filter_by(status='active').all()
    return jsonify([{
        'id': strategy.id,
        'name': strategy.name,
        'type': strategy.type,
        'description': strategy.description,
        'confidence': strategy.confidence,
        'ev': strategy.expected_value
    } for strategy in strategies])

@api.route('/api/analyze-nba/history')
def get_strategy_history():
    results = Result.query.order_by(Result.date.desc()).limit(50).all()
    return jsonify([{
        'date': result.date.strftime('%Y-%m-%d'),
        'strategy': result.strategy_name,
        'predicted_ev': result.predicted_ev,
        'profit': result.profit,
        'roi': result.roi,
        'confidence': result.confidence
    } for result in results])

@api.route('/api/analyze-opportunity/<int:strategy_id>')
def analyze_strategy(strategy_id):
    strategy = Strategy.query.get_or_404(strategy_id)
    analysis = analyze_opportunity(strategy)
    
    return jsonify({
        'details_chart': analysis['chart'],
        'parameters': analysis['parameters'],
        'risk_level': analysis['risk'],
        'volatility': analysis['volatility'],
        'recommendation': analysis['recommendation']
    })

# Rotas para o Game Analysis
@api.route('/api/game-data/<int:game_id>')
def get_game_data(game_id):
    game = Game.query.get_or_404(game_id)
    stats = get_game_stats([game])
    
    return jsonify({
        'team1': {
            'name': game.team1_name,
            'logo': game.team1_logo,
            'score': game.team1_score,
            'stats': [
                {'label': 'FG%', 'value': f"{game.team1_fg_pct:.1f}%"},
                {'label': '3P%', 'value': f"{game.team1_3p_pct:.1f}%"},
                {'label': 'Rebotes', 'value': game.team1_rebounds},
                {'label': 'Assistências', 'value': game.team1_assists}
            ]
        },
        'team2': {
            'name': game.team2_name,
            'logo': game.team2_logo,
            'score': game.team2_score,
            'stats': [
                {'label': 'FG%', 'value': f"{game.team2_fg_pct:.1f}%"},
                {'label': '3P%', 'value': f"{game.team2_3p_pct:.1f}%"},
                {'label': 'Rebotes', 'value': game.team2_rebounds},
                {'label': 'Assistências', 'value': game.team2_assists}
            ]
        },
        'quarter': game.current_quarter,
        'time': game.current_time,
        'score_progression': {
            'data': [{
                'x': stats['times'],
                'y': stats['team1_scores'],
                'type': 'scatter',
                'name': game.team1_name
            }, {
                'x': stats['times'],
                'y': stats['team2_scores'],
                'type': 'scatter',
                'name': game.team2_name
            }],
            'layout': {
                'title': 'Progressão do Placar'
            }
        },
        'quarter_distribution': {
            'data': [{
                'values': stats['quarter_points'],
                'labels': ['1Q', '2Q', '3Q', '4Q'],
                'type': 'pie'
            }],
            'layout': {
                'title': 'Pontos por Quarter'
            }
        },
        'players': [{
            'name': p.name,
            'points': p.points,
            'assists': p.assists,
            'rebounds': p.rebounds,
            'efficiency': p.efficiency,
            'plusMinus': p.plus_minus,
            'trend': p.trend,
            'performance': p.performance
        } for p in game.players]
    })
