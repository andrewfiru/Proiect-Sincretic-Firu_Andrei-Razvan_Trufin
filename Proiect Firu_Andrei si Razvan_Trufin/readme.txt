Proiect Smart Temperature & Flood Monitor

Componente:
-Raspberry PI Gen 4 Model B
-Baterie Externa
-Cablu USB-A la USB-C
-Breadboard
-Senzor temperatura DHT22
-Sonda Soil Moisture
-Led + Resistor 300ohm
-Buton pentru RESET

Conexiune GPIO
-Magistrala principala VCC+GND 3.3V
-GPIO17 -Led
-GPIO26 -DHT22
-GPIO22 -Buton RESET
-GPIO27 -Soil Moisture Sensor

-Cod:
-Script python pentru colectarea datelor
-Interfata web Flask
-ChatBot Telegram pentru alerte inundatie

%Codul se gaseste in fisierul proiect.py
%Codul in bash pentru rulare la pornire se gaseste in fisierul startup.sh
%Interfața web se găsește la http://adresa-ip:port in aceeași rețea cu dispozitivul raspberry pi
