import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from financial_sniper import FinancialSniper

def execute(context):
    sniper = FinancialSniper()
    data = sniper.analyze_sms(context)
    
    if "error" in data:
        return f"[FINANCIAL SNIPER ERROR] {data['error']}"
        
    response = f"[FINANCIAL SNIPER ACTION] Extracted transaction. Type: {data.get('type')}, Amount: {data.get('amount')}, Vendor: {data.get('vendor')}."
    if data.get('is_alert'):
        response += " WARNING: This is a critical EMI or low balance alert."
        
    return response
