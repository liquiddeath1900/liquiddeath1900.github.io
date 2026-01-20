# SeamlessFlow Chatbot v2 - Setup Guide

## What's New in v2
- **Bypass Prevention**: Users can't skip questions - friendly but firm
- **Mobile Full Screen**: Takes over entire screen on mobile devices
- **Full Transcript Capture**: Every message logged for case studies
- **Google Sheets Storage**: All leads + transcripts saved for review

## What This Does
```
User clicks chat → Bot asks questions → Can't bypass →
Data + transcript → n8n webhook → Slack notification + Google Sheets
```

---

## Quick Setup (10 min)

### Step 1: Create Google Sheet for Transcripts
1. Create new Google Sheet called "Chatbot Leads"
2. Add these column headers in Row 1:
   ```
   Timestamp | Name | Business | Email | Service | Message | Transcript | Source | Mobile | Bypass Attempts | Page URL
   ```
3. Copy the Sheet ID from the URL (the long string between /d/ and /edit)

### Step 2: Import n8n Workflow
1. Open n8n dashboard
2. Click **"..."** menu → **Import from File**
3. Select `n8n-chatbot-to-slack.json`

### Step 3: Connect Google Sheets
1. Click the **"Save to Google Sheets"** node
2. Under Credentials → Create New → **Google Sheets OAuth2**
3. Follow OAuth flow to connect your Google account
4. Paste your Sheet ID where it says `YOUR_GOOGLE_SHEET_ID`

### Step 4: Connect Slack
1. Click the **"Send to Slack"** node
2. Under Credentials → Create New → **Slack API**
3. Follow OAuth flow to connect workspace
4. Change `#leads` to your preferred channel

### Step 5: Activate & Get Webhook URL
1. Toggle workflow **Active** (top right)
2. Click **"Chatbot Webhook"** node
3. Copy the **Production URL**

### Step 6: Update Chat Widget
1. Open `chatbot-widget.html`
2. Find line ~395: `const WEBHOOK_URL = 'YOUR_N8N_WEBHOOK_URL_HERE';`
3. Paste your webhook URL

### Step 7: Test It!
1. Open `chatbot-widget.html` in browser
2. Try to bypass (type "skip", "no", "later") - it should refuse!
3. Complete the flow with real info
4. Check Slack for notification
5. Check Google Sheets for full transcript

---

## How Bypass Prevention Works

The bot detects these patterns:
- "skip", "next", "later", "no thanks"
- "not now", "pass", "nevermind"
- "just tell me", "can you just"
- "no", "nah", "nope"

When detected, it responds firmly but friendly:
> "I hear you! But I really need your info first so we can actually help you out."

After valid input, bypass counter resets.

---

## Transcript Data Structure

Every conversation is logged with:
```json
{
  "transcript": [
    {"sender": "bot", "message": "Hey! What's your name?", "timestamp": "..."},
    {"sender": "user", "message": "John", "timestamp": "..."},
    ...
  ],
  "transcript_text": "[BOT] Hey! What's your name?\n[USER] John\n..."
}
```

The `transcript_text` field is perfect for case studies - human readable!

---

## Adding to Your Site

### Option 1: Embed the widget
Copy the entire `<style>` and widget HTML/JS from the demo into your site, before `</body>`.

### Option 2: External file
1. Extract JS to `chatbot-widget.js`
2. Extract CSS to `chatbot-widget.css`
3. Add to your site:
```html
<link rel="stylesheet" href="chatbot-widget.css">
<div class="chat-widget">...</div>
<script src="chatbot-widget.js"></script>
```

---

## Customization

### Change Bot Name/Avatar
Edit the `.chat-header` section in HTML.

### Change Questions
Edit `conversationFlow` array:
```javascript
{
    message: "Your question here",
    field: 'fieldName',
    placeholder: 'Input hint...',
    required: true,  // Can't be bypassed
    quickReplies: ['Option 1', 'Option 2']  // Optional buttons
}
```

### Add More Bypass Phrases
```javascript
const bypassPatterns = [
    /skip/i,
    /your-new-phrase/i,
    // Add more...
];
```

### Change Bypass Responses
```javascript
const bypassResponses = [
    "Your friendly but firm response here",
    // These cycle through on repeated attempts
];
```

---

## Troubleshooting

**Bypass not working?**
- Check console for errors
- Make sure `required: true` is set on the step

**Mobile not full screen?**
- Check viewport meta tag exists
- Test in actual mobile browser, not just dev tools resize

**Transcripts not saving?**
- Check Google Sheets credentials in n8n
- Verify column headers match exactly
- Check n8n execution history for errors

**Slack not posting?**
- Verify bot has permission in channel
- Check Slack credentials aren't expired

---

## Case Study Usage

Pull transcripts from Google Sheets to:
1. Analyze common questions/objections
2. Improve bot responses
3. Create marketing case studies (anonymized)
4. Train team on customer conversations

Filter by `Bypass Attempts > 0` to see problem interactions!
