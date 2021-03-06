import requests
import configparser
import json
from time import sleep
# импортируем библиотеки ^
config = configparser.ConfigParser()  # создаём объекта парсера
config.read("near_alarm.ini") 
TELEGRAM_URL = 'https://api.telegram.org/bot%s/sendMessage?' \
               'text=%s&chat_id=%s&parse_mode=markdown&disable_web_page_preview=True'

TELEGRAM_API = config['T_BOT']['TELEGRAM_URL']
chat_id = config['T_BOT']['CHAT_ID']
def send_message(text, chat_id):
    send_url = TELEGRAM_URL % (TELEGRAM_API, text, chat_id)
    print(send_url)
    try:
        requests.get(send_url)
    except Exception as ex:
        print(ex)
json={
  "jsonrpc": "2.0",
  "id": "dontcare",
  "method": "validators",
  "params":[None]         
}
eponch = []
prev = 24205843
call_me = 0
while True:
    try:
        r = requests.post('https://rpc.mainnet.near.org', json=json)
        #r.status_code
        t =r.json()
        for i in t['result']['current_validators']:
            if i['account_id'] == config['T_BOT']['ACCOUNT_ID']:
                print(i['num_produced_blocks'],i['num_expected_blocks'])
                num_produced = i['num_produced_blocks']
                num_expected = i['num_expected_blocks']
                diff =num_expected - num_produced
                if diff>=int(config['T_BOT']['THRESHOLD']) and call_me<=2:
                    print('ALARM')
                    send_message('*[ALARM]*\n\ncheck your node\r\nProdused block:%s\r\nExpected block:%s' %(num_produced, num_expected), chat_id)
                    requests.post(config['T_BOT']['CALL_API'])
                    call_me +=1
                current=t['result']['epoch_start_height'] 
                print('Eponch: %s\r\nProduced:%s\r\nExpected:%s' %(current, num_produced, num_expected))
                if diff and call_me>2:
                    send_message('*[ALARM]*\n\ncheck your node\r\nProdused block:%s\r\nExpected block:%s' %(num_produced, num_expected), chat_id)
                    print('Check your node')
                    sleep(360)
        if current != prev:
            prev=current
            send_message('New Eponch No: %s' %current, chat_id)
            call_me = 0
            sleep(60)
            continue
        sleep(180)
    except Exception as ex:
        print(ex)
        send_message('Something went wrong:%s' % ex) 
        sleep(180)
        continue
