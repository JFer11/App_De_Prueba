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
    