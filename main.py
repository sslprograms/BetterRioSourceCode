import threading, subprocess, string, random, time, os, sys, json, websocket, pymsgbox, ssl, base64, playsound, cloudscraper as requests

# ssl_opt = {"cert_reqs": ssl.CERT_REQUIRED, "ssl_version":ssl.PROTOCOL_TLSv1_2, 'check_host':True}
subprocess.getoutput('title Better Rio')

print('Server is online, this application is in testing!')

pymsgbox.alert('Please Confirm your Config file!', 'Config Confirm')
os.system('notepad.exe config.txt')


def encode_to_base64_pageId():
    def generate_data_with_timestamps():
        data_dict = {}
        current_timestamp = int(time.time())

        platforms = [
            "apn", "ttd", "pub", "rub", "tapa", "adx", "goo", "openx", 
            "ado", "cpnt", "index", "impr", "amp", "smart", "bees", 
            "unruly", "taboolasy", "bids", "utbolas", "sa", "bels", 
            "unrulys", "tab", "adobe", "sony", "cobranded"
        ]

        for platform in platforms:
            data_dict[platform] = current_timestamp

        return data_dict
    json_str = json.dumps(generate_data_with_timestamps())
    encoded_data = base64.b64encode(json_str.encode()).decode('utf-8')
    return encoded_data

def parseConfig():
    try:
        options = {
            'races':None,
            'captcha_key':None,
            'accounts':None,
            'max_wpm':None
        }
        config = open('config.txt', 'r').read().splitlines()
        for c in config:
            s = c.split("=")
            if s[0] != 'accounts':
                options[s[0]] = s[1]
            else:
                options['accounts'] = s[1].split(',')
        
        return options
    except:
        print(f"Fix your conifg file, Better Rio can't run unless you become a tiny bit smarter.")
        input()
        sys.exit()

print('Captcha key is recommended for login but not required.')

current_patch = '48e899a7b0e99068aad568b4540f2091875700d9'
current_version = 1807
os_user = subprocess.getoutput('echo %username%')
config = parseConfig()

def calculate_typing_time_per_letter(wpm, num_words):
    total_letters = num_words * 5 
    total_seconds = (60 / wpm) * num_words
    seconds_per_letter = total_seconds / total_letters
    return seconds_per_letter

def startTyping(client, words, set_wpm):
    c = 0
    e = 0
    rounds = 0        
    word_s = words.replace(' ', ' \n').split('\n')
    current = time.time()
    last_time = 0
    n = 0
    tex_ = ''

    for i in word_s:
        packet_count = 0
        packet = []
        rounds += 1
        for x in i:
            c += 1
            
            if c == 1:
                last_time = 0
            else:
                last_time = int(time.time() * 1000)-last_time

            if random.randint(1,30) == 1:
                let = random.choice(string.ascii_uppercase)
                e+=1
                # 
                client.send(
                    '5' + json.dumps(
                        {"stream":"race","msg":"update","payload":{"e":e,"k":[[let,random.randint(1,500),1,None]]}}
                    )
                )  
                last_time = 0
            
            packet.append([x,random.randint(1,500),None,None])
            time.sleep(calculate_typing_time_per_letter(random.randint(set_wpm-15, set_wpm+15), len(words)/5))

            total = 0
            for pac in packet:
                if pac[1]:
                    total+=pac[1]
            if total >=450 or len(packet) >=5:
                client.send(
                    '5' + json.dumps(
                        {"stream":"race","msg":"update","payload":{"t":c,"k":packet}}
                    )
                )
                packet_count += len(packet)
                for pack_ in packet:
                    tex_ = tex_ + pack_[0]
                packet = []

            elif packet_count + len(packet) == len(i):
                client.send(
                    '5' + json.dumps(
                        {"stream":"race","msg":"update","payload":{"t":c,"k":packet}}
                    )
                )
                packet_count += len(packet)
                for pack_ in packet:
                    tex_ = tex_ + pack_[0]

                packet = []

def checkIfSafeToRun():
    patch = getPatch()
    if patch[0] == current_patch and int(patch[1]) == current_version:
        return True
    else:
        return False

