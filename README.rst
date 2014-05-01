Gerrit-Powered-Agenda
=====================

This project aims to provide an easier way to manage OpenStack team meetings.
Currently, each team's meeting time and agenda are listed at:

  https://wiki.openstack.org/wiki/Meetings.

This project replaces each meeting with well-defined YAML files.

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

  `$ python jobs.py`

in the gerrit-powered-agenda directory.

The generated iCal files will appear in the /icals directory.

As a Jenkins Job
----------------

When this project is complete, this tool will run as a Jenkins job. A developer
wishing to create a meeting will push a YAML file to Gerrit, which will then be
reviewed. If the review passes, Jenkins will run this tool to generate ical
files.

YAML Meeting File
=================

Refer to the meetings page on the OpenStack Wiki for a list of meetings:

  https://wiki.openstack.org/wiki/Meetings

For a list of yaml meeting files, visit

  https://git.openstack.org/cgit/openstack-infra/gerrit-powered-agenda/tree/meetings

Each meeting consists of:

* `project` -- the name of the project
* `schedule` -- a list of schedule each consisting of
  - `time` -- time string in UTC
  - `day` -- the day of week the meeting takes place
  - `irc` -- the irc room in which the meeting is held
  - `frequency` -- frequent occurence of the meeting
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

* The chair is just a one liner. The might be left empty if there is not a chair.

  ::

    chair:  Russell Bryant

* The project description is as follows.  Use `>` to for the parapraph so new
  lines are folded.

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

    agenda: |
        * general annoucement
        * sub-teams
        * bugs
        * blueprints
        * open discussion
