import boto3
import time
# from botocore.client import ClientError

client = boto3.client('cloudformation')
s3 = boto3.resource('s3')


class Stack:
    def __init__(self, parameter):
        self.parameter = parameter

    def stack_handler(self):
        status = self.stack_status()
        print(status)
        if status == 'ROLLBACK_COMPLETE' or status == 'ROLLBACK_FAILED' or status == 'UPDATE_ROLLBACK_COMPLETE' or \
                status == 'DELETE_FAILED':
            self.delete_object()
            client.delete_stack(StackName=self.parameter["StackName"])
            time.sleep(5)
            while self.stack_status() == 'DELETE_IN_PROGRESS':
                time.sleep(5)
            print("stack deleted")
            self.create_stack()
            print("stack created")
        elif status == 'CREATE_COMPLETE' or status == 'UPDATE_COMPLETE':
            self.update_stack()
            print("stack updated")
        else:
            self.create_stack()
            print("creating stack")
        while self.stack_status() == 'CREATE_IN_PROGRESS' or \
                self.stack_status() == 'UPDATE_IN_PROGRESS' or \
                self.stack_status() == 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS':
            time.sleep(2)
        print("stack created")
        return self.stack_status()

    def create_stack(self):
        client.create_stack(
            StackName=self.parameter["StackName"],
            TemplateURL=self.parameter["YamlFilePath"],
            Capabilities=[
                'CAPABILITY_NAMED_IAM'],
            Parameters=[
                {
                    'ParameterKey': "SourceBucket",
                    'ParameterValue': self.parameter["SourceBucketName"]
                }]
        )

    def update_stack(self):
        try:
            client.update_stack(
                StackName=self.parameter["StackName"],
                TemplateURL=self.parameter["YamlFilePath"],
                Capabilities=['CAPABILITY_NAMED_IAM'],
                Parameters=[
                    {
                        'ParameterKey': "SourceBucket",
                        'ParameterValue': self.parameter["SourceBucketName"]
                    }
                ]
            )
        except Exception:
            print("No update To Perform")

    def stack_status(self):
        try:
            stack = client.describe_stacks(StackName=self.parameter["StackName"])
            status = stack['Stacks'][0]['StackStatus']
            return status
        except Exception:
            return "NO_STACK"

    def delete_object(self):
        try:
            bucket = s3.Bucket(self.parameter["SourceBucketName"])
            bucket.objects.all().delete()
        except Exception:
            print("Bucket Not Present")
