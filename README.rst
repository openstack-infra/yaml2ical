=========
yaml2ical
=========

This tool converts a series of meeting descriptions in YAML format into one
or several .ics files suitable for calendaring. It checks for scheduling
conflicts in specific locations.

Rationale
=========

yaml2ical aims to provide an easier way to manage online team meetings.

This project allows to define each meeting with well-defined YAML files,
which can be code-reviewed, then continuously-integrated into .ics files for
general consumption.

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
directory. To create a new meeting YAML file, read the `YAML Meeting File`
section below.

  ::

    $ pip install yaml2ical
    $ yaml2ical
    usage: yaml2ical [-h] -y YAML_DIR (-i ICAL_DIR | -o ICALFILE)
                 [-t INDEX_TEMPLATE] [-w INDEX_OUTPUT] [-n CALNAME]
                 [-d CALDESCRIPTION] [-f]

    A tool that automates the process for testing, integrating, and
    publishing changes to online meeting schedules.

    optional arguments:
      -h, --help            show this help message and exit
      -y YAML_DIR, --yamldir YAML_DIR
                            directory containing YAML to process
      -i ICAL_DIR, --icaldir ICAL_DIR
                            output directory (one file per meeting)
      -o ICALFILE, --output ICALFILE
                            output file (one file for all meetings)
      -t INDEX_TEMPLATE, --indextemplate INDEX_TEMPLATE
                            generate an index from selected meetings
      -w INDEX_OUTPUT, --indexoutput INDEX_OUTPUT
                            output index file
      -n CALNAME, --name CALNAME
                            name of calendar to set within the ical
      -d CALDESCRIPTION, --description CALDESCRIPTION
                            description of calendar to set within the ical
      -f, --force           remove/overwrite previous output files


The following are a few scenarios:

Generate .ics files locally from existing yaml meeting files:

  ::

    $ yaml2ical -y meetings/ -i icals/

The generated .ics files are not tracked in this git repository,
but they are available locally to import into your calendar. Note,
to remove stale .ics files, use the ``--force`` argument:

  ::

    $ ls icals/
    Barbican Meeting-b58d78a4.ics
    Ceilometer Team Meeting-9ed7b5b4.ics
    Chef Cookbook Meeting-2418b331.ics

