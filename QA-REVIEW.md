# QA Review — OpenClaw Skills

**Reviewer:** QA Subagent  
**Date:** 2026-03-10  
**Skills Reviewed:** options-flow, newsletter-autopilot, homeassistant  
**Benchmark Skills:** weather, github, coding-agent, gh-issues

---

## Summary

| Skill | Score | Verdict |
|-------|-------|---------|
| **options-flow** | 8/10 | Solid. Best of the three — good structure, scripts, references. |
| **homeassistant** | 7/10 | Good foundation but missing referenced files and references dir. |
| **newsletter-autopilot** | 4/10 | SKILL.md only — no scripts, no references, no assets. Unusable as-is. |

---

## 1. options-flow — 8/10

### What's Good
- **Frontmatter description** is excellent — comprehensive trigger list with 8 specific use cases and clear NOT-for boundaries. Matches the quality of the `github` skill's description.
- **Progressive disclosure** done right: SKILL.md is 144 lines (well under 500), with detailed API docs pushed to `references/api-endpoints.md` and anomaly explanations in `references/anomaly-types.md`.
- **Scripts are well-written:** `uw_api.py` has proper rate limiting, auth validation, error handling, and clean CLI interface. `analyze_flow.py` has a logical multi-step analysis pipeline.
- **Reference files** are useful and appropriately scoped — `anomaly-types.md` (79 lines) and `api-endpoints.md` (106 lines) provide real value without bloating SKILL.md.
- **No junk files** (no README, CHANGELOG, etc.) — follows skill-creator guidelines.

### Issues

1. **`SKILL.md:1-3` — Missing metadata field:** No `metadata` block with `openclaw.requires` or `primaryEnv`. Compare to `github` skill which declares `requires.bins: ["gh"]`. Should declare:
   ```yaml
   metadata: { "openclaw": { "emoji": "📈", "requires": { "bins": ["python3", "curl"] }, "primaryEnv": "UNUSUAL_WHALES_API_KEY" } }
   ```

2. **`scripts/uw_api.py:49` — `sys.exit(1)` on HTTP errors is aggressive.** When called as a library (from `analyze_flow.py`), this kills the entire process instead of raising an exception. The `analyze_flow.py` wraps calls in try/except, but `sys.exit()` bypasses exception handling. Should raise `RuntimeError` instead when imported as a module.

3. **`scripts/analyze_flow.py` — No ticker validation.** Accepts any string; could add basic validation (e.g., 1-5 uppercase alpha chars) to fail fast on typos.

4. **`references/api-endpoints.md` — Missing query params.** The `flow-alerts` endpoint in the reference lists `ticker`, `is_sweep`, `is_block`, `min_premium` params, but `uw_api.py:flow_alerts()` only supports `limit`. The script should match the documented API surface or the reference should note which params are implemented.

5. **SKILL.md "Analysis Workflow" section** is a nice touch but could reference that `analyze_flow.py` already implements steps 1-4, so the agent doesn't duplicate work.

### Suggested Improvements
- Add `metadata` block with `primaryEnv` and `requires`
- Change `sys.exit(1)` to exceptions in `uw_api.py` when used as library
- Add a `--json` flag to `analyze_flow.py` for structured output that the agent can parse programmatically
- Consider a `references/interpretation-guide.md` for how to synthesize findings into actionable summaries (the "so what?" factor)

---

## 2. homeassistant — 7/10

### What's Good
- **Frontmatter description** is thorough — 8 specific trigger scenarios covering lights, sensors, climate, automations, media, history, and a catch-all "any smart home / IoT task." Well-matched to the `weather` skill pattern.
- **SKILL.md is concise** at 151 lines — leaves plenty of room for the context window.
- **Device types table** is excellent — quick-reference format that an agent can use immediately.
- **Common Patterns table** at the bottom is great for trigger-to-action mapping.
- **`scripts/ha_api.py`** is solid — proper class structure, comprehensive methods (state, service, events, history, logbook), good error handling with `RuntimeError` (not `sys.exit`!), and a useful CLI mode.
- **`scripts/ha_dashboard.py`** is well-designed — area grouping, domain icons, battery summary with low-battery warnings.

### Issues

1. **`SKILL.md:149-151` — References to non-existent files:** The skill references three files that don't exist:
   - `references/rest-api.md`
   - `references/common-services.md`
   - `references/entity-naming.md`
   
   There is no `references/` directory at all. This is a significant gap — the agent will try to read these and fail. Either create them or remove the references.

2. **`SKILL.md:1-3` — Missing metadata:** Same issue as options-flow. Should declare:
   ```yaml
   metadata: { "openclaw": { "emoji": "🏠", "requires": { "bins": ["python3", "curl"] }, "primaryEnv": "HA_TOKEN" } }
   ```

3. **`SKILL.md:113-117` — SSH section is risky.** Providing `ssh root@<ha-host>` commands without any safety guardrails is dangerous. An agent could restart HA or modify config files unintentionally. Should add a clear warning: "⚠️ Ask user before running SSH commands — these can disrupt the smart home."

4. **`SKILL.md:102` — `ha_dashboard.py` referenced but path wrong.** SKILL.md says `scripts/ha_dashboard.py` but lists it under "Python Helpers" alongside `ha_api.py`. Consistent, but should note that dashboard requires `ha_api.py` (it imports from it).

5. **`scripts/ha_api.py:35-36` — Timeout not configurable.** Hardcoded 30s timeout is fine for most calls but `get_all_states()` on a large HA instance can be slow. Minor, but worth noting.

