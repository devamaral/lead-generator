import random
import asyncio
import re
from telethon import TelegramClient
from datetime import datetime
import threading
import keyboard

def generate_phone_number():
    country_code_br = "+55"
    area_code = "81"
    
    first_digit = "9" + str(random.randint(7, 9))
    
    other_digits = "".join(str(random.randint(0, 9)) for _ in range(7))
    
    phone_number = f"{country_code_br}{area_code}{first_digit}{other_digits}"
    
    return phone_number

api_id = 28151226
api_hash = '1bcb4f2ea915998c64f68ba474d7db9b'
client = TelegramClient('anon', api_id, api_hash)

phone_pattern = r'\*\*• TELEFONE:\*\* `(\d+)`'
name_pattern = r'\*\*• NOME:\*\* `([^`]+)`'
cpf_pattern = r'\*\*• CPF/CNPJ:\*\* `(\d+)`'
age_pattern = r'\*\*• IDADE:\*\* `(\d+)`'

blue = '\033[34m'
green = '\033[32m'
yellow = '\033[33m'


stop_program = False

def check_keyboard():
    global stop_program
    keyboard.wait('q')
    stop_program = True
    print('')
    print(yellow + 'Programa interrompido pelo usuário, por favor aguarde!')

async def main():
    group_link = 'https://t.me/sevenpuxada'

    print(blue + '==============================')
    print(blue + '      CAPTURA DE LEADS        ')
    print(blue + '==============================')
    print('')
    print(yellow + 'Pressione a tecla "Q" para parar o programa.')

    try:
        # Inicia a thread para verificar o teclado em segundo plano
        threading.Thread(target=check_keyboard).start()

        while not stop_program:
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            group_entity = await client.get_entity(group_link)

            await client.send_message(group_link, '/telefone ' + generate_phone_number())

            await asyncio.sleep(3)
            
            messages = await client.get_messages(group_entity, limit=2)

            for message in messages:
                if stop_program:
                    break

                if message.mentioned == True and '**𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔 𝗗𝗘 𝗧𝗘𝗟𝗘𝗙𝗢𝗡𝗘**' in message.text:
                    cpf = re.search(cpf_pattern, message.text).group(1)
                    
                    await client.send_message(group_link, '/cpf1 ' + cpf)

            await asyncio.sleep(3)

            messages_cpf = await client.get_messages(group_entity, limit=2)

            for message in messages_cpf:
                if stop_program:
                    break

                if '🔍 **𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔 𝗗𝗘 𝗖𝗣𝗙 🔍' in message.text:
                    name = re.search(name_pattern, message.text).group(1)
                    age = int(re.search(age_pattern, message.text).group(1))

                    if age >= 18 and age <= 40:
                        with open('leads.txt', 'a') as leads:
                            leads.write(f'\nTELEFONE: {generate_phone_number()}\nNOME: {name}\nCPF: {cpf}\nIDADE: {age}')
                            leads.write('\n=========================================================')
                        
                        print(green + f'{formatted_datetime} | LEAD ADICIONADO COM SUCESSO! ')

            await asyncio.sleep(8)

    except Exception as e:
        print(f'Erro ao buscar mensagem de grupo ou enviar mensagem {e}')

with client:
    client.loop.run_until_complete(main())
