# Grover
```
   _____    ______       ____     __    __    _____   ______    
  / ___ \  (   __ \     / __ \    ) )  ( (   / ___/  (   __ \   
 / /   \_)  ) (__) )   / /  \ \  ( (    ) ) ( (__     ) (__) )  
( (  ____  (    __/   ( ()  () )  \ \  / /   ) __)   (    __/   
( ( (__  )  ) \ \  _  ( ()  () )   \ \/ /   ( (       ) \ \  _  
 \ \__/ /  ( ( \ \_))  \ \__/ /     \  /     \ \___  ( ( \ \_)) 
  \____/    )_) \__/    \____/       \/       \____\  )_) \__/ 
```
Craft a complete web server


## What is this?
Grover is a simple interactive Python tool that allows you to craft a complete web server with LEMP stack (nginx, MySQL, PHP7.0), Fail2Ban, Firewall, only-SSH login, disable root account and other tools with simple questions like *What is your domain name?*

All of operations are made following DigitalOcean's tutorials.

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
   * **PHP7.0** (+ FPM, CLI, mcrypt, mbstring, gd)
   * **Git**
   * **MariaDB**
      * <sub><sup>New user (optional, but suggested)</sup></sub>
      * <sub><sup>New database (optional)</sup></sub>
   * **Nginx** (Web Server)
      * <sub><sup>A project folder (in /var/www)</sup></sub>
      * <sub><sup>HTTPS (optional) with SSL certificate + Auto redirect + HTTP/2</sup></sub>
      * <sub><sup>Auto-redirect to www. or non-www.</sup></sub>
   * **Disable root account** (suggested)
      * <sub><sup>New user with sudo privileges</sup></sub>
         * <sub><sup>Auto-copying SSH authorized_keys to new user</sup></sub>
      * <sub><sup>Disable PermitRootLogin (/etc/ssh/sshd_config file)</sup></sub>
   * **Enable only SSH** (disabling password login)
      * <sub><sup>Disable PasswordAuthentication (/etc/ssh/sshd_config file)</sup></sub>
