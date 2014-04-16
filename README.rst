Gerrit-Powered-Agenda
=====================

This project aims to provide an easier way to manage OpenStack team meetings.
Currently, each team's meeting time and agenda are listed at:
https://wiki.openstack.org/wiki/Meetings. This project replaces each meeting
with well-defined YAML files.

This tool will run as a Jenkins job, so that each time a YAML meeting is
created, Jenkins will generate an iCal file.

Getting Started
===============

Running locally
---------------

To test this project locally, you must have the following requirements
installed:

* Python 3.3+
* icalendar python library
* PyYaml

Before running this tool, first place some meeting YAML files in the meetings
directory. This directory already contains some meetings. To create your own
meeting, see the meetings/README file.

To run this tool, run

$ python jobs.py

in the gerrit-powered-agenda directory.

The generated iCal files will appear in the /icals directory.

As a Jenkins Job
----------------

When this project is complete, this tool will run as a Jenkins job. A developer
wishing to create a meeting will push a YAML file to Gerrit, which will then be
reviewed. If the review passes, Jenkins will run this tool to generate ical
files.
