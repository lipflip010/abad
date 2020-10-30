# abad
Simple python webserver

### Deployment
    sudo aptitude install python3-venv
    sudo aptitude install python3
    git clone git@github.com:lipflip010/abad.git
    cd abad
    python3 -m venv ./env
    cd env/bin
    source activate
    cd ../../../abad
    pip install -r requirements.txt
    
### Startup script
    [Unit]
    Description=Gunicorn instance to serve abad
    After=network.target

    [Service]
    User=root
    Group=www-data
    WorkingDirectory=/var/www/abad
    Environment="PATH=/bin:/var/www/abad/env/bin"
    ExecStart=/var/www/abad/env/bin/gunicorn --workers 2 --bind 0.0.0.0:8080 -m 007 wsgi:app

    [Install]
    WantedBy=multi-user.target

    
### Firewall rule
    ufw allow from $private_network to any port 8080

### Etymology
‛âbad is hebrew for to serve


