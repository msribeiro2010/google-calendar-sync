#!/usr/bin/env python3
"""Diagnóstico completo do Google Calendar API"""
import json, urllib.request, urllib.parse, os, sys

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
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

print(f"✅ Access Token obtido: {access_token[:20]}...")

# 2) Testar endpoint com erro detalhado
def api_detailed(url):
    r = urllib.request.Request(url)
    r.add_header("Authorization", f"Bearer {access_token}")
    try:
        resp = urllib.request.urlopen(r)
        return json.loads(resp.read()), 200
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
        except:
            err = {"raw": body}
        return err, e.code

# 3) Testar tokeninfo
print("\n🔍 Testando tokeninfo...")
info, code = api_detailed("https://oauth2.googleapis.com/tokeninfo?access_token=" + access_token)
print(f"   Status: {code}")
print(f"   Detalhes: {json.dumps(info, indent=2)}")

# 4) Testar calendar list
print("\n🔍 Testando calendarList...")
result, code = api_detailed("https://www.googleapis.com/calendar/v3/users/me/calendarList")
print(f"   Status: {code}")
print(f"   Resposta: {json.dumps(result, indent=2)}")

# 5) Testar com primary
print("\n🔍 Testando calendar primary...")
result2, code2 = api_detailed("https://www.googleapis.com/calendar/v3/calendars/primary")
print(f"   Status: {code2}")
print(f"   Resposta: {json.dumps(result2, indent=2)}")
