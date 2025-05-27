import os
import os.path
from datetime import datetime
import pytz
from google.oauth2.credentials import Credentials

# Use same scope as main script
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def check_token_validity():
    """Check and print token validity information."""
    if not os.path.exists('token.json'):
        print(f"No token.json found in {SCRIPT_DIR}")
        return
    
    try:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        expiry_utc = creds.expiry.astimezone(pytz.UTC)
        current_time_utc = datetime.now(pytz.UTC)
        
        # Convert to IST
        ist = pytz.timezone('Asia/Kolkata')
        expiry_ist = expiry_utc.astimezone(ist)
        current_time_ist = current_time_utc.astimezone(ist)
        time_remaining = expiry_utc - current_time_utc
        
        print("\nToken Status:")
        print(f"Token Valid: {creds.valid}")
        print(f"Token Expired: {creds.expired}")
        print(f"Current Time (UTC): {current_time_utc}")
        print(f"Current Time (IST): {current_time_ist}")
        print(f"Expiry Time (UTC): {expiry_utc}")
        print(f"Expiry Time (IST): {expiry_ist}")
        print(f"Time Remaining: {time_remaining}")

    except Exception as e:
        print(f"Error reading token: {e}")

if __name__ == "__main__":
    check_token_validity()