def getPatch():
    with requests.create_scraper(disableCloudflareV1=True, browser={'custom':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}) as session:

        cacheId=session.get(
            'https://www.nitrotype.com/garage'
        ).text.split('<script src="/index/')[1].split('/bootstrap.js"')[0].split('-')
        
        return cacheId
    
print(f'Update Supported: {current_patch}|{current_version}')
print('''
      ##                 #          #                             # #     #   ######   #   # 
    ##   ##########   #######    #######  ########## #########    # #     #     #      #   # 
  ## #           #     # #        # #             #  #       #           #  ########## #   # 
##   #          #      # #        # #            #   #       #          #       #      #   # 
     #       # #    ########## ##########     # #    #       #        ##        #         #  
     #        #          #          #          #     #########      ##          #        #   
     #         #         #          #           #                 ##             ####  ##    
''')
print('Made by @ssl8 on discord')
print('Checking nitrotype updates..')
if checkIfSafeToRun() != True:
    print("Better Rio may not be safe to run, to continue press enter!")
    print(f'(Nitrotype Update Detector)')
    input()

print(f'Starting accounts..')
time.sleep(1)


def nitroTypeLogin(username, password, proxy=None):
    try:
        with requests.create_scraper(disableCloudflareV1=True, browser={'custom':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}) as session:
            session.headers['x-username'] = username
            session.headers['referer'] = 'https://www.nitrotype.com/login'
            session.headers['origin'] = 'https://www.nitrotype.com'
            session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
            # session.cookies['_au_last_seen_pixels'] = encode_to_base64_pageId()
            # session.cookies['st-id'] = '1'

            login = session.post(
                'https://www.nitrotype.com/api/v2/auth/login/username',
                json = {
                    'captchaToken':'',
                    'password':password,
                    'username':username,
                    'tz':'America/Los_Angeles',
                    'authCode':'',
                    'trustDevice':False
                }
            )



            if login.status_code == 200:
                if login.json()['status'] == 'OK':
                    session.cookies['_au_last_seen_pixels'] = encode_to_base64_pageId()
                    cookies = session.cookies
                    cookies = '; '.join([cookie.name + '=' + cookie.value for cookie in cookies])

                    return login.json()['results'], cookies, proxy, session.cookies
            else:
                while True:
                    cap = solveCaptcha()
                    if cap != None:
                        break
                    
                login = session.post(
                    'https://www.nitrotype.com/api/v2/auth/login/username',
                    json = {
                        'captchaToken':cap,
                        'password':password,
                        'username':username,
                        'tz':'America/Los_Angeles',
                        'authCode':'',
                        'trustDevice':False
                    }
                )


                if login.status_code == 200:
                    if login.json()['status'] == 'OK':
                        session.cookies['_au_last_seen_pixels'] = encode_to_base64_pageId()
                        cookies = session.cookies
                        cookies = '; '.join([cookie.name + '=' + cookie.value for cookie in cookies])
                        return login.json()['results'], cookies, proxy, session.cookies

    except:
        return None, None, None, None
    
def solveCaptcha():
    with requests.create_scraper(disableCloudflareV1=True, browser={'custom':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}) as session:
        createTask = session.post(
            'https://api.capsolver.com/createTask',
            json = {
                "clientKey": config['captcha_key'],
                "task": {
                    "type": "ReCaptchaV2EnterpriseTaskProxyLess",
                    "websiteURL": "https://www.nitrotype.com",
                    "websiteKey": "6Ldn5v8UAAAAAE5PrdgV4hHlWZSXxGR2QsItv_hM",
                    "enterprisePayload":{
                        'v':'Ya-Cd6PbRI5ktAHEhm9JuKEu',
                        'hl':'en'
                    }
                }
            }
        )

        if createTask.status_code == 200:
            task = createTask.json()['taskId']
            for x in range(60):
                time.sleep(1)
                solved = session.post(
                    'https://api.capsolver.com/getTaskResult',
                    json = {
                        'clientKey':config['captcha_key'],
                        'taskId':task
                    }
                )
                if solved.json()['status'] == 'ready':
                    return solved.json()['solution']['gRecaptchaResponse']

