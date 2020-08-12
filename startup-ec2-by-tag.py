import boto3
 
region = 'us-east-1'
ec2 = boto3.client('ec2', region_name=region)
 
def lambda_handler(event, context):
 instances_describe = ec2.describe_instances(
        Filters = [
 {
 'Name': 'tag:Startup',
 'Values': ['True']
 },
 {
             'Name': 'instance-state-name', 
         'Values': ['stopped']
 }
 ]
 )
 
 instances_list = []
 
 for reservation in (instances_describe["Reservations"]):
 for instance in reservation["Instances"]:
 instances_list.append(instance["InstanceId"])
 
 ec2.start_instances(InstanceIds=instances_list)
 
 return instances_list
