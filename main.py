import optparse
import socket
import sys
import time
import requests
from bs4 import BeautifulSoup


def auth(token):
    headers = {
        'Host': 'pypi.org',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://pypi.org/account/login/',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Content-Length': '97',
        'Origin': 'https://pypi.org',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        # Requests sorts cookies= alphabetically
    }

    time.sleep(1)
    print(bColors.OKBLUE + '[+] Checking if host ' + host + ' is Up...' + bColors.ENDC)
    host_up = x.get(host)
    try:
        if host_up.status_code == 200:
            print(bColors.OKGREEN + '[+] Host Up! ...' + bColors.ENDC)
    except:
        print(bColors.FAIL + '[+] This host seems to be down :( ')
        sys.exit(0)

    print(bColors.OKBLUE + '[+] Trying to authenticate with credentials ' + str(user) + ':' + str(
        password) + '' + bColors.ENDC)
    time.sleep(1)

    data = 'csrf_token=' + token + '&username=' + options.user + '&password=' + options.passw

    response = requests.post(login, data=data, cookies=cookies, headers=headers)

    if response.status_code == 200 and "/manage/project/" not in response:
        print(bColors.OKGREEN + '[+] Login success!' + bColors.ENDC)
        time.sleep(1)
    else:
        print(bColors.FAIL + '[x] Login failed :(' + bColors.ENDC)
        sys.exit(0)

    soup = BeautifulSoup(response.text, features="lxml")
    for a in soup.find_all("h3", {"class": "package-snippet__title"}):
        project = a.next.replace("\n", "").replace(" ", "")
        project_urls.append(project)


def getAuthor():
    print(bColors.OKBLUE + "[+] Get Author Names of the Projects" + bColors.ENDC)

    for p in project_urls:
        url = project_page + p
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="lxml")
        for a in soup.find_all('a', href=True):
            mailto = a['href']
            if "mailto:" in mailto:
                if author:
                    for t in author:
                        if mailto == t:
                            pass
                else:
                    author.append(mailto)


def checkDomain():
    print(bColors.OKBLUE + "[+] Checking Domains" + bColors.ENDC)

    for d in author:
        d = d.split("@")[1]

        try:
            addr = socket.gethostbyname(d)
            print(bColors.OKGREEN + "[+] Not Vulnerable {}".format(d))

        except:
            print(bColors.WARNING + "[+] {} your account is vulnerable".format(d))


def checkAccount(token):
    auth(token)
    getAuthor()
    checkDomain()


class bColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


parser = optparse.OptionParser()
parser.add_option('-u', '--user', action="store", dest="user", help="User credential to login")
parser.add_option('-p', '--passw', action="store", dest="passw", help="Pass credential to login")

options, args = parser.parse_args()
if not options.passw or not options.user:
    print(bColors.WARNING + '[+] Check Vulnerable Account on PYPI' + bColors.ENDC)
    print(
        bColors.WARNING + "[+] Example usage: main.py -u test -p admin " + bColors.ENDC)
    exit()

host = "https://pypi.org"
login = host + '/account/login/'
project_page = host + '/project/'
project_urls = []
author = []

user = options.user
password = options.passw

request = requests.Session()

print(bColors.OKBLUE + "[+] Retrieving CSRF token to submit the login form")
print(bColors.OKBLUE + "[+] URL : %s" % login)

time.sleep(1)
page = request.get(login)
cookies = page.cookies
html_content = page.text
soup = BeautifulSoup(html_content, features="lxml")

token = soup.find('input', {'name': 'csrf_token'})['value']

x = requests.Session()

checkAccount(token=token)
