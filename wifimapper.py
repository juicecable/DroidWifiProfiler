#Copyright (c) 2020 Derek Frombach
import socket as so
import androidhelper
import time
droid = androidhelper.Android()

netname='eduroam'
key='key'.encode('utf-8')
tout=0.2
currsig=[0]*128
allcurrsig=[0]*128
currsigdesc=[0]*128
strsig=[0]*128
lasig=[0]*128
laconn=[0]*128
wasconn=False
anything=[0]*128
did=False
yo=False

#toggle parameters
enanything=True #Enable Recording of Anything that is Valid
enlasig=True #Enable Last Connection Recording
encountsig=True #Enable Histogram Plotting
engps=False #Enable GPS
enloc=False #Enable Location Services
enlock=True #Enable Wakelock and full Wifi Lock
enanylock=True #Enable Scan only Wifi Lock
debug=False #Debug
isgooglestupid=True #If you have android 8 or 9
toscan=True #Do Scanning

ip=so.gethostbyname('google.ca')
port=8081
buff=1400
seaddr=(ip,port)
s=so.socket(so.AF_INET,so.SOCK_DGRAM)
s.settimeout(tout)

ss=s.sendto
sr=s.recvfrom
ts=time.sleep
tc=time.clock
dc=droid.wifiGetConnectionInfo
dn=droid.wifiStartScan
dr=droid.wifiGetScanResults
dl=droid.getLastKnownLocation
di=droid.readLocation
ds=droid.startLocating
dp=droid.stopLocating
dw=droid.checkWifiState
dt=droid.toggleWifiState
da=droid.wakeLockAcquireDim
dq=droid.wakeLockRelease
wl=droid.wifiLockAcquireFull
wt=droid.wifiLockAcquireScanOnly
wr=droid.wifiLockRelease

print('Running')
print('Disabled')
if dw()[1]:
    pass
else:
    dt(True)
    ts(10)

dn()
ts(3)
qs=dr()[1] #Scan Results
a=dl()[1]
qlg=a['gps'] #Location GPS
qln=a['network'] #Location Network
conn=False #Connected to Internet
csup='Not_Executed'
cssid='N/A'
crssi=-127
cbssid='00:00:00:00:00:00'
cspeed=0
eis=[] #Indexing for scans

