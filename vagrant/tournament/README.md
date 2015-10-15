# Project 2: Tournament Results
### by Steven Wooding
Tournament Results project, part of the Udacity [Full Stack Web Developer
Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## What it is and does
A Python program and PostgreSQL database that produces pairings and standings of players
taking part in a tournament run under the
[Swiss-system](https://en.wikipedia.org/wiki/Swiss-system_tournament) of organising a
tournament.

## Required Libraries and Dependencies
The project code requires Python 2.7.x and that the [Psycopg](http://initd.org/psycopg/)
package is available on your system for import. It also requires PostSQL 9.3 or higher.

You can run the project in a Vagrant managed virtual machine (VM) which includes all the
required dependencies (see below for how to run the VM). For this you will need
[Vagrant](https://www.vagrantup.com/downloads) and
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) software installed on your
system.

## Project contents
This project consists for the following files:

* tournament.sql - Creates the database, defines tables and views
* tournament.py - Contains functions that implement the Swiss-system
* tournament_test.py - Contains unit tests to test the functions in tournament.py

## How to Run the Project
Download the project zip file to you computer and unzip the file. Or clone this
repository to your desktop.

Open the text-based interface for your operating system (e.g. the terminal
window in Linux, the command prompt in Windows).

Navigate to the project directory and then enter the `vagrant` directory.

### Bringing the VM up
Bring up the VM with the following command:

```bash
vagrant up
```

The first time you run this command it will take awhile, as the VM image needs to
be downloaded.

You can then log into the VM with the following command:

```bash
vagrant ssh
```

More detailed instructions for installing the Vagrant VM can be found
[here](https://www.udacity.com/wiki/ud197/install-vagrant).

### Running the tournament unit tests
Once inside the VM, navigate to the tournament directory with this command:

```bash
cd /vagrant/tournament
```

You can then run the unit tests for the project with the following command:

```bash
python tournament_test.py
```

All tests should pass successfully.

### Shutting the VM down
When you are finished with the VM, press `Ctrl-D` to logout of it and shut it down
with this command:

```bash
vagrant halt
```

## Extra Credit Description
The Swiss-system algorithm avoids rematches between players during a tournament.

## Miscellaneous
This README document is based on a template suggested by PhilipCoach in this
Udacity forum [post](https://discussions.udacity.com/t/readme-files-in-project-1/23524).

The function all_pairs() was written by gatoatigrado (Stack Overflow username) and
the original can be found [here](http://stackoverflow.com/a/13020502). I have explained
how this function works and why it is needed in the docstring for the function. I have
also added comments to the code.