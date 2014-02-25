class Meeting:
    """An OpenStack meeting."""

    def __init__(self, yaml_file):

        # create yaml object from yaml file. use it initialize following fields.

        self.proj_name = yaml.name
        self.uuid = yaml.uuid
        self.chair = yaml.chair
        self.descript = yaml.descript
        self.agenda = yaml.agenda # this is a list of topics

        # create schedule object
        self.schedule = newly_created_schedule_object

        # create checksum from something, perhaps entire object (this would 
        # be an easy way to check is anything has changed that needs to be
        # published)
        self.checksum = generated_checksum

    class Schedule:
        """A meeting schedule."""
        
        def __init__(self, time, day, irc, period):
            self.time = time
            self.day = day
            self.irc = irc
            self.period = period
