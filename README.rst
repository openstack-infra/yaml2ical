Gerrit-Powered-Agenda
=====================

This project aims to provide an easier way to manage OpenStack team meetings.
Currently, each team's meeting time and agenda are listed at:

  https://wiki.openstack.org/wiki/Meetings

This project replaces each meeting with well-defined YAML files.

This tool will run as a Jenkins job, so that each time a YAML meeting is
created, Jenkins will generate an iCal file. Additionally, user can also run
the program locally to check for conflict before submitting the meeting changes
for review.

Getting Started
===============

Running Locally from Command Line
---------------------------------

To test this project locally, you must have the following requirements
installed:

* Python 3.3+
* `iCalendar` python library
* `PyYaml` python library

Before running this tool, first edit some meeting YAML files in the meetings
directory. This directory already contains YAML files for the meetings
found on the `Meetings <https://wiki.openstack.org/wiki/Meetings>`_ wiki page.
To create a new meeting YAML file, read the `YAML Meeting File` section below.

To start with, we need to clone the repository to a local directory. Afterward,
`cd` into the directory where the `jobs.py` script is found.

  ::

    $ git clone https://git.openstack.org/cgit/openstack-infra/gerrit-powered-agenda
    $ cd gerrit-powered-agenda/gerrit-powered-agenda/

The different command line options are as follows.  For help, use `-h`
(or `--help`) to show a list of options and exit.

  ::

    $ python jobs.py -h

The `-t TEST` (or `--test TEST`) is used to execute a test. The valid values
for `TEST` are `check`, `gate` and `post`. It'd be a good idea to run a quick
check job to test for conflicts before pushing for review.

  ::

    $ python jobs.py -t check
    $ python jobs.py -t gate
    $ python jobs.py -t post

For converting YAML files to iCal files, there are four flags to consider:

* Use the `-y YAML_DIR` (or `--yamldir YAML_DIR`) to specify the path to the
  directory `YAML_DIR` where the YAML files are located. The default
  `YAML_DIR` is `meetings` when this flag is not provided.
* Use the `-i ICAL_DIR` (or `--icaldir ICAL_DIR`) to specify the path to the
  directory `ICAL_DIR` where the iCals files will be written to.
* Use the `-m MEETING_LIST_FILE` (or `--meetings MEETING_LIST_FILE`) to write
  selected YAML files in `MEETING_LIST_FILE` to `ICAL_DIR`.

  * Note: `MEETING_LIST_FILE` consists of names of YAML files per line.
* Add the `-c` (or `--convert`) to convert.

The following are a few scenarios:

* Read all the YAML files in meetings and output iCal files to iCals folder:

  ::

    $ cd gerrit-powered-agenda/gerrit-powered-agenda/
    $ mkdir ../iCals
    $ python jobs.py -i ../iCals -c

* Read all the YAML files in myYAML folder and output iCal files to iCals
  folder:

  ::

    $ cd gerrit-powered-agenda/gerrit-powered-agenda/
    $ mkdir ../iCals
    $ python jobs.py -y ../myYAML -i ../iCals -c

* Read myMeetings.txt, select the YAML file listed in there from myYAML
  directory, convert these files and write them to iCals folder:

  ::

    $ cd gerrit-powered-agenda/gerrit-powered-agenda/
    $ mkdir ../iCals
    $ python jobs.py -y ../myYAML -m ../myMeetings.txt -i ../iCals -c

Running as a Jenkins Job
------------------------

When this project is complete, this tool will run as a Jenkins job. A developer
wishing to modify existing meetings or create a new meeting will push the
respecitve YAML file to Gerrit, which will then be reviewed. When the review
passes, Jenkins will run this tool to generate iCal files.

YAML Meeting File
=================

Refer to the meetings page on the OpenStack Wiki for a list of meetings:

  https://wiki.openstack.org/wiki/Meetings

For a list of yaml meeting files, visit

  https://git.openstack.org/cgit/openstack-infra/gerrit-powered-agenda/tree/meetings

Each meeting consists of:

* `project` -- the name of the project
* `schedule` -- a list of schedule each consisting of

  * `time` -- time string in UTC
  * `day` -- the day of week the meeting takes place
  * `irc` -- the irc room in which the meeting is held
  * `frequency` -- frequent occurence of the meeting
* `chair` -- name of the meeting's chair
* `description` -- a paragraph description about the meeting
* `agenda` -- a paragraph consisting of the bulleted list of topics

The file name should be a lower-cased, hyphenated version of the meeting name,
ending with `.yaml` or `.yml`. For example, `Keystone team meeting` should be
saved under `keystone-team-meeting.yml`.

Example
-------

This is an example for the yaml meeting for Nova team meeting.  The whole file
will be import into Python as a dictionary.

* The project name is shown below.

  ::

    project:  Nova Team Meeting

* The schedule is a list of dictionaries each consisting of `time` in UTC,
  `day` of the week, the `irc` meeting room, and the `frequency` of the
  meeting. Options for the `frequency` are `weekly`, `biweekly-even`, and
  `biweekly-odd` at the moment.

  ::

    schedule:
        - time:       '1400'
          day:        Thursday
          irc:        openstack-meeting-alt
          frequency:  weekly

        - time:       '2100'
          day:        Thursday
          irc:        openstack-meeting
          frequency:  weekly

* The chair is just a one liner. The might be left empty if there is not a
  chair.

  ::

    chair:  Russell Bryant

* The project description is as follows.  Use `>` for parapraphs where new
  lines are folded, or `|` for paragraphs where new lines are preserved.

  ::

    description:  >
        This meeting is a weekly gathering of developers working on OpenStack.
        Compute (Nova). We cover topics such as release planning and status,
        bugs, reviews, and other current topics worthy of real-time discussion.

* The project agenda is show below.  Note the use of `|` to treat the agenda as
  a paragraph where newlines are perserved. Currently we plan to use * to
  format the list of item so it is similar to the wiki format. Add additional
  for each level of sublist items. I.e. `**` for a sub-item and `***` for a
  sub-item of a sub-item.

  ::

    agenda:  |
        * General annoucement
        * Sub-teams
        * Bugs
        * Blueprints
        * Open discussion
