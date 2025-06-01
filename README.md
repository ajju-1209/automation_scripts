# Gmail Inbox Cleaning Automation

An automated solution to manage Gmail inbox by handling promotional and social emails based on their age. The script uses Gmail API to identify and process old emails in batches.

## Features

- Authenticates with Gmail API using OAuth2
- Processes emails in batches to respect API rate limits
- Identifies old promotional emails based on configurable age threshold
- Supports GitHub Actions for automated runs
- Handles timezone differences in email dates
- Safe email processing with error handling

## Prerequisites

- Python 3.x
- Google Cloud Project with Gmail API enabled
- OAuth2 credentials from Google Cloud Console
- Required Python packages:
  ```bash
  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
  ```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mail-deletion-script.git
   cd mail-deletion-script
   ```

2. Set up Google Cloud Project:
   - Create a project in Google Cloud Console
   - Enable Gmail API
   - Create OAuth2 credentials
   - Download credentials as `credentials.json`

3. First Run Authentication:
   ```bash
   python mail_delete_script.py
   ```
   - Follow browser prompts for Gmail authentication
   - This will create `token.json`

4. GitHub Actions Setup (Optional):
   - Convert credentials to base64:
     ```bash
     base64 credentials.json | tr -d '\n' > credentials_b64.txt
     base64 token.json | tr -d '\n' > token_b64.txt
     ```
   - Add contents as secrets in GitHub repository:
     - `GMAIL_CREDENTIALS`
     - `GMAIL_TOKEN`

## Configuration

- Default age threshold: 30 days (configurable in code)
- Batch size: 20 messages (adjustable for rate limiting)
- Processes promotional emails by default

## Usage

### Local Execution
```bash
python mail_delete_script.py
```

### GitHub Actions
- Navigate to Actions tab in repository
- Select "Clean Gmail Inbox" workflow
- Click "Run workflow"

## Security Notes

- Never commit `credentials.json` or `token.json`
- Keep OAuth2 credentials secure
- Use environment variables or secrets for sensitive data

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

