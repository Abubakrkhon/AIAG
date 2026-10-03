# Interview.ai - Voice AI Hiring Screener for SMBs

## 🎯 Mission
Replace 2-5 hours/week of candidate screening calls for local businesses with a $49/hire or $299/month voice AI agent.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Twilio Account (Voice API)
- OpenAI API Key (GPT-4 + TTS)
- Deepgram API (transcription)
- Stripe Account (payments)
- PostgreSQL Database

### Installation

```bash
# Clone and setup
git clone <repo-url>
cd interview-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Environment setup
cp .env.example .env
# Edit .env with your API keys
```

## 📁 Project Structure

```
interview-ai/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── voice_agent/         # Voice AI core
│   │   ├── __init__.py
│   │   ├── agent.py         # Interview logic
│   │   ├── prompts.py       # Question templates
│   │   └── transcription.py # Deepgram integration
│   ├── twilio/              # Phone integration
│   │   ├── __init__.py
│   │   ├── webhook.py       # Incoming call handler
│   │   └── outbound.py      # Schedule calls
│   ├── database/            # PostgreSQL models
│   │   ├── __init__.py
│   │   ├── models.py        # SQLAlchemy models
│   │   └── crud.py          # DB operations
│   ├── payments/            # Stripe integration
│   │   ├── __init__.py
│   │   ├── subscriptions.py # Flat-rate plans
│   │   └── pay_per_hire.py  # $49/hire tracking
│   └── integrations/        # Zapier, webhooks
│       ├── __init__.py
│       └── zapier.py        # Zapier webhook handler
├── templates/               # Email/SMS templates
├── tests/                   # Pytest suite
├── requirements.txt
├── .env.example
└── README.md
```

## 💰 Pricing Models

### Plan A: Pay-Per-Performance
- **$49 per successful interview scheduled**
- No monthly commitment
- Perfect for low-volume hirers (5-10/year)

### Plan B: Flat-Rate Unlimited
- **$299/month**
- Up to 20 interviews/month
- Overages at $35/interview
- Best for high-volume (20+ hires/year)

## 🎙️ Voice Agent Features

### Pre-Built Templates
1. **General Service** (retail, hospitality, admin)
2. **Skilled Trades** (HVAC, plumbing, construction)
3. **Healthcare** (dental, medical, chiropractic)
4. **Staffing Agency** (availability, flexibility, travel)

### Interview Flow
1. **Intro** (15 sec): "Hi [Name], this is an automated screening call from [Company]..."
2. **Qualification Questions** (5-7 questions, 2-3 min total):
   - Experience level
   - Availability
   - Certifications (role-specific)
   - Salary expectations
   - Transportation/reliability
3. **Scheduling** (30 sec): "You're qualified! When can you come in?"
4. **Summary**: Auto-send transcript + score to employer

### Tech Stack
- **Voice Model**: ElevenLabs (most natural) or OpenAI TTS
- **Transcription**: Deepgram Universal-3 Pro (99% accuracy)
- **Phone System**: Twilio Voice API
- **LLM Logic**: GPT-4 Turbo for dynamic questioning
- **Database**: PostgreSQL for call logs & analytics

## 🔗 Integrations

### Zapier Webhook (No-Code Setup)
```json
POST https://api.interview-ai.com/webhook/zapier
{
  "candidate_name": "John Doe",
  "candidate_phone": "+15551234567",
  "job_title": "HVAC Technician",
  "template": "skilled_trades",
  "callback_url": "https://yourcompany.com/callback"
}
```

### Direct API
```python
import requests

response = requests.post(
    "https://api.interview-ai.com/v1/interviews",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "candidate_phone": "+15551234567",
        "job_template": "healthcare",
        "custom_questions": ["Comfortable with kids?", "Years of experience?"],
        "schedule_link": "https://calendly.com/your-link"
    }
)
```

## 📊 Metrics Dashboard

Track in real-time:
- Interviews completed
- Qualification rate (%)
- Average call duration
- Cost per hire
- Candidate satisfaction scores

## ⚖️ Compliance

- **EEOC Disclaimer**: "This is a screening tool only. Final decisions require human review."
- **FCRA Compliant**: Candidates can request transcripts
- **TCPA Compliant**: Opt-in required for automated calls
- **Data Retention**: 90-day default, configurable

## 🛠️ Development

```bash
# Run locally
uvicorn app.main:app --reload

# Run tests
pytest tests/ -v

# Deploy to production
docker-compose up -d
```

## 📈 Roadmap

- [ ] **Week 1**: MVP with 3 templates + Twilio integration
- [ ] **Week 2**: Zapier webhook + Stripe payments
- [ ] **Week 3**: Staffing agency partnerships (beta)
- [ ] **Week 4**: ProductHunt launch + case studies
- [ ] **Month 2**: 10 agency partners, 150 customers
- [ ] **Month 3**: Franchise network expansion

## 🎯 Target Metrics (Month 1-3)

| Metric | Month 1 | Month 2 | Month 3 |
|--------|---------|---------|---------|
| Customers | 20 | 150 | 500 |
| MRR | $6K | $75K | $300K |
| Interviews/Month | 240 | 3,000 | 10,000 |
| Staffing Partners | 0 | 10 | 50 |

## 📞 Support

- **Setup Call**: 30-min white-glove onboarding (first 50 customers free)
- **Email**: support@interview-ai.com
- **Docs**: https://docs.interview-ai.com

---

**Built for local businesses. Powered by AI. Designed for scale.**