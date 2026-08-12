from kafka import KafkaProducer
from kafka import KafkaConsumer

class KafkaManager:

    def producer(self):

        return KafkaProducer(

            bootstrap_servers=
            "localhost:9092"
        )

    def consumer(

        self,

        topic
    ):

        return KafkaConsumer(

            topic,

            bootstrap_servers=
            "localhost:9092"
        )


kafka_manager = (
    KafkaManager()
)