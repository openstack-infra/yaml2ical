# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import division

import datetime
import jinja2
import logging
import os
import os.path


def batch_meetings(meetings, batch_size):
    """Batches the meetings to be consumed by the jinja2 'batch' filter.

    This will pivot the meeting list into a virtual number of columns.  This
    can be used in a jinja template like:

    {% for column in batch_meetings(meetings, 4)|batch(4) %}

    So the list:
    [A, B, C, D, E, F , G, H, I]

    Is returned as:
    [A, D, F, H,   B, E, G, I,   C]]

    Or another way of looking at it is:
    [A, D, F, H,
     B, E, G, I,
     C]]

    And displays as:
    A D F H
    B E G I
    C

    Rather than:
    A B C D
    E F G H
    I

    :param meetings: An iterable
    :param batch_size: Number of columns to split up the output into
    :returns: A list that has 'pivoted' the meetings input

    """
    if batch_size <= 0:
        return meetings
    col_length = (len(meetings) // batch_size) + 1
    new_meetings = [None] * len(meetings)
    src = 0

    for row in range(batch_size):
        for col in range(col_length):
            dest = col * batch_size + row
            if dest >= len(meetings):
                break
            new_meetings[dest] = meetings[src]
            src += 1

    # Sanity check
    if all(meetings):
        assert all(new_meetings), "Empty item found in: {}".format(
            new_meetings)
    return new_meetings


def convert_meetings_to_index(meetings, template, output_file):
    """Creates index file from list of meetings.

    :param meetings: list of meetings to convert
    :param template: jinja2 template to use
    :param output_file: output index file

    """

    (template_dir, template_file) = os.path.split(template)
    loader = jinja2.FileSystemLoader(template_dir)
    env = jinja2.environment.Environment(trim_blocks=True, loader=loader)
    template = env.get_template(template_file)
    template.globals['batch_meetings'] = batch_meetings

    with open(output_file, "w") as out:
        out.write(template.render(meetings=meetings,
                                  timestamp=datetime.datetime.utcnow()))

    logging.info('Wrote %d meetings to index.' % (len(meetings)))
