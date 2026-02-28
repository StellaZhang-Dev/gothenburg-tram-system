# Lab 3 peer review

### Reviewing group number: 106
### Submitting group number: 148

## Section 1: Core functionality

* Does the application run? **Yes.**
* Does the application display the complete map of tram lines? **Yes.**
* Is it possible to query shortest path between any two points? **Yes.**
* Does the application deal with changes correctly? **No.**
* Does the application show current traffic information? **No.**
* Does the application correctly handle invalid input? **Yes. Some optional functionality was added to handle incorrect capitalization and removing the need for the characters åäö.**

## Section 2: Code quality

Overall great code quality, with interesting solutions and decisions! We particularly enjoy the implementation of normalize_stop_name() and resolve_stop_name(), which help massively with the user experience. Furthermore, the decision to calculate the distance yourself is admirable. Furthermore, the code is nicely written with blank lines which helps with readability. Short and concise comments helps the programmer understand what functions and methods aim to achieve.  
We would like to see the implementation of specialize_stops_to_lines(), as well as the parameters changetime and changedistance being used. With these functions implemented and used in the show_shortest() function, the application should be able to deal with changes correctly.  
The code from lab 2 seems to have been reused properly, and there doesn't seem to be any boilerplate code.  
The dijkstra() function has been implemented and used as intended, as far as we can tell. The cost parameter is used to get the shortest and the quickest path.

## Section 3: Screenshots

![Web application screenshot](web_app_screenshot.png)
![Show shortest function 1/3](show_shortest_1.png)
![Show shortest function 2/3](show_shortest_2.png)
![Show shortest function 3/3](show_shortest_3.png)
