# Frontmatter Spec

YAML frontmatter for archived Markdown reports.

## Schema

```yaml
---
title: "Required — article title"
date: "YYYY-MM-DD"
slug: "url-friendly-short-name"
type: "daily | deep-dive | theme-scout"
themes:
  - "theme tag 1"
  - "theme tag 2"
sectors:
  - "tech"
  - "macro"
companies:
  - name: "Company Name"
    ticker: "TICK"
    note: "Why it matters"
takeaways:
  - "Key takeaway 1"
  - "Key takeaway 2"
  - "Key takeaway 3"
summary: "One-line summary for index/search"
sources:
  - "https://source-url-1.com"
  - "https://source-url-2.com"
---
```

## Field Rules

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| title | Yes | string | |
| date | Yes | string | ISO 8601 date |
| slug | Yes | string | Lowercase, hyphens only, max 60 chars |
| type | Yes | enum | `daily`, `deep-dive`, or `theme-scout` |
| themes | No | list | For deep-dives and theme-scouts |
| sectors | No | list | Sectors covered |
| companies | No | list of objects | Each has `name`, `ticker`, `note` |
| takeaways | No | list | For deep-dives |
| summary | Yes | string | One sentence |
| sources | No | list | URLs referenced |

## Examples

### Daily Digest

```yaml
---
title: "Daily Digest"
date: "2026-03-10"
slug: "2026-03-10"
type: daily
sectors: ["tech", "macro", "crypto"]
summary: "NVIDIA earnings beat, Fed holds steady, Bitcoin ETF inflows surge"
sources:
  - "https://reuters.com/..."
  - "https://bloomberg.com/..."
---
```

### Deep Dive

```yaml
---
title: "The Quantum Error Correction Breakthrough"
date: "2026-03-10"
slug: "quantum-error-correction"
type: deep-dive
themes: ["quantum computing", "semiconductors"]
sectors: ["tech", "finance"]
companies:
  - name: "IBM"
    ticker: "IBM"
    note: "Leading the QEC breakthrough with Heron processor"
  - name: "IonQ"
    ticker: "IONQ"
    note: "Trapped-ion approach may benefit from IBM's error correction research"
takeaways:
  - "Quantum error correction crossed the practical threshold"
  - "Timeline to quantum advantage shortened by 3-5 years"
  - "Semiconductor suppliers positioned to benefit first"
summary: "IBM's quantum error correction milestone changes the timeline for practical quantum computing"
sources:
  - "https://research.ibm.com/..."
---
```
