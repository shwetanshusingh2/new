import boto3


# import functions
# import time
# from botocore.client import ClientError


def make_tags(tagss):
    tag_list = []
    for k, v in tagss.items():
        tag_list.append({'Key': k, 'Value': v if v is not None else ''})
    return {'TagSet': tag_list}


class Tags:
    def __init__(self, parameter):
        self.parameter = parameter

    def tagging_insertion(self, source_objectname, tagset):
        s3_client = boto3.client('s3', region_name=self.parameter["default_region"])
        response2 = s3_client.put_object_tagging(
            Bucket=self.parameter["SourceBucketName"],
            Key=source_objectname,
            Tagging=tagset
        )

        print("what is needed    :")
        print(response2)


    def tagging_deletion(self):
        s3_client = boto3.client('s3', region_name=self.parameter["default_region"])
        s3_resource = boto3.resource('s3', region_name=self.parameter["default_region"])
        bucket = s3_resource.Bucket(self.parameter["SourceBucketName"])
        for key in bucket.objects.all():
            try:
                var = key.key
                response = s3_client.get_object_tagging(
                    Bucket=self.parameter["SourceBucketName"],
                    Key=var,
                )
                for tag in response.get('TagSet'):
                    if tag.get('Key') == self.parameter["deltagK"] and tag.get('Value') == self.parameter["deltagV"]:
                        s3_client.delete_object(
                            Bucket=self.parameter["SourceBucketName"],
                            Key=var
                        )
            except:
                pass
