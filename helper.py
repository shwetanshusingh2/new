import boto3
import functions
import stacks
import tags
from botocore.client import ClientError

# CONSTANT PARAMETERS DECLARATION

INIT_BUCKET_NAME = "data-shivam"
BUCKET_CONFIG = "ap-south-1"
YAML_FILENAME = "Template.yaml"
STACK_NAME = "stack1"
SOURCE_BUCKET_NAME = "shivam1052061"
YAML_FILEPATH = "https://data-shivam.s3.ap-south-1.amazonaws.com/Template.yaml"
UPLOAD_FOLDER_NAME = "numbers"
DEL_TAG_KEY = "notdivby2"
DEL_TAG_VALUE = "2no"
DEFAULT_REGION = "ap-south-1"
parameter = {
    "InitBucketName": INIT_BUCKET_NAME,
    "BucketConfig": BUCKET_CONFIG,
    "YamlFileName": YAML_FILENAME,
    "StackName": STACK_NAME,
    "SourceBucketName": SOURCE_BUCKET_NAME,
    "YamlFilePath": YAML_FILEPATH,
    "UploadFolderName": UPLOAD_FOLDER_NAME,
    "deltagK": DEL_TAG_KEY,
    "deltagV": DEL_TAG_VALUE,
    "default_region": DEFAULT_REGION
}

client = boto3.client('cloudformation')
s3 = boto3.resource('s3')


def main():
    # OBJECT CREATION OF CLASSES
    functions_class_object = functions.Functions(parameter)
    stack_class_object = stacks.Stack(parameter)
    tags_class_object = tags.Tags(parameter)

    # INITIAL BUCKET CREATION FOR YAML FILE UPLOADING
    try:
        s3.create_bucket(Bucket=parameter["InitBucketName"],
                         CreateBucketConfiguration={'LocationConstraint': parameter["BucketConfig"]})
    except ClientError:
        print("Data Bucket Already Created")

    # UPLOADING OF YAML FILE OBJECT
    functions_class_object.upload_object()

    # STACK CREATION , UPDATION OR DELETION AS PER REQUIREMENT
    stack_class_object.stack_handler()

    # UPLOADING OF OBJECTS USING FOLDER
    functions_class_object.upload_objects()


    # Tag Creation
    tagset1 = tags.make_tags({'notdivby2': '2no', 'key1': 'val1'})
    #print(tagset1)
    tagset2 = tags.make_tags({'divby2': '2yes', 'key1': 'val1'})
    #print(tagset1)
    # Tag Insertion
    tracker = 1
    while tracker != 11:
        if tracker % 2 == 0:
            obj_name = '{}.txt'.format(tracker)
            tags_class_object.tagging_insertion(obj_name, tagset2)
            print("yo")
        else:
            obj_name = '{}.txt'.format(tracker)
            tags_class_object.tagging_insertion(obj_name, tagset1)
            print("no")
        tracker = tracker + 1
    # Tag Deletion
    # Tags_Class_Object.tagging_deletion()


# MAIN FUNCTION
if __name__ == "__main__":
    main()
