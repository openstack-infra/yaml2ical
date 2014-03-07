import pprint

class Meeting:
    """An OpenStack meeting."""

    def __init__(self, yaml):

        # create yaml object from yaml file. use it initialize following fields.
        self.project = yaml['project']
        self.chair = yaml['chair']
        self.description = yaml['description']
        self.agenda = pprint.pformat(yaml['agenda']) # this is a list of topics

        # create schedule object
        schedule = yaml['schedule'][0]
        self.schedule = Schedule(schedule['time'], schedule['day'], schedule['irc'], schedule['period'])

    def display(self):
        return "project:\t%s\nchair:\t%s\ndescription:\t%s\nagenda:\t%s\nschedule:\t%s" % (self.project, self.chair, self.description, self.agenda, self.schedule.display())

class Schedule:
    """A meeting schedule."""
        
    def __init__(self, time, day, irc, period):
        self.time = time
        self.day = day
        self.irc = irc
        self.period = period

    def display(self):
        return "Schedule:\n\ttime:\t%s\n\tday:\t%s\n\tirc:\t%s\n\tperiod:\t%s\n" % (self.time, self.day, self.irc, self.period)
