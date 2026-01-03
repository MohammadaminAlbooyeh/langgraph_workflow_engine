import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda function to automate stopping all running EC2 instances in the current region.
    This can be scheduled to run at specific times for cost optimization.
    """
    try:
        # Create EC2 client
        ec2 = boto3.client('ec2')

        # Describe all running instances
        response = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )

        # Extract instance IDs
        instance_ids = []
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_ids.append(instance['InstanceId'])

        if not instance_ids:
            logger.info("No running EC2 instances found to stop.")
            return {
                'statusCode': 200,
                'body': 'No running instances to stop'
            }

        # Stop the instances
        stop_response = ec2.stop_instances(InstanceIds=instance_ids)

        # Log the stopped instances
        stopped_instances = [instance['InstanceId'] for instance in stop_response['StoppingInstances']]
        logger.info(f"Successfully stopped EC2 instances: {stopped_instances}")

        return {
            'statusCode': 200,
            'body': f'Successfully stopped {len(stopped_instances)} EC2 instances: {stopped_instances}'
        }

    except Exception as e:
        logger.error(f"Error stopping EC2 instances: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }