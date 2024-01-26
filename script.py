import random
from telethon import TelegramClient
# import telethon.sync

def gerar_numero_telefone():
    cod_int_br = "+55"
    ddd = "81"
    
    # Gera o dígito após o 9 (pode ser 7, 8 ou 9)
    primeiro_digito = "9" + str(random.randint(7, 9))
    
    # Gera os outros 8 dígitos aleatórios
    outros_digitos = "".join(str(random.randint(0, 9)) for _ in range(7))
    
    # Combina todos os elementos para formar o número de telefone
    numero_telefone = f"{cod_int_br}{ddd}{primeiro_digito}{outros_digitos}"
    
    return numero_telefone

api_id = 28151226
api_hash = '1bcb4f2ea915998c64f68ba474d7db9b'

with TelegramClient('teste', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('https://t.me/puxadasfreeproved', '/telefone ' + gerar_numero_telefone()))