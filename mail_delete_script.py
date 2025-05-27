import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


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
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    profile= service.users().getProfile(userId='me').execute()
    # promotion=service.users().labels().get(userId='me', id='CATEGORY_PROMOTIONS').execute();
    promotional_messages = service.users().messages().list(
        userId='me',
        labelIds=['CATEGORY_PROMOTIONS']
    ).execute()
    
    if 'messages' in promotional_messages:
        print(f"Total promotional messages: {len(promotional_messages['messages'])}")

        for msg in promotional_messages['messages']:
            full_message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()

            # Now we can access email details
            headers = full_message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'No Sender')
            
            print(f"\nEmail: {sender}")
            print(f"Subject: {subject}")

    # Print the user's profile information
    print(f"User Profile is {profile}")
    print(f"User Email: {profile['emailAddress']}")
    # print(f"Promotions Label: {promotion}")
    print(f"Total Labels: {len(labels)}")
    # Print the labels


    if not labels:
      print("No labels found.")
      return
    # print("Labels:")
    # for label in labels:
    #   print(label["name"])

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()