# AWS Management Scripts

This repository contains automation scripts for managing AWS resources.

## Prerequisites

1. Python 3.6 or higher
2. AWS CLI configured with your credentials
3. Required Python packages (install with `pip install -r requirements.txt`)

## Setup

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure AWS credentials:
   ```bash
   aws configure
   ```
   Or set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

## EC2 Automation Script

The `aws_automation_scripts/ec2.py` script provides comprehensive EC2 instance management capabilities.

### Usage

```bash
# List all instances
python aws_automation_scripts/ec2.py list

# List instances with filters
python aws_automation_scripts/ec2.py list --filter instance-state-name=running

# Start an instance
python aws_automation_scripts/ec2.py start --instance-id i-1234567890abcdef0

# Stop an instance
python aws_automation_scripts/ec2.py stop --instance-id i-1234567890abcdef0

# Create a new instance
python aws_automation_scripts/ec2.py create \
  --ami-id ami-12345678 \
  --instance-type t2.micro \
  --key-name my-key-pair \
  --tags Name=MyInstance Environment=Dev

# Terminate an instance
python aws_automation_scripts/ec2.py terminate --instance-id i-1234567890abcdef0
```

### Available Actions

- `list`: List EC2 instances (with optional filters)
- `start`: Start a stopped EC2 instance
- `stop`: Stop a running EC2 instance
- `create`: Create a new EC2 instance
- `terminate`: Terminate an EC2 instance

### Command Line Options

- `--region`: AWS region (default: us-east-1)
- `--instance-id`: EC2 instance ID (required for start, stop, terminate)
- `--ami-id`: AMI ID (required for create)
- `--instance-type`: Instance type (required for create)
- `--key-name`: Key pair name (required for create)
- `--security-groups`: Security group IDs (optional for create)
- `--user-data`: User data script (optional for create)
- `--tags`: Tags in Key=Value format (optional for create)
- `--filter`: Filters in Name=Value format (optional for list)

### Examples

#### List running instances in us-west-2
```bash
python aws_automation_scripts/ec2.py list --region us-west-2 --filter instance-state-name=running
```

#### Create an Ubuntu instance with tags
```bash
python aws_automation_scripts/ec2.py create \
  --ami-id ami-0abcdef1234567890 \
  --instance-type t3.small \
  --key-name my-ssh-key \
  --tags Name=WebServer Environment=Production \
  --region us-east-1
```

#### Start multiple instances (modify script for batch operations)
The current script handles one instance at a time. For batch operations, you can modify the script or run it multiple times.

## Security Considerations

- Ensure your AWS credentials have the minimum required permissions for EC2 operations
- Use IAM roles when possible instead of access keys
- Regularly rotate your AWS credentials
- Monitor your AWS usage and costs

## Troubleshooting

1. **Credentials Error**: Make sure AWS credentials are properly configured
2. **Region Error**: Verify the region name and that the instance exists in that region
3. **Permissions Error**: Check that your IAM user/role has the necessary EC2 permissions
4. **Instance Not Found**: Double-check the instance ID

## Contributing

Feel free to contribute improvements or additional AWS automation scripts!