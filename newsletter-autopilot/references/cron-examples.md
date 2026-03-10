# Cron Configuration Examples

OpenClaw cron jobs for newsletter automation.

## Daily Digest

Run weekdays at 07:00 Europe/Berlin:

```bash
openclaw cron add \
  --name "newsletter-daily-digest" \
  --schedule "0 7 * * 1-5" \
  --timezone "Europe/Berlin" \
  --prompt "You are running the newsletter-autopilot daily digest workflow. \
1. Read the newsletter-autopilot skill. \
2. Load newsletter-config.json from workspace for delivery target and sectors. \
3. Run web_search for each sector: tech, macro, crypto, energy, biotech. \
4. Summarize findings — 3-5 bullets per sector, signal only, no noise. \
5. Format per references/chat-formatting.md daily digest template. \
6. Send via message tool to the configured channel. \
7. Save report to newsletter/reports/daily/YYYY-MM-DD.md with frontmatter."
```

## Theme Scout

Run Monday and Thursday at 10:00:

```bash
openclaw cron add \
  --name "newsletter-theme-scout" \
  --schedule "0 10 * * 1,4" \
  --timezone "Europe/Berlin" \
  --prompt "You are running the newsletter-autopilot theme scout workflow. \
1. Read the newsletter-autopilot skill. \
2. Load newsletter-config.json for sectors and delivery target. \
3. Search each sector for emerging trends, breakthroughs, and shifts. \
4. Rank by novelty, cross-sector impact, and investability. \
5. Pick top 5-8 themes. \
6. Format as numbered options per references/chat-formatting.md theme scout template. \
7. Send to configured channel via message tool. \
8. Save scout results to newsletter/reports/theme-scout/YYYY-MM-DD.md."
```

## Managing Cron Jobs

```bash
# List all cron jobs
openclaw cron list

# Remove a job
openclaw cron remove --name "newsletter-daily-digest"

# Pause/resume
openclaw cron disable --name "newsletter-daily-digest"
openclaw cron enable --name "newsletter-daily-digest"
```

## Deep Dive (Manual Trigger)

Deep dives are triggered by user reply to theme scout, not by cron.
When user replies with a theme number, the main session agent:

1. Reads the theme scout report for that day
2. Spawns 5 sub-agents in sequence (world scan → parallels → sectors → deep dive → synthesis)
3. Each writes output to `newsletter/reports/deep-dive/{slug}/stage-{n}.md`
4. Final synthesis agent formats and sends to chat
5. Saves final report to `newsletter/reports/deep-dive/YYYY-MM-DD-{slug}.md`

## Weekend Digest (Optional)

For a weekend summary covering Sat+Sun news, delivered Monday 06:30:

```bash
openclaw cron add \
  --name "newsletter-weekend-digest" \
  --schedule "30 6 * * 1" \
  --timezone "Europe/Berlin" \
  --prompt "You are running a weekend newsletter digest. \
Search for news from Saturday and Sunday across all sectors. \
Format as a combined weekend digest and send to configured channel."
```
