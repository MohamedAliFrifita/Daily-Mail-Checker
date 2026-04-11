import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


#uses scopes with readonly (least privelege )  
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']



def get_gmail_service():
    creds = None
    
    # Check if token.pickle exists (The Saved Session)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials, we need to log in
    if not creds or not creds.valid:
        # Scenario A: Token is just expired, refresh token silently
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        # Scenario B: First time login or totally invalid token
        else:
            # This looks for the file you downloaded from Cloud Console
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            # This opens your default browser automatically
            creds = flow.run_local_server(port=0)

        # 3. Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Return the 'Resource' object to talk to Gmail
    return build('gmail', 'v1', credentials=creds)

# testing the authentication only in  this file 
if __name__ == "__main__":
    service = get_gmail_service()
    print("Handshake Successful! Gmail service is ready.")



from datetime import datetime

def fetch_and_batch_emails(service, batch_size=10, snippet_limit=150):
    """
    we re going to serach unread emails and and make batches of 10 emails each.
    Batches are used here to minimize api calls!!
    """

    # This ensures we only look at very recent mail
    today_str = datetime.now().strftime('%Y/%m/%d')
    query = f"is:unread after:{today_str}"
    
    # Get the list of Message IDs
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("No unread emails found for today. Great job on Inbox Zero!")
        return []

    all_cleaned_emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me', 
            id=msg['id'], 
            format='metadata'
        ).execute()
        
        # Extract headers to find 'From' and 'Subject'
        headers = msg_data.get('payload', {}).get('headers', [])
        
        
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
        
        # set limit to snippet length to save tokens 
        raw_snippet = msg_data.get('snippet', '')
        clean_snippet = (raw_snippet[:snippet_limit] + '...') if len(raw_snippet) > snippet_limit else raw_snippet

        # Create the Mail Object
        email_obj = {
            "sender": sender,
            "subject": subject,
            "snippet": clean_snippet
        }
        all_cleaned_emails.append(email_obj)

    batched_list = [all_cleaned_emails[i:i + batch_size] for i in range(0, len(all_cleaned_emails), batch_size)]
    
    return batched_list

if __name__ == "__main__":

    try:
    
        print("\nFetching today's unread emails...")
        batches = fetch_and_batch_emails(service, batch_size=10, snippet_limit=150)
        
        if not batches:
            print("No unread emails found for today.")
        else:
            print(f"Total Batches Created: {len(batches)}")
            
            for i, batch in enumerate(batches):
                print(f"\n--- BATCH #{i+1} (Contains {len(batch)} emails) ---")
                for mail in batch:
                    print(f"--> SENDER:  {mail['sender'][:40]}...")
                    print(f"    SUBJECT: {mail['subject'][:40]}...")
                    print(f"    SNIPPET: {mail['snippet']}")
                    print("-" * 20)

    except Exception as e:
        print(f"!!!!! Error during test: {e}")




