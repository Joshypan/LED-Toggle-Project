import network
import socket
import machine
import time

# Set up Access Point
def setup_ap(ssid, password):
    ap = network.WLAN(network.AP_IF)  #Access Point mode
    
    # Deactivate and clear old settings
    ap.active(False)
    time.sleep(1)
    ap.active(True)  # Activate the AP

    if len(password) < 8:
        print("Error: Password must be at least 8 characters long.")
        return None

    try:
        ap.config(essid=ssid, password=password)
        print("Attempting to configure AP with SSID:", ssid)
    except Exception as e:
        print(f"Error configuring AP: {e}")
        return None

    while not ap.active():
        print("Activating AP mode...")
        time.sleep(1)

    if ap.active():
        print('AP Mode Active:', ap.active())
        print('Network config:', ap.ifconfig())
        return ap.ifconfig()[0]
    else:
        print("Error: AP mode could not be activated.")
        return None

html = """<!DOCTYPE html>
<html>
    <head>
        <title>LED Control</title>
    </head>
    <body>
        <h1>Control LEDs</h1>
        <p><a href="/led1on"><button>Turn LED 1 On</button></a></p>
        <p><a href="/led1off"><button>Turn LED 1 Off</button></a></p>
        <p><a href="/led2on"><button>Turn LED 2 On</button></a></p>
        <p><a href="/led2off"><button>Turn LED 2 Off</button></a></p>
    </body>
</html>
"""

# Handle client requests and toggle LEDs
def serve_webpage(ap_ip):
    try:
        addr = socket.getaddrinfo(ap_ip, 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        print(f'Listening on {addr}')

        # GPIO pins for LEDs
        led1 = machine.Pin(15, machine.Pin.OUT)
        led2 = machine.Pin(16, machine.Pin.OUT)

        print("Web server started. Waiting for clients to connect...")

        while True:
            cl, addr = s.accept()
            print(f'Client connected from {addr}')
            request = cl.recv(1024).decode('utf-8')
            print(f'Request: {request}')

            # Control LED 1
            if '/led1on' in request:
                print('Turning LED 1 ON')
                led1.value(1)  # Turn LED 1 on
            elif '/led1off' in request:
                print('Turning LED 1 OFF')
                led1.value(0)  # Turn LED 1 off

            # Control LED 2
            if '/led2on' in request:
                print('Turning LED 2 ON')
                led2.value(1)  # Turn LED 2 on
            elif '/led2off' in request:
                print('Turning LED 2 OFF')
                led2.value(0)  # Turn LED 2 off

            # Send the updated HTML web page
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n' + html
            cl.sendall(response.encode('utf-8'))
            cl.close()

    except Exception as e:
        print(f"Error in serve_webpage: {e}")

# Set up Wi-Fi connection
ap_ip = setup_ap('JoshAP', 'Mypassword')

if ap_ip:
    print(f"AP is active. Access the web interface at: http://{ap_ip}")
    serve_webpage(ap_ip)
else:
    print("Error: Failed to set up the Wi-Fi AP")
