from secrets import choice
import requests
import sys
import os
import time

URLS = {
    'prod': 'https://a2a-apigee-prod-prod.apigee.net/mama/api/v1/anagrafiche/upload',
    'preprod': 'https://a2a-apigee-noprod-preprod.apigee.net/mama/api/v1/anagrafiche/upload',
}

HEADERS = {
    'preprod': {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Bearer ',
        'sec-ch-ua-mobile': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://portale.prep.a2aenergia.eu',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://portale.prep.a2aenergia.eu/',
        'Accept-Language': 'en-US,en;q=0.9',
    },
    'prod': {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Bearer ',
        'sec-ch-ua-mobile': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://portale.a2aenergia.eu',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://portale.a2aenergia.eu',
        'Accept-Language': 'en-US,en;q=0.9',
    }
}

PAYLOADS = {
    'TIS': {
        'cod_distributore': 'DUMMY',
        'cod_company': 'AEN',
        'cod_mercato': 'null',
        'commodity': 'ELE',
        'cod_prestazione': 'TIS',
        'cod_flusso': 'RUC',
        'cod_contr_disp': 'null'
    },
    'SMG1': {
        'cod_distributore': 'DUMMY',
        'cod_company': 'AEN',
        'cod_mercato': 'null',
        'commodity': 'GAS',
        'cod_prestazione': 'SMG1',
        'cod_flusso': 'ANAG',
        'cod_contr_disp': 'null'
    },
    'FTR': {
        'cod_distributore': 'DUMMY',
        'cod_company': 'AEN',
        'cod_mercato': 'null',
        'commodity': 'ELE',
        'cod_prestazione': 'FTR',
        'cod_flusso': 'FTR',
        'cod_contr_disp': 'null'
    },
    'RCU': {
        'cod_distributore': 'DUMMY',
        'cod_company': 'AEN',
        'cod_mercato': 'null',
        'commodity': 'ELE',
        'cod_prestazione': 'RCU',
        'cod_flusso': 'CC',
        'cod_contr_disp': 'null'
    }
}

if __name__ == '__main__':
    """
        Arg[1] = Nome della cartella da caricare (non serve il ".csv")
        Arg[2] = Ambiente in cui caricare (preprod/prod)
        Arg[3] = TIS/SMG1/FTR/RCU
        Arg[4] = Token
    """
    # TODO eventuale controllo sugli argomenti

    ambiente_choiche = {
        1: 'prod',
        2: 'preprod',
    }
    flusso_choiche = {
        1: 'TIS',
        2: 'SMG1',
        3: 'FTR',
        4: 'RCU',
    }


    folder = input("Inserisci il nome della cartella da caricare: ")
    choice = int(input("Ambiente \n(1)prod  \n(2)preprod\n->"))
    upload_url = URLS[ambiente_choiche[choice]]
    header = HEADERS[ambiente_choiche[choice]]
    choice = int(input("Flusso \n(1)TIS  \n(2)SMG1  \n(3)FTR  \n(4)RCU  \n->"))
    flusso = flusso_choiche[choice]
    token = input("Token: ")
    header['Authorization'] += token
    session = requests.session()

    current = os.getcwd()
    target_path = f"{current}\\{folder}"

    payload = PAYLOADS[flusso]

    c = 1
    tot_file = len(os.listdir(f'.\\{folder}'))
    for csv in os.listdir(f'.\{folder}'):
        payload['filename'] = csv
        doc = {'file': (csv, open(f"{target_path}\\{csv}", 'rb'), "application/octet-stream")}
        res = session.post(upload_url, data=payload, headers=header, files=doc)
        print(f"{c}/{tot_file}")
        print(res.status_code)
        print(res.text)
        c += 1

        if flusso == 'FTR':
            time.sleep(90)
        else:
            time.sleep(60)