#!/usr/bin/env python3
"""
AWS EC2 Automation Script

This script provides automation capabilities for managing Amazon EC2 instances.
It supports listing, starting, stopping, creating, and terminating EC2 instances.

Prerequisites:
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
- boto3 library installed
- Appropriate IAM permissions for EC2 operations

Usage:
    python ec2.py list
    python ec2.py start --instance-id i-1234567890abcdef0
    python ec2.py stop --instance-id i-1234567890abcdef0
    python ec2.py create --ami-id ami-12345678 --instance-type t2.micro --key-name my-key
    python ec2.py terminate --instance-id i-1234567890abcdef0
"""

import argparse
import sys
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class EC2Automation:
    """Class for EC2 automation operations."""

    def __init__(self, region_name='us-east-1'):
        """
        Initialize EC2 client and resource.

        Args:
            region_name (str): AWS region name (default: us-east-1)
        """
        try:
            self.ec2_client = boto3.client('ec2', region_name=region_name)
            self.ec2_resource = boto3.resource('ec2', region_name=region_name)
            print(f"Connected to AWS region: {region_name}")
        except NoCredentialsError:
            print("Error: AWS credentials not found. Please configure your AWS credentials.")
            sys.exit(1)
        except Exception as e:
            print(f"Error initializing EC2 client: {e}")
            sys.exit(1)

    def list_instances(self, filters=None):
        """
        List EC2 instances with optional filters.

        Args:
            filters (list): List of filter dictionaries (optional)
        """
        try:
            if filters:
                response = self.ec2_client.describe_instances(Filters=filters)
            else:
                response = self.ec2_client.describe_instances()

            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        'InstanceId': instance['InstanceId'],
                        'State': instance['State']['Name'],
                        'InstanceType': instance['InstanceType'],
                        'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                        'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                        'Tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                    })

            if not instances:
                print("No instances found.")
                return

            print("\nEC2 Instances:")
            print("-" * 100)
            print(f"{'Instance ID':<20} {'State':<12} {'Type':<12} {'Public IP':<15} {'Private IP':<15} {'Name'}")
            print("-" * 100)

            for instance in instances:
                name = instance['Tags'].get('Name', 'N/A')
                print(f"{instance['InstanceId']:<20} {instance['State']:<12} {instance['InstanceType']:<12} "
                      f"{instance['PublicIpAddress']:<15} {instance['PrivateIpAddress']:<15} {name}")

        except ClientError as e:
            print(f"Error listing instances: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def start_instance(self, instance_id):
        """
        Start an EC2 instance.

        Args:
            instance_id (str): EC2 instance ID
        """
        try:
            response = self.ec2_client.start_instances(InstanceIds=[instance_id])
            print(f"Starting instance {instance_id}...")

            # Wait for the instance to be running
            waiter = self.ec2_client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[instance_id])

            print(f"Instance {instance_id} is now running.")

        except ClientError as e:
            print(f"Error starting instance {instance_id}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def stop_instance(self, instance_id):
        """
        Stop an EC2 instance.

        Args:
            instance_id (str): EC2 instance ID
        """
        try:
            response = self.ec2_client.stop_instances(InstanceIds=[instance_id])
            print(f"Stopping instance {instance_id}...")

            # Wait for the instance to be stopped
            waiter = self.ec2_client.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=[instance_id])

            print(f"Instance {instance_id} is now stopped.")

        except ClientError as e:
            print(f"Error stopping instance {instance_id}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def create_instance(self, ami_id, instance_type, key_name, security_groups=None, user_data=None, tags=None):
        """
        Create a new EC2 instance.

        Args:
            ami_id (str): AMI ID
            instance_type (str): Instance type (e.g., t2.micro)
            key_name (str): Key pair name
            security_groups (list): List of security group IDs (optional)
            user_data (str): User data script (optional)
            tags (list): List of tag dictionaries (optional)

        Returns:
            str: Instance ID of the created instance
        """
        try:
            params = {
                'ImageId': ami_id,
                'InstanceType': instance_type,
                'KeyName': key_name,
                'MinCount': 1,
                'MaxCount': 1
            }

            if security_groups:
                params['SecurityGroupIds'] = security_groups

            if user_data:
                params['UserData'] = user_data

            response = self.ec2_client.run_instances(**params)

            instance_id = response['Instances'][0]['InstanceId']
            print(f"Creating instance {instance_id}...")

            # Wait for the instance to be running
            waiter = self.ec2_client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[instance_id])

            # Add tags if provided
            if tags:
                self.ec2_client.create_tags(
                    Resources=[instance_id],
                    Tags=tags
                )

            print(f"Instance {instance_id} created and running.")
            return instance_id

        except ClientError as e:
            print(f"Error creating instance: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def terminate_instance(self, instance_id):
        """
        Terminate an EC2 instance.

        Args:
            instance_id (str): EC2 instance ID
        """
        try:
            response = self.ec2_client.terminate_instances(InstanceIds=[instance_id])
            print(f"Terminating instance {instance_id}...")

            # Wait for the instance to be terminated
            waiter = self.ec2_client.get_waiter('instance_terminated')
            waiter.wait(InstanceIds=[instance_id])

            print(f"Instance {instance_id} has been terminated.")

        except ClientError as e:
            print(f"Error terminating instance {instance_id}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='AWS EC2 Automation Script')
    parser.add_argument('action', choices=['list', 'start', 'stop', 'create', 'terminate'],
                       help='Action to perform')
    parser.add_argument('--region', default='us-east-1',
                       help='AWS region (default: us-east-1)')
    parser.add_argument('--instance-id', help='EC2 instance ID')
    parser.add_argument('--ami-id', help='AMI ID for creating instance')
    parser.add_argument('--instance-type', help='Instance type for creating instance')
    parser.add_argument('--key-name', help='Key pair name for creating instance')
    parser.add_argument('--security-groups', nargs='*', help='Security group IDs for creating instance')
    parser.add_argument('--user-data', help='User data script for creating instance')
    parser.add_argument('--tags', nargs='*', help='Tags for creating instance (format: Key=Value)')
    parser.add_argument('--filter', nargs='*', help='Filters for listing instances (format: Name=Value)')

    args = parser.parse_args()

    # Initialize EC2 automation
    ec2 = EC2Automation(region_name=args.region)

    if args.action == 'list':
        filters = None
        if args.filter:
            filters = []
            for f in args.filter:
                if '=' in f:
                    name, value = f.split('=', 1)
                    filters.append({'Name': name, 'Values': [value]})
        ec2.list_instances(filters=filters)

    elif args.action == 'start':
        if not args.instance_id:
            print("Error: --instance-id is required for start action")
            sys.exit(1)
        ec2.start_instance(args.instance_id)

    elif args.action == 'stop':
        if not args.instance_id:
            print("Error: --instance-id is required for stop action")
            sys.exit(1)
        ec2.stop_instance(args.instance_id)

    elif args.action == 'create':
        if not all([args.ami_id, args.instance_type, args.key_name]):
            print("Error: --ami-id, --instance-type, and --key-name are required for create action")
            sys.exit(1)

        tags = None
        if args.tags:
            tags = []
            for tag in args.tags:
                if '=' in tag:
                    key, value = tag.split('=', 1)
                    tags.append({'Key': key, 'Value': value})

        instance_id = ec2.create_instance(
            ami_id=args.ami_id,
            instance_type=args.instance_type,
            key_name=args.key_name,
            security_groups=args.security_groups,
            user_data=args.user_data,
            tags=tags
        )
        if instance_id:
            print(f"Created instance: {instance_id}")

    elif args.action == 'terminate':
        if not args.instance_id:
            print("Error: --instance-id is required for terminate action")
            sys.exit(1)
        ec2.terminate_instance(args.instance_id)


if __name__ == '__main__':
    main()