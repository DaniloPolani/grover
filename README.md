# Grover
Grover - Craft a complete web server


## What is this?
Grover is a simple Python script that allows you to craft a complete web server with LEMP stack (nginx, MySQL, PHP7.0), Fail2Ban, Firewall, only-SSH login, disable root account and other tools with simple questions like *What is your domain name?*

All of operations are made following DigitalOcean's tutorials.

## Why should I use it?
It's free, open source and simple to use: why not?

## Ok, got it. How can I start?
1. Download grover in your server. SSH in it and execute `wget TO-DO`.
1. Install python3, if you don't have it (you should, man).
1. Execute `sudo python3 grover.py` and answer to the questions.

## FAQs
* Why should I launch the script with sudo privileges?
  * The script needs to update and install packages and edit files, so... It needs them.
  
* What is a domain name?
  * Usually the domain name is your site domain without http and www, for example http://www.example.com will be **example.com**. If you are using a Load Balancer, type your machine IP.
  
