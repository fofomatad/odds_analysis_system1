from flask import Flask
from waitress import serve
import config
from app import app

if __name__ == '__main__':
    print(f"\nServidor iniciado em: http://{config.HOST}:{config.PORT}")
    print("Para acessar externamente, use seu IP público e a porta configurada")
    print("\nPressione CTRL+C para parar o servidor\n")
    
    # Usar waitress como servidor WSGI
    serve(app, host=config.HOST, port=config.PORT) 