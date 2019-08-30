# BitsOJ
Offline Judge for competitive programming contests.  

## Setup
### Setting up RabbitMQ server:

### Install Pika


## Goals:
### Requirements  
1.Python3.x  
2.Subprocess Module  
3.~Socket Programming~  
4.Pika + RabbitMQ  
5.PyQt Module(Might change)  

### Check List
#### Admins
1.Can set problems, their time limits and IO files.  
2.Can generate users profiles.  
3.Can manually view and judge user solutions.  
4.Can block users from the contest.  
5.Can start and stop the contest, and set its duration.  
6.Can broadcast messages and respond to queries.  

#### Users  
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
0.Manage connections.  (Work in progress : 30%)    
1.Verify user details.  (Work in progress : Enqueued)  
2.Implement client data queue.  (Work in progress : Enqueued)  
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
