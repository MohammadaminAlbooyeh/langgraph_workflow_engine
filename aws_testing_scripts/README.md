# AWS Testing Scripts

This directory contains testing scripts for the AWS automation functionality.

## test_ec2.py

Unit tests for the EC2 automation script using the moto library to mock AWS services.

### Running the tests

1. Ensure you have a virtual environment set up and activated.
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m pytest test_ec2.py -v`

### Test Coverage

- Test listing EC2 instances
- Test starting an EC2 instance
- Test stopping an EC2 instance
- Basic state management tests

## Adding More Tests

To add tests for other AWS services (RDS, Lambda), create similar test files following the same pattern.