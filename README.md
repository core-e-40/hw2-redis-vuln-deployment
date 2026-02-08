# Vulnerable Redis Service Deployment with Flask and Nginx

## Overview
(1-2 paragraphs: What is this project? Why does it exist? What does it deploy?)

## Vulnerability Description
(Brief description of the Redis misconfiguration and why it's dangerous)

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

Blue Team can practice deducting unauthenticated service access from anonymous IPs, monitoring configuration changes, spotting unauthorized SSH keys, and identifying persistence mechanisms like cron jobs. Experience like this  

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