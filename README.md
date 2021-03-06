![Grover Logo](http://i.imgur.com/CbpIhow.jpg)

## What is this?
Grover is a simple interactive Python tool that allows you to craft a complete web server with LEMP stack (nginx, MySQL, PHP7.0), Fail2Ban, Firewall, only-SSH login, disable root account and other tools with simple questions like *What is your domain name?*

At this time Grover is available **only for Ubuntu servers**.

## Why should I use it?
It's free, open source and simple to use: why not?

## Ok, got it. How can I start?
1. Install pexcept with `sudo apt-get install python3-pexpect`
1. Download grover in your server. SSH in it and execute `wget https://raw.githubusercontent.com/DaniloPolani/grover/master/grover.py`.
1. Install python3, if you don't have it (you should, man).
1. Execute `sudo python3 grover.py` and answer to the questions.

## FAQs
* Why should I launch the script with sudo privileges?
  * The script needs to update and install packages and edit files, so... It needs them.
  
* What is a domain name?
  * Usually the domain name is your site domain without http and www, for example http://www.example.com will be **example.com**. If you are using a Load Balancer, type your machine IP.
  
* What this will install in my server?
   * **PHP7.0**
      * *FPM*
      * *CLI*
      * *mcrypt*
      * *mbstring*
      * *GD*
      * *Secure removing version from public details*
   * **Git**
   * **NodeJS**
   * **npm**
   * **MariaDB**
      * *New user (optional, but suggested)*
      * *New database (optional)*
   * **Nginx** (Web Server)
      * *A project folder (in /var/www)*
      * *HTTPS (optional) with SSL certificate + Auto redirect + HTTP/2*
      * *Auto-redirect to www. or non-www.*
      * *Secure removing version from public details*
   * **Disable root account** (suggested)
      * *New user with sudo privileges*
         * *Auto-copy SSH authorized_keys to new user*
      * *Disable PermitRootLogin (/etc/ssh/sshd_config file)*
   * **Enable only SSH** (disabling password login)
      * *Disable PasswordAuthentication (/etc/ssh/sshd_config file)*
   * **Fail2Ban**
   * **Firewall** (iptables + iptables-persistent)
