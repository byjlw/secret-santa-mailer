#!/usr/bin/env python3
"""
Secret Santa Pairing Script

This script pairs up participants for Secret Santa and sends emails.
- Dry run mode: Shows pairings without sending emails
- Real run mode: Sends emails without revealing pairings to the runner

Usage:
    python secret_santa.py participants.csv --dry-run
    python secret_santa.py participants.csv --send
"""

import csv
import random
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Tuple


def load_participants(csv_file: str) -> List[Dict[str, str]]:
    """Load participants from CSV file."""
    participants = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'name' in row and 'email' in row:
                participants.append({
                    'name': row['name'].strip(),
                    'email': row['email'].strip()
                })
    return participants


def create_pairings(participants: List[Dict[str, str]]) -> List[Tuple[Dict, Dict]]:
    """
    Create Secret Santa pairings ensuring no one gets themselves.
    Returns list of tuples: (giver, receiver)
    """
    if len(participants) < 2:
        raise ValueError("Need at least 2 participants for Secret Santa")
    
    givers = participants.copy()
    receivers = participants.copy()
    
    # Shuffle until we get a valid derangement (no one gets themselves)
    max_attempts = 1000
    for _ in range(max_attempts):
        random.shuffle(receivers)
        # Check if anyone got themselves
        if all(givers[i]['email'] != receivers[i]['email'] for i in range(len(givers))):
            return list(zip(givers, receivers))
    
    raise RuntimeError("Could not create valid pairings. This is very unlikely!")


def send_email(giver: Dict[str, str], receiver: Dict[str, str], 
               smtp_server: str, smtp_port: int, 
               sender_email: str, sender_password: str):
    """Send Secret Santa assignment email."""
    
    subject = "🎅 Your Secret Santa Assignment!"
    
    body = f"""Ho Ho Ho {giver['name']}!

You are the Secret Santa for: {receiver['name']}

Remember to keep this a secret! 🤫

Happy gift shopping!

🎄 Secret Santa Organizer
"""
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = giver['email']
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


def dry_run(csv_file: str):
    """Run in dry-run mode: show pairings without sending emails."""
    print("🎄 SECRET SANTA - DRY RUN MODE 🎄")
    print("=" * 50)
    
    participants = load_participants(csv_file)
    print(f"\nLoaded {len(participants)} participants:")
    for p in participants:
        print(f"  - {p['name']} ({p['email']})")
    
    print("\n" + "=" * 50)
    print("PAIRINGS:")
    print("=" * 50)
    
    pairings = create_pairings(participants)
    for giver, receiver in pairings:
        print(f"{giver['name']:20} → {receiver['name']}")
    
    print("\n✅ Dry run complete! No emails sent.")


def real_run(csv_file: str):
    """Run in real mode: send emails without showing pairings."""
    print("🎅 SECRET SANTA - REAL RUN MODE 🎅")
    print("=" * 50)
    
    participants = load_participants(csv_file)
    print(f"\nLoaded {len(participants)} participants")
    
    # Get email credentials
    print("\n📧 Email Configuration:")
    sender_email = input("Enter sender email address: ").strip()
    sender_password = input("Enter sender email password/app password: ").strip()
    
    # Common SMTP servers
    print("\nCommon SMTP servers:")
    print("  Gmail: smtp.gmail.com (port 587)")
    print("  Outlook: smtp-mail.outlook.com (port 587)")
    print("  Yahoo: smtp.mail.yahoo.com (port 587)")
    
    smtp_server = input("Enter SMTP server (default: smtp.gmail.com): ").strip()
    if not smtp_server:
        smtp_server = "smtp.gmail.com"
    
    smtp_port_input = input("Enter SMTP port (default: 587): ").strip()
    smtp_port = int(smtp_port_input) if smtp_port_input else 587
    
    # Create pairings (but don't show them!)
    print("\n🎲 Creating secret pairings...")
    pairings = create_pairings(participants)
    
    # Confirm before sending
    print(f"\n⚠️  Ready to send {len(pairings)} emails.")
    confirm = input("Type 'SEND' to confirm: ").strip()
    
    if confirm != 'SEND':
        print("❌ Cancelled. No emails sent.")
        return
    
    # Send emails
    print("\n📤 Sending emails...")
    success_count = 0
    
    for giver, receiver in pairings:
        try:
            send_email(giver, receiver, smtp_server, smtp_port, 
                      sender_email, sender_password)
            print(f"  ✓ Email sent to {giver['name']}")
            success_count += 1
        except Exception as e:
            print(f"  ✗ Failed to send email to {giver['name']}: {str(e)}")
    
    print(f"\n✅ Complete! Successfully sent {success_count}/{len(pairings)} emails.")
    print("🎁 Secret Santa assignments have been distributed!")


def main():
    parser = argparse.ArgumentParser(description='Secret Santa Pairing Script')
    parser.add_argument('csv_file', help='CSV file with name and email columns')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show pairings without sending emails')
    parser.add_argument('--send', action='store_true',
                       help='Send emails without showing pairings')
    
    args = parser.parse_args()
    
    if args.dry_run and args.send:
        print("❌ Error: Cannot use both --dry-run and --send")
        return
    
    if not args.dry_run and not args.send:
        print("❌ Error: Must specify either --dry-run or --send")
        print("\nUsage:")
        print("  Dry run:  python secret_santa.py participants.csv --dry-run")
        print("  Real run: python secret_santa.py participants.csv --send")
        return
    
    try:
        if args.dry_run:
            dry_run(args.csv_file)
        else:
            real_run(args.csv_file)
    except FileNotFoundError:
        print(f"❌ Error: File '{args.csv_file}' not found")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == '__main__':
    main()