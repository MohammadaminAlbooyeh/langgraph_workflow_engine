import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda function to automate stopping all running RDS instances in the current region.
    This can be scheduled to run at specific times for cost optimization.
    Note: RDS instances can be stopped for up to 7 days.
    """
    try:
        # Create RDS client
        rds = boto3.client('rds')

        # Describe all DB instances
        response = rds.describe_db_instances()

        # Filter for running instances
        running_instances = []
        for db_instance in response.get('DBInstances', []):
            if db_instance['DBInstanceStatus'] == 'available':
                running_instances.append(db_instance['DBInstanceIdentifier'])

        if not running_instances:
            logger.info("No running RDS instances found to stop.")
            return {
                'statusCode': 200,
                'body': 'No running RDS instances to stop'
            }

        # Stop the instances
        stopped_instances = []
        for instance_id in running_instances:
            try:
                rds.stop_db_instance(DBInstanceIdentifier=instance_id)
                stopped_instances.append(instance_id)
                logger.info(f"Successfully stopped RDS instance: {instance_id}")
            except Exception as e:
                logger.error(f"Error stopping RDS instance {instance_id}: {str(e)}")

        if stopped_instances:
            return {
                'statusCode': 200,
                'body': f'Successfully stopped {len(stopped_instances)} RDS instances: {stopped_instances}'
            }
        else:
            return {
                'statusCode': 500,
                'body': 'Failed to stop any RDS instances'
            }

    except Exception as e:
        logger.error(f"Error in RDS automation: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }