# BitsOJ
Offline Judge for competitive programming contests.  

## Setup
### Setting up backend services:
#### 1.Update the system:  
`sudo apt-get update`  
`sudo apt-get upgrade`  
#### 2.Install ErLang
`cd ~  `  
`wget http://packages.erlang-solutions.com/site/esl/esl-erlang/FLAVOUR_1_general/esl-erlang_20.1-1~ubuntu~xenial_amd64.deb`  
`sudo dpkg -i esl-erlang_20.1-1\~ubuntu\~xenial_amd64.deb`  
`erl`  
#### 3.Install RabbitMQ  
Add the Apt repository to your Apt source list directory (/etc/apt/sources.list.d):  
`echo "deb https://dl.bintray.com/rabbitmq/debian xenial main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list`  
Next add our public key to your trusted key list using apt-key:   
`wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -`  
`sudo apt-get update`  
`sudo apt-get install rabbitmq-server`  
#### 4.Start the server:  
`sudo systemctl start rabbitmq-server.service`  
`sudo systemctl enable rabbitmq-server.service`  
To check status of RabbitMQ server,  
`sudo rabbitmqctl status`  
#### 5.Create a new admin account  
You should give custom values to user_name and user_password in the next command:  
`sudo rabbitmqctl add_user user_name user_password`     
`sudo rabbitmqctl set_user_tags user_name administrator`    
`sudo rabbitmqctl set_permissions -p / user_name ".*" ".*" ".*"`    
#### 6.Enable RabbitMQ management console  
`sudo rabbitmq-plugins enable rabbitmq_management`   
`sudo chown -R rabbitmq:rabbitmq /var/lib/rabbitmq/`   
Visit : http://localhost:15672/ and login using user_name and user_password  

#### 7.Install Pika
`pip3 install pika`  

#### 8.Install PyQt5
`pip3 install pyqt5`  

#### 9. For testing purposes, add following users into RabbitMQ management portal:
   Username     Password     Status        Permissions
1. BitsOJ       root		administrator   All
2. client 		client      None			vhost
3. judge1		judge1		management 		All

#### And you're done!!!!

## Goals:
### Requirements  
1.Python3.x  
2.Subprocess Module  
3.~Socket Programming~  
4.Pika + RabbitMQ  
5.PyQt Module  
6.~Kivy~  


### Check List
#### Admins
1.Can set problems, their time limits and IO files.  
2.Can generate users profiles.  
3.Can manually view and judge user solutions.  
4.Can block users from the contest.  
5.Can start and stop the contest, and set its duration.  
6.Can broadcast messages and respond to queries.  

#### Users  
0.Can Login
1.Can view problems.  
2.Can submit solution, and view result.   
3.Can view their submission results.   
4.Can send queries.   
5.Can request a rejudge and get NO as a reply.  
6.Can view ranklist locally.  
  
#### OJ:Interface  
1.Assign a run ID to each code.  
2.Execute the code in a sandbox, according to their run IDs.  
3.Allow for rejudge but assign a new run ID.  
4.Allow only one active session per user ID.  
5.Implement time limit per solution.  
6.Update the result in database.  
7.Maintain a scoreboard.  
8.Maintain 1 submission per minute rule, to avoid spam.  
9.As soon as contest time is over, it must not accept any new solutions.  

#### OJ:Innards
0.Manage connections.  (Work in progress : 70%)    
1.Verify user details.  (Work in progress : 30%)  
2.Implement client data queue.  (Completed)  
3.Manage Judge queue.  (Scheduled for later)  
4.Database manager  (Scheduled for later)  

#### Error Interface
0.If no judges are active (Critical)  
1.One of the judges goes down (Moderate)  
2.Client disconnects (Trivial)  
3.Connection establishment errors (Critical)  

#### Future updates  
1.Multiple judges.  
2.Allow Interactive problems.  
