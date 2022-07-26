import requests, time, json, configparser, smtplib, logging, datetime

config = configparser.ConfigParser()
config.read('cfauth.ini')

zone_id = config.get('tokens', 'zone_id')
bearer_token = config.get('tokens', 'bearer_token')
record_id = config.get('tokens', 'record_id')
logging.basicConfig(level=logging.INFO, filename='ipchanges.log', format='%(levelname)s :: %(message)s')

headers = {
    "Authorization": f"Bearer {bearer_token}", 
    "content-type": "application/json"
    }

while True:
    a_record_url = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}", headers=headers)
    arecordjson = a_record_url.json()
    current_set_ip = arecordjson['result']['content']

    currentip = requests.get("https://ipv4.icanhazip.com/")

    ipcheck_status = currentip.status_code

    while ipcheck_status != 200:
        time.sleep(10)
        currentip = requests.get("https://ipv4.icanhazip.com/")
        ipcheck_status = currentip.status_code

    currentactualip = currentip.text.strip()

    while currentactualip == current_set_ip:
        time.sleep(60)
        currentip = requests.get("https://ipv4.icanhazip.com/")
        ipcheck_status = currentip.status_code

        while ipcheck_status != 200:
            time.sleep(10)
            currentip = requests.get("https://ipv4.icanhazip.com/")
            ipcheck_status = currentip.status_code

        currentactualip = currentip.text.strip()
        logging.info('ip server: {currentactualip}')
        logging.info('ip cloudflare: {current_set_ip}')
    else: 
        pass

    payload = {"content": currentactualip}

    requests.patch(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}", headers=headers, data=json.dumps(payload))
    
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    logging.info(f"{now} - IP change from {current_set_ip} to {currentactualip}")