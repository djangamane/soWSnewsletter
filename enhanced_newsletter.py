from datetime import datetime
import json
from textblob import TextBlob

class CriticalAnalyzer:
    def generate_combined_analysis(self, article):
        """Generate combined Welsing-Wilson analysis based on content"""
        content = f"{article['title']} {article.get('full_text', '')}"
        content = content.lower()

        # Violence/hate incident analysis
        if any(word in content for word in ['violence', 'attack', 'hate', 'threat', 'kill']):
            return ("This incident reveals the ongoing manifestation of white supremacy's survival response through violence and intimidation. The intersection of psychological warfare and material force demonstrates how systemic racism maintains dominance through both terror and institutional power. This represents the continuing pattern of white supremacy's reaction to perceived threats to its global position.")

        # Political/institutional analysis
        elif any(word in content for word in ['policy', 'government', 'law', 'court', 'school']):
            return ("This institutional development exemplifies the sophisticated mechanics of systemic racism operating through bureaucratic channels. The psychological warfare identified by Dr. Welsing merges with Dr. Wilson's analysis of political-economic control, revealing how white supremacy maintains power through seemingly neutral institutional processes. This represents the ongoing refinement of systemic oppression through policy and governance.")

        # Cultural/media analysis
        elif any(word in content for word in ['media', 'culture', 'social', 'twitter', 'facebook']):
            return ("This cultural manifestation demonstrates how white supremacy operates through both symbolic warfare and social control mechanisms. The psychological dynamics highlight the system's use of media and cultural products to maintain dominance, while the political-economic implications reveal how these platforms serve as tools for maintaining systemic power relationships.")

        # Resistance/movement analysis
        elif any(word in content for word in ['protest', 'resistance', 'movement', 'activist', 'organize']):
            return ("This resistance represents a critical challenge to both the psychological and material dimensions of white supremacy. Dr. Welsing would identify this as a necessary confrontation with the global system, while Dr. Wilson would emphasize its potential for building independent political-economic power. This demonstrates the type of conscious, organized opposition needed to challenge systemic racism effectively.")

        # Default analysis
        else:
            return ("This development must be analyzed within the broader context of global white supremacy's operational mechanics. The psychological patterns identified by Dr. Welsing intersect with the material conditions emphasized by Dr. Wilson, revealing how systemic racism maintains power through multiple, interconnected mechanisms of control.")

def create_meter_visualization(severity_score):
    """Create a text-based meter visualization"""
    meter_width = 50
    filled = int((severity_score * meter_width) / 100)
    meter = f"""
STATE OF WHITE SUPREMACY METER:
{'-' * 60}
Current Level: {severity_score:.1f}%

[{'█' * filled}{'░' * (meter_width - filled)}]
0%{' ' * (meter_width-6)}100%

"""
    if severity_score >= 75:
        meter += """CRITICAL ALERT: The system is intensifying its survival response. Recent events
indicate coordinated efforts to maintain white genetic dominance through both
institutional and cultural warfare. Stay vigilant, stay organized, and above all,
stay conscious of the true nature of our struggle."""
    elif severity_score >= 50:
        meter += """WARNING: Significant white supremacy activity present.
Continued monitoring and organized response recommended."""
    else:
        meter += """NOTICE: Baseline white supremacy activity observed.
Maintain standard monitoring and resistance protocols."""

    return meter

def create_newsletter(filename):
    # Load the article data
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    analyzer = CriticalAnalyzer()

    # Sort articles by severity score
    articles = sorted(data['articles'], 
                     key=lambda x: x['severity_score'], 
                     reverse=True)[:10]  # Get top 10 most severe articles

    # Generate newsletter
    newsletter = f"""
🔍 Critical Race Analysis Newsletter 🔍
State of White Supremacy Alert
{datetime.now().strftime('%B %d, %Y')}

SYSTEM STATUS ALERT:
Current Severity Level: {data['average_severity']:.1f}%
Total Articles Monitored: {data['total_articles']}

TOP STORIES ANALYSIS:
"""

    for idx, article in enumerate(articles, 1):
        newsletter += f"""
{idx}. {article['title']}
Severity Score: {article['severity_score']:.1f}

Summary:
{article.get('summary', 'No summary available')}

Critical Analysis:
{analyzer.generate_combined_analysis(article)}

🔗 Read more: {article['url']}
---
"""

    newsletter += """
Analysis Framework:
This newsletter combines Dr. Frances Cress Welsing's Color Confrontation 
theory with Dr. Amos Wilson's political-economic analysis to provide a 
comprehensive understanding of how white supremacy operates through both 
psychological and material mechanisms of control.
"""

    # Add the meter visualization
    newsletter += "\n" + create_meter_visualization(data['average_severity'])

    # Save newsletter
    output_filename = f'critical_newsletter_{datetime.now().strftime("%Y%m%d")}.txt'
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(newsletter)

    return output_filename, newsletter

def main():
    today = datetime.now().strftime('%Y%m%d')
    input_file = f'full_articles_{today}.json'
    try:
        filename, newsletter = create_newsletter(input_file)
        print(f"\nNewsletter created: {filename}")
        print("\nPreview of first few lines:")
        print("\n".join(newsletter.split("\n")[:10]))
    except Exception as e:
        print(f"Error creating newsletter: {e}")

if __name__ == "__main__":
    main()