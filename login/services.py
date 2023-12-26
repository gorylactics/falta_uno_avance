import requests


def generar_request_serv(url , params={}):
    respuesta = requests.get(url , params=params)
    if respuesta.status_code == 200:
        return respuesta.json()

def get_users(params={}):
    respuesta = generar_request_serv('https://reqres.in/api/users' , params)
    if respuesta:
        return respuesta.get('data')
    return ''

