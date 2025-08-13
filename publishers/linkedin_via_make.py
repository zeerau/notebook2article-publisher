import os
import requests

def post_to_linkedin_via_make(title, body):
    webhook_url = os.getenv("MAKE_WEBHOOK_URL")
    if not webhook_url:
        print("❌ Make.com webhook URL not found in environment.")
        return

    payload = {
        "title": title,
        "body": body
    }
    print(f"[📤] Posting to LinkedIn via Make: {title}")
    print(f"Posting to webhook: {webhook_url} with payload: {payload}")
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("✅ Successfully posted to LinkedIn via Make.")
    else:
        print(f"❌ Failed to post. Status: {response.status_code}, Message: {response.text}")
