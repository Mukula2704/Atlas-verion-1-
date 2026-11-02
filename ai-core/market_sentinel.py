import os
import yfinance as yf
from api_manager import APIManager

class MarketSentinel:
    def __init__(self):
        self.api = APIManager.get_instance()
        self.client = self.api.get_client()
        # Track a mix of Indian markets and Crypto (Bitcoin)
        self.target_assets = {
            "^NSEI": "NIFTY 50",
            "RELIANCE.NS": "Reliance Industries",
            "BTC-USD": "Bitcoin"
        }
        print("[MARKET SENTINEL] Online. Scanning for market crashes and dip-buying opportunities.")

    def scan_markets(self, available_budget: float):
        """Scans the market and generates tactical advice if a dip is detected."""
        alerts = []
        
        for ticker, name in self.target_assets.items():
            try:
                stock = yf.Ticker(ticker)
                # Get the last 2 days of data to calculate percentage drop
                hist = stock.history(period="2d")
                if len(hist) < 2:
                    continue
                    
                prev_close = hist['Close'].iloc[0]
                current_price = hist['Close'].iloc[1]
                
                percent_change = ((current_price - prev_close) / prev_close) * 100
                
                # If there's a drop of 1.5% or more, we flag it as a dip
                if percent_change <= -1.5:
                    alerts.append({
                        "asset": name,
                        "ticker": ticker,
                        "drop_percent": round(percent_change, 2),
                        "current_price": round(current_price, 2)
                    })
                    
            except Exception as e:
                print(f"[MARKET SENTINEL] Error fetching data for {ticker}: {e}")

        if not alerts:
            return "Markets are stable. No major dips detected."

        return self._generate_tactical_alert(alerts, available_budget)

    def _generate_tactical_alert(self, alerts: list, available_budget: float):
        """Uses ATLAS (Gemini) to format a ruthless financial action plan."""
        if not self.client:
            return "[Error: API Offline]"

        prompt = f"""
        You are ATLAS, the ruthless and highly analytical Financial Supervisor. 
        Your Market Sentinel module just detected the following market crashes today:
        {alerts}
        
        The user has a total spare budget this month of Rs. {available_budget}.
        Write a very concise (3-4 sentences max), tactical text message alert to send to the user's Comm-Link.
        Tell them the market is bleeding, calculate a smart micro-investment amount (e.g., 5-10% of their spare budget) to "buy the dip", and give them a direct order to execute it.
        Keep the tone dominant, hyper-professional, and urgent. Do not use markdown, just raw text.
        """

        max_retries = len(self.api.keys)
        attempts = 0
        
        while attempts < max_retries:
            try:
                self.client = self.api.get_client()
                response = self.client.chats.create(model=self.api.model_name).send_message(prompt)
                return response.text.strip()
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if self.api.rotate_key():
                        attempts += 1
                        continue
                    else:
                        return "Market is bleeding, but ATLAS is offline due to rate limits."
                else:
                    return f"Error: {str(e)}"
                    
        return "Market is bleeding, but ATLAS is offline due to rate limits."

if __name__ == "__main__":
    sentinel = MarketSentinel()
    # Simulating a user who has Rs. 15,000 in spare cash this month
    print("Executing Market Scan...")
    
    # We force a fake alert just to test the AI generation if the real market is stable today
    fake_alerts = [
        {"asset": "Bitcoin", "ticker": "BTC-USD", "drop_percent": -5.2, "current_price": 54000.50},
        {"asset": "NIFTY 50", "ticker": "^NSEI", "drop_percent": -2.1, "current_price": 23500.00}
    ]
    
    print("\n[Simulating a Crash Alert]")
    print(sentinel._generate_tactical_alert(fake_alerts, 15000))