6. **No "When NOT to Use" section** unlike weather and github skills. Should add: NOT for: Zigbee/Z-Wave device pairing, add-on installation, HA OS updates, HA configuration.yaml editing (use SSH access skill if available).

### Suggested Improvements
- **Create the referenced `references/` files** — at minimum `common-services.md` with service call parameters per domain. This is the biggest gap.
- Add metadata block
- Add safety warnings for SSH commands
- Add "When NOT to Use" section
- Consider a `scripts/ha_scene.py` for scene activation (common use case not covered)

---

## 3. newsletter-autopilot — 4/10

### What's Good
- **Concept is ambitious and interesting** — a multi-agent newsletter pipeline is a genuinely useful skill idea.
- **SKILL.md is well-structured** at 129 lines — clear sections for Setup, Workflows, Publishing, Cron, Delivery.
- **Frontmatter description** is decent — covers the main trigger scenarios and keywords.
- **The 5-agent deep dive pipeline table** is a nice progressive workflow design.

### Critical Issues

1. **No scripts exist.** SKILL.md references:
   - `scripts/init-newsletter.sh` (line 11)
   - `scripts/publish-daily.py` (line 26)
   - `scripts/publish-issue.py` (line 41)
   
   None of these files exist. The skill is effectively a design doc, not a working skill. An agent trying to use this will immediately fail.

2. **No references exist.** SKILL.md references:
   - `references/frontmatter-spec.md` (lines 24, 47)
   - `references/html-template.md` (lines 46, 47)
   - `references/cron-examples.md` (line 50)
   
   None exist. The agent has no way to know the frontmatter schema or HTML template structure.

3. **No assets exist.** SKILL.md references:
   - `assets/templates/` (line 13)
   - `assets/css/style.css` (line 13)
   
   None exist. The init script can't work without templates.

4. **`SKILL.md:1-3` — Missing metadata.** Should declare:
   ```yaml
   metadata: { "openclaw": { "emoji": "📰", "requires": { "bins": ["gh", "python3", "git"] } } }
   ```

5. **Frontmatter description lacks NOT-for boundaries.** Every good skill (weather, github, coding-agent) explicitly states what it's NOT for. This helps avoid false triggers.

6. **No error handling guidance.** What happens if web search returns nothing? If GitHub Pages isn't enabled? If the repo doesn't exist? The skill gives no failure path.

7. **"5-Agent Pipeline" has no implementation details.** The table describes what each agent should do conceptually, but there's no actual prompt template, no spawn configuration, no example of how to pass context between stages. Compare to `gh-issues` which provides complete sub-agent prompts.

### Suggested Improvements
- **Implement the scripts** — this is the #1 priority. Without them, the skill is vapor.
- **Create reference files** — at least the frontmatter spec and HTML template.
- **Create asset templates** — landing page, article page, CSS.
- Add NOT-for section in description
- Add error handling guidance for common failure modes
- Provide actual sub-agent prompt templates for the deep-dive pipeline (follow gh-issues pattern)
- Add metadata block

---

## Cross-Cutting Issues

### Metadata Blocks
None of the three skills include `metadata` with `openclaw.requires` or `primaryEnv`. The bundled skills (weather, github, gh-issues, coding-agent) all include these. This means OpenClaw can't auto-check if required binaries are installed or if API keys are configured before loading the skill.

**Fix all three.**

### Naming Conventions
All three follow the skill-creator naming rules: lowercase, hyphens, short, descriptive. ✅

### Would These Be Useful Fresh?

| Skill | Useful Fresh? | Notes |
|-------|--------------|-------|
| options-flow | **Yes** — install, set API key, go | Needs the API key but otherwise complete |
| homeassistant | **Mostly** — needs missing references | Core functionality works, but agent will hit dead-end references |
| newsletter-autopilot | **No** — broken out of the box | No scripts = no functionality |

---

## Comparison to Benchmark Skills

| Aspect | weather | github | options-flow | homeassistant | newsletter-autopilot |
|--------|---------|--------|-------------|--------------|---------------------|
| Description quality | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Metadata present | ✅ | ✅ | ❌ | ❌ | ❌ |
| Scripts tested/working | n/a | n/a | ✅ | ✅ | ❌ (missing) |
| References complete | n/a | n/a | ✅ | ❌ (missing) | ❌ (missing) |
| Under 500 lines | ✅ | ✅ | ✅ | ✅ | ✅ |
| Progressive disclosure | ✅ | ✅ | ✅ | ✅ | ✅ (in theory) |
| Error handling in scripts | n/a | n/a | ⭐⭐ | ⭐⭐⭐ | n/a |
| Usable out of box | ✅ | ✅ | ✅ | ⚠️ | ❌ |

---

## Priority Actions

### Must Fix (blocks usability)
1. **newsletter-autopilot:** Create all referenced scripts, references, and assets
2. **homeassistant:** Create `references/` directory with the 3 referenced files

### Should Fix (quality gaps)
3. All three: Add `metadata` blocks with `requires` and `primaryEnv`
4. **options-flow:** Fix `sys.exit()` in `uw_api.py` when used as library
5. **homeassistant:** Add safety warnings for SSH commands
6. **homeassistant:** Add "When NOT to Use" section

### Nice to Have
7. **options-flow:** Add `--json` output flag to `analyze_flow.py`
8. **newsletter-autopilot:** Add complete sub-agent prompt templates (follow gh-issues pattern)
9. **homeassistant:** Add scene activation script

---

*Review complete. The options-flow skill is production-ready with minor tweaks. The homeassistant skill needs its references created. The newsletter-autopilot skill needs substantial implementation work before it can be shipped.*
