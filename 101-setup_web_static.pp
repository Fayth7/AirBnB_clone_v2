# AirBnB clone web server setup and configuration

# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n',
  owner   => 'root',
  group   => 'root',
}

# Ensure the symbolic link is created
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  owner   => 'root',
  group   => 'root',
}

# Set up Nginx configuration to serve web_static
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => "server {\n\tlisten 80 default_server;\n\tserver_name _;\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n}\n",
  owner   => 'root',
  group   => 'root',
  require => Package['nginx'],
}

# Restart Nginx to apply changes
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
