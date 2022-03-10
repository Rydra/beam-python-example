#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""A word-counting workflow."""

# pytype: skip-file

# beam-playground:
#   name: WordCount
#   description: An example that counts words in Shakespeare's works.
#   multifile: false
#   pipeline_options: --output output.txt
#   context_line: 44
#   categories:
#     - Combiners
#     - Options
#     - Quickstart

import logging
import re

import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


class WordExtractingDoFn(beam.DoFn):
  """Parse each line of input text into words."""
  def process(self, element):
    """Returns an iterator over the words of this element.
    The element is a line of text.  If the line is blank, note that, too.
    Args:
      element: the element being processed
    Returns:
      The processed element.
    """
    return re.findall(r'[\w\']+', element, re.UNICODE)


def run(save_main_session=True):
  """Main entry point; defines and runs the wordcount pipeline."""

  options = PipelineOptions([
    "--runner=FlinkRunner",
    "--flink_master=localhost:8081",
    "--flink_version=1.13",
    "--environment_type=EXTERNAL",
    "--environment_config=localhost:50000"
  ])

  # We use the save_main_session option because one or more DoFn's in this
  # workflow rely on global context (e.g., a module imported at module level).
  # pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

  with beam.Pipeline(options=options) as p:
    (p
     | 'Create words' >> beam.Create(['to be or not to be'])
     | 'Split words' >> beam.FlatMap(lambda words: words.split(' '))
     | 'Write to file' >> beam.Map(print)
     )

  # The pipeline will be run on exiting the with block.
  # with beam.Pipeline(options=pipeline_options) as p:
  #
  #   # Read the text file[pattern] into a PCollection.
  #   lines = p | 'Read' >> ReadFromText("lorem.txt")
  #
  #   counts = (
  #       lines
  #       | 'Split' >> (beam.ParDo(WordExtractingDoFn()).with_output_types(str))
  #       | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
  #       | 'GroupAndSum' >> beam.CombinePerKey(sum))
  #
  #   # Format the counts into a PCollection of strings.
  #   def format_result(word, count):
  #     return '%s: %d' % (word, count)
  #
  #   output = counts | 'Format' >> beam.MapTuple(format_result)
  #
  #   # Write the output using a "Write" transform that has side effects.
  #   # pylint: disable=expression-not-assigned
  #   output | 'Write' >> beam.Map(print)
  #   # output | 'Write' >> WriteToText("dir1/counts")


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
