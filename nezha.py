import requests
import csv
import os
from dotenv import load_dotenv

def login_and_get_jwt(api_url, username, password):
    login_url = api_url.rstrip('/') + '/api/v1/login'
    payload = {"username": username, "password": password}
    headers = {'content-type': 'application/json', 'accept': '*/*'}
    resp = requests.post(login_url, json=payload, headers=headers)
    if resp.status_code == 200 and 'nz-jwt' in resp.cookies:
        return resp.cookies['nz-jwt']
    else:
        raise Exception(f"登录失败: {resp.status_code} {resp.text}")

def fetch_server_info(api_url, jwt):
    server_url = api_url.rstrip('/') + '/api/v1/server'
    headers = {'accept': '*/*', 'content-type': 'application/json'}
    cookies = {'nz-jwt': jwt}
    resp = requests.get(server_url, headers=headers, cookies=cookies)
    if resp.status_code == 200:
        data = resp.json()
        servers = []
        for item in data.get('data', []):
            ip = item.get('geoip', {}).get('ip', {}).get('ipv4_addr', '')
            name = item.get('name', '')
            desc = item.get('host', {}).get('platform', '') + ' ' + item.get('host', {}).get('platform_version', '')
            servers.append([ip, name, desc])
        return servers
    else:
        raise Exception(f"获取服务器失败: {resp.status_code} {resp.text}")

def save_servers_to_csv(servers, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ip', 'name', 'desc'])
        writer.writerows(servers)

def get_ip_list():
    # 直接读取 server.csv
    csv_path = os.path.join(os.path.dirname(__file__), 'server.csv')
    ip_list = []
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ip = row.get('ip')
                if ip:
                    ip_list.append(ip)
    return ip_list

def main():
    load_dotenv()
    api_url = os.getenv('NEZHA_API_URL')
    username = os.getenv('NEZHA_USER')
    password = os.getenv('NEZHA_PASSWORD')
    if not api_url or not username or not password:
        print("请在 .env 文件中配置 NEZHA_API_URL, NEZHA_USER, NEZHA_PASSWORD")
        return
    csv_path = os.path.join(os.path.dirname(__file__), 'server.csv')
    jwt = login_and_get_jwt(api_url, username, password)
    servers = fetch_server_info(api_url, jwt)
    save_servers_to_csv(servers, csv_path)
    print(f"已保存 {len(servers)} 台服务器信息到 {csv_path}")

if __name__ == '__main__':
    main()
