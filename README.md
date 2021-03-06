 
 To run the project:
 ---
 To run app, before: ```export FLASK_APP=training.app```

 Then: ```flask run```
 

 To enable a local email server
 ---
 To use an emulated email server, Python provides one that is very handy that you can start in a
 second terminal with the following command:
 
 ```$ python -m smtpd -n -c DebuggingServer localhost:8025```
 
 Redis server
 ---
 ##### To install redis-server package:
 ```$ sudo apt-get install redis-server```
 
 ##### To ran redis-server:
 First the prompt has to be in te root directory and with your virtual environment activated.
 Then:
 ```$ rq worker my-app-tasks```
 Remember that "my-app-tasks" is the name for the redis server that the worker will be connected.
    
 
 To access postgres database:
 ---
 ```sudo -u postgres psql```
  
 How to run tests:
 ---
 
 First the prompt has to be in te root directory (before training) and with your virtual environment activated.
 
 Then:
 
 1. First option:
 
    For one test: ```FLASK_ENV=testing python -m unittest training/tests/test_basic.py```
    
    Or to run all tests: ```FLASK_ENV=testing python -m unittest training/tests/*```
 2. Second option:
    
    For one test: ```./bin/test training/tests/test_basic.py```
    
    Or to run all tests: ```./bin/test```
    
 
 IMPORTANT: First option run 46 tests and one fails, and Second Option run 45 successfully
 
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
 
