import requests


access_token = 'PUSH ACCESS TOKEN INTO ENVIROMENT VARIABLES AND CALL IT HERE'
headers = dict(
        accept = 'application/json',
        Authorization = 'Bearer ' + access_token
    )

def genres(url):
    response = requests.get(url, headers=headers).json()
    genres = [v['name'] for v in response['genres']]
    return genres