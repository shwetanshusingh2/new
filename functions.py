import boto3
import zipfile
import os
# import glob

client = boto3.client('cloudformation')
s3 = boto3.resource('s3')

DIRECTORY_IN_STR = "/numbers"


class Functions(object):
    # contains all the functions used in the project.
    def __init__(self, parameter):
        self.parameter = parameter

    def upload_object(self):
        s3.Object(self.parameter["InitBucketName"], self.parameter["YamlFileName"]).upload_file(
            Filename=self.parameter["YamlFileName"])


    def upload_objects(self):
        a = os.listdir(self.parameter["UploadFolderName"])
        for file in a:
            s3.Object(self.parameter["SourceBucketName"], file).upload_file(
                Filename=self.parameter["UploadFolderName"] + '/' + file)


    def upload_zip_object(self, bucket_name, input_filename, output_filename, location):
        zip = zipfile.ZipFile(output_filename, "w")
        zip.write(input_filename, os.path.basename(input_filename))
        zip.close()
        self.upload_object(bucket_name, output_filename, location)
        os.remove(output_filename)