lip=0
lbssid='00:00:00:00:00:00'
lrssi=-127
nt=False
lt=False
cond=False
try:
    while True:
        if debug: print('iteration')
        a=dc()[1]
        csup=a['supplicant_state']
        if csup=='completed': #Connected to wifi
            cssid=a['ssid'][1:-1]
            if debug: print(cssid)
            if debug: print(netname)
            if cssid==netname: #connected to eduroam
                if debug: print('recognised')
                crssi=int(a['rssi'])
                cbssid=a['bssid']
                cip=a['ip_address']
                cspeed=int(a['link_speed'])
                if not cond: #Disable Low Power Mode
                    cond=True
                    if engps: ds(1000,1)
                    if enlock:
                        da()
                        wl()
                    elif enanylock:
                        wt()
                    if not isgooglestupid:
                        dn()
                        ts(3)
                    elif toscan: yo=True
                    if engps:
                        a=di()[1]
                    elif enloc:
                        a=dl()[1]
                    if engps or enloc:
                        try:
                            qlg=a['gps'] #Location GPS
                            qln=a['network'] #Location Network
                        except:
                            try: qln=a['network'] #Location Network
                            except: qln=qlg
                            else: qlg=qln
                    if not isgooglestupid: qs=dr()[1]
                    if nt: nt=False
                    else: nt=True
                    print('Enabled')
                else: #Keep High Power Mode
                    if not isgooglestupid:
                        dn()
                        ts(3)
                    elif toscan: yo=True
                    if enloc:
                        a=di()[1]
                        try:
                            qlg=a['gps'] #Location GPS
                            qln=a['network'] #Location Network
                        except:
                            try: qln=a['network'] #Location Network
                            except: qln=qlg
                            else: qlg=qln
                    if not isgooglestupid: qs=dr()[1]
                    if nt: nt=False
                    else: nt=True
            else: #Connected to Something other than eduroam
                if debug: print('other network')
                if not isgooglestupid:
                    dn()
                    ts(3)
                    qs=dr()[1]
                elif toscan: yo=True
                if nt: nt=False
                else: nt=True
        else: #Not connected to wifi (could be reconnecting)
            if debug: print('wpa supplicant not connected')
            if not cond: #Wasn't Just Connected to Eduroam
                wr()
                ts(60)
            else: #Was Just connected to Eduroam
                if not isgooglestupid:
                    dn()
                    ts(3)
                elif toscan: yo=True
                if engps:
                    a=di()[1]
                elif enloc:
                    a=dl()[1]
                if engps or enloc:
                    try:
                        qlg=a['gps'] #Location GPS
                        qln=a['network'] #Location Network
                    except:
                        try: qln=a['network'] #Location Network
                        except: qln=qlg
                        else: qlg=qln                
                if not isgooglestupid: qs=dr()[1]
                if nt: nt=False
                else: nt=True
        if not isgooglestupid:
            #Checking if scans have updated
            if nt!=lt: #Scan has been updated
                #Checking for Eduroam in scans
                if debug: print('has scanned')
                lt=nt
                wood=False
                eis=[]
                eisa=eis.append
                for i in range(0,len(qs)):
                    a=qs[i]
                    #frequency=a['frequency']
                    #rssi=a['level']
                    #bssid=a['bssid']
                    ssid=a['ssid']
                    if ssid==netname:
                        wood=True
                        eisa(i)
            else: #Scan Failed
                if debug: print('not scanned')
                wood=False
        else:
            if debug: print('google is stupid')
            if cond:
                if debug: print('what we expected')
                try: ss(key,seaddr)
                except: conn=False #Failure
                else:
                    a=tc()
                    conn=False
                    while tc()-a<tout: #Timeout Handler
                        try:
                            data,addr=sr(buff)
                            if addr[0]==seaddr[0] and addr[1]==seaddr[1]:
                                conn=True
                                break
                        except:
                            #ts(tout/10.0)
                            break
                if not conn:
                    if debug: print('No Data')
                    dn()
                    ts(3)
                    qs=dr()[1]
                    #Checking for Eduroam in scans
                    if debug: print('has scanned')
                    wood=False
                    yo=True
                    eis=[]
                    eisa=eis.append
                    for i in range(0,len(qs)):
                        a=qs[i]
                        #frequency=a['frequency']
                        #rssi=a['level']
                        #bssid=a['bssid']
                        ssid=a['ssid']
                        if ssid==netname:
                            wood=True
                            eisa(i)
                else:
                    if debug: print('OK THEN')
                    wood=True
                    yo=False
            elif yo==True:
                if debug: print('they wanted me to scan')
                dn()
                ts(3)
                qs=dr()[1]
                #Checking for Eduroam in scans
                if debug: print('has scanned')
                wood=False
                eis=[]
                eisa=eis.append
                for i in range(0,len(qs)):
                    a=qs[i]
                    #frequency=a['frequency']
                    #rssi=a['level']
                    #bssid=a['bssid']
                    ssid=a['ssid']
                    if ssid==netname:
                        wood=True
                        eisa(i)
        if not wood: #No Eduroam in range
            if cond: #Go Ahead and Go into Low Power Mode
                cond=False
                dp()
                wr()
                dq()
                print('Disabled')
                ts(60)
            else: #Stay in low power mode
                if debug: print('LP Mode')
                ts(60)
        else: #Eduroam detected nearby or connected
            if debug: print('network is somehow detected')
            try: ss(key,seaddr)
            except: conn=False #Failure
            else:
                a=tc()
                conn=False
                while tc()-a<tout: #Timeout Handler
                    try:
                        data,addr=sr(buff)
                        if addr[0]==seaddr[0] and addr[1]==seaddr[1]:
                            conn=True
                            break
                    except:
                        #ts(tout/10.0)
                        break
            if cond: #Eduroam connected
                if enanything:
                    anything[abs(int(crssi))]+=1
                    currsigdesc[abs(int(crssi))]=int(crssi)
                if encountsig:
                    if conn: #Internet Available
                        currsig[abs(int(crssi))]+=1
                        currsigdesc[abs(int(crssi))]=int(crssi)
                        if yo:
                            for i in eis:
                                if qs[i]['bssid']==cbssid: pass
                                else:
                                    if int(qs[i]['level'])>=crssi:
                                        strsig[abs(int(qs[i]['level']))]+=1
                                        currsigdesc[abs(int(qs[i]['level']))]=int(qs[i]['level'])
                                    break
                    else: #Internet Temporarily Unavailable
                        if yo:
                            for i in eis:
                                if qs[i]['bssid']==cbssid: pass
                                else:
                                    if int(qs[i]['level'])>=crssi:
                                        strsig[abs(int(qs[i]['level']))]+=1
                                        currsigdesc[abs(int(qs[i]['level']))]=int(qs[i]['level'])
                                    break
                    allcurrsig[abs(int(crssi))]+=1
                    currsigdesc[abs(int(crssi))]=int(crssi)
                if enlasig:
                    did=True
                    if int(cip)!=lip or lbssid!=cbssid:
                        lasig[abs(int(lrssi))]+=1
                    if (not conn) and wasconn:
                        laconn[abs(int(lrssi))]+=1
                    lip=int(cip)
                    lbssid=cbssid
                    lrssi=int(crssi)
                    wasconn=conn
                #qlg=a['gps'] #Location GPS
                #qln=a['network'] #Location Network
                #qs=dr()[1] #Scan Results
                #conn=False #Connected to Internet
                #csup='Not_Executed'
                #cssid='N/A'
                #crssi=-127
                #cbssid='00:00:00:00:00:00'
                #cspeed=0
            else: #Eduroam not connected, but in Range
                if debug: print('found in scan')
                if enlasig:
                    if did:
                        did=False
                        lasig[abs(int(lrssi))]+=1
                    if (not conn) and wasconn:
                        laconn[abs(int(lrssi))]+=1
                    wasconn=conn
                #qlg=a['gps'] #Location GPS
                #qln=a['network'] #Location Network
                #qs=dr()[1] #Scan Results
                #conn=False #Connected to Internet
        if yo:
            yo=False
        ts(1.0)

except KeyboardInterrupt: #Ctrl-C Shutdown
    dp()
    wr()
    dq()
    print('Disabled')
    #File IO goes here
    print('Stopped')

if encountsig:
    print('encountsig')
    print(currsig) #Internet and Connected
    print(currsigdesc) #Power
    print(strsig) #No Internet but Eduroam, and stronger signal strength
    print(allcurrsig) #Connected to Eduroam
if enlasig:
    print('enlasig')
    print(lasig) #Reconnected with Different Wifi
    print(laconn) #Last connected to eduroam
