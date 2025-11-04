import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from .models import GitHubRepository, GitHubLanguage, GitHubCommit


class GitHubService:
    """Service to interact with GitHub API"""
    
    def __init__(self, username=None, token=None):
        self.username = username or settings.GITHUB_USERNAME
        self.token = token or getattr(settings, 'GITHUB_TOKEN', None)
        self.base_url = settings.GITHUB_API_URL
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
    
    def fetch_repositories(self, sync_to_db=True):
        """Fetch all repositories for the user"""
        if not self.username:
            raise ValueError("GitHub username not configured")
        
        url = f"{self.base_url}/users/{self.username}/repos"
        params = {
            'sort': 'updated',
            'per_page': 100,
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            repos = response.json()
            
            if sync_to_db:
                return self._sync_repositories_to_db(repos)
            return repos
        except requests.RequestException as e:
            print(f"Error fetching repositories: {e}")
            return []
    
    def fetch_repository_details(self, repo_name, sync_to_db=True):
        """Fetch detailed information for a specific repository"""
        url = f"{self.base_url}/repos/{self.username}/{repo_name}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            repo_data = response.json()
            
            if sync_to_db:
                return self._sync_single_repository(repo_data)
            return repo_data
        except requests.RequestException as e:
            print(f"Error fetching repository {repo_name}: {e}")
            return None
    
    def fetch_repository_languages(self, repo_name):
        """Fetch programming languages used in a repository"""
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/languages"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching languages for {repo_name}: {e}")
            return {}
    
    def fetch_repository_commits(self, repo_name, limit=10):
        """Fetch recent commits for a repository"""
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/commits"
        params = {'per_page': limit}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching commits for {repo_name}: {e}")
            return []
    
    def _sync_repositories_to_db(self, repos_data):
        """Sync repository data to database"""
        synced_repos = []
        
        for repo_data in repos_data:
            repo = self._sync_single_repository(repo_data)
            if repo:
                synced_repos.append(repo)
                # Fetch and sync languages
                self._sync_repository_languages(repo, repo_data['name'])
        
        return synced_repos
    
    def _sync_single_repository(self, repo_data):
        """Sync a single repository to database"""
        try:
            repo, created = GitHubRepository.objects.update_or_create(
                github_id=repo_data['id'],
                defaults={
                    'name': repo_data['name'],
                    'full_name': repo_data['full_name'],
                    'description': repo_data.get('description', ''),
                    'url': repo_data['html_url'],
                    'homepage': repo_data.get('homepage', ''),
                    'stars_count': repo_data.get('stargazers_count', 0),
                    'forks_count': repo_data.get('forks_count', 0),
                    'watchers_count': repo_data.get('watchers_count', 0),
                    'open_issues_count': repo_data.get('open_issues_count', 0),
                    'size': repo_data.get('size', 0),
                    'primary_language': repo_data.get('language', ''),
                    'topics': repo_data.get('topics', []),
                    'is_fork': repo_data.get('fork', False),
                    'is_private': repo_data.get('private', False),
                    'is_archived': repo_data.get('archived', False),
                    'created_at': self._parse_datetime(repo_data['created_at']),
                    'updated_at': self._parse_datetime(repo_data['updated_at']),
                    'pushed_at': self._parse_datetime(repo_data.get('pushed_at')),
                }
            )
            return repo
        except Exception as e:
            print(f"Error syncing repository {repo_data.get('name', 'unknown')}: {e}")
            return None
    
    def _sync_repository_languages(self, repo, repo_name):
        """Sync programming languages for a repository"""
        languages_data = self.fetch_repository_languages(repo_name)
        
        if not languages_data:
            return
        
        # Calculate total bytes
        total_bytes = sum(languages_data.values())
        
        # Clear existing languages
        repo.languages.all().delete()
        
        # Create new language entries
        for lang_name, bytes_count in languages_data.items():
            percentage = (bytes_count / total_bytes * 100) if total_bytes > 0 else 0
            GitHubLanguage.objects.create(
                repository=repo,
                name=lang_name,
                bytes_count=bytes_count,
                percentage=round(percentage, 2)
            )
    
    def _parse_datetime(self, dt_string):
        """Parse GitHub datetime string to Django datetime"""
        if not dt_string:
            return None
        try:
            dt = datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%SZ')
            return timezone.make_aware(dt, timezone.utc)
        except (ValueError, TypeError):
            return None
    
    def sync_all_data(self):
        """Sync all GitHub data (repositories, languages, commits)"""
        repos = self.fetch_repositories(sync_to_db=True)
        print(f"Synced {len(repos)} repositories")
        return repos
