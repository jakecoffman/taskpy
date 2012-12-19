taskpy
======

Taskpy is a Continuous Integration web server written in Python focusing on the DRY principle. Taskpy's design is based on Jenkins, however it aims to make management of jobs easier by extracting custom steps into "tasks" and making the plug-in architecture obsolete. If you aren't familiar with Jenkins, think of Taskpy as a glorified cron with a web interface.

Taskpy uses flask for the web framework and server.

Taskpy is currently in early development, but planned features are:

* Each job contains multiple tasks
* Tasks take parameters and produce outputs which can be piped to the next task within a job or hard-coded
* Multiple language support for tasks (Python, Ruby, etc)
* Triggers are units just like tasks and can be added to jobs
* Executing a job produces a run page which can be modified by the tasks

Here's a demo: http://youtu.be/LmBeipoZ5WU