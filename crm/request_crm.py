from requests import request
from datetime import datetime
from time import sleep

from dotenv import load_dotenv
import os

load_dotenv()

token_estrutura = os.getenv('token_estrutura')
token_usuario = os.getenv('token_usuario')
painel_id = os.getenv('painel_id')

hora_request = 10
minuto_request = 56

def request_crm(inicio_carga, fim_carga):
    url = 'https://app.neosales.com.br/producao-painel-integration-v2'

    payload = f"""{{
        \n\"tokenEstrutura\":\"{token_estrutura}\",
        \n\"tokenUsuario\":\"{token_usuario}\",
        \n\"dataHoraInicioCarga\":\"2024-01-30 09:00:00\",
        \n\"dataHoraFimCarga\":\"2024-01-30 10:00:00\",
        \n\"painelId\":\"{painel_id}\",
        \n\"outputFormat\":\"csv\"\n
    }}"""

    print('sekiro online')


def load_crm_requests():
    while True:
        now = datetime.now()

        if now.hour == hora_request and now.minute == minuto_request:
            inicio_carga = f'{now.year}-{now.month}-{now.day} 00:00:00'
            fim_carga = f'{now.year}-{now.month}-{now.day} 23:59:00'

            request_crm(inicio_carga, fim_carga)

            sleep(60)

        else:
            pass
