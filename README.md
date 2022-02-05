Elevator API
---

# Overview 

This project is a test task for elevator controller. It made as
flask API application with swagger interface. The project contains two 
different vertions of application.

## app1 
app1 is a simple database based application. 

Init database (only once)
```
./init_database.py

```

Start project
```
FLASK_APP=app1.py flask run
```

## app2
app2 mimics real eleavtor, using statemachine. Any script can be appied to emulate real
behavour like elevator speed, open doors, light switch and more. Simple script implemented to to emulate simple elevator. Files used:

1. elevator.py - emulates elevator device. It has basic device functions - light,door,engine to handle elevator moving.
2. controller.py - elevator controller. Controller implements elevator behavior - actions sequence.

Start project
```
FLASK_APP=app2.py flask run
```


## Elevator features (features.py)
According to task each elevator has number of features : num_persons,cargo_weight, speed and fllors it can visit. When elivator called it should fit requirments. features.py is a class to handle features matching

## Elevator scoring (score.py)
If number of elevators matches request, elevator with best serv will be choosen. score.py handles this selection, based on fastest serve, elevator speed. Very simple scoring system implemented. It may be improved to handle best fit

## Serve history
Each elevator keeps serve history. History may be used for monitoring.

## Logging and monitoring
This is test project and so Logger sends log to simple stdout. Project running proces may be seen in console, include state machine running progress, elevators states, requests monitor

Example:
```
INFO:root:[API]Call elevator according to filter {'num_persons': '4', 'cargo_weight': '0', 'floor': '12'}
INFO:elevator.elevator:[ELEVATOR][fast] got score 16
INFO:root:[API]Found elevator match with score 16
INFO:elevator.elevator:[ELEVATOR][slow] got score 25
INFO:root:[API]Found elevator match with score 25
DEBUG:elevator.elevator:[ELEVATOR][cargo] not match
INFO:elevator.elevator:[ELEVATOR][slow][GOTO]12 
DEBUG:root:[EVENT]Got status change slow => {'time': 1642879863, 'floor_from': 8, 'floor_to': 12, 'busy_till': 1642879899} 
INFO:elevator.elevator:[ELEVATOR][slow][TRIPTIME]36 
INFO:elevator.timer:[Timer]Start for period 36 sec (1642879899)
INFO:werkzeug:127.0.0.1 - - [22/Jan/2022 21:31:03] "POST /elevators HTTP/1.1" 200 -
INFO:root:[API]Call elevator according to filter {'num_persons': '4', 'cargo_weight': '0', 'floor': '12'}
INFO:elevator.elevator:[ELEVATOR][fast] got score 16
INFO:root:[API]Found elevator match with score 16
DEBUG:elevator.elevator:[ELEVATOR][slow] match but in use
DEBUG:elevator.elevator:[ELEVATOR][cargo] not match
INFO:elevator.elevator:[ELEVATOR][fast][GOTO]12 
DEBUG:root:[EVENT]Got status change fast => {'time': 1642879871, 'floor_from': 0, 'floor_to': 12, 'busy_till': 1642879889} 
INFO:elevator.elevator:[ELEVATOR][fast][TRIPTIME]18 
INFO:elevator.timer:[Timer]Start for period 18 sec (1642879889)

```

## Unittesting
In this project unittests driven development used. Most functions covered by unittests to minimize bugs. Some unittest still not fully implemented as it test only




