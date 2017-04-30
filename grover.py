#!/usr/bin/env python3
# Grover - Craft a complete web server
# By Danilo Polani (@Grork)
# Usage: sudo python3 grover.py

import urllib.request, subprocess, pexpect, time, os

# Colors for terminal
colors = {
    'PURPLE': '\033[95m',
    'BLUE': '\033[94m',
    'BOLD_BLUE': '\033[1;94m',
    'GREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'END': '\033[0m',
}

# Print a success string
# @param string text
def success(text):
    print(colors['GREEN'] + text + colors['END'])
    time.sleep(1)

# Print a success string
# @param string text
def header(text):
    print(colors['PURPLE'] + text + colors['END'])

# Replace string in file
# @param string file - The path
# @param string str  - String to find
# @param string repl - Replacement
def replace_in_file(path, find, repl):
    # Read in the file
    with open(path, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(find, repl)

    # Write the file out again
    with open(path, 'w') as file:
        file.write(filedata)

# Force an input from user
# @param string text - Text to prompt
# @return string
def force_prompt(text):
    output = input(text)
    while not output:
        output = input(text)

    return output

# Force prompt with y/n
# @param string text - Text to prompt
# @return boolean
def prompt_yes_no(text):
    yes = set(['yes','y', 'ye'])
    no = set(['no','n'])

    choice = input(text + ' [y/n]: ').lower()
    if choice in yes:
        return True
    elif choice in no:
        return False
    else:
        prompt_yes_no(text)

# Clear domain from http(s) and www
# @param str - String to clean
# @return string
def clear_domain(str):
    str = str.replace('http://www.', '').replace('https://www.', '').replace('http://', '').replace('https://', '')
    # Remove initial www., if there is
    if str.startswith('www.'):
        str = str.replace('www.', '', 1)

    return str

# Print a line
def line():
    print('_' * 20)

# Answer to prompt
# @param class spawn
# @param string question
# @param string answer
def answer_to(spawn, question, answer):
    spawn.expect(question)
    spawn.sendline(answer)

if __name__ == '__main__':

    # Welcome on the hell
    print("""
__________________________________________________________________    
    _____    ______       ____     __    __    _____   ______    
   / ___ \  (   __ \     / __ \    ) )  ( (   / ___/  (   __ \   
  / /   \_)  ) (__) )   / /  \ \  ( (    ) ) ( (__     ) (__) )  
 ( (  ____  (    __/   ( ()  () )  \ \  / /   ) __)   (    __/   
 ( ( (__  )  ) \ \  _  ( ()  () )   \ \/ /   ( (       ) \ \  _  
  \ \__/ /  ( ( \ \_))  \ \__/ /     \  /     \ \___  ( ( \ \_)) 
   \____/    )_) \__/    \____/       \/       \____\  )_) \__/  

                    Web Server Crafter
Nginx, PHP7, MariaDB, Firewall, Fail2Ban, Cache, GZip, Security

                By Danilo Polani (@Grork)
__________________________________________________________________
    """)

    header('Welcome on Grover, web server crafter!')
    time.sleep(1)
    header('It will be configure a LEMP stack with Firewall, Fail2Ban, PHP performance, cache, gzip and other. Start!')
    time.sleep(2)

    # Update
    header('Updating apt...')
    subprocess.check_output(['apt-get','update'])
    success('Updated.')

    
    # --------------
    # START LEMP
    # --------------

    # Install NGINX, PHP and Git
    header('Installing nginx, php7 and git...')
    subprocess.check_output(['apt-get', 'install', '-y', 'nginx', 'php7.0-fpm', 'php7.0-cli', 'php7.0-mcrypt', 'php7.0-mbstring', 'php7.0-gd', 'git', 'debconf-utils'])
    success('Installed.')

    # Retrieve versions
    nginx_version_p = subprocess.Popen(['nginx', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, nginx_version = nginx_version_p.communicate() # That genius of Nginx is returning output as stderr
    php_version = subprocess.check_output(['php', '-v'])
    git_version = subprocess.check_output(['git', '--version'])

    print(colors['BOLD_BLUE'] + 'NGINX version: ' + colors['END'] + colors['BLUE'] + nginx_version.decode('ascii') + colors['END'])
    print(colors['BOLD_BLUE'] + 'PHP version: ' + colors['END'] + colors['BLUE'] + php_version.decode('ascii') + colors['END'])
    print(colors['BOLD_BLUE'] + 'Git version: ' + colors['END'] + colors['BLUE'] + git_version.decode('ascii') + colors['END'])
    time.sleep(1)

    # Change PHP settings...
    header('Editing php.ini...')
    replace_in_file('/etc/php/7.0/fpm/php.ini', ';cgi.fix_pathinfo=1', 'cgi.fix_pathinfo=0')
    # ...and restart PHP
    header('Restarting PHP...')
    subprocess.check_output(['service', 'php7.0-fpm', 'restart'])
    success('Done.')

    # Project folder
    project_name = input('Which will be the project folder name under /var/www/? Leave empty for "site": ')
    if not project_name:
        project_name = 'site'
    # Create
    subprocess.check_output(['mkdir', '-p', '/var/www/' + project_name.lower()])
    success('Project folder created in /var/www/' + project_name.lower() + '.')

    # Edit nginx conf
    server_name = clear_domain(force_prompt('Which is the server name? (e.g. mysite.com): '))
    line()
    
    # Retrieve site domain
    site_domain = clear_domain(force_prompt('Which is the site domain without http(s)://(www)? (e.g. mysite.com, danilo.rocks ...): '))
    line()

    # Will the site be with www?
    use_www = prompt_yes_no('Will you use the www subdomain (e.g. http(s)://www.mysite.com) or not (http(s)://mysite.com)?')
    line()

    # Retrieve config details
    public_path = input('Which will be the public path of your /var/www/' + project_name + '? (starting with a slash, e.g. /public. Leave empty for the root): ')
    if not public_path:
        public_path = '/'
    if not public_path.startswith('/'):
        public_path = '/' + public_path
    
    public_path = project_name + public_path
    is_ssl = prompt_yes_no('Will you have SSL certificate for HTTPS?')
    line()
    if is_ssl:
        ssl_cert = force_prompt('Path for SSL certificate (.crt file, type "n" to cancel SSL): ')
        line()
        if ssl_cert.lower() in 'no':
            is_ssl = False
        else:
            ssl_cert_key = force_prompt('Path for SSL certificate key (usually .key file, type "n" to cancel SSL): ')
            if ssl_cert_key.lower() in 'no':
                is_ssl = False

    # Create config file
    conf_file_name = site_domain + '.conf'
    remote_conf_file = 'https://gist.githubusercontent.com/DaniloPolani/057f1efd1c1ade7c49e959d6d11d085f/raw'

    if is_ssl:
        remote_conf_file = 'https://gist.githubusercontent.com/DaniloPolani/903994aa18de626f47d49822f3e91bbd/raw'

    file_content = urllib.request.urlopen(remote_conf_file).read().decode('ascii')
    if is_ssl:
        file_content = file_content.format(
            project_folder=project_name.lower(),
            server_name=server_name,
            site_domain=site_domain,
            ssl_cert=ssl_cert,
            ssl_cert_key=ssl_cert_key
        )
    else:
        file_content = file_content.format(
            project_folder=project_name.lower(),
            server_name=server_name,
            site_domain=site_domain
        )

    use_www_replace = '' if use_www else '#'
    file_content.replace('#R ', use_www_replace)

    with open('/etc/nginx/sites-available/' + conf_file_name, 'w') as file:
        file.write(file_content)

    # Remove default conf
    os.remove('/etc/nginx/sites-available/default')
    os.remove('/etc/nginx/sites-enabled/default')

    # Create symlink
    os.symlink('/etc/nginx/sites-available/' + conf_file_name, '/etc/nginx/sites-enabled/' + conf_file_name)
    success('Configuration file created under /etc/nginx/sites-available/' + conf_file_name + '.')

    # Restart nginx
    header('Restarting nginx...')
    subprocess.check_output(['service', 'nginx', 'restart'], stderr=subprocess.DEVNULL)
    success('Done.')

    # Install MariaDB
    mysql_password = force_prompt('What will be your MySQL password? ')
    # Set password to disable prompt of MariaDB
    subprocess.check_output('echo "mariadb-server mysql-server/root_password password ' + mysql_password + '" | debconf-set-selections', stderr=subprocess.DEVNULL, shell=True)
    subprocess.check_output('echo "mariadb-server mysql-server/root_password password ' + mysql_password + '" | debconf-set-selections', stderr=subprocess.DEVNULL, shell=True)
    # Install
    subprocess.check_output(['apt-get', '-y', '-qq', 'install', 'mariadb-server'])
    # Start it
    subprocess.check_output(['service', 'mysql', 'start'])
    # Secure installation
    answer = pexpect.spawn('mysql_secure_installation')
    answer_to(answer, 'Enter current password.*', 'asd123')
    answer_to(answer, 'Change the root password.*', 'n')
    answer_to(answer, 'Remove anonymous users.*', 'Y')
    answer_to(answer, 'Disallow root login remotely.*', 'Y')
    answer_to(answer, 'Remove test database and access to it.*', 'Y')
    answer_to(answer, 'Reload privilege tables now.*', 'Y')
    success('MariaDB installed.')

    # Create new MySQL user
    if prompt_yes_no('Would you like to create another MySQL user (suggested)?'):
        new_mysql_user_name = force_prompt('What will be the user name? (Type "n" to cancel creation): ')
        if new_mysql_user_name != 'n':
            new_mysql_user_password = force_prompt('What will be the user password? (Type "n" to cancel creation): ')
            if new_mysql_user_password != 'n':
                subprocess.check_output('mysql -e "CREATE USER \'' + new_mysql_user_name + '\'@\'localhost\' IDENTIFIED BY \'' + new_mysql_user_password + '\';"', shell=True)
                subprocess.check_output('mysql -e "GRANT ALL PRIVILEGES ON *.* TO \'' + new_mysql_user_name + '\'@\'localhost\';"', shell=True)
                subprocess.check_output('mysql -e "FLUSH PRIVILEGES;"', shell=True)
                success('MySQL user created.')
    
    # Create new database
    if prompt_yes_no('Would you like to create a new database?'):
        new_mysql_db = force_prompt('What will be the database name? (Type "n" to cancel creation): ')
        if new_mysql_db != 'n':
            subprocess.check_output('mysql -e "CREATE DATABASE ' + new_mysql_db + ';"', shell=True)
                success('Database created.')

    # --------------
    # DISABLE ROOT USER
    # --------------
    current_user = php_version = subprocess.check_output(['whoami'])
    if current_user == 'root' and prompt_yes_no('You would like to disable root account (suggested)?'):
        # Do things here
        pass
    
    # --------------
    # ENABLE ONLY SSH (DISABLE PASSWORD)
    # --------------
    if prompt_yes_no('You would like to disable password login and enable only SSH? WARNING: Remember to upload your SSH key to authorized_keys!'):
        # Do things here
        pass
