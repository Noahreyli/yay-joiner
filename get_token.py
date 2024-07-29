import requests

def read_account_info(filepath):
    accounts = []
    with open(filepath, 'r') as file:
        for line in file:
            if ':' in line:  
                email, password = line.strip().split(':')
                accounts.append((email, password))
    return accounts

def write_access_token(filepath, token):
    with open(filepath, 'a') as file:  
        file.write(token + '\n')

def login_and_extract_token(accounts):
    url = "https://api.yay.space/v2/users/login_with_email"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
        "Content-Type": "application/json;charset=utf-8",
        "Agent": "YayWeb 3.33.0",
        "X-Device-Info": "Yay 3.33.0 Web (Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0)",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site"
    }
    
    for email, password in accounts:
        payload = {
            "email": email,
            "password": password,
            "api_key": "e9f1ae4c4470f29a92c0168dc42b13637cc332692103f23e626bc2b016f66603",
            "uuid": "8fb77380-12a1-4f93-85e9-a52653354011"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            data = response.json()
            if 'access_token' in data:
                write_access_token('token.txt', data['access_token'])
            else:
                print(f"No access token found for {email}")
        else:
            print(f"Failed to login for {email}")

def main():
    accounts = read_account_info('account_info.txt')
    login_and_extract_token(accounts)

if __name__ == "__main__":
    main()
