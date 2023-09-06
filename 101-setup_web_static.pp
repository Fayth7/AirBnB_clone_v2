# AirBnB clone web server setup and configuration

# Define the Nginx configuration
$nginx_conf = "
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://fayth.tech/;
    }

    error_page 404 /404.html;

    location /404 {
        root /var/www/html;
        internal;
    }
}
"

# Install Nginx package
package { 'nginx':
  ensure   => 'installed',
  provider => 'apt',
}

# Create directory structure for web server
file { '/data':
  ensure  => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

# Create index.html for test page
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "This webpage is found in /data/web_static/releases/test/index.htm\n",
}

# Create symbolic link for current version
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

# Change ownership of /data directory to 'ubuntu:ubuntu'
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
}

# Create directories for Nginx
file { '/var/www':
  ensure => 'directory',
}

file { '/var/www/html':
  ensure => 'directory',
}

# Create index.html for default page
file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "This is my first upload in /var/www/index.html\n",
}

# Create custom 404.html page
file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page - Error page\n",
}

# Configure the default Nginx site
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf,
}

# Restart Nginx to apply changes
exec { 'nginx restart':
  path => '/etc/init.d/',
}
