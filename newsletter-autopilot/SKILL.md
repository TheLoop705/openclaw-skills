---
name: newsletter-autopilot
description: Automated research newsletter delivered via chat (Telegram/Discord). Runs as OpenClaw cron jobs — daily digests, deep-dive articles, and theme scouting. Use when: (1) setting up newsletter cron schedules, (2) running a daily digest, (3) scouting themes for deep-dive research, (4) executing a deep-dive pipeline on a topic, (5) formatting research for chat delivery. Triggers on keywords like newsletter, digest, deep-dive, theme scout, research pipeline.
---

# Newsletter Autopilot

Cron-driven research pipeline → formatted chat messages → Telegram/Discord.

No website. No HTML. Research runs automatically, results land in chat.

## Setup

### Prerequisites

- OpenClaw with `message` tool configured for Telegram or Discord
- Web search available (`web_search`, `web_fetch`)
- Sub-agent spawning for deep-dive pipeline

### Configure delivery target

Set the target channel in the cron prompt or store in workspace:

```
# newsletter-config.json
{
  "channel": "telegram",
  "target": "-100123456789",
  "sectors": ["tech", "macro", "crypto", "energy", "biotech"],
  "archivePath": "newsletter/reports"
}
```

## Workflows

### 1. Daily Digest

Runs via cron (e.g., weekdays 07:00). Single agent, no sub-agents needed.

1. **Search** — Run 5-8 `web_search` calls across configured sectors
2. **Filter** — Drop noise, keep items with real signal (new developments, data, moves)
3. **Summarize** — 3-5 bullet points per sector, each with source context
4. **Format** — Structure for chat delivery (see `references/chat-formatting.md`)
5. **Send** — Post via `message` tool to configured channel
6. **Archive** (optional) — Save as `newsletter/reports/daily/YYYY-MM-DD.md`

Output format example:
```
📰 Daily Digest — March 10, 2026

🖥 **Tech**
• NVIDIA announced... — implications for...
• Apple's new... — signals that...

📊 **Macro**
• Fed minutes revealed... — market expects...

🔗 Sources: <url1>, <url2>
```

### 2. Deep Dive (5-Agent Pipeline)

Triggered by user pick from theme scout, or manually. Spawn as sub-agents:

| Stage | Agent Task | Output |
|-------|-----------|--------|
| **World Scan** | 20+ web searches on theme, extract key narratives | Raw findings doc |
| **Parallels** | Historical parallels, analogies, contrasting views | Context layer |
| **Sectors** | Map impact across sectors, identify winners/losers | Sector analysis |
| **Deep Dive** | Synthesize 2000-3000 word article from above | Draft article |
| **Synthesis** | Final edit — tighten, verify, format for chat | Final report |

Each stage reads the previous stage's output file from `newsletter/reports/deep-dive/`.

Delivery: Split into multiple messages if needed (see `references/chat-formatting.md` for splitting rules). Send company cards as a separate follow-up message.

Archive: Save final report as `newsletter/reports/deep-dive/YYYY-MM-DD-{slug}.md`

### 3. Theme Scouting

Runs via cron (e.g., Mon + Thu 10:00). Scans for emerging trends.

1. **Scan** — Web search each sector for "emerging trends", "breaking", "new development"
2. **Rank** — Score by novelty, cross-sector impact, and investability
3. **Compile** — Pick top 5-8 themes
4. **Send** — Post numbered options to chat:

```
🔭 Theme Scout — March 10, 2026

Pick a theme for this week's deep dive:

1️⃣ **Quantum Error Correction Breakthrough** — IBM's new...
2️⃣ **Rare Earth Supply Shock** — China's export...
3️⃣ **AI Agent Economy** — OpenAI and Anthropic racing to...
4️⃣ **Nuclear Renaissance** — Three new SMR approvals...
5️⃣ **Biotech M&A Wave** — Pfizer's $40B bid signals...

Reply with a number (or suggest your own).
```

5. When user replies with a number → trigger Deep Dive pipeline on that theme

## Chat Formatting

For detailed formatting rules per platform, read `references/chat-formatting.md`.

Key rules:
- **Telegram**: Use HTML or Markdown mode. No tables. Bold with `**`. Links: `[text](url)`
- **Discord**: Markdown supported. Wrap multiple URLs in `<>` to suppress embeds. No tables.
- **Both**: Keep messages under 4000 chars. Split longer content at section boundaries.
- **Company cards**: Use bold name + ticker on one line, note below. No HTML cards.

## Cron Configuration

See `references/cron-examples.md` for ready-to-use OpenClaw cron commands.

## Local Archive

Reports saved to `newsletter/reports/` in workspace:
```
newsletter/reports/
├── daily/
│   └── 2026-03-10.md
└── deep-dive/
    └── 2026-03-10-quantum-error-correction.md
```

Frontmatter spec for archived files: see `references/frontmatter-spec.md`.
