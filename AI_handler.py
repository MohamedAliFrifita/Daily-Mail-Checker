import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#This is the how the model will handle each prompt
SYSTEM_INSTRUCTION = """
You are a highly efficient academic assistant for a Software Engineering student at INSAT.
Your task is to analyze a batch of emails and return a JSON list.

URGENCY RULES:
- High Urgency (8-10): Anything regarding 'TD', 'Cours', 'DS', 'Examen', 'Notes', or 'Rattrapage'.
- Medium Urgency (4-7): General university announcements or project collaborations.
- Low Urgency (1-3): Newsletters, social media notifications, or ads.

OUTPUT FORMAT:
Return ONLY a valid JSON list of objects with these keys:
"urgency": (Integer 1-10)
"sender": (String)
"subject": (String)
"summary": (String, max 2 lines)
"""

def analyze_email_batch(email_batch):
    """
    Sends a batch of 10 emails to Gemini and returns parsed results.
    """
    # Convert the list of emails to a single string for the prompt
    batch_text = json.dumps(email_batch, indent=2)
    
    prompt = f"Analyze these emails according to your instructions:\n\n{batch_text}"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            config={"system_instruction": SYSTEM_INSTRUCTION, "response_mime_type": "application/json"},
            contents=prompt
        )
        
        # Turn the string response into a Python List
        return json.loads(response.text)
    
    except Exception as e:
        print(f"Error analyzing batch: {e}")
        return []

#testing only this file
if __name__ == "__main__":
    #create a dummy batch to test   
    test_batch = [
        {
            "sender": "Administration INSAT <admin@insat.u-cartage.tn>",
            "subject": "Rattrapage et Notes DS - GL2",
            "snippet": "Bonjour, veuillez trouver ci-joint le planning des rattrapages pour le module Network Programming ainsi que les notes du DS1."
        },
        {
            "sender": "LinkedIn Notifications",
            "subject": "You have 5 new job alerts",
            "snippet": "Check out the latest Software Engineering internships in Tunis that match your profile."
        }
    ]

    print(f"Sending {len(test_batch)} test emails to Gemini...")
    
    results = analyze_email_batch(test_batch)

    if not results:
        print("No results returned. Check your API key or connection.")
    else:
        for item in results:
            
            icon = "*******" if item['urgency'] >= 8 else "**"
            
            print(f"{icon} [URGENCY: {item['urgency']}/10]")
            print(f"   FROM:    {item['sender']}")
            print(f"   SUBJECT: {item['subject']}")
            print(f"   SUMMARY: {item['summary']}")
            print("-" * 30)