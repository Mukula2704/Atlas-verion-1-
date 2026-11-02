import requests
from bs4 import BeautifulSoup
import asyncio
from discord_commlink import DiscordCommLink
import time

class DeepWebCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def fetch_subreddit_top(self, subreddit, limit=3):
        """Scrapes old.reddit.com to bypass JavaScript blocks and fetch top daily posts."""
        url = f"https://old.reddit.com/r/{subreddit}/top/?sort=top&t=day"
        print(f"[CRAWLER] Fetching intel from {url}...")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"[ERROR] Failed to fetch {subreddit}. Status code: {response.status_code}")
                return []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            posts = soup.find_all('div', class_='thing', limit=limit)
            
            results = []
            for post in posts:
                title_elem = post.find('a', class_='title')
                if title_elem:
                    title = title_elem.text
                    link = title_elem.get('href')
                    if link and link.startswith('/r/'):
                        link = "https://reddit.com" + link
                    
                    results.append({
                        "title": title,
                        "link": link
                    })
            return results
            
        except Exception as e:
            print(f"[ERROR] Crawler failed: {e}")
            return []

    async def generate_intelligence_brief(self):
        """Compiles scraped data into a brief and sends it to Discord."""
        subreddits = ["LocalLLaMA", "MachineLearning", "cscareerquestions"]
        
        brief = "📊 **ATLAS MORNING INTELLIGENCE BRIEF** 📊\n\n"
        
        for sub in subreddits:
            posts = self.fetch_subreddit_top(sub, limit=2)
            if posts:
                brief += f"**r/{sub}**\n"
                for i, post in enumerate(posts):
                    brief += f"{i+1}. [{post['title']}]({post['link']})\n"
                brief += "\n"
            time.sleep(2) # Be polite to Reddit servers
            
        print("[CRAWLER] Brief compiled. Dispatching to Comm-Link...")
        
        try:
            pager = DiscordCommLink()
            await pager.send_message(brief)
            print("[SUCCESS] Intelligence Brief dispatched.")
        except Exception as e:
            print(f"[ERROR] Failed to send via Comm-Link: {e}")

if __name__ == "__main__":
    crawler = DeepWebCrawler()
    asyncio.run(crawler.generate_intelligence_brief())
