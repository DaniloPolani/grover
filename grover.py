#!/usr/bin/env python3
# Grover - Craft a complete web server
# By Danilo Polani (@Grork)
# Usage: sudo python3 grover.py

import urllib.request, subprocess, time, os

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

if __name__ == '__main__':

    # Welcome on the hell
    print("""
    _____    ______       ____     __    __    _____   ______    
   / ___ \  (   __ \     / __ \    ) )  ( (   / ___/  (   __ \   
  / /   \_)  ) (__) )   / /  \ \  ( (    ) ) ( (__     ) (__) )  
 ( (  ____  (    __/   ( ()  () )  \ \  / /   ) __)   (    __/   
 ( ( (__  )  ) \ \  _  ( ()  () )   \ \/ /   ( (       ) \ \  _  
  \ \__/ /  ( ( \ \_))  \ \__/ /     \  /     \ \___  ( ( \ \_)) 
   \____/    )_) \__/    \____/       \/       \____\  )_) \__/  
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
    subprocess.check_output(['apt-get', 'install', '-y', 'nginx', 'php7.0-fpm', 'php7.0-cli', 'php7.0-mcrypt', 'php7.0-mbstring', 'git'])
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
    
    # Retrieve site domain
    site_domain = clear_domain(force_prompt('Which is the site domain without http(s)://(www)? (e.g. mysite.com, danilo.rocks ...): '))

    # Will the site be with www?
    use_www = prompt_yes_no('Will you use the www subdomain (e.g. http(s)://www.mysite.com) or not (http(s)://mysite.com)?')

    # Retrieve config details
    public_path = input('Which will be the public path of your /var/www/' + project_name + '? (starting with a slash, e.g. /public. Leave empty for the root): ')
    if not public_path:
        public_path = '/'
    if not public_path.startswith('/'):
        public_path = '/' + public_path
    
    public_path = project_name + public_path
    is_ssl = prompt_yes_no('Will you have SSL certificate for HTTPS?')
    if is_ssl:
        ssl_cert = force_prompt('Path for SSL certificate (.crt file, type "n" to cancel SSL): ')
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

    # --------------
    # START ROOT USER
    # --------------
    current_user = php_version = subprocess.check_output(['whoami'])
    if current_user == 'root' and prompt_yes_no('You would like to disable root account? (Suggested)'):
        # Do things here
        pass
    
    # --------------
    # ENABLE ONLY SSH (DISABLE PASSWORD)
    # --------------
    if prompt_yes_no('You would like to disable password login and enable only SSH? WARNING: Remember to upload your SSH key to authorized_keys!'):
        # Do things here
        pass