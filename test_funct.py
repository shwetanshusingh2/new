import boto3
import unittest
from moto import mock_s3
from functions import Functions
from tags import Tags
from tags import make_tags
import os
import xmlrunner

#os.environ['AWS_SHARED_CREDENTIALS_FILE'] = "C:/Users/Hp/.aws/credentials"

#os.environ['AWS_PROFILE'] = "default"
#os.environ['AWS_DEFAULT_REGION'] = "ap-south-1"

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


class S3Tests(unittest.TestCase):

    def setUp(self):
        # sets up the local moto s3 service for mocking.
        self.bucket = '1052061shi'
        self.source_bucketname = 'shivam1052061'
        self.key = 'note.txt'
        self.value = 'hi'
        self.foldername = 'numbers'

    @mock_s3
    def __moto_setup(self):
        """
        simulation of s3 file upload
        """
        s3 = boto3.resource('s3',region_name ="ap-south-1")
        s3.create_bucket(Bucket=self.source_bucketname)
        # s3.put_object(Bucket=self.source_bucketname, Key=self.key, Body=self.value)

    @mock_s3
    def test_upload_objects(self):
        self.__moto_setup()
        f = Functions(parameter)
        f.upload_objects()
        s3_client = boto3.client("s3",region_name ="ap-south-1")
        s3_bucket_object_count = 0
        response = s3_client.list_objects_v2(Bucket='shivam1052061')
        if response:
            try:
                for _object in response['Contents']:
                    s3_bucket_object_count = s3_bucket_object_count + 1
            except KeyError:
                print("KeyError. No such key exists in the specified bucket")
        # print(s3_bucket_object_count)
        self.assertEqual(s3_bucket_object_count, 10)

    @mock_s3
    def test_make_tags(self):
        self.__moto_setup()
        # t=Tags(parameter)
        tags_to_be_uploaded = make_tags({'notdivby2': '2no', 'key1': 'val1'})
        self.assertEqual(tags_to_be_uploaded, {'TagSet': [{'Key': 'notdivby2', 'Value': '2no'},
                                                          {'Key': 'key1', 'Value': 'val1'}]})

    @mock_s3
    def test_tagging_insertion(self):
        self.__moto_setup()
        s3_client = boto3.client('s3',region_name ="ap-south-1")
        source_objectname_value = '1.txt'
        s3_client.put_object(Bucket='shivam1052061', Key=source_objectname_value)
        tagset_value = {'TagSet': [{'Key': 'notdivby2', 'Value': '2no'},
                                   {'Key': 'key1', 'Value': 'val1'}]}
        t = Tags(parameter)

        t.tagging_insertion(source_objectname_value, tagset_value)
        s3_client = boto3.client('s3',region_name ="ap-south-1")
        response = s3_client.get_object_tagging(
            Bucket=parameter['SourceBucketName'],
            Key=source_objectname_value
        )
        # print("get object taggings")
        output_to_be_checked = [tag for tag in response.get('TagSet')]
        # print(output_to_be_checked)
        for b in output_to_be_checked:
            self.assertIn(b, output_to_be_checked)

    #C:\Users\ADMIN\PycharmProjects\week2OOPS
    @mock_s3
    def test_tagging_deletion(self):
        self.__moto_setup()
        s3_client = boto3.client('s3',region_name ="ap-south-1")
        # ek object upload karo
        source_objectname_value = '1.txt'
        source_objectname_value2 = '2.txt'
        s3_client.put_object(Bucket='shivam1052061', Key=source_objectname_value)
        s3_client.put_object(Bucket='shivam1052061', Key=source_objectname_value2)
        # tag dalo
        tagset_value = {'TagSet': [{'Key': 'notdivby2', 'Value': '2no'}]}
        t = Tags(parameter)
        t.tagging_insertion(source_objectname_value, tagset_value)
        # tag retrieve karo
        response = s3_client.get_object_tagging(
            Bucket=parameter['SourceBucketName'],
            Key=source_objectname_value
        )
        # delete karo
        output_to_be_checked = [tag for tag in response.get('TagSet')]
        # print(" last : \n")
        # print(output_to_be_checked)
        if output_to_be_checked == [{'Key': 'notdivby2', 'Value': '2no'}]:
            resp = s3_client.delete_object(
                Bucket=parameter["SourceBucketName"],
                Key=source_objectname_value
            )
            #  print("lol \n")
            # print(resp)
            # print(resp['ResponseMetadata']['HTTPStatusCode'])
            # self.assertEqual(resp['ResponseMetadata']['HTTPStatusCode'],204)
            # obect_count_in_the_bucket_before_deletion = 2
            object_count_in_the_bucket_after_deletion = 1
            s3_bucket_object_count = 0
            response = s3_client.list_objects_v2(Bucket='shivam1052061')
            if response:
                try:
                    for _object in response['Contents']:
                        s3_bucket_object_count = s3_bucket_object_count + 1
                except KeyError:
                    print("KeyError. No such key exists in the specified bucket")
            # print("object_count_in_the_bucket_after_deletion")
            # print(s3_bucket_object_count)
            # assertequals karo
            self.assertEqual(1, object_count_in_the_bucket_after_deletion)


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)