With each .ics file looking something similar to:

  ::

    $ cat icals/Barbican\ Meeting-b58d78a4.ics
    BEGIN:VCALENDAR
    VERSION:2.0
    PRODID:-//yaml2ical agendas//EN
    BEGIN:VEVENT
    SUMMARY:Barbican Meeting (openstack-meeting-alt)
    DTSTART;VALUE=DATE-TIME:20141006T200000Z
    DURATION:PT1H
    DESCRIPTION:Project:  Barbican Meeting\nChair:  jraim\nIRC:  openstack-meet
     ing-alt\nAgenda:'* malini - update on Security Guide documentation\n\n  *
     alee_/atiwari - Crypto plugin changes\n\n  * arunkant - Target support in
     barbican policy enforcement\n\n  * jaraim - Support for debug mode start i
     n barbican\, can be merged?\n\n  '\n\nDescription:  The Barbican project t
     eam holds a weekly team meeting in\n#openstack-meeting-alt:\n* Weekly on M
     ondays at 2000 UTC\n* The blueprints that are used as a basis for the Barb
     ican project can be\n  found at https://blueprints.launchpad.net/barbican\
     n* Notes for previous meetings can be found here.\n* Chair (to contact for
      more information): jraim (#openstack-barbican @\n  Freenode)\n
    RRULE:FREQ=WEEKLY
    END:VEVENT
    END:VCALENDAR


YAML Meeting File
=================

Each meeting consists of:

* ``project``: the name of the project [MANDATORY]
* ``schedule``: a list of schedule each consisting of

  * ``time``: time string in UTC [MANDATORY]
  * ``duration``: duration of the meeting in minutes; defaults to 60
  * ``start_date``: the date the first meeting takes place on or after.
      Format `YYYYMMDD`, all values must be zero-padded.
  * ``day``: the day of week the meeting takes place [MANDATORY]
  * ``irc``: the irc room in which the meeting is held [MANDATORY]
  * ``frequency``: frequent occurrence of the meeting [MANDATORY]
  * ``skip_dates``: A set of dates that the meeting **DOES NOT** happen on

    * ``skip_date``: Skip the meeting for specified date.
      Format as ``start_date``
    * ``reason``: A comment for why the meeting was skipped
* ``chair``: name of the meeting's chair [MANDATORY]
* ``description``: a paragraph description about the meeting [MANDATORY]
* ``agenda_url``: a link to the agenda page for the meeting
* ``project_url``: a link to the project home page for the meeting

The file name should be a lower-cased, hyphenated version of the meeting name,
ending with ``.yaml`` . For example, ``Keystone team meeting`` should be
saved under ``keystone-team-meeting.yaml``.

Any other values listed in the YAML file are also available for use in
templates, making it easy to build links to agenda pages for the
meeting or logs of past meetings. In the template file, use
``meeting.extras.name`` to access the value.


Example 1
---------

This is an example for the yaml meeting for Nova team meeting.  The whole file
will be import into Python as a dictionary.

* The project name is shown below.

  ::

    project:  Nova Team Meeting

* The schedule is a list of dictionaries each consisting of `time` in UTC,
  `day` of the week, the `irc` meeting room, and the `frequency` of the
  meeting. Options for the `frequency` are `weekly`, `biweekly-even`, and
  `biweekly-odd` at the moment.

  `biweekly-odd` are weeks where the ISO week number is an odd value.
  Correspondingly `biweekly-even` are weeks where the ISO week number is even.
  This unfortunately will break down on the transition from 2015 to 2016 as
  2015 has 53 ISO weeks (an odd value) and then the first week of 2016 is week
  1 (also an odd value).

  ::

    schedule:
        - time:       '1400'
          day:        Thursday
          irc:        openstack-meeting-alt
          frequency:  biweekly-even

        - time:       '2100'
          day:        Thursday
          irc:        openstack-meeting
          frequency:  biweekly-odd

* The chair is just a one liner.

  ::

    chair:  Russell Bryant

* The project description is as follows.  Use `>` for paragraphs where new
  lines are folded, or `|` for paragraphs where new lines are preserved.

  ::

    description:  >
        This meeting is a weekly gathering of developers working on OpenStack.
        Compute (Nova). We cover topics such as release planning and status,
        bugs, reviews, and other current topics worthy of real-time discussion.

* An extra property containing the agenda for the meeting is saved in
  ``agenda_url`` and can be accessed in the template file as
  ``meeting.extras.agenda_url``.

  ::

    agenda_url: https://wiki.openstack.org/wiki/Meetings/Nova

* An extra property containing the project URL is saved in
  ``project_url`` and can be accessed in the template file as
  ``meeting.extras.project_url``.

  ::

    project_url: https://wiki.openstack.org/wiki/Nova

* An extra property containing the MeetBot #startmeeting ID for the project is
  saved in ``meeting_id`` and can be accessed in the template file as
  ``meeting.extras.meeting_id``.

  ::

    meeting_id: nova


Example 2
---------

The following shows a complete YAML file for the IRC meetings for "example
project".  The project starts holding weekly meetings from October 1st, the
project team has a "face to face" meeting on the 26th of October so that IRC
meeting should be ommited from the ical schedule

* This YAML

  ::

    project: Example Project Meeting
    project_url: https://wiki.openstack.org/wiki/Example
    agenda_url: https://wiki.openstack.org/wiki/Meetings/Example
    meeting_id: example
    chair: A. Random Developer
    description:  >
        This meeting is a weekly gathering of developers working on Example
        project.
    schedule:
        - time:       '2100'
          day:        Monday
          irc:        openstack-meeting
          start_date: 20151001
          frequency:  weekly
          skip_dates:
          - skip_date: 20151026
            reason: Face 2 Face meeting at some location

* Is converted into this iCal

  ::

    BEGIN:VCALENDAR
    VERSION:2.0
    PRODID:-//yaml2ical agendas//EN
    BEGIN:VEVENT
    SUMMARY:CANCELLED: Example Project Meeting (20151026T210000Z)
    DTSTART;VALUE=DATE-TIME:20151026T210000Z
    DURATION:PT1H
    DESCRIPTION:Face 2 Face meeting at some location
    LOCATION:#openstack-meeting
    END:VEVENT
    BEGIN:VEVENT
    SUMMARY:Example Project Meeting
    DTSTART;VALUE=DATE-TIME:20151005T210000Z
    DURATION:PT1H
    EXDATE:20151026T210000Z
    DESCRIPTION:Project:  Example Project Meeting\nChair:  A. Random Developer
     \nDescription:  This meeting is a weekly gathering of developers working o
     n Example project.\n\nAgenda URL:  https://wiki.openstack.org/wiki/Meeting
     s/Example\nProject URL:  https://wiki.openstack.org/wiki/Example
    LOCATION:#openstack-meeting
    RRULE:FREQ=WEEKLY
    END:VEVENT
    END:VCALENDAR
