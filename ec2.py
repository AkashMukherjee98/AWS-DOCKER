import boto3
import os
import io
from dotenv import load_dotenv
load_dotenv()

def create_instance():
    try:
        resource =boto3.client("ec2")
        resource.run_instances(
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


def describe_instance():
    try:
        resource =boto3.client("ec2")
        #print(resource.describe_instances())
        #print(resource.describe_instances(InstanceIds=['i-00e7f0151fb3c520e']))
        #print(resource.describe_instances()["Reservations"][0]["Instances"][0]["InstanceId"])
        describe=resource.describe_instances().get("Reservations")
        for instance in describe:
            for instances in instance["Instances"]:
                print("Instance Id: ",instances.get("InstanceId")) 
    except Exception as e:
        print(e)



def stop_instance(instance_id):
    try:
        resource =boto3.client("ec2")
        result=resource.stop_instances(InstanceIds=[instance_id])
        print(result)
        print("Stop Successful")
    except Exception as e:
        print(e)


def start_instance(instance_id):
    try:
        resource =boto3.client("ec2")
        result=resource.start_instances(InstanceIds=[instance_id])
        print(result)
        print("Started Successful")
    except Exception as e:
        print(e)

def terminate_instance(instance_id):
    try:
        resource =boto3.client("ec2")
        result=resource.terminate_instances(InstanceIds=[instance_id])
        print(result)
        print("Terminated Successful")
    except Exception as e:
        print(e)


def create_custom_vpc():
    try:
        AWS_REGION = os.getenv('REGION')
        vpc_resource = boto3.client("ec2", region_name=AWS_REGION)
        ip_cidr=os.getenv('CIDR')
        response = vpc_resource.create_vpc(CidrBlock=ip_cidr,
                                           InstanceTenancy='dedicated',
                                           TagSpecifications=[{
                                               'ResourceType':'vpc',
                                               'Tags': [{
                                                   'Key':'Name',
                                                   'Value':os.getenv('VPC_NAME')
                                               }]
                                           }])
        print("check",response)
        v_id=response['Vpc']["VpcId"]
        print("=== ",v_id)
        print("VPC is created")
        return v_id
    except Exception as e:
        print(e)

def describe_vpc_attribute(vpc_id):
    try:
        AWS_REGION = os.getenv('REGION')
        vpc_client = boto3.client("ec2", region_name=AWS_REGION)
        attribute = 'enableDnsSupport'
        response = vpc_client.describe_vpc_attribute(Attribute=attribute,
                                                     VpcId=vpc_id)
        print(response)
    except Exception as e:
        print(e)


def create_subnet():
    try:
        vpc_id=create_custom_vpc()
        AWS_REGION = os.getenv('REGION')
        vpc_resource = boto3.resource("ec2", region_name=AWS_REGION)
        ip_cidr=os.getenv('SUBNET_CIDR_BLOCK')
        response = vpc_resource.create_subnet(CidrBlock=ip_cidr, VpcId=vpc_id,
                                            TagSpecifications=[{
                                               'ResourceType':'subnet',
                                               'Tags': [{
                                                   'Key':'Name',
                                                   'Value': os.getenv('SUBNET_NAME')
                                               }]
                                           }])
        print(response)
        print("Subnet is created")
    except Exception as e:
        print(e)

def delete_vpc(vpc_id):
    try:
        AWS_REGION = os.getenv('REGION')
        vpc_client = boto3.client("ec2", region_name=AWS_REGION)
        response = vpc_client.delete_vpc(VpcId=vpc_id)
        print(response)
        print("Deleted vpc")
    except Exception as e:
        print(e)


def delete_subnet(subnet_id):
    try:
        AWS_REGION = os.getenv('REGION')
        vpc_client = boto3.client("ec2", region_name=AWS_REGION)
        response = vpc_client.delete_subnet(SubnetId=subnet_id)
        print(response)
        print("Deleted Subnet")
    except Exception as e:
        print(e)


def create_keypair():
    try:
        ec2 = boto3.client('ec2')
        key_pair = ec2.create_key_pair(KeyName=os.getenv('KEY_PAIR'))
        print(key_pair)
        a=key_pair["KeyMaterial"]
        print(a)
        with io.open(os.getenv('KEY_PAIR')+'.pem',"w",encoding="utf-8") as file:
            file.write(str(a))
            file.close()
            print("Key is created and Downloaded")
    except Exception as e:
        print(e)



if __name__ == "__main__": 
    #create_instance()
    #describe_instance()
    #stop_instance("i-0f476d51604fb0806")
    #start_instance("i-0f476d51604fb0806")
    #terminate_instance("i-0a30ea2db7bd86835")
    #create_custom_vpc()
    #create_subnet()
    #delete_vpc("vpc-0e8dbdacc6dc503a6")
    #delete_subnet("subnet-0a15cc280c8ab0495")
    #create_keypair()
    #describe_vpc_attribute("vpc-03987039d80c389d4")