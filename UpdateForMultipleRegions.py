'''
This python code provides the functionality to read EC2 resource Tags from csv file and update the Tags for EC2 resources hosted in all the regions for the given AWS account 
Author : Siva Mamillapalli (siva.mamillapalli@cepheid.com), CCoE Team

The same script can be used to update any number of Key-value pairs.
This script doesn't overwrite any of the existing Keys, It will only add new Key - value pairs / Update the existing Keys with new Values

Pre-requisites:

    You need to configure and login to aws using SSO , execute "aws configure sso" before you run this script
    Make sure you have the csv input file in the same location as your python file
    Make sure you have all the correct EC2 instance Ids and its regions captured in the file
    Make sure you replace your profile name before you execute this file . Ex: profile_name = <your-sso-profile-name>
 
'''
# Import the required python Modules
# boto3 is the Python package to interact with the AWS services


import boto3
from botocore.exceptions import ClientError
import csv
import os



def update_ec2_tags_by_resource_id(csv_file, profile_name):
    
    # This function reads csv file and which contains Resource ID, Region, Tags and update the tags based on the resource id
    
    session = boto3.Session(profile_name=profile_name)  # Open the session with given profile name
    
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            resource_id = row['Resource_Id']
            tags = []

            for key, value in row.items():
                if not key.startswith("Resource_Id") and key != "Region":
                    tags.append({'Key': key, 'Value': value})

            region_name = row['Region']
            ec2_client = session.client('ec2', region_name=region_name)
            
            try:
                ec2_client.create_tags(Resources=[resource_id], Tags=tags)
                print(f"Updated {len(tags)} tags for resource '{resource_id}' in region '{region_name}'")
                
            except ClientError as e:
                if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
                    print(f"Instance '{resource_id}' not found in region '{region_name}'. Skipping...")
                else:
                    raise e  
                
                
if __name__ == "__main__":
    
    file_path = os.getcwd()
    csv_file = file_path+"\\tagstoupdate.csv"
    profile_name = "IT-EC2-Admin-565209677751"  
    update_ec2_tags_by_resource_id(csv_file, profile_name)

