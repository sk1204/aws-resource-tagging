import boto3
import openpyxl

# Connect to AWS EC2 client
ec2 = boto3.client('ec2', region_name="us-west-2")

print("Connected to AWS EC2:")
print("Reading the tags file")

# Open the XLS file
workbook = openpyxl.load_workbook('removetags.xlsx')
sheet = workbook['Sheet1']  # Adjust sheet name if needed

# Read tag keys from the XLS file
tag_keys = [cell.value for cell in sheet['A']]  # Assuming tag keys are in column A

print("COllecting the list of instabces from AWS")

# Get a list of all EC2 instances, ensuring correct structure handling
instances = ec2.describe_instances()['Reservations']
instance_ids = [
    instance['InstanceId']
    for reservation in instances
    for instance in reservation['Instances']
]

print(instance_ids)  # Should now print the list of instance IDs

# Iterate through instances and remove tags
for instance_id in instance_ids:
    try:
        ec2.delete_tags(Resources=[instance_id], Tags=[{'Key': key} for key in tag_keys])
        print(f"Tags removed from instance: {instance_id}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidTagKeys.NotFound':  # Check for specific error code
            print(f"Tag(s) not found on instance {instance_id}. No action taken.")
        else:
            raise  # Re-raise other errors