import re
import subprocess


def get_info():
    info = {}
    text = subprocess.check_output(['netsh', 'wlan', 'show', 'profile'])
    text = text.decode().replace('\r', '').split("\n")
    for line in text:
        try:
            ap = re.search('(Profile\\s*:)(\\s[A-za-z0-9-].*)?', line)
            accp = ap.group(2)
            new_text = subprocess.check_output(f'netsh wlan show profile {accp} key=clear')
            new_text = new_text.decode()
            pw = re.search('(Content\\s*:\\s*)(.*)?', new_text)
            pwd = pw.group(2)
            info[accp] = pwd
        except Exception:
            continue
    return info


def print_results(info):
    print('Access Points\t\t\t\tPassword\n====================================================')
    for key,value in info.items():
        if len(key) >= 16:
            print(f'{key}\t|\t{value}')
        elif len(key) <= 6:
            print(f'{key}\t\t\t|\t{value}')
        else:
            print(f'{key}\t\t|\t{value}')


info = get_info()
print_results(info)
