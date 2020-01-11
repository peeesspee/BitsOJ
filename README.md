# BitsOJ
Offline Judge for competitive programming contests.  
<<<<<<< HEAD

## Setup
### Setting up backend services:
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
1. BitsOJ       root		administrator   All
2. client 		client      None			vhost
3. judge1		judge1		management 		All

#### And you're done!!!!

## Goals:
=======
>>>>>>> master
### Requirements  
1.Python3.x  
2.Subprocess Module  
3.~Socket Programming~  
4.Pika + RabbitMQ  
5.PyQt Module(Might change)  

### Check List
#### Admins
1.Can set problems, their time limits and IO files.  
2.Can generate users profiles.[DONE]    
3.Can manually view and judge user solutions.  
4.Can block users from the contest.[DONE]  
5.Can start and stop the contest, and set its duration.[PROGRESS 50%]    
6.Can broadcast messages and respond to queries.[DONE]  

#### Users  
<<<<<<< HEAD
0.Can Login[DONE]
1.Can view problems.[DONE]  
2.Can submit solution, and view result.[DONE]   
3.Can view their submission results.[DONE]   
4.Can send queries.[DONE]   
5.Can request a rejudge and get NO as a reply.[DONE]  
6.Can view ranklist locally.[NOT YET STARTED]  
=======
1.Can view problems.  
2.Can submit solution, and view result.   
3.Can view their submission results.   
4.Can send queries.   
5.Can request a rejudge and get NO as a reply.  
6.Can view ranklist locally.  
>>>>>>> master
  
#### OJ:Interface  
1.Assign a run ID to each code.[DONE]  
2.Execute the code in a sandbox, according to their run IDs.[PROGRESS 50%]  
3.Allow for rejudge but assign a new run ID.[CANCELLED]  
4.Allow only one active session per user ID.[NOT YET STARTED]  
5.Implement time limit per solution.[IN PROGRESS]  
6.Update the result in database.[DONE]  
7.Maintain a scoreboard.[NOT YET STARTED]  
8.Maintain 1 submission per minute rule, to avoid spam.[NOT YET STARTED]  
9.As soon as contest time is over, it must not accept any new solutions.[IN PROGRESS]  

#### OJ:Innards
<<<<<<< HEAD
0.Manage connections.[DONE]    
1.Verify user details.[DONE]  
2.Implement client data queue.[DONE]  
3.Manage Judge queue.[DONE]  
4.Database manager[DONE]  
=======
0.Manage connections.  (Work in progress : 30%)    
1.Verify user details.  (Work in progress : Enqueued)  
2.Implement client data queue.  (Work in progress : Enqueued)  
3.Manage Judge queue.  (Scheduled for later)  
4.Database manager  (Scheduled for later)  
>>>>>>> master

#### Error Interface
0.If no judges are active (Critical)  
1.One of the judges goes down (Moderate)  
2.Client disconnects (Trivial)  
3.Connection establishment errors (Critical)  

#### Future updates  
1.Multiple judges.  
2.Allow Interactive problems.  
