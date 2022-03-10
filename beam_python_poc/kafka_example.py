import logging

import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.kafka import ReadFromKafka, WriteToKafka

KAFKA_BOOTSTRAP = "localhost:9093"


def run_pipeline():
    options = PipelineOptions([
      "--runner=FlinkRunner",
      "--flink_master=localhost:8081",
      "--flink_version=1.13",
      "--environment_type=EXTERNAL",
      "--environment_config=localhost:50000"
    ])

    with beam.Pipeline(options=options) as p:
        (p
         # | 'Create words' >> beam.Create(['to be or not to be'])
         | 'Read from Kafka' >> ReadFromKafka(consumer_config={'bootstrap.servers': KAFKA_BOOTSTRAP,
                                                               'auto.offset.reset': 'latest'},
                                              topics=['test.source.topic'])
         | 'Par with 1' >> beam.Map(lambda word: (word, 1))
         | 'Window of 10 seconds' >> beam.WindowInto(window.FixedWindows(10))
         | 'Group by key' >> beam.GroupByKey()
         | 'Sum word counts' >> beam.Map(lambda kv: (kv[0], sum(kv[1])))
         # | 'Print to console' >> beam.Map(lambda wordcount: print(wordcount))
         | 'Write to Kafka' >> WriteToKafka(producer_config={'bootstrap.servers': KAFKA_BOOTSTRAP},
                                            topic='test.output.topic',
                                            )
        )

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run_pipeline()
