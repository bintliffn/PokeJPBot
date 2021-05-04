
import requests
import json
import time
from bs4 import BeautifulSoup

headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; rv:84.0) Gecko/20100101 Firefox/84.0'
}





s = requests.session()
sku = "4521329329437"

def monitor():
    t =0
    while(t == 0):
        try:
            print("scraping...")
            url = "https://www.pokemoncenter-online.com/?p_cd="+sku
            request1 = requests.get(url, headers=headers,  timeout = 60)
            soup1 = BeautifulSoup(request1.content, 'html.parser')
            t= 1
        except:
            print("ERROR SCRAPING")

        script = soup1.find_all('script')[6].string[181:]
        splitlist = script.split(' ]);')
        data = json.loads(splitlist[0])
        availability = data['available']
        if availability == 'y':
            print('ITEM IN STOCK')
            return 1
        if availability == 'n' :
            print('OOS')
            return 0

def getProdId(session,cartUrl):
    p = 0
    while (p==0):
        try:
            r = session.get(cartUrl, headers=headers, timeout = 60)
            p = 1
        except:
            print("ERROR GETTING ProdId, Retrying")

    soup = BeautifulSoup(r.content, 'html.parser')
    id =soup.find('td', class_='td_volume')
    id2 = id.find('input')
    return id2.get('value')


def getCaptcha(captchaURL):
    print("GETTING CAPTCHA TOKEN\n")
    r = requests.post('http://2captcha.com/in.php?key=7461b8d71d32efcdebe6211e0bcf3bc0&method=userrecaptcha&'+captchaURL)
    captchaId = r.text
    trimmedCaptchaId = captchaId[3:]
    time.sleep(20)
    found = 1
    getUrl = 'http://2captcha.com/res.php?key=7461b8d71d32efcdebe6211e0bcf3bc0&action=get&id=' + trimmedCaptchaId
    while (found == 1):
        r = requests.get(getUrl)
        if (r.text != 'CAPCHA_NOT_READY'):
            found = 2
        time.sleep(5)
    trimmedCaptchaId = r.text[3:]
    print("Captcha Token Found: "+trimmedCaptchaId+"\n")
    return trimmedCaptchaId



def login():
    captchaToken = getCaptcha('googlekey=6LcwhoEUAAAAAIPQCm9zx-S7Ai9VBfu28bxIFBw5&pageurl=https://www.pokemoncenter-online.com/?main_page=login')
    payload = {'login_address': "test@gmail.com", 'password': "Test1234", 'g-recaptcha-response': captchaToken}
    loggedIn = 0
    while (loggedIn == 0):
        try:
            print("LOGGING IN:\n")
            s.get('https://www.pokemoncenter-online.com/', headers=headers, timeout = 60)
            s.get('https://www.pokemoncenter-online.com/?main_page=login', headers=headers,  timeout = 60)
            r = s.post('https://www.pokemoncenter-online.com/?main_page=login&action=process', headers=headers, data=payload,  timeout = 60)
            if(r.status_code == 200):
                loggedIn = 1
            else:
                print('ERROR LOGGING IN')
        except:
            print("ERROR LOGGING IN")



