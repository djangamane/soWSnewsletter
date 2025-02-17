import feedparser
import trafilatura
from datetime import datetime
import json
import time
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup

class ArticleAnalyzer:
    def __init__(self):
        self.rss_feeds = {
            'systemic racism': 'https://www.google.com/alerts/feeds/10165470848348617632/1275500178973299905',
            'white supremacy': 'https://www.google.com/alerts/feeds/10165470848348617632/3940701198525793370',
            'MAGA': 'https://www.google.com/alerts/feeds/10165470848348617632/10597775849581651827',
            'anti-racism': 'https://www.google.com/alerts/feeds/10165470848348617632/11994432634058940791',
            'christian nationalism': 'https://www.google.com/alerts/feeds/10165470848348617632/3940701198525793370',
            'great replacement theory': 'https://www.google.com/alerts/feeds/10165470848348617632/3940701198525793370',
            'racism': 'https://www.google.com/alerts/feeds/10165470848348617632/11928844387287997250'
        }

    def clean_text(self, text):
        """Clean HTML and extra whitespace from text"""
        if not text:
            return ""
        text = text.replace('<b>', '').replace('</b>', '')
        text = ' '.join(text.split())
        return text

    def get_article_text(self, url):
        """Download and extract article text"""
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded, include_links=False)
                return self.clean_text(text) if text else None
            return None
        except Exception as e:
            print(f"Error fetching article from {url}: {str(e)}")
            return None

    def create_summary(self, text, max_sentences=3):
        """Create a simple summary from the article text"""
        if not text:
            return ""
        sentences = text.split('.')
        summary = '. '.join(sentences[:max_sentences]) + '.'
        return self.clean_text(summary)

    def analyze_content(self, text):
        """Analyze the content for sentiment and key themes"""
        if not text:
            return None

        analysis = TextBlob(text)
        sentiment = analysis.sentiment.polarity

        # Calculate severity score
        base_score = 50
        sentiment_factor = (1 - sentiment) * 25
        severity_score = max(0, min(100, base_score + sentiment_factor))

        return {
            'sentiment': sentiment,
            'severity_score': severity_score
        }

    def fetch_and_analyze_alerts(self):
        """Fetch alerts and analyze full articles"""
        all_articles = []
        seen_urls = set()

        for keyword, feed_url in self.rss_feeds.items():
            print(f"\nProcessing alerts for '{keyword}'...")

            try:
                feed = feedparser.parse(feed_url)

                for entry in feed.entries:
                    if entry.link in seen_urls:
                        continue

                    seen_urls.add(entry.link)
                    print(f"\nAnalyzing article: {entry.title}")

                    # Get full article text
                    full_text = self.get_article_text(entry.link)
                    if not full_text:
                        description = self.clean_text(entry.summary if hasattr(entry, 'summary') else '')
                        full_text = description

                    # Create summary and analyze
                    summary = self.create_summary(full_text)
                    analysis = self.analyze_content(full_text)

                    if analysis:
                        article = {
                            'keyword': keyword,
                            'title': self.clean_text(entry.title),
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'url': entry.link,
                            'full_text': full_text,
                            'summary': summary,
                            'sentiment': analysis['sentiment'],
                            'severity_score': analysis['severity_score']
                        }

                        all_articles.append(article)

                    # Add delay
                    time.sleep(1)

            except Exception as e:
                print(f"Error processing feed for {keyword}: {str(e)}")
                continue

        return all_articles

def main():
    print("Starting Enhanced Article Analysis...")

    analyzer = ArticleAnalyzer()
    articles = analyzer.fetch_and_analyze_alerts()

    # Prepare output data
    output_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'total_articles': len(articles),
        'average_severity': sum(a['severity_score'] for a in articles) / len(articles) if articles else 0,
        'articles': articles
    }

    # Save results
    filename = f'full_articles_{datetime.now().strftime("%Y%m%d")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nAnalysis complete!")
    print(f"Total articles analyzed: {len(articles)}")
    print(f"Average severity score: {output_data['average_severity']:.1f}")
    print(f"Data saved to: {filename}")

if __name__ == "__main__":
    main()