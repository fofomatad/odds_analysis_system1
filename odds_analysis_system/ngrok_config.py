from pyngrok import ngrok
import os

# Configure seu token do ngrok aqui
NGROK_AUTH_TOKEN = "2sDKUh1cEpkcuTva7wm3D8EOjGe_6ej9hjkHhbQsjY6kSGQvT"

def setup_ngrok():
    try:
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
        # Configurar túnel HTTP com região específica
        tunnel = ngrok.connect(5000, "http", region="sa")  # Região América do Sul
        return tunnel.public_url
    except Exception as e:
        print(f"Erro ao configurar ngrok: {e}")
        return None 