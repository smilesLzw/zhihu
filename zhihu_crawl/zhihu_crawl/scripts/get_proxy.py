import requests


def get_proxy_from_api():
    api_url = 'http://webapi.http.zhimacangku.com/getip?num=20&type=2&pro=0&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=320000,330000'
    res = requests.get(api_url)
    json_data = res.json()
    proxy_array = json_data['data']
    return proxy_array