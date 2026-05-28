# Troubleshooting Guide

## Common Issues

### Server won't start
- Check Python version (3.11+ required)
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check `.env` configuration

### API returns 500
- Check server logs for error details
- Verify database connection
- Ensure all environment variables are set

### Workflow execution fails
- Verify graph has no cycles (use validation endpoints)
- Check node configurations are valid
- Ensure required fields are provided

### Frontend not loading
- Verify API proxy is configured in `package.json`
- Check browser console for errors
- Ensure backend server is running

## Getting Help

Open an issue on GitHub with:
- Steps to reproduce
- Server logs
- Workflow definition (if applicable)
