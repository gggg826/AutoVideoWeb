# Docker Deployment Guide

This guide explains how to deploy AutoVideoWeb using Docker.

## Prerequisites

- Docker installed (version 20.10 or higher)
- Docker Compose installed (version 2.0 or higher)

## Quick Start

### Using Docker Compose (Recommended)

1. **Start the application**:
   ```bash
   docker-compose up -d
   ```

2. **Access the application**:
   - Main site: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Admin panel: http://localhost:8000/admin/login.html
   - Test page: http://localhost:8000/public/index.html

3. **View logs**:
   ```bash
   docker-compose logs -f
   ```

4. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image**:
   ```bash
   docker build -t autovideoweb .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name autovideoweb \
     -p 8000:8000 \
     -v $(pwd)/data:/app/data \
     autovideoweb
   ```

3. **Stop the container**:
   ```bash
   docker stop autovideoweb
   docker rm autovideoweb
   ```

## Configuration

### Environment Variables

You can customize the application by modifying environment variables in `docker-compose.yml`:

- `APP_NAME`: Application name (default: "AutoVideoWeb")
- `APP_VERSION`: Application version (default: "1.0.0")
- `ENVIRONMENT`: Environment mode (default: "production")
- `DEBUG`: Enable debug mode (default: "false")
- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: "8000")
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key (CHANGE THIS IN PRODUCTION!)
- `ADMIN_USERNAME`: Admin username (default: "admin")
- `ADMIN_PASSWORD`: Admin password (default: "Admin@123" - CHANGE THIS!)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 15)

### Security Configuration

**IMPORTANT**: Before deploying to production:

1. **Change the SECRET_KEY**:
   ```yaml
   environment:
     - SECRET_KEY=your-random-secret-key-here-use-long-random-string
   ```

   Generate a secure secret key:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Change the admin password**:
   ```yaml
   environment:
     - ADMIN_PASSWORD=YourSecurePassword123!
   ```

3. **Use environment file** (recommended for production):

   Create a `.env` file:
   ```env
   SECRET_KEY=your-secret-key-here
   ADMIN_PASSWORD=your-secure-password
   ```

   Update docker-compose.yml:
   ```yaml
   services:
     web:
       env_file: .env
   ```

## Data Persistence

The database is persisted in a Docker volume mounted to `./data` on the host. This ensures your data survives container restarts.

**Backup the database**:
```bash
# Stop the container
docker-compose down

# Backup the database
cp data/visits.db data/visits.db.backup

# Restart
docker-compose up -d
```

## Health Check

The container includes a health check that verifies the application is running:

```bash
# Check container health
docker-compose ps
```

## Troubleshooting

### Container won't start

Check logs:
```bash
docker-compose logs
```

### Permission issues with volume

On Linux, you may need to adjust permissions:
```bash
sudo chown -R $USER:$USER ./data
```

### Database locked errors

Ensure only one instance is running:
```bash
docker-compose down
docker-compose up -d
```

### Port already in use

If port 8000 is already in use, change it in docker-compose.yml:
```yaml
ports:
  - "8080:8000"  # Use port 8080 instead
```

## Production Deployment

For production deployment:

1. **Use HTTPS**: Place a reverse proxy (nginx/Caddy) in front
2. **Change secrets**: Update SECRET_KEY and ADMIN_PASSWORD
3. **Regular backups**: Set up automated database backups
4. **Monitor logs**: Use a log aggregation service
5. **Resource limits**: Add resource limits to docker-compose.yml:

   ```yaml
   services:
     web:
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 512M
           reservations:
             cpus: '0.5'
             memory: 256M
   ```

## Updating

To update to a new version:

```bash
# Stop the current container
docker-compose down

# Pull new code
git pull

# Rebuild and restart
docker-compose up -d --build
```

## Cleanup

Remove all containers, volumes, and images:

```bash
# Stop and remove containers
docker-compose down -v

# Remove image
docker rmi autovideoweb
```

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- GitHub Issues: https://github.com/gggg826/AutoVideoWeb/issues
