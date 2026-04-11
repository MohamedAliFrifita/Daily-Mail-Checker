import time
import mail_handler
import AI_handler

def run_automation():
    print("...Starting Mail Check Pipeline...")
    
    #Authenticate
    service = mail_handler.get_gmail_service()
    
    #Fetch and Batch
    batches = mail_handler.fetch_and_batch_emails(service, batch_size=10)
    
    if not batches:
        print("Inbox Zero or no new academic alerts today. Enjoy the break!")
        return

    print(f"Found {sum(len(b) for b in batches)} unread emails. Processing in {len(batches)} batches...")

    all_results = []

    #Processing the batches
    for i, batch in enumerate(batches):
        print(f".....Analyzing batch {i+1}/{len(batches)}...")
        
        
        results = AI_handler.analyze_email_batch(batch)
        
        if results:
            all_results.extend(results)
        #keep time between each request to prevent api throttling 
        if i < len(batches) - 1:
            time.sleep(2)


    
    print("<<<<<TODAY'S MAIL SUMMARY>>>>>")
    
    
    # Sort results by urgency (High to Low)
    sorted_results = sorted(all_results, key=lambda x: x['urgency'], reverse=True)

    for item in sorted_results:
        # Use a visual indicator for high urgency
        prefix = "!!!!!![URGENT]" if item['urgency'] >= 8 else "---- [NORMAL]"
        
        print(f"{prefix} (Score: {item['urgency']}/10)")
        print(f"FROM:    {item['sender']}")
        print(f"SUBJECT: {item['subject']}")
        print(f"TAKE:    {item['summary']}")
        print("-" * 30)

if __name__ == "__main__":
    run_automation()