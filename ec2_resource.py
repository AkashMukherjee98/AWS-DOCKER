import boto3
import os
import io
from dotenv import load_dotenv
load_dotenv()


ec2 = boto3.resource('ec2')

def create_vpc_subnet_instance():
    try:
        vpc = ec2.create_vpc(CidrBlock=os.getenv('CIDR'))
        vpc.create_tags(Tags=[{"Key":"Name",
                        "Value":os.getenv('VPC_NAME')}])
        #vpc.wait_until_available()
        print("created vpc id >",vpc.id)
        subnet = ec2.create_subnet(CidrBlock = os.getenv('SUBNET_CIDR_BLOCK'), VpcId= vpc.id)
        subnet.create_tags(Tags=[{"Key":"Name",
                        "Value":os.getenv('SUBNET_NAME')}])
        print("created subnet id >",subnet.id)

        instances = ec2.create_instances(
            ImageId=os.getenv('AMI'),
            MinCount=1,
            MaxCount=1,
            SubnetId=subnet.id,
            InstanceType=os.getenv('INSTANCE'),
            KeyName=os.getenv('KEY_PAIR'),
            TagSpecifications=
                [
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value':os.getenv('EC2_NAME'),
                            },
                        ]
                    },
                ],
            )
        print("Instance is created")
        for instance in instances:
            print("Instance ID: ",instance.id)
            return instance.id
    except Exception as e:
        print(e)

def stop_instance(instance_id):
    try:
        ec2.Instance(instance_id).stop()
        print("istance is stoped")
    except Exception as e:
        print(e)

def terminate_ec2_instance(id):
    try:
        ids = [id]
        ec2.instances.filter(InstanceIds = ids).terminate()
        print("instance is terminated")
    except Exception as e:
        print(e)

def delete_subnet_vpc(vpc_id):
    try:
        ec2client = ec2.meta.client
        vpc = ec2.Vpc(vpc_id)
        for subnet in vpc.subnets.all():
            subnet.delete()
            vpc.delete()
            print("delete subnet and vpc")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    #create_vpc_subnet_instance()
    #stop_instance("i-0c6cac2db5f8fa529")
    #delete_subnet_vpc("vpc-010f2d89d8dac044f")
    #terminate_ec2_instance("i-056eb9220a2826e5b")
