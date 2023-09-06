#!/usr/bin/env bash
# sets up my web servers for the deployment of web_static

# Install Nginx if it is not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/current/

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_path="/etc/nginx/sites-available/default"
config_alias="location /hbnb_static/ { alias /data/web_static/current/; }"
if ! grep -q "$config_alias" "$config_path"; then
    sudo sed -i "/location \/ {/a $config_alias" "$config_path"
fi

# Restart Nginx
sudo service nginx restart

exit 0