def loginNitroType(username, password):
    with requests.session() as session:
        session.disableCloudflareV1 = True
        session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
        session.headers['X-Username'] = username
        session.headers['Referer'] = 'https://www.nitrotype.com/login'
        session.headers['Origin'] = 'https://www.nitrotype.com'

        session.get('https://www.nitrotype.com/login')

        login = session.post(
            'https://www.nitrotype.com/api/v2/auth/login/username',
            json = {
                'authCode':'',
                'captchaToken':'',
                'password':password,
                'trustDevice':False,
                'tz':'America/Los_Angeles',
                'username':username
            }
        ) 

        if login.status_code == 200:
            results = login.json()['results']
            token = results['token']
            cookies = '; '.join([cookie.name + '=' + cookie.value for cookie in session.cookies])
            
            return (token, cookies, results)
        
        elif login.json()['results']['captchaStatus'] == 'logins':
            login = session.post(
                'https://www.nitrotype.com/api/v2/auth/login/username',
                json = {
                    'authCode':'',
                    'captchaToken':solveCaptcha(),
                    'password':password,
                    'trustDevice':False,
                    'tz':'America/Los_Angeles',
                    'username':username
                }
            ) 

            if login.status_code == 200:
                results = login.json()['results']
                token = results['token']
                cookies = '; '.join([cookie.name + '=' + cookie.value for cookie in session.cookies])
                
                return (token, cookies, results)
    
