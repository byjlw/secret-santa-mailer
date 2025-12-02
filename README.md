# Secret Santa Script

A Python script to automatically pair up Secret Santa participants and send email notifications.

## Features

- ✅ **Dry Run Mode**: Test pairings without sending emails
- ✅ **Real Run Mode**: Send emails without revealing pairings to the organizer
- ✅ **Smart Pairing**: Ensures no one gets themselves
- ✅ **CSV Input**: Easy participant management

## Setup

### 1. Install Python
Make sure you have Python 3.6+ installed.

### 2. Prepare Your CSV File

Create a CSV file with two columns: `name` and `email`

Example (`participants.csv`):
```csv
name,email
Alice Smith,alice@example.com
Bob Johnson,bob@example.com
Carol Williams,carol@example.com
```

### 3. Email Configuration (for Real Run)

For Gmail users:
1. Enable 2-factor authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the app password (not your regular password) when prompted

For other email providers, you'll need:
- SMTP server address
- SMTP port (usually 587)
- Your email and password/app password

## Usage

### Dry Run (Test Mode)
Preview the pairings without sending emails:

```bash
python secret_santa.py participants.csv --dry-run
```

This will show you:
- List of all participants
- Who is paired with whom
- No emails are sent

### Real Run (Send Emails)
Send actual Secret Santa assignments:

```bash
python secret_santa.py participants.csv --send
```

You'll be prompted for:
- Sender email address
- Sender email password (app password for Gmail)
- SMTP server (defaults to Gmail)
- SMTP port (defaults to 587)

**Important**: In real run mode, pairings are NOT shown to the organizer to maintain the surprise!

## Example Workflow

1. **First, test with dry run:**
   ```bash
   python secret_santa.py participants.csv --dry-run
   ```

2. **Review the pairings** - make sure they look good

3. **Run again if needed** (pairings are randomized each time)

4. **When ready, send emails:**
   ```bash
   python secret_santa.py participants.csv --send
   ```

## Email Template

Each participant receives an email like this:

```
Subject: 🎅 Your Secret Santa Assignment!

Ho Ho Ho [Participant Name]!

You are the Secret Santa for: [Recipient Name]

Remember to keep this a secret! 🤫

Happy gift shopping!

🎄 Secret Santa Organizer
```

## Troubleshooting

### Gmail Authentication Errors
- Make sure you're using an App Password, not your regular password
- Enable "Less secure app access" if not using 2FA (not recommended)

### SMTP Connection Errors
- Check your SMTP server and port
- Ensure your firewall allows SMTP connections
- Try port 465 with SSL if port 587 doesn't work

### "Could not create valid pairings"
- This is extremely rare but can happen with small groups
- Simply run the script again

## Security Notes

- Passwords are not stored anywhere
- In real run mode, pairings are not displayed to protect the surprise
- Consider using environment variables for email credentials if automating

## Customization

You can edit the script to customize:
- Email subject line (line 62)
- Email message template (lines 64-74)
- Maximum pairing attempts (line 40)

## Requirements

- Python 3.6+
- No external packages required (uses standard library only)

## License

Free to use and modify for your Secret Santa needs! 🎁