def checkout():
        #ADDING TO CART
        gp = 0
        while(gp == 0):
            try:
                print('GETTING PRODUCT')
                getProd = s.get('https://www.pokemoncenter-online.com/?p_cd='+sku, headers=headers, timeout = 60)
                if(getProd.status_code == 200):
                    gp = 1
                else:
                    print('ERROR GETTING PRODUCT')
            except:
                print('ERROR GETTING PRODUCT')

        atc = 0
        while(atc==0):
            try:
                print('ADDING TO CART')
                adding = s.get('https://www.pokemoncenter-online.com/api/request.php?method=add_cart&j='+sku+'&qty=1', headers=headers,  timeout = 60)
                if(adding.status_code == 200):
                    atc = 1
                else:
                    print('ERROR ADDING TO CART')
            except:
                print('ERROR ADDING TO CART')

        gtc = 0
        while (gtc == 0):
            try:
                print('GOING TO CART')
                getCart = s.get('https://www.pokemoncenter-online.com/?main_page=shopping_cart', headers=headers,  timeout = 60)
                if(getCart.status_code == 200):
                    gtc = 1
                else:
                    print("ERROR GOING TO CART")
            except:
                print("ERROR GOING TO CART")

        gpi = 0
        while (gpi==0):
            try:
                print('GETTING PRODID')
                prodId= getProdId(s,'https://www.pokemoncenter-online.com/?main_page=shopping_cart')
                print(prodId)
                payload = {'cart_quantity%5B%5D': '1', 'products_id%5B%5D': prodId}
                gpi = 1
            except:
                print('ERROR GETTING PRODID')

        #SHIPPING

        gtch = 0
        while (gtch==0):
            try:
                print('GOING TO CHECKOUT:')
                goToCheck = s.post('https://www.pokemoncenter-online.com/?main_page=shopping_cart&action=process', headers=headers, data=payload,  timeout = 60)
                if(goToCheck.status_code == 200):
                    gtch = 1
                else:
                    print('ERROR GOING TO CHECKOUT')
            except:
                print('ERROR GOING TO CHECKOUT')

        gts = 0
        while (gts==0):
            try:
                print('GOING TO SHIPPING')
                goToShip = s.get('https://www.pokemoncenter-online.com/?main_page=checkout_entry&from_page=cart', headers=headers,  timeout = 60)
                if(goToShip.status_code == 200):
                    gts = 1
                else:
                    print('ERROR GOING TO SHIPPING')
            except:
                print('ERROR GOING TO SHIPPING')

        gsi = 0
        while (gsi == 0):
            try:
                print('GETTING SHIPPING INFO')
                getShip = s.get('https://www.pokemoncenter-online.com/?main_page=checkout_shipping', headers=headers,  timeout = 60)
                if(getShip.status_code == 200):
                    gsi = 1
                else:
                    print('ERROR GETTING SHIPPING INFO')
            except:
                print('ERROR GETTING SHIPPING INFO')

        ss = 0

        while (ss == 0):
            try:
                newPayload = {'action': 'process', 'shipping_date_choice': '1', 'hope_delivery_date': '', 'hope_delivery_time_id': '0'}
                print("Submitting Shipping:")
                submitShip = s.post('https://www.pokemoncenter-online.com/?main_page=checkout_shipping', headers=headers, data = newPayload,  timeout = 60)
                if(submitShip.status_code == 200):
                    ss = 1
                else:
                    print("ERROR SUBMITTING SHIPPING")
            except:
                print("ERROR SUBMITTING SHIPPING")

        #PAYMENT

        gtp = 0

        while (gtp == 0):
            try:
                print("GOING TO PAYMENT:")
                goToPay = s.get('https://www.pokemoncenter-online.com/?main_page=checkout_payment', headers=headers,  timeout = 60)
                if(goToPay.status_code == 200):
                    gtp = 1
                else:
                    print("ERROR GOING TO PAYMENT")
            except:
                print("ERROR GOING TO PAYMENT")

        spi = 0

        while (spi == 0):
            try:
                print("SUBMITTING PAYMENT INFO:")
                paymentPayload = {'action': 'process', 'payment': 'regcc'}
                submitPayment = s.post('https://www.pokemoncenter-online.com/?main_page=checkout_confirmation', headers=headers, data=paymentPayload,  timeout = 60)
                if(submitPayment.status_code == 200):
                    spi = 1
                else:
                    print("ERROR SUBMITTING PAYMENT INFO")
            except:
                print("ERROR SUBMITTING PAYMENT INFO")

        so = 0

        while (so == 0):
            try:
                print("GETTING CHECKOUT CAPTCHA")
                captchaToken= getCaptcha('googlekey=6LfDcPoUAAAAAM5gneG6VuVeJQLfDpErocIh4fwD&pageurl=https://www.pokemoncenter-online.com/?main_page=checkout_confirmation&&invisible=1')
                finalPayload = {'cc_token': '', 'recaptchaResponse': captchaToken, 'agecheck': '1'}
                print('SUBMITTING ORDER')
                order = s.post('https://www.pokemoncenter-online.com/?main_page=checkout_process', headers=headers, data=finalPayload,  timeout = 60)
                if(order.status_code == 200):
                    so = 1
                else:
                    print("ERROR SUBMITTING ORDER")
            except:
                print("ERROR SUBMITTING ORDER")
        print('CHECK EMAIL')


prodFound = 0

login()
while(prodFound == 0):
    print("MONITORING")
    prodFound = monitor()
    time.sleep(5)

checkout()
