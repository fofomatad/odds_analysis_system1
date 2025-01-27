import requests

def test_site():
    url = "https://nba-analysis-2024.pythonanywhere.com"
    
    print(f"Testando {url}...")
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    
    print("\nTestando /health...")
    response = requests.get(f"{url}/health")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")

if __name__ == "__main__":
    test_site() 