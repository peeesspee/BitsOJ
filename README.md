# BitsOJ
Offline Judge for competitive programming contests.  

## Setup
### Run this script to bypass the following steps:
1.  `sudo chmod +x configure.sh`
2.  `./configure.sh`
### Or, run these commands manually:
#### 1.Update the system:  
`sudo apt-get update`  
`sudo apt-get upgrade`  
#### 2.Install ErLang
1. `cd ~  `  
2. `wget http://packages.erlang-solutions.com/site/esl/esl-erlang/FLAVOUR_1_general/esl-erlang_20.1-1~ubuntu~xenial_amd64.deb`  
3. `sudo dpkg -i esl-erlang_20.1-1\~ubuntu\~xenial_amd64.deb`   
Check your ErLang installation by running:  
4. `erl`  
#### 3.Install RabbitMQ  
Add the Apt repository to your Apt source list directory (/etc/apt/sources.list.d):  
1. `echo "deb https://dl.bintray.com/rabbitmq/debian xenial main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list`  
 Next add our public key to your trusted key list using apt-key:   
1. `wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -`  
2. `sudo apt-get update`  
3. `sudo apt-get install rabbitmq-server`  
#### 4.Start the RabbitMQ server:  
1. `sudo systemctl start rabbitmq-server.service`  
2. `sudo systemctl enable rabbitmq-server.service`    
To check status of RabbitMQ server,  
3. `sudo rabbitmqctl status`  
#### 5.Create a new admin account  
You should give custom values to user_name and user_password in the next command:  
1. `sudo rabbitmqctl add_user user_name user_password`     
2. `sudo rabbitmqctl set_user_tags user_name administrator`    
3. `sudo rabbitmqctl set_permissions -p / user_name ".*" ".*" ".*"`    
#### 6.Enable RabbitMQ management console  
1. `sudo rabbitmq-plugins enable rabbitmq_management`   
2. `sudo chown -R rabbitmq:rabbitmq /var/lib/rabbitmq/`   
Visit : http://localhost:15672/ and login using user_name and user_password  

#### 7.Install Pika
`sudo pip3 install pika`  

#### 8.Install PyQt5
`sudo pip3 install pyqt5`  

#### 9. For testing purposes, add following users into RabbitMQ management portal:
   Username     Password     Status        Permissions
1. BitsOJ       root		    administrator       All
2. client 		    client      None		          	vhost
3. judge1		     judge1	  	management 	       	All

#### And you're done!!!!

## This is a test version of the BitsOJ system. Many security features are not pushed on the web for obvious reasons.   
## Download the executables for the complete software.
