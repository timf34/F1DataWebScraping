import boto3

from aws_keys import ACCESS_KEY, SECRET_ACCESS_KEY


class SendTimingTableToMQTT:
    def __init__(self, topic: str = "RACE/new_json_file"):
        self.access_key: str = ACCESS_KEY
        self.secret_key: str = SECRET_ACCESS_KEY
        self.topic: str = topic
        self.iot_client = boto3.client('iot-data', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY, region_name='eu-west-1')

    def publish_to_topic(self, data) -> None:
        response = self.iot_client.publish(
            topic=self.topic,
            qos=1,
            payload=str(data)
        )