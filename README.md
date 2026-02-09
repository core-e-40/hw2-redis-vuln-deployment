# Vulnerable Redis Service Deployment with Flask and Nginx

## Overview
This project provides and automate, Ansible-based deployment of a vulnerable Redis service stack designed for use in cybersecurity competitions or educational labs. It deploys a three compoenent system including Redis as an intentionally misconfigured backend database, a Flask web application providing a browser-based interface for users to interact with Redis, and a Nginx reverse proxy to sit in front of the web application to act as its only entry point. All of these are configured with realistic security weaknesses that mirror misconfigurations commonly found in production environments but most of the vulnerbilities can be found in the Redis deployment.

The main goal of this project was to make easy to deploy competition infrastructure for Grey Team use through Ansible, enabling rapid deployment and teardown of a vulnerable environment with a single command. It serves Red Teams as a realistic target for particing exploitation chains from reconnaissance through persistance and Blue Team has a training environment for building detection rules and learning defensive hardening techniques. All configuration is driven through Ansible variables allowing compeition administrators to easily adjust the difficulty level by enabling or disabling specific vulnerbilities.

## Vulnerability Description
This deployment features a Redis instance connected to a Flask web application that has Nginx in front of it acting as the entry point of connection to the web application. The Redis instance is intentionally configured with critical security misconfigurations such as no authentication required. bound to all network interfaces (0.0.0.0), protected mode disabled, and dangerous administrative commands left enabled. This allows for any attacker on the network to discover the exposed Redis service via a simple port scan, cnnect without credentials, exfiltrate all stored data including credentials and flags, and ultimately gain persistent access by writing SSH keys through Redis's CONFIG SET and other administrative commands.

## Prerequisites
- **Target OS:** Ubuntu 24.04 LTS
- **Ansible Version:** 2.16+
- **Control Node:** WSL2 Ubuntu or any Linux with Ansible installed
- **Required on target:** openssh-server installed and running
- **Required on control node:** ansible, git, sshpass, redis-tools
- **Network:** Target must be reachable via SSH from control node

## Quick Start
```bash
git clone https://github.com/core-e-40/hw2-redis-vuln-deployment.git
cd hw2-redis-vuln-deployment
nano inventory.ini  # Update with your target IP and username
ansible-playbook -i inventory.ini playbook.yml --ask-become-pass
```

## Documentation
- [Deployment Guide](docs/DEPLOYMENT.pdf)
- [Exploitation Guide](docs/EXPLOITATION.pdf)

## Competition Use Cases
Red Team can practice a real-world exploit chain by discovering exposed services (Redis, Nginx), enumerate data, and write SSH keys for persistance. This mirrors attacks against misconfigured =Redis instances that can occur in production.

Blue Team can practice deducting unauthenticated service access from anonymous IPs, monitoring configuration changes, spotting unauthorized SSH keys, and identifying persistence mechanisms like cron jobs. Experience like this is ver y valuable to learn how to write modern detections in real production environments.

Grey Team can rapdily deploy a vulnerable environment using a single Ansible command and that same environment can be torn dow and rebuilt in minutes for compeition resets. All configurations are in variables so difficulty of the compeition and changes can be made on the fly to either make the compeition easier or harder with ease.

## Technical Details
The playbook first updates system packages and then installs require prerequisite services and packages on the target machine: Redis, Nginx, Python, Flask. Then a dedicated service account and directory for the Flask web application. A python virtual envonment and all Flask dependencies are installed to support the Flask web application. An intentionally vulnerable Redis configuration is then deployed which includes no authentication, the service being bound to all interfaces, protected mode off, and dangerous commands being enabled. After Redis is deployed, the Flask web application is deployed and connected to Redis and then Nginx is deployed to act as a reverse proxy that sits in fornt of Flask, acting as the only entry point to the web application. The playbook then ends by openning firewall ports ofr HTTP and Redis and verifying that all three services are running. 

## Troubleshooting
-	SSH Connection Refused
    -	The target machine likely does not have SSH server installed
        -	Run: ‘sudo apt install -y openssh-server’
        -	Then, run: ‘sudo systemctl enable ssh --now’

-	Missing Sudo Password
    -	Ansible needs sudo privileges on the target to perform configurations and setup
        -	Add: ‘--ask-become-pass’ to the end of the command when running a playbook on the control node

-	Port 5000 Showing as Filtered in Nmap
    -	This is expected behavior and not a problem because of Flask’s positioning behind Nginx. Due to this, access to the web happens through port 80 instead as the traffic will pass through nginx and into Flask.


## Repository Structure
```
hw2-redis-vuln-deployment/
├── README.md
├── playbook.yml
├── inventory.ini
├── vars/
│   └── main.yml
├── templates/
│   ├── redis.config.j2
│   ├── flask.config.j2
│   └── nginx-flask.config.j2
├── files/
│   └── flask_app.py
├── screenshots/
│   ├── deployment/
│   └── exploitation/
├── docs/
│   ├── DEPLOYMENT.md
│   └── EXPLOITATION.md
└── .gitignore
```

## Author
Cory Le (chl2099) — RIT Cyber Defense Techniques, Spring 2026