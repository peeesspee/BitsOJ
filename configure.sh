# Requires SUDO permission to install ErLang and rabbitMQ
sudo -v
sudo apt update
sudo apt upgrade -y

# Get ErLang
cd ~
wget http://packages.erlang-solutions.com/site/esl/esl-erlang/FLAVOUR_1_general/esl-erlang_20.1-1~ubuntu~xenial_amd64.deb
sudo dpkg -i esl-erlang_20.1-1\~ubuntu\~xenial_amd64.deb
# Add RabbitMQ to sources list
echo "deb https://dl.bintray.com/rabbitmq/debian xenial main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list
# Get RabbitMQ
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
sudo apt-get update
# Install RabbitMQ
sudo apt-get install rabbitmq-server

# Start RabbitMQ Server
sudo systemctl start rabbitmq-server.service
sudo systemctl enable rabbitmq-server.service
# Enable Management plugin
sudo rabbitmq-plugins enable rabbitmq_management
sudo chown -R rabbitmq:rabbitmq /var/lib/rabbitmq/

# Install Pika and PyQt5 for connection and GUI management respectively
sudo pip3 install pika
sudo pip3 install pyqt5

# Add users with appropiate permissions in RabbitMQ server
# Server account
sudo rabbitmqctl add_user BitsOJ micro
sudo rabbitmqctl set_user_tags BitsOJ administrator
sudo rabbitmqctl set_permissions -p / BitsOJ ".*" ".*" ".*"
# Judge account
sudo rabbitmqctl add_user judge1 micro1
sudo rabbitmqctl set_permissions -p / judge1 ".*" ".*" ".*"
# Client account
sudo rabbitmqctl add_user client client
sudo rabbitmqctl set_permissions -p / client "^team.*" "^team.*|client_requests|connection_manager" "^team.*|connection_manager"