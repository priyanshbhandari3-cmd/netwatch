NetWatch - Cloud-Based Network Monitoring and Troubleshooting System

A simple web-based tool built with Python Flask and hosted on a cloud platform (Render). A user enters a domain name or IP address, and the app reports whether it is reachable, how fast it responds, and the likely cause when something is wrong.

Features :-

DNS resolution (domain to IP address)
HTTP/HTTPS status check with response code
Latency (response time) measurement
TCP port check for ports 80 and 443
Automatic troubleshooting message (DNS failure, closed ports, high latency)
History table of the last 10 checks
Responsive dashboard built with Bootstrap

Tech Stack:-

Python 3, Flask
Requests library
Bootstrap 5 (via CDN)
Gunicorn (WSGI server for cloud deployment)
Render (cloud hosting) and GitHub (version control)

Project Structure:-

netwatch/
├── app.py
├── requirements.txt
├── README.md
└── templates/
    └── index.html

Run Locally:-
bash
pip install -r requirements.txt
python app.py

Open http://localhost:5000 in your browser.

Deploy on Render

Push this repository to GitHub.

On render.com, create a new Web Service and select this repository.

Build Command: pip install -r requirements.txt


Start Command: gunicorn app:app

Choose the Free instance type and deploy.

How It Works:-

The user submits a domain or IP.
The app resolves DNS (skipped when an IP is given).
It checks TCP ports 80 and 443.
It sends an HTTP/HTTPS request and measures the response time.
It shows the result with a troubleshooting message and stores it in the history table.

Limitations:-

A cloud server cannot reach private networks (for example 192.168.x.x addresses).
ICMP ping is not used because cloud hosts usually block it.
The free Render instance sleeps after inactivity, and history resets on restart.
Only basic checks are performed (no SNMP or packet capture).

Future Scope:-

Automatic periodic checks with Telegram or email alerts
Database storage and history graphs
Traceroute and SSL certificate expiry check
User login