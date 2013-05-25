===============
Fastfood module
===============
This module aims to replace the kettle process
currently used at YouTellMe


============
Architecture
============

Fastfood consists of three layers

1. Transformation (The highest level describing which steps to execute)
2. Goal
3. Magic (Responsible for automagically creating a transformation based on the specified goal)

The YouTellMe interface will
- Display the basic feed information
- Layer the magics choices
- Write based on user input to a transformation 
