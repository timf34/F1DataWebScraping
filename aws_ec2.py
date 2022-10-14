import boto3
import json
import os

from aws_keys import SECRET_ACCESS_KEY, ACCESS_KEY


class AWS_EC2:
    def __init__(self):
        self.region_name = "ap-northeast-1"
        self.ec2_client = boto3.client("ec2", region_name=self.region_name,
                                       aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)
        self.instance_type: str = "t2.micro"

    def write_pem_to_file(self):
        with open("ec2-key-pair.pem", "w") as f:
            f.write("-----BEGIN RSA PRIVATE KEY-----\n"
                    "MIIEpAIBAAKCAQEAwL6gHJ0dL9X5Y5e5r5h0m5ZaA5KmPn+KwW6J8f6Lh9XK2b6n\n"
                    "1k5Zi6jZ5+5Z5zW8a6vZU6XQ2Xb0Y6xQ2qz3q0K7l6bKj6O8y0JcH9X0fjgY5x4z\n"
                    "Gk4z4J4w4qW8Vv3j3X9XVgN4S0T8jvZ+T2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q\n"
                    "2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q\n"
                    "2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q\n"
                    "2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q\n"
                    "2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q\n"
                    )

    def create_key_pair(self):
        key_pair = self.ec2_client.create_key_pair(KeyName="y-key-pair")
        print(key_pair)

        private_key = key_pair["KeyMaterial"]
        print(private_key)

        # write private key to local file for use
        with open("y-key-pair.pem", "w") as f:
            f.write(private_key)

        # change permissions of private key file
        os.chmod("y-key-pair.pem", 0o400)

        print(key_pair)

        # Ensure key pair exists

    def create_instance(self):
        instances = self.ec2_client.run_instances(
            ImageId="ami-03f4fa076d2981b45",  # Basic Ubuntu instance
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName="y-key-pair"
        )

        print(instances["Instances"][0]["InstanceId"])

    def get_instance_status(self, instance_id: str):
        status = self.ec2_client.describe_instance_status(InstanceIds=[instance_id])
        print(status)

    def get_instance_ip(self, instance_id: str):
        ip = self.ec2_client.describe_instances(InstanceIds=[instance_id])
        print(ip["Reservations"][0]["Instances"][0]["PublicIpAddress"])

    def get_running_instances(self):
        instances = self.ec2_client.describe_instances()
        print(instances)

    def stop_instance(self, instance_id: str):
        response = self.ec2_client.stop_instances(InstanceIds=[instance_id])
        print(response)

    def get_public_ip(self, instance_id: str):
        response = self.ec2_client.describe_instances(InstanceIds=[instance_id])
        print(response["Reservations"][0]["Instances"][0]["PublicIpAddress"])


def main():
    x = AWS_EC2()
    x.create_key_pair()
    x.create_instance()
    x.get_running_instances()
    # x.write_pem_to_file()


if __name__ == '__main__':
    main()
