To turn off and on:

(1) Send command, set the sensor with ID A160 to sleep:
AA B4 06 01 00 00 00 00 00 00 00 00 00 00 00 A1 60 08 AB 
Sensor with ID A160 response:
AA C5 06 01 00 00 A1 60 08 AB

(2) Send command, set the sensor with ID A160 to work:
AA B4 06 01 01 00 00 00 00 00 00 00 00 00 00 A1 60 09 AB 
Sensor with ID A160 response:
AA C5 06 01 01 00 A1 60 09 AB

(3) Send command, query the working mode of the sensor with ID A160: 
AA B4 06 00 00 00 00 00 00 00 00 00 00 00 00 A1 60 07 AB

Sensor with ID A160 response, show it is in working mode:
AA C5 06 00 01 00 A1 60 08 AB
Or reply Sensor with ID A160 response, show it is NOT in working mode:
AA C5 06 00 00 00 A1 60 07 AB 

Notes: The data is stable when the sensor works after 30 seconds; 
The fan and laser stop working in sleeping mode.
