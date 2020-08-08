# NOTES
- project name used here is items-rest (this could be replaced)
- username used here is wilfred (this could be replaced)

### DROPLET SETUP
1. create droplet with Ubuntu os.
2. login as root (ssh roo@:12.22.2.2 [whatever the ip is and add password you got at email]).
3. Instal postgresql
```bash
apt-get update
apt-get install postgresql postgresql-contrib
```
4. Create new user.
- `add user wilfred` and set password
```bash
add user wilfred
visudo
```
- Search for `User privilege specification` and under root add the new created user.
```
root ALL=(ALL:ALL) ALL
wilfred ALL=(ALL:ALL) ALL
```
- Use `ctrl O` to save changes. then `ctrl X` to exit.
- Add ability for user to login as root to the server.
```
vi /etc/ssh/sshd_config
```
- Search for `Authentication` press `i` for insert mode and change PermitRootLogin to `no`. press `Esc` to go out of insert mode.
- Go to the end of the file and add  `AllowUsers wilfred` go out of insert mode and press `:wq` to save.
- reload service 
```bash
service sshd reload
```
5. login with the new created user. exit and then ssh wilfred@<IP ADDRESS>. (TO GO AS ROOT USE COMMAND `sudo su`)
6. Link new user to Postgres.
```
sudo -i -u postgres
createuser wilfred -P
createdb wilfred
exit
exit
```
7. Disable default behavior of postgres with local user
- Go to File
```
sudo vi /etc/postgresql/9.5/main/pg_hba.conf
```
- Go to bottom of file and change the `local all all peer` to `local all all md5` (save with `:wq`)

### SETUP NGINX
1. Install
```
sudo apt-get update
sudo apt-get install nginx
sudo ufw enable
sudo ufw allow "Nginx HTTP"
sudo ufw allow ssh
```
2. Check Nginx status `systemctl status nginx` (Should be active and running)

3. Create Config file for new site.
```
sudo vi /etc/nginx/site-available/items-rest.conf
```
4. Add configuration to file. example below
```conf
server {
    listen 80;
    real_ip_header X-Forwarded-For;
    set_real_ip_from 127.0.0.1;
    server_name localhost;

    location / {
        include uwsgi_params;
        uwsgi_pass inix:/var/www/html/items-rest/socket.sock;
        uwsgi_modifier1 30;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /usr/share/nginx/html;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```
5. save `:wq` and enable the config `sudo ln -s /etc/nginx/site-available/items-rest.conf /etc/nginx/sites-enabled/ `.

6. Create Socket File
```
sudo mkdir /var/www/html/items-rest
sudo chown wilfred:wilfred /var/www/html/items-rest
cd /var/www/html/items-rest
```
7. Clone the repo in the dir (/var/www/html/items-rest) using `.` at the end.
```
git clone https://gitbub....<your repo> .
mkdir log
```

### Instal PIP and Libs
```
sudo apt-get install python-pip python3-dev libpq-dev 
```
```
pip install virtualenv
virtualenv venv --python=python3.8.3
source venv/bin/activate
pip install -r requirements.txt
```

# SET UP UWSGI
1. create file
```
sudo vi /etc/systemd/system/uwsgi_items_rest.service
```
2. add to file this.
```service
[Unit]
Description=uwsgi items rest

[Service]
Environment=DATABASE_URL=postgres://wilfred:<password of the postgres user>@localhost:5432/wilfred
ExecStart=/var/www/html/items-rest/venv/bin/uwsgi --master --emperor /var/www/html/items-rest/uwsgi.ini --die-on-term --uid wilfred --gid wilfred --logto /var/www/html/items-rest/log/emperor.log
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
> Save and quit `ESC :wq`
> Modifyconfig file called uwsgi.ini to match the next 
```
[uwsgi]
base = /var/www/html/items-rest
app = run
module = %(app)
home = %(base)/venv
pythonpath = %(base)
socket = %(base)/socket.sock
chmod-socket = 777
processes = 8
threads = 8
harakiri = 15
callable = app
logto = /var/www/html/items-rest/log/%n.log
```
(Save with `ESC :wq`)

3. Delete Default NGINX Config file
```
sudo rm /etc/nginx/site-enabled/default
sudo systemctl restart nginx
```
4. Run App
```
sudo systemctl start uwsqi_items_rest
```

BY NOW SERVICE SHOULD BE RUNNING IN YOUR DIGITAL OCEAN IP ADDRESS. VISIT IT AND YOU SHOULD SEE THE API WORKING VIA HTTP.