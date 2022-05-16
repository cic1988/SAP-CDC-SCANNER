import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

apiKey = os.getenv('APIKEY')
secretKey = os.getenv('SECRETKEY')
userKey = os.getenv('USERKEY')

url = 'https://accounts.eu1.gigya.com'

headers = {
    'content-type': 'application/x-www-form-urlencoded',
}

## error handling
def error_handling(err):
    if 'errorCode' in err and err["errorCode"] != 0:
        print(f'Got error: {err["errorCode"]} {err["errorDetails"]}')
        return False

    return True

def sendRequest(url, method, headers, data, filename):
    try:
        response = requests.post(url + '/' + method, headers=headers, data=data)

        if response.status_code == 200:
            if error_handling(response.json()):
                with open(f"data/{filename}", "w") as f:
                    json.dump(response.json(), f)

    except requests.exceptions.RequestException as e: 
        print('Got error: ' + e)
        raise SystemExit(e)

## Accounts
def account():
    # TODO: pagination not implemented, limit to max. 5000, see:
    # https://help.sap.com/docs/SAP_CUSTOMER_DATA_CLOUD/8b8d6fffe113457094a17701f63e3d6a/b32ce0918af44c3ebd7e96650fa6cc1d.html?locale=en-US
    number = os.getenv('ACCOUNT_NUMBER')
    method = 'accounts.search'
    query = f'SELECT * FROM accounts LIMIT {number}'

    data = f'apiKey={apiKey}&secret={secretKey}&userKey={userKey}&query={query}'
    sendRequest(url, method, headers, data, 'accounts.json')

if __name__ == "__main__":
    account()
