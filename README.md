# Professional Portfolio Website

A modern, feature-rich personal portfolio website built with Django, featuring a professional blog with advanced editing capabilities, GitHub integration, and interactive content support.

## Features

### 🎯 Core Features
- **Professional Portfolio**: Showcase your education, research, experience, and skills
- **Advanced Blog System**: Rich text editor with support for:
  - Images, Videos, and GIFs
  - Code snippets with syntax highlighting
  - Interactive maps (Leaflet.js)
  - Categories and tags
  - Comment system
  - View tracking
- **GitHub Integration**: Automatically fetch and display your repositories via GitHub API
- **Responsive Design**: Modern, mobile-friendly UI with animations
- **Admin Dashboard**: Easy content management through Django admin

### 📚 Apps

1. **Portfolio**: Profile, education, research, experience, skills, CV
2. **Blog**: Advanced blogging with rich media support
3. **GitHub Integration**: Repository showcase with live API sync

## Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Instructions

1. **Clone or navigate to the project directory**
```bash
cd personal_website
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure settings**
Edit `personal_website/settings.py` and set:
- `GITHUB_USERNAME`: Your GitHub username for API integration
- `SECRET_KEY`: Generate a new secret key for production
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain names

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files** (for production)
```bash
python manage.py collectstatic
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view your website!

## Usage

### Admin Panel
Access the admin panel at `http://127.0.0.1:8000/admin/` to:
- Create and manage your profile
- Add education, research, and experience entries
- Write and publish blog posts
- Manage GitHub repositories
- Moderate comments

### GitHub Integration
1. Set your GitHub username in `settings.py`:
```python
GITHUB_USERNAME = "your-github-username"
```

2. (Optional) Add GitHub token for higher API rate limits:
```python
GITHUB_TOKEN = "your-github-token"
```

3. Sync repositories from admin panel or run:
```bash
python manage.py shell
>>> from github_integration.services import GitHubService
>>> service = GitHubService()
>>> service.sync_all_data()
```

### Creating Blog Posts

1. Go to Admin → Blog → Blog Posts → Add Blog Post
2. Use the CKEditor to create rich content:
   - Insert images, videos, and GIFs
   - Add code snippets with syntax highlighting
   - Embed YouTube/Vimeo videos
3. Add code snippets and interactive maps using inline forms
4. Set categories, tags, and featured status
5. Publish when ready!

### Adding Interactive Maps

In the blog post admin, use the "Interactive Maps" inline form to add maps with:
- Custom center coordinates (latitude/longitude)
- Zoom level
- GeoJSON data for custom features
- External map URLs

### Code Snippets

Add standalone code snippets to blog posts with:
- Multiple language support (Python, JavaScript, Java, C++, etc.)
- Syntax highlighting
- Copy-to-clipboard functionality
- Custom titles and descriptions

## Project Structure

```
personal_website/
├── blog/                      # Blog app
│   ├── models.py             # BlogPost, Category, CodeSnippet, InteractiveMap
│   ├── views.py              # Blog views
│   ├── admin.py              # Admin customization
│   └── urls.py               # Blog URLs
├── portfolio/                 # Portfolio app
│   ├── models.py             # Profile, Education, Research, Experience, Skill
│   ├── views.py              # Portfolio views
│   ├── admin.py              # Admin customization
│   └── urls.py               # Portfolio URLs
├── github_integration/        # GitHub integration app
│   ├── models.py             # GitHubRepository, GitHubLanguage
│   ├── services.py           # GitHub API service
│   ├── views.py              # Repository views
│   └── admin.py              # Admin customization
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── portfolio/            # Portfolio templates
│   └── blog/                 # Blog templates
├── static/                    # Static files
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript files
│   └── images/               # Images
├── media/                     # User-uploaded files
├── personal_website/          # Project settings
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI configuration
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

## Technologies Used

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5, Font Awesome, AOS (Animate On Scroll)
- **Rich Text Editor**: CKEditor with code snippet support
- **Maps**: Leaflet.js
- **Code Highlighting**: Prism.js
- **API Integration**: GitHub REST API
- **Database**: SQLite (development), PostgreSQL/MySQL (production recommended)

## Customization

### Styling
Edit `static/css/style.css` to customize:
- Color scheme (CSS variables in `:root`)
- Typography
- Component styles
- Animations

### Templates
Modify templates in `templates/` directory to change:
- Layout and structure
- Content sections
- Navigation

### Adding New Features
1. Create new models in respective apps
2. Add views and URLs
3. Create templates
4. Register in admin.py for easy management

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for sensitive data
- [ ] Set up PostgreSQL/MySQL database
- [ ] Configure static file serving (WhiteNoise or CDN)
- [ ] Set up media file storage (AWS S3 or similar)
- [ ] Enable HTTPS
- [ ] Configure email backend for notifications
- [ ] Set up backup strategy

### Recommended Hosting
- **Heroku**: Easy deployment with Git
- **DigitalOcean**: App Platform or Droplets
- **AWS**: Elastic Beanstalk or EC2
- **PythonAnywhere**: Simple Django hosting
- **Railway**: Modern platform with free tier

## Contributing

This is a personal portfolio project, but feel free to fork and customize for your own use!

## License

MIT License - feel free to use this project for your own portfolio.

## Support

For issues or questions, please create an issue in the repository or contact the developer.

---

**Built with ❤️ using Django**
