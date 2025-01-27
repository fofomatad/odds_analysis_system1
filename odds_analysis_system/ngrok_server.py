from pyngrok import ngrok
from app import app
import config
from ngrok_config import setup_ngrok
import sys

def start_server():
    try:
        # Configurar túnel ngrok
        public_url = setup_ngrok()
        if not public_url:
            print("Erro ao criar túnel ngrok. Verifique seu token e conexão.")
            sys.exit(1)
            
        print(f'\n * Servidor público disponível em: {public_url}\n')
        
        # Iniciar servidor
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG
        )
    except Exception as e:
        print(f"Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    start_server() 