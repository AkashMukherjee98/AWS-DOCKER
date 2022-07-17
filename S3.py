import boto3
import os
from dotenv import load_dotenv
load_dotenv()


def create_bucket():
    try:
        AWS_REGION = os.getenv('REGION')
        print(AWS_REGION)
        client = boto3.client("s3", region_name=AWS_REGION)
        bucket_name = os.getenv('BUCKET_NAME')
        location = {'LocationConstraint': AWS_REGION}
        response = client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print("Amazon S3 bucket has been created")
    except Exception as e:
        print(e)

def list_buckets():
    try:
        AWS_REGION = os.getenv('REGION')
        client = boto3.client("s3", region_name=AWS_REGION)
        response = client.list_buckets()
        print("Listed Buckets Are: ")
        for bucket in response['Buckets']:
            print({bucket['Name']})
        print("Ends Here")
    except Exception as e:
        print(e)

def upload_file(file_name, bucket, object_name):
    try:
        AWS_REGION = os.getenv('REGION')
        client = boto3.client("s3", region_name=AWS_REGION)
        object_name=os.path.basename(file_name)
        response=client.upload_file(file_name, bucket, object_name)
        print("Uploaded Successfully")
    except Exception as e:
        print(e)

def delete_empty_bucket(bucket_name):
    try:
        AWS_REGION = os.getenv('REGION')
        client = boto3.client("s3", region_name=AWS_REGION)
        response=client.delete_bucket(Bucket=bucket_name)
        print(response)
        print("Empty Bucket is Deleted")
    except Exception as e:
        print(e)

def delete_non_empty_bucket(bucket_name):
    try:
        AWS_REGION = os.getenv('REGION')
        client = boto3.resource("s3", region_name=AWS_REGION)
        response=client.Bucket(bucket_name)
        response.objects.all().delete()
        response.meta.client.delete_bucket(Bucket=bucket_name)
        print(response)
        print("Non Empty Bucket is Deleted")
    except Exception as e:
        print(e)
    
def delete_file_object(bucket,object_name):
    try:
        AWS_REGION = os.getenv('REGION')
        client = boto3.client("s3", region_name=AWS_REGION)
        response=client.delete_object(Bucket=bucket, Key=object_name)
        print(response)
        print("Deleted File Object")
    except Exception as e:
        print(e)    

def download_file(file_name, bucket, object_name):
    try:
        AWS_REGION = os.getenv('REGION')
        client = boto3.client("s3", region_name=AWS_REGION)
        response=client.download_file(bucket, object_name, file_name)
        print("File is Downloaded")
    except Exception as e:
        print(e)    
        
def multiple_file_upload():
    try:
        s3 = boto3.resource('s3')
        directory_in_str="./File"   # change directory path to your images folder
        directory = os.fsencode(directory_in_str)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                strg=directory_in_str+'/'+filename
                print(strg)     
                file = open(strg,'rb')
                object = s3.Object(os.getenv('BUCKET_NAME'),filename)
                object.put(Body=file,ContentType='txt')
        print("All_Done")
    except Exception as e:
        print(e)    
    

if __name__ == "__main__":
    #create_bucket()
    #list_buckets()
    #upload_file("./test.txt", "akash-s3-bucket-1234", "test.txt")
    #delete_empty_bucket("akash-bucket-1234")
    #delete_non_empty_bucket("akash-bucket-1234")
    #delete_file_object("akash-s3-bucket-1234","test.txt")
    #download_file("./Hello123.txt", "akash-bucket-1234", "Hello.txt")
    #multiple_file_upload()



