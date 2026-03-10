# Chat Formatting Reference

## Platform Rules

### Telegram
- Use Markdown mode for `message` tool
- Bold: `**text**`
- Italic: `_text_`
- Code: `` `text` ``
- Links: `[label](url)`
- No tables — use bullet lists
- Max message length: ~4096 chars
- Line breaks: use `\n` (double newline for paragraph break)

### Discord
- Full Markdown support
- Bold: `**text**`
- Headers: `## text` (use sparingly, they're large)
- Links: wrap in `<url>` to suppress embeds when listing multiple
- No tables — use bullet lists or bold+indent
- Max message length: 2000 chars (stricter than Telegram)
- Embeds: avoid, keep it plain text

## Message Splitting

When content exceeds platform limits, split at logical boundaries:

1. Split at `## ` section headers first
2. If a section is still too long, split at paragraph breaks
3. Never split mid-sentence or mid-bullet
4. Add a continuation marker: `(1/3)`, `(2/3)`, `(3/3)` at the top of each part
5. Send with a 1-second delay between messages to maintain order

## Daily Digest Format

```
📰 **Daily Digest — {date}**

🖥 **Tech**
• {headline} — {one-line analysis}
• {headline} — {one-line analysis}

📊 **Macro**
• {headline} — {one-line analysis}

₿ **Crypto**
• {headline} — {one-line analysis}

⚡ **Energy**
• {headline} — {one-line analysis}

🧬 **Biotech**
• {headline} — {one-line analysis}

🔗 _Sources_: <url1>, <url2>, ...
```

Sector emojis: 🖥 Tech, 📊 Macro, ₿ Crypto, ⚡ Energy, 🧬 Biotech, 🏭 Industrial, 🏦 Finance

## Deep Dive Format

Split into 3-4 messages:

**Message 1 — Header + Intro**
```
📝 **Deep Dive: {title}**
_{date} · Themes: {theme1}, {theme2}_

{2-3 paragraph introduction setting up the thesis}
```

**Message 2 — Analysis (repeat if needed)**
```
**{Section Title}**

{3-5 paragraphs of analysis}
```

**Message 3 — Companies**
```
🏢 **Companies to Watch**

**{Company Name}** ({TICKER})
{1-2 line note on relevance}

**{Company Name}** ({TICKER})
{1-2 line note on relevance}
```

**Message 4 — Takeaways**
```
🎯 **Key Takeaways**

1. {takeaway}
2. {takeaway}
3. {takeaway}

_Full report saved to: newsletter/reports/deep-dive/{slug}.md_
```

## Theme Scout Format

```
🔭 **Theme Scout — {date}**

Pick a theme for deep dive:

1️⃣ **{Theme}** — {one-line description}
2️⃣ **{Theme}** — {one-line description}
3️⃣ **{Theme}** — {one-line description}
4️⃣ **{Theme}** — {one-line description}
5️⃣ **{Theme}** — {one-line description}

Reply with a number (or suggest your own).
```
