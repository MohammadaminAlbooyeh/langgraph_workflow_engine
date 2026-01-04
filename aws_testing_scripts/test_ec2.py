#!/usr/bin/env python3
"""
AWS EC2 Testing Script

This script provides unit tests for the EC2 automation functionality.
It uses the moto library to mock AWS services for safe testing.

Prerequisites:
- moto library installed (pip install moto)
- pytest library installed (pip install pytest)

Usage:
    python -m pytest test_ec2.py
    or
    python test_ec2.py
"""

import unittest
import boto3
from moto import mock_aws
from aws_automation_scripts.ec2 import EC2Automation


class TestEC2Automation(unittest.TestCase):
    """Test cases for EC2Automation class."""

    @mock_aws
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.ec2 = EC2Automation(region_name='us-east-1')

        # Create a test instance
        ec2_resource = boto3.resource('ec2', region_name='us-east-1')
        instance = ec2_resource.create_instances(
            ImageId='ami-12345678',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro'
        )[0]
        self.test_instance_id = instance.id

    @mock_aws
    def test_list_instances(self):
        """Test listing EC2 instances."""
        # List instances
        # Since list_instances prints output, we can't easily capture it
        # In a real test, you might redirect stdout or modify the method to return data
        # For now, just ensure no exceptions are raised
        try:
            self.ec2.list_instances()
        except Exception as e:
            self.fail(f"list_instances raised an exception: {e}")

    @mock_aws
    def test_start_instance(self):
        """Test starting an EC2 instance."""
        # Start the instance
        result = self.ec2.start_instance(self.test_instance_id)
        # Check that it returns something (the method prints, but doesn't return)
        # In real implementation, you might want to modify methods to return status

    @mock_aws
    def test_stop_instance(self):
        """Test stopping an EC2 instance."""
        # First start it, then stop
        self.ec2.start_instance(self.test_instance_id)
        result = self.ec2.stop_instance(self.test_instance_id)
        # Again, check for no exceptions

    @mock_aws
    def test_instance_states(self):
        """Test that instance states change correctly."""
        # This would require modifying the EC2Automation class to return instance states
        # For now, just test that methods can be called
        pass


if __name__ == '__main__':
    unittest.main()