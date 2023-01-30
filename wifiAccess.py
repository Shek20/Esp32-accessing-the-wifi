import urequests
from machine import RTC

def locationAndTime():
    print("locating...")
    r = urequests.get('https://api.ipify.org')
    publicAddress = r.text
    if r.status_code == 200:
            q = urequests.get("https://api.ipgeolocation.io/ipgeo?apiKey=25c61e35171f48a6986286352571270a&ip={}".format(publicAddress))
            if q.status_code == 200:
                retrievedData = q.json()
                country = retrievedData["country_name"]
                timeAndDate = retrievedData["time_zone"]["current_time"]
                date = timeAndDate[0:10]
                time_ = timeAndDate[11:16]
                print("The internet was accessed at",time_,"by the Esp32 on",date,"and it is located in",country,"right now.")          
                rtc.datetime((int(timeAndDate[0:4]), int(timeAndDate[5:7]), int(timeAndDate[8:10]), 1, int(timeAndDate[11:13]), int(timeAndDate[14:16]), int(timeAndDate[17:19]), 0))                            
            else:
                print("The information about the location could not be not found.")
    else:
        print("The address was not found.")
    
    
def connectionMethod():
    global gate
    global address
    global link
    gate.active(True)
    if not gate.isconnected():
        print("Connecting...")
        gate.connect("KINGAKATI [2Ghz]","mandombe26")
        while not gate.isconnected():
            pass
        address = str(gate.ifconfig()[0])
        link = "http://{}".format(address)
        print("Here is the ipv4 address: ",address)
        print("Here is the link of the web page: ",link)
        locationAndTime()
        url = "https://api.callmebot.com/whatsapp.php?phone=27659342212&text=Here+is+the+link:+{}&apikey=7980347".format(link)
        q = urequests.get(url)
        if q.status_code == 200:
            print("The link was sent successfully.")
        else:
            print("The link was not sent.")
        
rtc = RTC()
address = ""
link = ""
gate = network.WLAN(network.STA_IF)
connectionMethod()

