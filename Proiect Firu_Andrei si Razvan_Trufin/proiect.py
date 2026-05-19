from flask import Flask, render_template_string, redirect
from gpiozero import LED, Button
from threading import Thread
from datetime import datetime
import time
import random
import requests
import adafruit_dht
import board


#GPIO SETUP BCM:
#17 - Led, 26 - DHT22, 22 - Reset Alarm Button, 27 - Water Sensor

LED_PIN = 17
TEMP_PIN = 26
WATER_PIN = 27
RESET_PIN = 22

#Telegram ChatBot Alerts
BOT_TOKEN="Token-ul Botului de Telegram"
CHAT_ID="Chat IDul DVS."

#Hardware
led=LED(LED_PIN)
water_sensor = Button(WATER_PIN, pull_up=False)
reset_button = Button(RESET_PIN, pull_up=False)

#Variabile Globale
alarm_mode = False
manual_led_state = False
temperature_log = []
alarm_log = []
dht = adafruit_dht.DHT22(board.D26)

#Citire Temperatura
def read_temperature():
    global last_temp
    try:
        temperature = dht.temperature
        if temperature is not None:
            last_temp = round(temperature, 1)
    except:
        pass
    return last_temp

#Temperature Loop
def temperature_loop():
    while True:
        temp = read_temperature()
        timestamp = datetime.now().strftime("%H:%M:%S")
        temperature_log.append({
            "temp": temp,
            "time": timestamp
            })
        if len(temperature_log) >10:
                temperature_log.pop(0)
                
        print(f"Temperature: {temp}C")
        time.sleep(15)
        
#Telegram Message Alert
def send_telegram_message(message):
    url=f"https://api.telegram.org/BOT-ID/sendMessage"
    data={
        "chat_id": CHAT_ID,
        "text": message
        }
    requests.post(url, data=data)
#Alarm
def trigger_alarm():
    global alarm_mode
    if not alarm_mode:
        alarm_mode = True
        timestamp = datetime.now().strftime("%H:%M:%S")
        alarm_log.append({
            "time": timestamp
            })
        
        if len(alarm_log) > 10:
            alarm_log.pop(0)
        
        print("Water Detected")
        send_telegram_message(
            f"!Water DETECTED!\nTime: {timestamp}"
            )

#Reset
def reset_alarm():
    global alarm_mode
    alarm_mode = False
    led.off()
    print("Alarm reset")
    
#Buttons
water_sensor.when_pressed = trigger_alarm
reset_button.when_pressed = reset_alarm

#LED
def led_loop():
    while True:
        if alarm_mode:
            led.on()
            time.sleep(0.15)
            led.off()
            time.sleep(0.15)
        else:
            if manual_led_state:
                led.on()
            else:
                led.off()
            time.sleep(0.1)
            

#Threads
Thread(target=temperature_loop, daemon=True).start()
Thread(target=led_loop, daemon=True).start()

#Declare flask Web app
app = Flask(__name__)\
#HTML

HTML = """
<!Doctype HTML>
<html>
    <head>
        <title>SMART FLOOD/TEMP MONITOR</title>
        <style>
        body{
            background:#111;
            color:white;
            font-family:Arial;
            padding:20px;
            }
        .card{
            background:#1e1e1e;
            padding:20px;
            margin-bottom:20px;
            border-radius:20px;
            }
        button{
            padding:15px;
            border:none;
            border-radius:10px;
            background:#00aa55;
            color:white;
            font-size:16px;
            cursor:pointer;
            }
        button:hover{
                opacity:0.8;
                }
        .alarm{
            color:red;
            font-weight:bold;
            font-size:20px;
            }
        </style>
    </head>
    <body>
        <h1>Smart Flood & Temperature Monitor</h1>
        <div class="card">
            <h2>LED Control</h2>
            <form action="/toggle_led" method="post">
            <button type="submit">Toggle LED</button>
            </form>
        </div>
        <div class="card">
            <h2>Alarm Status</h2>
            {%if alarm%}
            <p class="alarm">ALARM ACTIVE</p>
            {% else %}
            <p>System Normal</p>
            {% endif %}
            
            <form action="/reset_alarm" method="post">
            <button type="submit">Reset Alarm</button>
            </form>
        </div>
        <div class="card">
        <h2>Temperature Registers</h2>
        <ul>
            {% for item in temperatures %}
            <li>
            {{ item["time"] }} -> {{ item["temp"] }}C
            </li>
            {% endfor %}
        </ul>
        </div>
        <div class="card">
            <h2>Past alerts</h2>
            <ul>
                {% for item in alarms %}
                <li>
                Water detected at: {{ item.time }}
                </li>
                {% endfor %}
            </ul>
        </div>
    </body>
</html>
"""

#Home Page
@app.route("/")
def home():
    return render_template_string(
        HTML,
        alarm=alarm_mode,
        temperatures=temperature_log,
        alarms=alarm_log
        )

#Toggle LED
@app.route("/toggle_led",methods=["POST"])
def toggle_led():
    global manual_led_state
    if not alarm_mode:
        manual_led_state = not manual_led_state
    return redirect("/")

#RESET ALARM FROM WEB
@app.route("/reset_alarm",methods=["POST"])
def reset_alarm_web():
    reset_alarm()
    return redirect("/")

#START SERVER
if __name__ == "__main__":
    print("Server Started")
    print("Open Browser at:")
    print("http://172.20.10.2:5000")
    
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
        )

    


