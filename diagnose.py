#!/usr/bin/env python3
"""Diagnóstico completo do Google Calendar API"""
import json, urllib.request, urllib.parse, os

CONFIG_DIR = os.path.expanduser("~/google-calendar-sync")
CREDS_PATH = os.path.join(CONFIG_DIR, "credentials.json")
TOKEN_PATH = os.path.join(CONFIG_DIR, "token.json")
TOKEN_URL = "https://oauth2.googleapis.com/token"

creds = json.load(open(CREDS_PATH))["installed"]

# 1) Refresh token
token_data = json.load(open(TOKEN_PATH))
data = urllib.parse.urlencode({
    "client_id": creds["client_id"],
    "client_secret": creds["client_secret"],
    "refresh_token": token_data["refresh_token"],
    "grant_type": "refresh_token",
}).encode()
req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
req.add_header("Content-Type", "application/x-www-form-urlencoded")
resp = urllib.request.urlopen(req)
tokens = json.loads(resp.read())
access_token = tokens["access_token"]

print(f"✅ Access Token: {access_token[:25]}...")

# 2) Testar tokeninfo
print("\n🔍 TOKEN INFO:")
try:
    ti = urllib.request.urlopen(f"https://oauth2.googleapis.com/tokeninfo?access_token={access_token}")
    info = json.loads(ti.read())
    print(f"   email: {info.get('email', 'N/A')}")
    print(f"   scope: {info.get('scope', 'N/A')}")
    print(f"   expires_in: {info.get('expires_in', 'N/A')}s")
except urllib.error.HTTPError as e:
    print(f"   Erro {e.code}: {e.read().decode()}")

# 3) Testar calendarList
print("\n🔍 CALENDAR LIST:")
try:
    r = urllib.request.Request("https://www.googleapis.com/calendar/v3/users/me/calendarList")
    r.add_header("Authorization", f"Bearer {access_token}")
    cals = json.loads(urllib.request.urlopen(r).read())
    for c in cals.get("items", []):
        print(f"   📌 {c.get('summary')} ({c.get('id')})")
except urllib.error.HTTPError as e:
    err = json.loads(e.read().decode())
    print(f"   Erro {e.code}:")
    print(f"   {json.dumps(err, indent=4)}")

# 4) Testar primary
print("\n🔍 CALENDAR PRIMARY:")
try:
    r2 = urllib.request.Request("https://www.googleapis.com/calendar/v3/calendars/primary")
    r2.add_header("Authorization", f"Bearer {access_token}")
    cal = json.loads(urllib.request.urlopen(r2).read())
    print(f"   ✅ {cal.get('summary')} - {cal.get('id')}")
except urllib.error.HTTPError as e:
    err = json.loads(e.read().decode())
    print(f"   Erro {e.code}:")
    print(f"   {json.dumps(err, indent=4)}")
