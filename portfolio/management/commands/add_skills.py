from django.core.management.base import BaseCommand
from portfolio.models import Skill


class Command(BaseCommand):
    help = 'Bulk add skills from command line'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help='Category: HARD, SOFT, or HOBBIES')
        parser.add_argument('skills', nargs='+', help='Skills in format: name or name:proficiency or name:proficiency:icon')

    def handle(self, *args, **options):
        category = options['category'].upper()
        skills_data = options['skills']
        
        if category not in ['HARD', 'SOFT', 'HOBBIES']:
            self.stdout.write(self.style.ERROR('Category must be HARD, SOFT, or HOBBIES'))
            return
        
        created_count = 0
        max_order = Skill.objects.filter(category=category).count()
        
        for idx, skill_str in enumerate(skills_data):
            parts = skill_str.split(':')
            name = parts[0]
            proficiency = int(parts[1]) if len(parts) > 1 else 50
            icon = parts[2] if len(parts) > 2 else ''
            
            skill, created = Skill.objects.get_or_create(
                name=name,
                category=category,
                defaults={
                    'proficiency': proficiency,
                    'icon': icon,
                    'order': max_order + idx
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Added: {name} ({proficiency}%)'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Already exists: {name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully added {created_count} skills to {category} category'))
