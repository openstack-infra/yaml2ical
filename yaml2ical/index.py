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

import datetime
import jinja2
import logging
import os
import os.path


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

    with open(output_file, "w") as out:
        out.write(template.render(meetings=meetings,
                                  timestamp=datetime.datetime.utcnow()))

    logging.info('Wrote %d meetings to index.' % (len(meetings)))
