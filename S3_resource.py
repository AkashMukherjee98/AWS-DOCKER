import boto3
import os
import io
from dotenv import load_dotenv
load_dotenv()

resource = boto3.resource('s3')


def create_bucket():
    try:
        AWS_REGION = os.getenv('REGION')
        #print(AWS_REGION)
        resource = boto3.resource("s3", region_name=AWS_REGION)

        bucket_name = os.getenv('BUCKET_NAME')
        location = {'LocationConstraint': AWS_REGION}

        bucket = resource.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration=location)
        print("Amazon S3 bucket has been created")
    except Exception as e:
        print(e)

def list_buckets():
    try:
        AWS_REGION = os.getenv('REGION')
        resource = boto3.resource("s3", region_name=AWS_REGION)
        iterator = resource.buckets.all()
        print("Listing Amazon S3 Buckets:")
        for bucket in iterator:
            print(f"-- {bucket.name}")
        print("Ends Here")
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

def delete_bucket():
    try:
        AWS_REGION = os.getenv('REGION')
        resource = boto3.resource("s3", region_name=AWS_REGION)
        bucket_name = os.getenv('BUCKET_NAME')
        s3_bucket = resource.Bucket(bucket_name)
        s3_bucket.delete()
        print("Amazon S3 Bucket has been deleted")
    except Exception as e:
        print(e)

def upload_single_file(file_path, file_name):
    try:
        resource.Bucket(os.getenv('BUCKET_NAME')).upload_file(file_path, file_name)
        print("Upload done")
    except Exception as e:
        print(e)

def download_single_file(file_path, file_name):
    try:
        AWS_REGION = os.getenv('REGION')
        S3_BUCKET_NAME = os.getenv('BUCKET_NAME')
        s3_resource = boto3.resource("s3", region_name=AWS_REGION)
        s3_object = s3_resource.Object(S3_BUCKET_NAME, file_name)
        s3_object.download_file(file_path)
        print('S3 object download complete')
    except Exception as e:
        print(e)

def upload_multiple_file():
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


def delete_single_file(object_name):
    try:
        AWS_REGION = os.getenv('REGION')
        S3_BUCKET_NAME = os.getenv('BUCKET_NAME')
        s3_resource = boto3.resource("s3", region_name=AWS_REGION)
        s3_object = s3_resource.Object(S3_BUCKET_NAME, object_name)
        s3_object.delete()
        print("Deleted File Object")
    except Exception as e:
        print(e)







if __name__ == "__main__":
    #create_bucket()
    #list_buckets()
    #delete_non_empty_bucket("akash-bucket-1234")
    #delete_bucket()
    #upload_single_file("./hi.txt" , "hi.txt")
    #download_single_file("./check", "hi.txt")
    #upload_multiple_file()
    #delete_single_file("hi.txt")