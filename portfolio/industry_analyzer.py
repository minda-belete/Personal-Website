"""
Industry Index AI Analyzer
Uses OpenAI to analyze user's profile and generate industry relevance rankings
"""
import json
from datetime import datetime
from openai import OpenAI


def gather_profile_data():
    """Gather all relevant data from the website for analysis"""
    from .models import (
        HomePage, AboutPageSettings, Education, Research, 
        Skill, Experience, TimelineEntry
    )
    from blog.models import BlogPost
    
    data = {
        'homepage': {},
        'about': {},
        'education': [],
        'research': [],
        'skills': [],
        'experience': [],
        'blog_posts': [],
        'timeline': []
    }
    
    # Homepage data - includes current position and background
    try:
        homepage = HomePage.objects.first()
        if homepage:
            data['homepage'] = {
                'title': homepage.hero_title,
                'description': homepage.hero_description,
                'cta_primary': homepage.cta_primary_text,
                'cta_secondary': homepage.cta_secondary_text,
                'about_section': homepage.about_section[:500] if homepage.about_section else '',
            }
    except:
        pass
    
    # About page data
    try:
        about = AboutPageSettings.objects.first()
        if about:
            data['about'] = {
                'bio': about.intro_bio[:500] if about.intro_bio else '',
            }
    except:
        pass
    
    # Education - comprehensive background
    try:
        for edu in Education.objects.all()[:5]:
            data['education'].append({
                'degree': edu.degree,
                'field': edu.field_of_study,
                'institution': edu.institution,
                'location': edu.location if hasattr(edu, 'location') and edu.location else '',
                'description': edu.description[:200] if hasattr(edu, 'description') and edu.description else '',
                'start_date': str(edu.start_date) if edu.start_date else '',
                'end_date': str(edu.end_date) if edu.end_date else 'Present',
            })
    except:
        pass
    
    # Research
    try:
        for research in Research.objects.all()[:10]:
            data['research'].append({
                'title': research.title,
                'type': research.research_type,
                'abstract': research.abstract[:200] if research.abstract else '',
            })
    except:
        pass
    
    # Skills
    try:
        for skill in Skill.objects.all()[:30]:
            data['skills'].append({
                'name': skill.name,
                'category': skill.category,
                'proficiency': skill.proficiency,
            })
    except:
        pass
    
    # Experience - includes current position
    try:
        for exp in Experience.objects.all()[:5]:
            is_current = exp.end_date is None if hasattr(exp, 'end_date') else False
            data['experience'].append({
                'title': exp.title,
                'company': exp.company,
                'description': exp.description[:300] if exp.description else '',
                'location': exp.location if hasattr(exp, 'location') and exp.location else '',
                'start_date': str(exp.start_date) if hasattr(exp, 'start_date') and exp.start_date else '',
                'end_date': str(exp.end_date) if hasattr(exp, 'end_date') and exp.end_date else 'Present',
                'is_current': is_current,
            })
    except:
        pass
    
    # Blog posts
    try:
        for post in BlogPost.objects.filter(status='PUBLISHED')[:10]:
            data['blog_posts'].append({
                'title': post.title,
                'excerpt': post.excerpt[:150] if post.excerpt else '',
            })
    except:
        pass
    
    # Timeline entries
    try:
        for entry in TimelineEntry.objects.filter(is_active=True)[:10]:
            data['timeline'].append({
                'period': entry.period,
                'title': entry.title,
                'year': entry.year,
            })
    except:
        pass
    
    return data


def generate_industry_rankings(api_key):
    """Use OpenAI to generate industry rankings based on profile data"""
    
    # Gather all profile data
    profile_data = gather_profile_data()
    
    # Create OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Construct the prompt
    prompt = f"""
You are an expert career analyst. Based on the following comprehensive professional profile data, analyze and rank the top 10 industries where this person would be most relevant and valuable.

IMPORTANT: Pay special attention to:
- Homepage content (hero_title, hero_description) which describes their current position and professional identity
- Current work experience (where end_date is "Present") which indicates their active industry
- Education background (degree, field of study, institution) which shows their academic foundation
- Research interests and publications which demonstrate expertise areas
- Skills and proficiency levels across different categories
- Blog posts and thought leadership content
- Timeline entries showing career progression

Profile Data:
{json.dumps(profile_data, indent=2)}

Please provide:
1. Top 10 industries ranked by relevance (1 = most relevant)
2. For each industry:
   - Industry name
   - Relevance score (0-100)
   - Brief reasoning (2-3 sentences explaining why they're relevant to this industry, citing specific evidence from their profile)
   - Key skills that make them relevant (comma-separated list of 3-5 skills)

CRITICAL: To identify their CURRENT industry, use ONLY the homepage hero_description field. Look at the FIRST line which describes their current position/role. 
- If they work at a university, college, or educational institution (e.g., "Academic Researcher at [University]", "Professor at", "Research Fellow at"), their current industry is "Higher Education"
- If they work at a tech company, their current industry is "Technology"
- If they work at a financial institution, their current industry is "Finance"
Focus on WHERE they currently work (their employer), not what they're studying or their educational background.

Respond in JSON format:
{{
  "current_industry": "Industry Name",
  "rankings": [
    {{
      "rank": 1,
      "industry_name": "Industry Name",
      "relevance_score": 95,
      "reasoning": "Explanation here...",
      "key_skills": "Skill1, Skill2, Skill3"
    }},
    ...
  ]
}}
"""
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert career analyst specializing in industry fit analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Parse the response
        result_text = response.choices[0].message.content
        
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        return result
        
    except Exception as e:
        print(f"Error generating rankings: {e}")
        return None


def update_industry_rankings(api_key):
    """Generate new rankings and update the database"""
    from .models import IndustryRanking, IndustryIndexSettings
    from django.utils import timezone
    
    # Generate rankings using AI
    result = generate_industry_rankings(api_key)
    
    if not result:
        return False
    
    # Clear existing rankings
    IndustryRanking.objects.all().delete()
    
    # Get current industry from result
    current_industry = result.get('current_industry', '')
    
    # Separate current industry from others
    rankings_list = result.get('rankings', [])[:10]
    current_industry_data = None
    other_rankings = []
    
    for ranking_data in rankings_list:
        if ranking_data['industry_name'].lower() == current_industry.lower():
            current_industry_data = ranking_data
        else:
            other_rankings.append(ranking_data)
    
    # Create current industry as rank #1 if found
    if current_industry_data:
        IndustryRanking.objects.create(
            industry_name=current_industry_data['industry_name'],
            rank=1,
            relevance_score=max(current_industry_data['relevance_score'], 95),  # Ensure high score
            reasoning=current_industry_data['reasoning'],
            key_skills=current_industry_data['key_skills'],
            is_current_industry=True
        )
        # Adjust ranks for other industries
        rank_counter = 2
    else:
        rank_counter = 1
    
    # Create other rankings starting from rank 2 (or 1 if no current industry)
    for ranking_data in other_rankings[:9]:  # Top 9 others
        IndustryRanking.objects.create(
            industry_name=ranking_data['industry_name'],
            rank=rank_counter,
            relevance_score=ranking_data['relevance_score'],
            reasoning=ranking_data['reasoning'],
            key_skills=ranking_data['key_skills'],
            is_current_industry=False
        )
        rank_counter += 1
    
    # Update last generated timestamp
    settings, created = IndustryIndexSettings.objects.get_or_create(pk=1)
    settings.last_generated = timezone.now()
    if not settings.current_industry and current_industry:
        settings.current_industry = current_industry
    settings.save()
    
    return True
