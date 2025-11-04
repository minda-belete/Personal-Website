# Google Cloud Deployment Guide

This guide will help you deploy your Django personal website to Google Cloud Platform using Google App Engine.

## Prerequisites

1. **Google Cloud Account**: Create an account at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud SDK**: Install the gcloud CLI tool
   ```bash
   # For macOS
   brew install --cask google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

3. **Google Cloud Project**: Create a new project in the Google Cloud Console

## Setup Steps

### 1. Initialize Google Cloud SDK

```bash
# Login to your Google account
gcloud auth login

# Set your project ID (replace YOUR_PROJECT_ID with your actual project ID)
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable appengine.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable storage-api.googleapis.com
```

### 2. Create Cloud SQL Database (PostgreSQL)

```bash
# Create a PostgreSQL instance
gcloud sql instances create personal-website-db \
    --database-version=POSTGRES_14 \
    --tier=db-f1-micro \
    --region=us-central1

# Create a database
gcloud sql databases create personal_website_db \
    --instance=personal-website-db

# Create a database user
gcloud sql users create dbuser \
    --instance=personal-website-db \
    --password=YOUR_SECURE_PASSWORD
```

### 3. Create Cloud Storage Bucket (for media files)

```bash
# Create a bucket for media files
gsutil mb -l us-central1 gs://YOUR_PROJECT_ID-media

# Make the bucket publicly readable
gsutil iam ch allUsers:objectViewer gs://YOUR_PROJECT_ID-media
```

### 4. Set Environment Variables in app.yaml

Edit `app.yaml` and add your environment variables:

```yaml
env_variables:
  DJANGO_SETTINGS_MODULE: 'personal_website.settings'
  DEBUG: 'False'
  SECRET_KEY: 'your-production-secret-key-here'
  ALLOWED_HOSTS: 'your-app-id.appspot.com'
  DATABASE_URL: 'postgres://dbuser:YOUR_SECURE_PASSWORD@//cloudsql/YOUR_PROJECT_ID:us-central1:personal-website-db/personal_website_db'
  GITHUB_USERNAME: 'minda-belete'
  OPENAI_API_KEY: 'your-openai-api-key'
  GS_BUCKET_NAME: 'YOUR_PROJECT_ID-media'
  GS_PROJECT_ID: 'YOUR_PROJECT_ID'
```

### 5. Collect Static Files

```bash
# Collect all static files
python manage.py collectstatic --noinput
```

### 6. Run Migrations Locally First

```bash
# Test migrations locally
python manage.py migrate
```

### 7. Deploy to Google App Engine

```bash
# Deploy your application
gcloud app deploy

# Deploy will:
# - Upload your code
# - Install dependencies from requirements.txt
# - Start your application
```

### 8. Run Database Migrations on Production

```bash
# Connect to Cloud SQL and run migrations
gcloud sql connect personal-website-db --user=dbuser

# Or use Cloud SQL Proxy
./cloud_sql_proxy -instances=YOUR_PROJECT_ID:us-central1:personal-website-db=tcp:5432

# Then in another terminal, run migrations with production DATABASE_URL
python manage.py migrate
```

### 9. Create Superuser

```bash
# SSH into your App Engine instance
gcloud app instances ssh [INSTANCE_ID] --service=default --version=[VERSION_ID]

# Create superuser
python manage.py createsuperuser
```

### 10. View Your Application

```bash
# Open your deployed app in browser
gcloud app browse
```

## Environment Variables Reference

Create these environment variables in `app.yaml`:

- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DEBUG`: Set to 'False' in production
- `ALLOWED_HOSTS`: Your App Engine URL (e.g., 'your-project.appspot.com')
- `DATABASE_URL`: PostgreSQL connection string for Cloud SQL
- `GITHUB_USERNAME`: Your GitHub username
- `OPENAI_API_KEY`: Your OpenAI API key
- `GS_BUCKET_NAME`: Google Cloud Storage bucket name for media files
- `GS_PROJECT_ID`: Your Google Cloud project ID

## Monitoring and Logs

```bash
# View logs
gcloud app logs tail -s default

# View in Cloud Console
# Go to: https://console.cloud.google.com/logs
```

## Updating Your Application

```bash
# After making changes, redeploy
python manage.py collectstatic --noinput
gcloud app deploy
```

## Cost Optimization

- **Free Tier**: App Engine offers a free tier with limited resources
- **F1 Instance**: The app.yaml uses F1 instance class (lowest cost)
- **Auto-scaling**: Configured to scale between 1-10 instances based on traffic
- **Database**: Using db-f1-micro (smallest/cheapest tier)

## Troubleshooting

### Static Files Not Loading
- Ensure `collectstatic` was run before deployment
- Check that WhiteNoise is properly configured in settings.py

### Database Connection Issues
- Verify DATABASE_URL format in app.yaml
- Ensure Cloud SQL instance is running
- Check that database user has proper permissions

### Application Errors
- Check logs: `gcloud app logs tail -s default`
- Verify all environment variables are set in app.yaml
- Ensure DEBUG is set to 'False' in production

## Security Notes

1. **Never commit** `app.yaml` with real credentials to version control
2. Use **Secret Manager** for sensitive data in production
3. Keep `.env` file local only
4. Rotate your `SECRET_KEY` regularly
5. Use strong passwords for database users

## Alternative: Using Secret Manager (Recommended)

Instead of putting secrets in `app.yaml`, use Google Secret Manager:

```bash
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secrets
echo -n "your-secret-key" | gcloud secrets create django-secret-key --data-file=-
echo -n "your-openai-key" | gcloud secrets create openai-api-key --data-file=-

# Grant App Engine access to secrets
gcloud secrets add-iam-policy-binding django-secret-key \
    --member=serviceAccount:YOUR_PROJECT_ID@appspot.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor
```

Then update your code to fetch secrets from Secret Manager instead of environment variables.

## Support

For issues or questions:
- Google Cloud Documentation: https://cloud.google.com/appengine/docs/python
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
