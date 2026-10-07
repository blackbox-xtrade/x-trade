import os
import json
import urllib.request
import urllib.error
from datetime import datetime

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.")
    exit(1)

# URL API Gemini
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent?key={API_KEY}"

# Prompt untuk Gemini
PROMPT = """
You are an elite AI Gold (XAUUSD) Trader.
Based on the latest geopolitical news, DXY, and market sentiment, generate a new trade setup for XAUUSD.
Return ONLY a valid JSON object (without any markdown formatting like ```json) with the exact structure below:
{
    "signal": {
        "type": "BUY LIMIT or SELL LIMIT",
        "entry": "$X,XXX.XX",
        "sl": "$X,XXX.XX",
        "tp": "$X,XXX.XX",
        "confidence": "X/10"
    },
    "macro": {
        "dxy": "Short 2-sentence analysis of DXY and US Yields.",
        "geopolitics": "Short 2-sentence analysis of Geopolitics, Liquidity, and Retail Sentiment."
    }
}
"""

data = {
    "contents": [{"parts": [{"text": PROMPT}]}],
    "generationConfig": {
        "temperature": 0.7,
        "responseMimeType": "application/json"
    }
}

headers = {"Content-Type": "application/json"}
req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

print("Meminta analisa dari AI...")
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        ai_text = result['candidates'][0]['content']['parts'][0]['text']
        ai_data = json.loads(ai_text)
        
        # Load existing data.js
        with open("data.js", "r") as f:
            content = f.read()
            
        # Extract JSON from data.js
        json_str = content.replace("const tradeData = ", "").replace(";", "").strip()
        current_data = json.loads(json_str)
        
        # Update current_data
        today = datetime.now().strftime("%d %b %Y").upper()
        current_data["last_update"] = today
        current_data["signal"] = ai_data["signal"]
        current_data["macro"] = ai_data["macro"]
        
        # Tambahkan ke history
        new_history = {
            "date": today,
            "type": ai_data["signal"]["type"].split()[0], # BUY atau SELL
            "entry": ai_data["signal"]["entry"],
            "tp": ai_data["signal"]["tp"],
            "sl": ai_data["signal"]["sl"],
            "status": "PENDING",
            "result": "_ _ _ _"
        }
        current_data["history"].insert(0, new_history) # Masukkan di paling atas
        
        # Write back to data.js
        new_content = f"// data.js\nconst tradeData = {json.dumps(current_data, indent=4)};"
        with open("data.js", "w") as f:
            f.write(new_content)
            
        print("data.js berhasil diperbarui!")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