def mainModule(auth, username, password, cookies, proxy, userId, cookies_raw):
    total_races = 0

    headers = {
        "Host": "realtime1ws.nitrotype.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Origin": "https://www.nitrotype.com",
        "Sec-WebSocket-Extensions": "permessage-deflate",
        "Sec-WebSocket-Key": "4jIHipXCk9gejpohIVvUHQ==",
        "Connection": "keep-alive, Upgrade",
        "Cookie": cookies,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "websocket",
        "Sec-Fetch-Site": "same-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade": "websocket"
    }

    # POST https://www.nitrotype.com/api/v2/settings/sounds

    last_race = None
    real_amount = 0
    completed_errors = 0
    server_count = 1
    server_main_count = 0
    for xi in range(int(config['races'])):
        total_races += 1
        game_text = ''
        pings = 0
        # server_main_count += 1

        # if server_main_count > 10:
        #     server_main_count = 0
        #     server_count += 1
        #     if server_count >= 8:
        #         server_count = 1
        #         continue

        # if server_count > 1:
        #     print('Attempting to change cookies')
        #     server_count = 0
        #     cookie_, headers_, auth = nitrotype_cookie_grab(headers['User-Agent'], cookies_raw, auth)
        #     cookie_ = '; '.join([cookie.name + '=' + cookie.value for cookie in cookie_])
        #     headers['Cookie'] = cookie_
        #     print('Cookies Changed')


        # if unique_counter >= unique_race_count:
        #     time.sleep(random.randint(60,180))
        #     unique_race_count = random.randint(1,4)
        #     unique_counter = 0

        # unique_counter += 1
            
        # sid = requests.create_scraper(disableCloudflareV1=True, browser={'custom':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}).get('https://realtime1.nitrotype.com/ws/?token='+auth+'&_primuscb=OrDLPBo&EIO=3&transport=polling&b64=1&t=OrDLPBp', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0', 'origin':'https://www.nitrotype.com', 'Cookie':headers['Cookie']})
        # sid = json.loads(sid.text[4:])['sid']

        ssl_opt = {"cert_reqs": ssl.CERT_REQUIRED, "ssl_version":ssl.PROTOCOL_TLSv1_2, 'check_host':True}
        
        if total_races >= 50 and password != None:
            try:
                results, cookies, proxy, raw = nitroTypeLogin(username, password, proxy)
                auth = results['token']
                headers['Cookie'] = cookies
                total_races = 0 
            except:
                print( f'Login error: {username}')
        if checkIfSafeToRun() != True:
            print('Patch detected, please rerun the application or referer to the discord!')
            input()
            sys.exit()
            
        # Set the minimum and maximum TLS versions to TLSv1.3

        try:
            client = websocket.create_connection(f'wss://realtime1ws.nitrotype.com/ws?token='+auth, header=headers, sslopt=ssl_opt)
        except:
            continue

        payload = {"path":f"/race","friends":[],"friendsHash":None}

        if total_races == 1:
            payload.update({'first':True})

        client.send(
            '5' + json.dumps({"stream":"notifications","type":"checkin","payload":payload}
            )
        )
        
        client.send(
            '5' + json.dumps(
                {"stream":"race","msg":"join","payload":{"update":"03417","cacheId":current_patch,"cacheIdInteger":current_version, "site":"nitrotype"}}
            )
        )

        completed_errors = 0
        while True:
            try:
                recv = client.recv()[1:]

                if recv == 'PING':
                    pings += 1
                    client.send("1PONG")
                    continue

                recv = json.loads(recv)
            
                if recv['stream'] == 'auth':
                    auth = recv['token']        
                    continue

                if recv['msg'] == 'status':
                    
                    if recv['payload'].get('l') != None:
                        game_text += recv['payload']['l']
                    
                    if recv['payload']['status'] == 'racing':
                        set_wpm = random.randint(int(config['max_wpm'])-10, int(config['max_wpm']))
                        print(f'lesson: {game_text}')
                        threading.Thread(target=startTyping, args=(client, game_text, set_wpm,)).start()

                if recv['msg'] == 'update':
                    ended = False
                    if recv['payload'].get('racers') != None:
                        for x in recv['payload'].get('racers'):
                            if x.get('u') == userId:
                                if x.get('r') != None:
                                    check_race_success = requests.create_scraper(disableCloudflareV1=True, browser={'custom':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}).get(
                                        'https://www.nitrotype.com/api/v2/stats/data/racelog?page=0&limit=30',
                                        headers = {
                                            'Authorization':f'Bearer {auth}'
                                        }
                                    ).json()['results']['logs'][0]
                                    
                                    if check_race_success != last_race:
                                        real_amount += 1
                                        last_race = check_race_success
                                        print(f'Total Races: {real_amount}; User: {username}')
                                    
                                    ended = True
                                    time.sleep(95)
                                    break

                        if ended:
                            break
                        
                if recv['msg'] == 'disqualified':
                    break

                if recv['msg'] == 'error':

                    if recv['payload']['type'] == 'captcha':
                        print('attempting to solve..')
                        if config['captcha_key'] != '':
                            with requests.create_scraper(disableCloudflareV1=True, browser={'custom':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}) as session:
                                session.proxies = {
                                    'http':'http://pc5v79bu5geqieo:ul1by5ynublajir@rp.proxyscrape.com:6060',
                                    'https':'http://pc5v79bu5geqieo:ul1by5ynublajir@rp.proxyscrape.com:6060'
                                }
                                session.headers['authorization'] = f'Bearer {auth}'
                                
                                session.headers['cookie'] = cookies
                                session.headers['referer'] = 'https://www.nitrotype.com/'
                                session.headers['origin']  ='https://www.nitrotype.com'
                                while True:
                                    cap = solveCaptcha()
                                    if cap != None:
                                        break
                                validate = session.post(
                                    'https://www.nitrotype.com/api/v2/auth/validate-captcha',
                                    json = {
                                        'token':cap
                                    }
                                )
                                

                                if validate.status_code == 200:
                                    print('Captcha has been Successfully solved..!')
                                    break
                                else:
                                    print('Captcha may have failed to be solved, treating as solved..')
                                    break

                                time.sleep(1)
                                    
                        else:
                            print("Captcha prompted, no captcha key was provided!")
                            return
            except Exception:
                completed_errors += 1
                if completed_errors >= 35:
                    total_races = 45
                    completed_errors = 0
                    break
                continue


def thread_(x):
    if x == '':
        return
    auth, cookies, proxy, cookies_raw = nitroTypeLogin(x.split(':')[0], x.split(':')[1])
    if auth != None:
        print(f'Logged in successfully!')
        userId = auth['userID']
        mainModule(auth['token'], x.split(':')[0], x.split(':')[1], cookies, proxy, userId, cookies_raw)
    else:
        print("your shitty account didn't work...")

for x in config['accounts']:
    try:
        threading.Thread(target=thread_, args=(x,),).start()
    except:
        pass