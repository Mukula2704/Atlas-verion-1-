import os
import json
from api_manager import APIManager

class FinancialSniper:
    def __init__(self):
        self.api = APIManager.get_instance()
        self.client = self.api.get_client()
        print("[FINANCIAL SNIPER] Online. Monitoring for financial intel.")

    def analyze_sms(self, sms_text: str) -> dict:
        """
        Uses Gemini to parse raw bank SMS messages into structured financial data.
        """
        if not self.client:
            print("[FINANCIAL SNIPER] Offline. Missing API Key.")
            return {"error": "Missing API Key"}

        prompt = f"""
        You are the Financial Sniper, a highly analytical financial tracking module.
        Analyze the following SMS message. Determine if it is a financial transaction.
        If it is, extract the data and return EXACTLY this JSON structure, and absolutely nothing else:
        {{
            "is_transaction": true/false,
            "type": "debit" | "credit" | "emi_reminder" | "spam",
            "amount": (number without currency symbol),
            "currency": "INR",
            "vendor": "Name of the merchant/bank",
            "is_alert": true/false (true if it's an upcoming EMI or low balance warning)
        }}

        SMS TEXT:
        "{sms_text}"
        """

        max_retries = len(self.api.keys)
        attempts = 0
        
        while attempts < max_retries:
            try:
                # Refresh client just in case we rotated
                self.client = self.api.get_client()
                response = self.client.chats.create(model=self.api.model_name).send_message(prompt)
                
                # Clean up JSON formatting if present
                raw_json = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_json)
                print(f"[FINANCIAL SNIPER] Parsed Transaction: {data.get('amount')} at {data.get('vendor')}")
                return data
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print("[FINANCIAL SNIPER] Rate limit hit! Attempting to rotate to backup API key...")
                    if self.api.rotate_key():
                        attempts += 1
                        continue
                    else:
                        return {"error": "Rate limit hit and no backup keys available."}
                else:
                    print(f"[FINANCIAL SNIPER] Error parsing SMS: {e}")
                    return {"error": str(e)}
        
        return {"error": "All API keys exhausted."}

if __name__ == "__main__":
    sniper = FinancialSniper()
    test_sms = "Your a/c no. XXXXXX1234 is debited for Rs.450.00 on 29-08-26 and a/c linked to Swiggy. Available Bal Rs.12,450.00."
    print("Testing SMS 1:")
    print(sniper.analyze_sms(test_sms))
    
    test_emi = "Reminder: Your EMI of Rs. 15000 for HDFC Loan is due on 05-09-26. Please ensure sufficient balance."
    print("\nTesting SMS 2 (EMI Reminder):")
    print(sniper.analyze_sms(test_emi))
