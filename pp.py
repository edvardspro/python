from flask import Flask, request
import os
import subprocess
import platform
import socket
import binascii

app = Flask(__name__)

SECRET_TOKEN = "popkorns_2022"   # nomaini!
MAC = "AA:BB:CC:DD:EE:FF"            # nomaini uz sava datora MAC

def wake_on_lan(mac):
    mac = mac.replace(":", "").replace("-", "")
    data = "FF" * 6 + mac * 16
    send_data = binascii.unhexlify(data)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(send_data, ("255.255.255.255", 9))

@app.route("/poweron", methods=["POST"])
def poweron():
    if request.args.get("token") != SECRET_TOKEN:
        return "Unauthorized", 401
    wake_on_lan(MAC)
    return "WOL sent", 200

@app.route("/shutdown", methods=["POST"])
def shutdown():
    if request.args.get("token") != SECRET_TOKEN:
        return "Unauthorized", 401

    system = platform.system().lower()
    if "windows" in system:
        subprocess.run(["shutdown", "/s", "/t", "0"])
    else:
        os.system("sudo shutdown -h now")

    return "Shutting down", 200

@app.route("/")
def home():
    return "PC control server is running"

