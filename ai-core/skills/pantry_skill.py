import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pantry_module import PantryModule

def execute(context):
    pantry = PantryModule()
    
    # Standardize the log
    pantry.log_meal("food_intake", 1)
    
    # Anti-Craving Protocol (120g Protein Goal)
    is_junk = pantry.detect_junk_food(context, source="atlas_brain")
    
    if is_junk:
        return "[PANTRY ACTION] Triggered Junk Food protocol. Logged strike. Alerted user."
    return "[PANTRY ACTION] Meal successfully logged. Protein goals on track."
