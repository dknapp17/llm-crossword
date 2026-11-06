Plan for app:
Initial State:

1) User clicks solve puzzle
2) python passes 'select 1 Across' to component
3) component sends data to python on completion
4) python 'solves' the clue
5) python passes 'enter clue' to component
6) exolve enters text and sends data to python on completion
7) python checks if puzzle complete
8) if puzzle not complete: 

Better State:
1) Python only enters the clue if there is enough confidence in the answer
