# Interview.ai - MVP Launch Checklist

## Week 1: Build & Launch (Days 1-7)

### Day 1-2: Core Infrastructure ✅
- [x] Project structure created
- [x] FastAPI app setup
- [x] Database models (Customer, Candidate, Interview)
- [x] Voice agent core logic
- [ ] Deploy to staging (Railway/Render/Fly.io)
- [ ] Set up PostgreSQL database

### Day 3: API Integrations
- [ ] Configure Twilio account & phone number
- [ ] Get OpenAI API key
- [ ] Get ElevenLabs API key (optional, for better voice)
- [ ] Get Deepgram API key
- [ ] Test outbound call flow

### Day 4: Payment Setup
- [ ] Create Stripe account
- [ ] Set up products/prices:
  - [ ] $49/hire (pay-per-hire)
  - [ ] $299/month (unlimited, 20 interviews)
- [ ] Configure webhook endpoint
- [ ] Test checkout flow

### Day 5: Zapier Integration
- [ ] Build Zapier app manifest
- [ ] Test webhook endpoint
- [ ] Create sample Zaps:
  - [ ] Google Sheets → Interview trigger
  - [ ] Airtable → Interview trigger
  - [ ] Typeform → Interview trigger

### Day 6: Soft Launch Prep
- [ ] Recruit 5 beta testers (friends in staffing/service biz)
- [ ] Prepare demo script
- [ ] Set up error tracking (Sentry)
- [ ] Create onboarding checklist

### Day 7: SOFT LAUNCH 🚀
- [ ] Onboard first 5 beta users (FREE)
- [ ] Collect testimonials
- [ ] Record demo videos
- [ ] Fix critical bugs

---

## Week 2: Distribution (Days 8-14)

### Content & Marketing
- [ ] Write LinkedIn post: "We replaced screening calls with AI"
- [ ] Post on r/smallbusiness, r/entrepreneur, HN
- [ ] Create landing page (Carrd/Webflow)
- [ ] Set up email capture (ConvertKit/Beehiiv)

### Staffing Agency Outreach
- [ ] Build list of 50 local staffing agencies
- [ ] Send personalized emails:
  ```
  Subject: Quick question about your candidate screening

  Hi [Name],

  I noticed [Agency] places [role type] candidates.
  We built an AI screener that calls candidates within hours
  and qualifies them before you ever talk to them.

  One agency went from 50% → 90% first-round success rate.

  Worth a 10-min demo this week?

  - [Your name]
  ```
- [ ] Offer affiliate deal: $100/referral or 20% rev share

### Product Improvements
- [ ] Add interview analytics dashboard
- [ ] Improve voice quality (A/B test voices)
- [ ] Add SMS follow-up automation
- [ ] Build candidate portal (simple status checker)

---

## Week 3-4: Scale (Days 15-30)

### Partnerships
- [ ] Close 5 staffing agency partners
- [ ] Pitch to franchise networks (Angi, TaskRabbit affiliates)
- [ ] Contact local Chamber of Commerce chapters
- [ ] Reach out to Indeed/ZipRecruiter API teams

### ProductHunt Launch
- [ ] Prepare launch assets (screenshots, demo video)
- [ ] Line up 20 supporters for Day 1 upvotes
- [ ] Write maker comment story
- [ ] Schedule launch for Tuesday/Wednesday

### Paid Acquisition Test
- [ ] Run LinkedIn ads targeting:
  - Job titles: "Owner", "HR Manager", "Recruiter"
  - Company size: 1-50 employees
  - Industries: Construction, Healthcare, Retail
- [ ] Budget: $500 test
- [ ] Target CAC: <$200

### Metrics to Hit by Day 30
- [ ] 20 paying customers
- [ ] $6K MRR
- [ ] 240 interviews conducted
- [ ] 3 case studies published
- [ ] 5 staffing agency partners
- [ ] NPS score >50

---

## Technical Debt to Address

### Security & Compliance
- [ ] EEOC legal review ($2K budget)
- [ ] FCRA compliance check
- [ ] TCPA consent flow for automated calls
- [ ] Data retention policy (90-day default)
- [ ] GDPR/CCPA data export/delete

### Performance
- [ ] Add Redis caching for templates
- [ ] Implement rate limiting
- [ ] Set up CDN for static assets
- [ ] Optimize database queries
- [ ] Add connection pooling

### Monitoring
- [ ] Set up uptime monitoring (UptimeRobot)
- [ ] Configure alerts for failed calls
- [ ] Track API costs per interview
- [ ] Monitor transcription accuracy
- [ ] Daily cost reports

---

## Go/No-Go Decision Points

### Week 2 Checkpoint
**GO if:**
- 5+ beta users active
- Call success rate >90%
- At least 1 testimonial collected

**PIVOT if:**
- Candidates hate the experience
- Legal concerns block launch
- COGS >$5/interview

### Week 4 Checkpoint
**GO if:**
- $6K MRR achieved
- CAC < $200
- Churn < 10%

**PIVOT if:**
- Can't close staffing agencies
- Enterprise wants custom features
- Margins compress below 80%

---

## Budget Breakdown (Month 1)

| Category | Cost |
|----------|------|
| Twilio (calls) | $500 |
| OpenAI API | $300 |
| ElevenLabs | $100 |
| Deepgram | $100 |
| Hosting (Railway) | $50 |
| Database (Neon/Supabase) | $50 |
| Stripe fees (3%) | ~$200 |
| Legal review | $2,000 |
| **Total** | **~$3,300** |

**Revenue target:** $6,000
**Net Month 1:** +$2,700 (before founder time)

---

## Success Metrics Dashboard

Track weekly:
- **MRR Growth:** Week-over-week % change
- **Interviews Conducted:** Total per week
- **Qualification Rate:** % of candidates who pass
- **NPS Score:** Customer satisfaction
- **CAC:** Cost per acquired customer
- **LTV:** Average revenue per customer
- **Churn:** Monthly cancellation rate
- **Support Tickets:** Per 100 customers

**Red flags:**
- Churn > 15%/month
- CAC > $300
- Qualification rate < 40% (too strict) or > 90% (too lenient)
- Support tickets > 10/100 customers

---

**Remember:** Speed beats perfection. Ship daily. Talk to customers weekly. Iterate based on data, not opinions.
