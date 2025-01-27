import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://nba-holzhauer-analysis.pythonanywhere.com"

def test_endpoints():
    """Testa todos os endpoints principais"""
    endpoints = {
        '/': 'Dashboard principal',
        '/nba/dashboard': 'Dashboard NBA',
        '/system/health': 'Status do sistema',
        '/nba/games': 'Lista de jogos NBA',
    }
    
    for endpoint, description in endpoints.items():
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            status = "OK" if response.status_code == 200 else "FALHOU"
            logger.info(f"Testando {description}: {status} ({response.status_code})")
        except Exception as e:
            logger.error(f"Erro ao testar {description}: {e}")

def test_analysis():
    """Testa análise de um jogo"""
    try:
        # Primeiro obtém lista de jogos
        response = requests.get(f"{BASE_URL}/nba/games")
        if response.status_code == 200:
            games = response.json()
            if games:
                # Testa análise do primeiro jogo
                game_id = games[0]['id']
                analysis_response = requests.get(f"{BASE_URL}/nba/analyze/{game_id}")
                status = "OK" if analysis_response.status_code == 200 else "FALHOU"
                logger.info(f"Testando análise de jogo: {status}")
                if status == "OK":
                    logger.info("Conteúdo da análise:")
                    logger.info(analysis_response.json())
    except Exception as e:
        logger.error(f"Erro ao testar análise: {e}")

if __name__ == "__main__":
    logger.info("Iniciando testes do servidor...")
    
    # Espera o servidor iniciar
    time.sleep(2)
    
    # Testa endpoints
    test_endpoints()
    
    # Testa análise
    test_analysis()
    
    logger.info("Testes concluídos") 