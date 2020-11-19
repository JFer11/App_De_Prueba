 To use an emulated email server, Python provides one that is very handy that you can start in a
 second terminal with the following command:
 
 ```$ python -m smtpd -n -c DebuggingServer localhost:8025```
 
 
 To install redis-server package:
 ```$ sudo apt-get install redis-server```
 
 To ran redis-server:
 First the prompt has to be in te root directory and with your virtual environment activated.
 Then:
 ```$ rq worker my-app-tasks```
 Remember that "my-app-tasks" is the name for the redis server that the worker will be connected.
    
 To access postgres database:
 ```sudo -u postgres psql```
 
 Migrations:
 ---
 Only the first time, we follow step number one:
 1. With an empty database:
 ```flask db init```
 This creates a flask migrations repository
 
 2. Then, with your models already created
 ```flask db migrate -m "custom_msg"```
 At this point, flask will realize that there were changes on the schema.
 
 3. Finally, run  ```flask db upgrade``` to modify detected migrations.
 
 If new changes appear, go back to step 2 and repeat.