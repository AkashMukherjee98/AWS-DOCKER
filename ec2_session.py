import boto3
import os
import io
from dotenv import load_dotenv
load_dotenv()
#import session



my_session = boto3.session.Session(aws_access_key_id=os.getenv('ACCESS_KEY'),
    aws_secret_access_key=os.getenv('SECRET_KEY'),
    region_name=os.getenv('REGION'))
print("--",my_session)

# ec2 = my_session.client('ec2')
# print(">>",ec2)

def create_instance():
    try:
        ec2_resource = my_session.resource('ec2')
        print(">>",ec2_resource)
        ec2_resource.create_instances(
            ImageId=os.getenv('AMI'),
            MinCount=1,
            MaxCount=1,
            InstanceType=os.getenv('INSTANCE'),
            KeyName=os.getenv('KEY_PAIR'),
            TagSpecifications=
                [
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value':os.getenv('EC2_NAME')
                            },
                        ]
                    },
                ],
        )
        print("Instance is created")
    except Exception as e:
        print(e)

def stop_instance(instance_id):
    try:
        ec2_resource = my_session.resource('ec2')
        ec2_resource.Instance(instance_id).stop()
        print("istance is stoped")
    except Exception as e:
        print(e)

def terminate_ec2_instance(id):
    try:
        ec2_resource = my_session.resource('ec2')
        ids = [id]
        ec2_resource.instances.filter(InstanceIds = ids).terminate()
        print("instance is terminated")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    #create_instance()
    #stop_instance("i-098d437793612e3c6")
    terminate_ec2_instance("i-098d437793612e3c6")