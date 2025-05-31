import os.path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from time import sleep


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]





# Method to print message details and check if the email is older than a specified number of days.
def MessageDetails(Label_Id,service=None):

    print("I am inside MessageDetails method\n")
    "Calling the Gmail API to get the message details."
    try:
        
        messages=[]
        next_page_token = None

        # Fetch messages in batches using nextPageToken
        while True:
            results= service.users().messages().list(
                        userId='me',
                        labelIds=[Label_Id],
                        # q='!in:trash',  # Exclude messages in trash
                        maxResults=20,  # Fetch up to 50 messages at a time
                        pageToken=next_page_token
                    ).execute()
            if 'messages' in results:
                messages.extend(results['messages'])
            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break
        print(f"Total messages in {Label_Id}: {len(messages)}")
        
        
        #process messages in batch

        "Responses dictionary to store message details"
        responses = {}
        # Callback function to handle each message response
        def batch_callback(request_id, response, exception):
            if exception is  None:
                responses[request_id] = response
            else:
                print(f"An error occurred: {exception}")


        # Process messages in batches of 100
        for i in range(0, len(messages),20):
            batch = service.new_batch_http_request(callback=batch_callback)
            batch_messages = messages[i:i+20]
            
            for msg in batch_messages:
                batch.add(
                    service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='full'
                    ),
                    request_id=msg['id']  # This ID links response to request
                )
            
            batch.execute()
            # Now responses dictionary contains all message data
            for msg_id, message_data in responses.items():
                headers = message_data['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'No Sender')
                
                # Get dates using the get_email_dates method
                sent_date, received_date = get_email_dates(message_data, headers)

                # Check if email is old
                is_old = is_email_old(received_date)
                age_marker = "[Old]" if is_old else "[New]"


                print(f"\n{age_marker} Message Details:")
                print(f"ID: {msg_id}")
                print(f"From: {sender}")
                print(f"Subject: {subject}")
                print(f"Sent Date: {sent_date}")
                print(f"Received: {received_date}")
                print("\n")

            responses.clear()  # Clear for next batch
            print("\n");
                    
    except HttpError as error:
        print(f"An error occurred: {error}")  





# Method to check if an email is older than a specified number of days.
def is_email_old(received_date_str, days_threshold=30):
    """Check if email is older than specified days."""
    try:
        received_date = datetime.strptime(received_date_str, '%Y-%m-%d %H:%M:%S')
        current_date = datetime.now()
        age = current_date - received_date
        return age.days >= days_threshold
    except Exception as e:
        print(f"Error parsing date: {e}")
        return False





# Method to extract sent and received dates from the email headers.
def get_email_dates(full_message,headers):
    # Get both sent and received dates from the email headers.
    sent_date=next(
        (h['value'] for h in full_message['payload']['headers'] if h['name'].lower() == 'date'), 
        'No Date Found'
    )
    # Convert internal date (timestamp in ms) to readable format
    received_date = datetime.fromtimestamp(
        int(full_message['internalDate']) / 1000
    ).strftime('%Y-%m-%d %H:%M:%S')
    return sent_date, received_date




def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    profile= service.users().getProfile(userId='me').execute()


    "Method to get the message details "
    MessageDetails('CATEGORY_PROMOTIONS',service)
    sleep(2)  # Sleep for 2 seconds to avoid hitting API limits
    # Method to get the message details for social category
    MessageDetails('CATEGORY_SOCIAL',service)
    

    # Print the user's profile information
    print(f"User Profile is {profile}")
    print(f"User Email: {profile['emailAddress']}")

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()