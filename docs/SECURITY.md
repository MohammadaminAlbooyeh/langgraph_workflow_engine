# Security Guide

This document outlines security best practices and configurations for the LangGraph Workflow Engine.

## Configuration

### Required Security Settings

Before deploying to production, ensure:

1. **Secret Key**: Change `APP_SECRET_KEY` in `.env` to a strong random string
   ```bash
   # Generate a secure key:
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Environment**: Set `APP_ENVIRONMENT=production`

3. **Debug Mode**: Ensure `APP_DEBUG=false` in production

4. **HTTPS**: Enable HTTPS in production (`SECURITY_REQUIRE_HTTPS=true`)

5. **CORS Origins**: Restrict CORS origins to specific domains
   ```env
   SECURITY_CORS_ORIGINS=["https://yourdomain.com"]
   ```

### API Key Authentication

Configure API key authentication:

```env
SECURITY_ENABLE_API_KEY_AUTH=true
```

Pass API keys in requests:
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/health
```

### JWT Tokens

JWT authentication is enabled by default:

```env
SECURITY_JWT_ENABLED=true
SECURITY_ALGORITHM=HS256
SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Security

### SQLAlchemy Protections

- Uses parameterized queries (ORM) - SQL injection safe by default
- No raw SQL allowed in codebase
- All input validated via Pydantic schemas

### Database URL Security

Store database credentials securely:

```env
# Use environment variables for credentials
DB_URL=postgresql://user:password@host:5432/database

# Or use connection string from secrets manager:
DB_URL=${DATABASE_URL_FROM_SECRETS_MANAGER}
```

## Input Validation

### Pydantic Validation

All API inputs are validated via Pydantic schemas:

```python
class WorkflowCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    nodes: list[NodeCreate]
    edges: list[EdgeCreate]
```

### Request Size Limits

```env
SECURITY_MAX_UPLOAD_SIZE=10485760  # 10 MB
```

## Authentication & Authorization

### API Authentication

1. **API Key Auth**: Add to headers
   ```bash
   X-API-Key: your-secret-key
   ```

2. **JWT Auth**: Get token and use in Authorization header
   ```bash
   Authorization: Bearer <token>
   ```

### Rate Limiting

Enable rate limiting in production:

```env
SECURITY_RATE_LIMIT_ENABLED=true
SECURITY_RATE_LIMIT_REQUESTS=100
SECURITY_RATE_LIMIT_PERIOD=60  # seconds
```

## LLM Integration Security

### API Keys

- Store LLM API keys securely in environment variables
- Never commit API keys to version control
- Rotate keys regularly

```env
LLM_OPENAI_API_KEY=${OPENAI_KEY}
LLM_ANTHROPIC_API_KEY=${ANTHROPIC_KEY}
```

### Prompt Injection Prevention

- Validate user inputs before passing to LLMs
- Use Pydantic validation on all workflow inputs
- Implement content filtering if needed

## Logging & Monitoring

### Secure Logging

- Never log sensitive data (API keys, user inputs)
- Use structured logging with appropriate levels
- Sanitize logs before storing

```python
from backend.utils.logger import get_logger
logger = get_logger(__name__)

# Good: logs action only
logger.info(f"Created workflow: {workflow_id}")

# Bad: logs sensitive data
logger.info(f"API Key: {api_key}")  # Don't do this!
```

## Deployment Security

### Docker Security

```dockerfile
# Use specific base image versions
FROM python:3.11-slim

# Run as non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Copy only necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

### Kubernetes Security

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: langgraph-engine
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
  containers:
  - name: backend
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

## Network Security

### HTTPS/TLS

- Always use HTTPS in production
- Use valid SSL certificates
- Configure HSTS headers

### Firewall Rules

- Restrict database access to application servers only
- Use VPC/security groups for network isolation
- Whitelist allowed IP addresses for API access

## Regular Security Practices

1. **Dependency Updates**: Keep dependencies updated
   ```bash
   pip install --upgrade pip
   pip list --outdated
   ```

2. **Security Scanning**: Scan dependencies for vulnerabilities
   ```bash
   pip install safety
   safety check
   ```

3. **Code Review**: Review security implications of code changes

4. **Secrets Management**: Use a secrets manager (Vault, AWS Secrets Manager, etc.)

5. **Audit Logging**: Log all important actions
   - Workflow creation/deletion
   - Execution start/stop
   - Configuration changes

## Security Checklist for Production Deployment

- [ ] Change `APP_SECRET_KEY` to a secure random value
- [ ] Set `APP_DEBUG=false`
- [ ] Set `APP_ENVIRONMENT=production`
- [ ] Enable HTTPS (`SECURITY_REQUIRE_HTTPS=true`)
- [ ] Configure CORS origins (restrict from `*`)
- [ ] Set up authentication (API Key or JWT)
- [ ] Enable rate limiting
- [ ] Configure database with strong credentials
- [ ] Store LLM API keys in secrets manager
- [ ] Set up SSL/TLS certificates
- [ ] Enable audit logging
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerts
- [ ] Run security scanning tools
- [ ] Review and update dependencies
- [ ] Create disaster recovery plan
- [ ] Document security procedures

## Incident Response

If a security incident occurs:

1. Rotate compromised keys immediately
2. Review audit logs for affected operations
3. Notify affected users
4. Deploy patches/fixes
5. Document incident and lessons learned

## Security Contacts

Report security vulnerabilities responsibly:

1. Do not open public issues for security vulnerabilities
2. Email security team with details
3. Allow 90 days for patch and disclosure

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- FastAPI Security: https://fastapi.tiangodb.com/tutorial/security/
- SQLAlchemy Best Practices: https://docs.sqlalchemy.org/
- Docker Security: https://docs.docker.com/engine/security/
