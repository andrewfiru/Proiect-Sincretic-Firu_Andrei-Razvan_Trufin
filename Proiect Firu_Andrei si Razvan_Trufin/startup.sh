[Unit]
Description=Smart Water Monitor
After=network-online.target

[Service]

Type=simple

ExecStartPre=-/usr/bin/pkill -f proiect.py
ExecStartPre=/bin/sleep 10

ExecStart=/usr/bin/python3 /home/andrew/Desktop/proiect.py

WorkingDirectory=/home/andrew/Desktop

Restart=always
RestartSec=5

User=root

[Install]
WantedBy=multi-user.target