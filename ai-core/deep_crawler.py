import requests
from bs4 import BeautifulSoup
from api_manager import APIManager
import time

class DeepWebCrawler:
    def __init__(self):
        self.api = APIManager.get_instance()
        
    def scrape_hacker_news(self):
        print("[CRAWLER] Scraping Hacker News for trending tech datasets & news...")
        url = "https://news.ycombinator.com/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            titles = soup.find_all('span', class_='titleline')
            top_articles = []
            
            for i, title in enumerate(titles[:5]):
                top_articles.append(title.text)
                
            return top_articles
        except Exception as e:
            print(f"[CRAWLER] Error scraping HN: {e}")
            return []

    def scrape_github_trending(self):
        print("[CRAWLER] Scraping GitHub for trending repositories...")
        url = "https://github.com/trending"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            repos = soup.find_all('h2', class_='h3 lh-condensed')
            top_repos = []
            
            for i, repo in enumerate(repos[:5]):
                name = repo.text.strip().replace("\n", "").replace(" ", "")
                top_repos.append(name)
                
            return top_repos
        except Exception as e:
            print(f"[CRAWLER] Error scraping GitHub: {e}")
            return []

    def synthesize_intel(self, hn_data, github_data):
        print("[CRAWLER] Fusing datasets and generating intelligence brief via ATLAS...")
        
        prompt = f"""
        You are ATLAS. I have just run a headless web crawler and extracted the following trending datasets from the web today.
        
        Hacker News Trending:
        {hn_data}
        
        GitHub Trending Repositories:
        {github_data}
        
        Write a concise, 3-bullet-point "Daily Tech Intelligence Brief".
        Tell me what the biggest tech trends of the day are based strictly on this raw data.
        Keep it sharp, analytical, and professional.
        """
        
        max_retries = len(self.api.keys)
        attempts = 0
        
        while attempts < max_retries:
            try:
                client = self.api.get_client()
                response = client.chats.create(model=self.api.model_name).send_message(prompt)
                return response.text.strip()
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print("[CRAWLER] Rate limit hit! Rotating to backup API key...")
                    if self.api.rotate_key():
                        attempts += 1
                        continue
                    else:
                        return "Rate limits exhausted across all keys."
                else:
                    return f"Error: {str(e)}"
                    
        return "All keys exhausted."

    def run(self):
        print("\n=== DEEP WEB CRAWLER INITIATED ===")
        hn_data = self.scrape_hacker_news()
        time.sleep(1) # Polite scraping
        github_data = self.scrape_github_trending()
        
        if not hn_data and not github_data:
            print("[CRAWLER] No data retrieved. Aborting synthesis.")
            return
            
        print("\n[RAW DATA EXTRACTED]")
        print(f"HN Items: {len(hn_data)} | GitHub Items: {len(github_data)}")
        
        intel_brief = self.synthesize_intel(hn_data, github_data)
        
        print("\n=== ATLAS INTELLIGENCE BRIEF ===")
        print(intel_brief)
        print("================================\n")


if __name__ == "__main__":
    crawler = DeepWebCrawler()
    crawler.run()
