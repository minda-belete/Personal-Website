from django.core.management.base import BaseCommand
from portfolio.models import Skill


class Command(BaseCommand):
    help = 'Remove duplicate skills keeping the ones with specific subcategories'

    def handle(self, *args, **options):
        # Find all skill names that have duplicates
        from django.db.models import Count
        
        duplicates = Skill.objects.values('name').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        cleaned = 0
        for dup in duplicates:
            name = dup['name']
            skills = Skill.objects.filter(name=name).order_by('-id')
            
            # Keep the most recent one (highest ID), delete others with subcategory='OTHER'
            latest = skills.first()
            
            if latest.subcategory != 'OTHER':
                # Delete older ones with OTHER subcategory
                deleted = Skill.objects.filter(name=name, subcategory='OTHER').delete()
                if deleted[0] > 0:
                    cleaned += deleted[0]
                    self.stdout.write(self.style.SUCCESS(f'✓ Cleaned {name} - kept {latest.subcategory}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Cleaned {cleaned} duplicate skills'))
