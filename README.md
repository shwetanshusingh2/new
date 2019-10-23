# Tags Creation , Insertion and Deletion :Testing
This project adds 2000 object files to s3 bucket. Once added , the objects are given specific taggings .
Based on these taggings , some objects are deleted successfully.
# Files
- **helper.py** - This file has the main function of the project. It consists of :-
    - Definition of all of the parameters used in the project.
    - Uploading of template to s3 bucket.
    - Creating or updating stack.
    - Uploading 2000 objects to s3.
    - Creation of tags.
    - Insertion of tags.
    - Deletion of tags.
- **stack.py** - This file contains a Stack class which handles all the stack functions like create, delete and  update a stack using boto3.&nbsp;
- **functions.py** - Comprises of upload functions like upload a folder, file or zip file to s3.
- **Template.yaml** - A cloudforamtion template which comprises of configuration of s3bucket.
- **tags.py** - Consists of tags creation ,tag insertion and tag deletion functions.
-**Testing.py** - to test the code

# Output
Deletion of objects containing specific tag done successfully.
