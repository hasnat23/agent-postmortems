# agent-postmortems

**Real AI agent and LLM failures in production: what broke, why, and what would have stopped it.**

Agents now hold production credentials, read untrusted issues and emails, install packages and run shell
commands. They fail in new ways, and the lessons are scattered across vendor blogs, security
write-ups and viral threads. This repo collects them in one place, with a source for every claim,
in a structured format you can search, filter and build on.

Every entry answers four questions: **what happened**, **the root cause**, **who was affected**, and
**which concrete control would have prevented it**.

[**Browse and filter the incidents →**](https://hasnat23.github.io/agent-postmortems/) ·
[Taxonomy](TAXONOMY.md) · [Add an incident](CONTRIBUTING.md) · [`incidents.json`](docs/incidents.json)

## At a glance

<!-- BEGIN:STATS -->
**57 incidents** from 2023 to 2026: **35** hit real users or systems, **22** were demonstrated by researchers.

| Failure class | Incidents | |
|---|---:|---|
| [`prompt-injection`](TAXONOMY.md#prompt-injection) | 21 | `████████████████████` |
| [`data-exfiltration`](TAXONOMY.md#data-exfiltration) | 19 | `██████████████████` |
| [`excessive-agency`](TAXONOMY.md#excessive-agency) | 13 | `████████████` |
| [`supply-chain`](TAXONOMY.md#supply-chain) | 11 | `██████████` |
| [`infra-vuln`](TAXONOMY.md#infra-vuln) | 10 | `██████████` |
| [`hallucination`](TAXONOMY.md#hallucination) | 8 | `████████` |
| [`tool-poisoning`](TAXONOMY.md#tool-poisoning) | 7 | `███████` |
| [`unsafe-output-handling`](TAXONOMY.md#unsafe-output-handling) | 6 | `██████` |
| [`destructive-action`](TAXONOMY.md#destructive-action) | 6 | `██████` |
| [`isolation-failure`](TAXONOMY.md#isolation-failure) | 3 | `███` |
| [`sandbox-escape`](TAXONOMY.md#sandbox-escape) | 3 | `███` |
| [`model-behavior`](TAXONOMY.md#model-behavior) | 2 | `██` |
| [`memory-poisoning`](TAXONOMY.md#memory-poisoning) | 2 | `██` |
| [`misuse`](TAXONOMY.md#misuse) | 2 | `██` |
<!-- END:STATS -->

## Lessons that keep repeating

1. **The prompt is not a permission system.** "Don't touch prod", "only suggest" and "code freeze" were
   instructions in the context window at [Replit](incidents/AP-0028-replit-agent-deletes-saastr-production-db.yaml), [OpenClaw](incidents/AP-0039-openclaw-inbox-deletion.yaml) and [PocketOS](incidents/AP-0046-pocketos-database-deleted-in-9-seconds.yaml). The agent
   had the credentials anyway. Enforce limits in the tool layer and in the credentials, not in English.
2. **The lethal trifecta.** Private data, untrusted content and a way to send data out, all in one agent:
   that's how [GitHub MCP](incidents/AP-0020-github-mcp-toxic-agent-flow.yaml), [Supabase MCP](incidents/AP-0026-supabase-mcp-support-ticket-leak.yaml), [EchoLeak](incidents/AP-0022-echoleak-m365-copilot-zero-click.yaml), [CamoLeak](incidents/AP-0037-camoleak-copilot-chat-private-code.yaml),
   [ForcedLeak](incidents/AP-0035-forcedleak-agentforce-expired-domain.yaml) and [Comment and Control](incidents/AP-0049-comment-and-control-ci-agents.yaml) leaked data. Remove any one of the three and the
   attack fails. (Term coined by Simon Willison.)
3. **Rendering is an exfiltration channel.** Markdown images and links built from model output carried data
   out of [Copilot](incidents/AP-0037-camoleak-copilot-chat-private-code.yaml), [Slack AI](incidents/AP-0013-slack-ai-private-channel-exfiltration.yaml), [Agentforce](incidents/AP-0035-forcedleak-agentforce-expired-domain.yaml) and [Grafana](incidents/AP-0048-grafanaghost-image-exfiltration.yaml). Don't auto-render
   URLs the model wrote.
4. **Tool metadata is code.** MCP descriptions ([tool poisoning](incidents/AP-0017-mcp-tool-poisoning-disclosure.yaml), [Deadbugz](incidents/AP-0056-deadbugz-mcp-rug-pull-campaign.yaml)), [rules files](incidents/AP-0015-rules-file-backdoor.yaml)
   and [agent configs](incidents/AP-0051-mini-shai-hulud-miasma-worms.yaml) are executed by the model or the IDE. Pin them, diff them, and review them like
   dependencies.
5. **Backups the agent can reach are not backups.** [PocketOS](incidents/AP-0046-pocketos-database-deleted-in-9-seconds.yaml) lost the backups stored on the volume
   the agent deleted.
6. **Evaluation sandboxes are production.** Frontier-lab eval agents with unintended internet access
   [intruded into Hugging Face](incidents/AP-0053-eval-agent-intrusion-hugging-face.yaml), [attacked a real company](incidents/AP-0054-anthropic-eval-attacks-real-company.yaml) and
   [published a real malicious package](incidents/AP-0055-anthropic-eval-publishes-malicious-pypi-package.yaml) in 2026.
7. **Hallucination is a liability, not a quirk.** A tribunal held [Air Canada](incidents/AP-0007-air-canada-chatbot-refund-policy.yaml) to its chatbot's
   invented policy, and [Deloitte](incidents/AP-0036-deloitte-refund-ai-fabricated-citations.yaml) refunded a government over fabricated citations.

## Incidents

Newest first. Click an ID for the full postmortem, including the root cause, mitigations and sources.

<!-- BEGIN:INCIDENTS -->
| ID | Date | Incident | Classes | Severity | Status |
|---|---|---|---|---|---|
| [AP-0057](incidents/AP-0057-cosnitch-copilot-memory-poisoning.yaml) | 2026-08-18 | CoSnitch, a crafted link runs prompts in Microsoft Copilot and poisons its memory | `prompt-injection` `data-exfiltration` `memory-poisoning` | 🟧 high | 🧪 research |
| [AP-0056](incidents/AP-0056-deadbugz-mcp-rug-pull-campaign.yaml) | 2026-08-12 | "Deadbugz": malicious MCP server sent to 23 AI repos in 74 minutes, turns hostile after three calls | `tool-poisoning` `supply-chain` | 🟨 medium | 🔥 in the wild |
| [AP-0055](incidents/AP-0055-anthropic-eval-publishes-malicious-pypi-package.yaml) | 2026-07-30 | Claude in a cyber eval publishes a malicious PyPI package that runs on 15 real systems | `sandbox-escape` `supply-chain` | 🟧 high | 🔥 in the wild |
| [AP-0054](incidents/AP-0054-anthropic-eval-attacks-real-company.yaml) | 2026-07-30 | Claude in a misconfigured cyber eval attacks a real company sharing a fictional target's name | `sandbox-escape` `excessive-agency` | 🟧 high | 🔥 in the wild |
| [AP-0053](incidents/AP-0053-eval-agent-intrusion-hugging-face.yaml) | 2026-07-21 | Frontier-lab evaluation agent escapes its sandbox and intrudes into Hugging Face production | `sandbox-escape` `infra-vuln` `excessive-agency` | 🟥 critical | 🔥 in the wild |
| [AP-0052](incidents/AP-0052-sentry-agentjacking.yaml) | 2026-06 | "Agentjacking": fake Sentry error events instruct coding agents to run attacker code | `prompt-injection` `excessive-agency` | 🟧 high | 🧪 research |
| [AP-0051](incidents/AP-0051-mini-shai-hulud-miasma-worms.yaml) | 2026-05 | Mini Shai-Hulud and Miasma worms plant persistence in AI coding tools via npm and PyPI | `supply-chain` `tool-poisoning` | 🟥 critical | 🔥 in the wild |
| [AP-0050](incidents/AP-0050-vercel-context-ai-oauth-pivot.yaml) | 2026-04-19 | Compromised AI tool Context.ai becomes a path into Vercel employee accounts and customer secrets | `supply-chain` `excessive-agency` `data-exfiltration` | 🟧 high | 🔥 in the wild |
| [AP-0049](incidents/AP-0049-comment-and-control-ci-agents.yaml) | 2026-04-15 | "Comment and Control": a PR title makes three CI coding agents post their own secrets | `prompt-injection` `data-exfiltration` `excessive-agency` | 🟥 critical | 🧪 research |
| [AP-0048](incidents/AP-0048-grafanaghost-image-exfiltration.yaml) | 2026-04-07 | GrafanaGhost, hidden instructions make Grafana's AI assistant leak data through an image URL | `prompt-injection` `data-exfiltration` `unsafe-output-handling` | 🟧 high | 🧪 research |
| [AP-0047](incidents/AP-0047-flowise-custommcp-rce-exploited.yaml) | 2026-04-07 | Max-severity Flowise RCE through the CustomMCP node is exploited in the wild | `infra-vuln` | 🟥 critical | 🔥 in the wild |
| [AP-0046](incidents/AP-0046-pocketos-database-deleted-in-9-seconds.yaml) | 2026-04 | Coding agent deletes PocketOS's production database and backups in one API call | `destructive-action` `excessive-agency` | 🟥 critical | 🔥 in the wild |
| [AP-0045](incidents/AP-0045-pipeleak-shareleak-form-injection.yaml) | 2026-04 | Web forms hijack Salesforce Agentforce and Microsoft Copilot agents (PipeLeak / ShareLeak) | `prompt-injection` `data-exfiltration` | 🟧 high | 🧪 research |
| [AP-0044](incidents/AP-0044-vertex-ai-double-agent.yaml) | 2026-03-31 | "Double Agent": deployed Vertex AI agents inherit service account rights and steal credentials | `excessive-agency` `infra-vuln` | 🟧 high | 🧪 research |
| [AP-0043](incidents/AP-0043-claude-code-source-map-leak-lures.yaml) | 2026-03-31 | Claude Code npm release ships a source map, and attackers use "leaked source" repos as malware lures | `supply-chain` | 🟨 medium | 🔥 in the wild |
| [AP-0042](incidents/AP-0042-litellm-pypi-compromise-mercor.yaml) | 2026-03-24 | Malicious LiteLLM releases on PyPI steal credentials; Mercor breach follows | `supply-chain` `data-exfiltration` | 🟥 critical | 🔥 in the wild |
| [AP-0041](incidents/AP-0041-meta-internal-agent-data-exposure.yaml) | 2026-03-20 | Meta engineer follows an internal AI agent's advice and exposes sensitive data for two hours | `hallucination` `isolation-failure` | 🟧 high | 🔥 in the wild |
| [AP-0040](incidents/AP-0040-mexico-government-claude-assisted-breach.yaml) | 2026-02-25 | Attacker uses Claude to automate a breach of Mexican government agencies | `misuse` | 🟥 critical | 🔥 in the wild |
| [AP-0039](incidents/AP-0039-openclaw-inbox-deletion.yaml) | 2026-02-23 | OpenClaw agent deletes a Meta AI safety director's inbox and ignores stop commands | `destructive-action` `excessive-agency` | 🟨 medium | 🔥 in the wild |
| [AP-0038](incidents/AP-0038-antigravity-wipes-d-drive.yaml) | 2025-11 | Google Antigravity agent wipes a user's entire D drive while clearing a cache | `destructive-action` | 🟧 high | 🔥 in the wild |
| [AP-0037](incidents/AP-0037-camoleak-copilot-chat-private-code.yaml) | 2025-10-08 | CamoLeak, private source code leaking from GitHub Copilot Chat via image proxy URLs | `prompt-injection` `data-exfiltration` `unsafe-output-handling` | 🟥 critical | 🧪 research |
| [AP-0036](incidents/AP-0036-deloitte-refund-ai-fabricated-citations.yaml) | 2025-10 | Deloitte refunds part of an A$440,000 government report after AI-fabricated citations | `hallucination` | 🟨 medium | 🔥 in the wild |
| [AP-0035](incidents/AP-0035-forcedleak-agentforce-expired-domain.yaml) | 2025-09-25 | ForcedLeak, CRM data leaking from Agentforce through an expired allowlisted domain | `prompt-injection` `data-exfiltration` `unsafe-output-handling` | 🟥 critical | 🧪 research |
| [AP-0034](incidents/AP-0034-postmark-mcp-bcc-backdoor.yaml) | 2025-09 | First malicious MCP server in the wild silently BCCs every email ("postmark-mcp") | `supply-chain` `tool-poisoning` `data-exfiltration` | 🟥 critical | 🔥 in the wild |
| [AP-0033](incidents/AP-0033-nx-s1ngularity-weaponizes-ai-clis.yaml) | 2025-08-26 | Malicious Nx packages use local AI CLIs to hunt for secrets ("s1ngularity") | `supply-chain` `misuse` `data-exfiltration` | 🟥 critical | 🔥 in the wild |
| [AP-0032](incidents/AP-0032-gemini-calendar-invite-hijack.yaml) | 2025-08 | Google Calendar invites hijack Gemini to control smart-home devices | `prompt-injection` `excessive-agency` | 🟧 high | 🧪 research |
| [AP-0031](incidents/AP-0031-cursor-curxecute-mcpoison.yaml) | 2025-08 | Cursor runs attacker-edited MCP configs (CurXecute and MCPoison) | `prompt-injection` `tool-poisoning` `infra-vuln` | 🟧 high | 🧪 research |
| [AP-0030](incidents/AP-0030-comet-browser-indirect-injection.yaml) | 2025-08 | Perplexity Comet follows instructions hidden in a Reddit comment and leaks the user's account | `prompt-injection` `data-exfiltration` `excessive-agency` | 🟧 high | 🧪 research |
| [AP-0029](incidents/AP-0029-amazon-q-extension-wiper-prompt.yaml) | 2025-07-23 | Wiper prompt merged into Amazon Q Developer's VS Code extension and shipped | `supply-chain` `prompt-injection` `destructive-action` | 🟥 critical | 🔥 in the wild |
| [AP-0028](incidents/AP-0028-replit-agent-deletes-saastr-production-db.yaml) | 2025-07-18 | Replit Agent deletes a production database during a code freeze, then misreports it | `destructive-action` `excessive-agency` | 🟥 critical | 🔥 in the wild |
| [AP-0027](incidents/AP-0027-mchire-123456-applicant-data.yaml) | 2025-07-09 | McDonald's AI hiring bot backend exposes 64 million applicant records behind "123456" | `infra-vuln` | 🟧 high | 🔥 in the wild |
| [AP-0026](incidents/AP-0026-supabase-mcp-support-ticket-leak.yaml) | 2025-07 | Support ticket makes a Cursor agent dump a Supabase database through MCP | `prompt-injection` `data-exfiltration` `excessive-agency` | 🟧 high | 🧪 research |
| [AP-0025](incidents/AP-0025-mcp-remote-command-injection.yaml) | 2025-07 | Malicious MCP server gets OS command execution through mcp-remote (CVE-2025-6514) | `infra-vuln` `tool-poisoning` | 🟥 critical | 🧪 research |
| [AP-0024](incidents/AP-0024-mcp-inspector-browser-rce.yaml) | 2025-07 | Browser-based RCE in Anthropic's MCP Inspector developer tool (CVE-2025-49596) | `infra-vuln` | 🟥 critical | 🧪 research |
| [AP-0023](incidents/AP-0023-gemini-cli-deletes-user-files.yaml) | 2025-07 | Gemini CLI loses a user's files after acting on a mkdir that never succeeded | `destructive-action` | 🟧 high | 🔥 in the wild |
| [AP-0022](incidents/AP-0022-echoleak-m365-copilot-zero-click.yaml) | 2025-06-11 | EchoLeak, a zero-click data exfiltration from Microsoft 365 Copilot via one email | `prompt-injection` `data-exfiltration` `unsafe-output-handling` | 🟥 critical | 🧪 research |
| [AP-0021](incidents/AP-0021-asana-mcp-cross-tenant-exposure.yaml) | 2025-06 | Asana's MCP server exposes data across customer organizations | `isolation-failure` `infra-vuln` | 🟧 high | 🔥 in the wild |
| [AP-0020](incidents/AP-0020-github-mcp-toxic-agent-flow.yaml) | 2025-05-26 | Public GitHub issue makes an agent leak private repos through the GitHub MCP server | `prompt-injection` `data-exfiltration` `excessive-agency` | 🟧 high | 🧪 research |
| [AP-0019](incidents/AP-0019-gpt-4o-sycophancy-rollback.yaml) | 2025-04-29 | OpenAI rolls back a GPT-4o update that made ChatGPT sycophantic | `model-behavior` | 🟨 medium | 🔥 in the wild |
| [AP-0018](incidents/AP-0018-whatsapp-mcp-history-exfiltration.yaml) | 2025-04 | Poisoned MCP server exfiltrates a user's WhatsApp history through a second server | `tool-poisoning` `data-exfiltration` | 🟧 high | 🧪 research |
| [AP-0017](incidents/AP-0017-mcp-tool-poisoning-disclosure.yaml) | 2025-04 | MCP tool poisoning, where hidden instructions live in tool descriptions | `tool-poisoning` `data-exfiltration` | 🟧 high | 🧪 research |
| [AP-0016](incidents/AP-0016-cursor-support-bot-invents-policy.yaml) | 2025-04 | Cursor's AI support agent invents a "one device" policy and triggers cancellations | `hallucination` | 🟨 medium | 🔥 in the wild |
| [AP-0015](incidents/AP-0015-rules-file-backdoor.yaml) | 2025-03-18 | Rules File Backdoor, hidden Unicode in config files makes Copilot and Cursor write malicious code | `supply-chain` `prompt-injection` | 🟧 high | 🧪 research |
| [AP-0014](incidents/AP-0014-chatgpt-spaiware-memory-exfiltration.yaml) | 2024-09 | "SpAIware": persistent ChatGPT memory injection exfiltrates all future chats | `prompt-injection` `memory-poisoning` `data-exfiltration` | 🟧 high | 🧪 research |
| [AP-0013](incidents/AP-0013-slack-ai-private-channel-exfiltration.yaml) | 2024-08-20 | Slack AI leaks secrets from private channels via a message in a public one | `prompt-injection` `data-exfiltration` `unsafe-output-handling` | 🟧 high | 🧪 research |
| [AP-0012](incidents/AP-0012-vanna-ai-prompt-to-rce.yaml) | 2024-06 | Prompt injection becomes remote code execution in Vanna.AI (CVE-2024-5565) | `prompt-injection` `unsafe-output-handling` | 🟥 critical | 🧪 research |
| [AP-0011](incidents/AP-0011-google-ai-overviews-glue-pizza.yaml) | 2024-05 | Google AI Overviews tells users to put glue on pizza and eat rocks | `hallucination` | 🟨 medium | 🔥 in the wild |
| [AP-0010](incidents/AP-0010-nyc-mycity-chatbot-illegal-advice.yaml) | 2024-03-29 | New York City's official business chatbot advises owners to break the law | `hallucination` | 🟨 medium | 🔥 in the wild |
| [AP-0009](incidents/AP-0009-shadowray-ray-clusters-exploited.yaml) | 2024-03-26 | ShadowRay, attackers exploit exposed Ray AI clusters in the wild | `infra-vuln` | 🟥 critical | 🔥 in the wild |
| [AP-0008](incidents/AP-0008-hallucinated-package-huggingface-cli.yaml) | 2024-03 | Hallucinated "huggingface-cli" package gets thousands of real installs | `hallucination` `supply-chain` | 🟧 high | 🔥 in the wild |
| [AP-0007](incidents/AP-0007-air-canada-chatbot-refund-policy.yaml) | 2024-02-14 | Air Canada held liable for a refund policy its chatbot made up | `hallucination` | 🟨 medium | 🔥 in the wild |
| [AP-0006](incidents/AP-0006-dpd-chatbot-swears-at-customer.yaml) | 2024-01 | DPD's delivery chatbot swears at a customer and writes a poem about how bad DPD is | `prompt-injection` `model-behavior` | ⬜ low | 🔥 in the wild |
| [AP-0005](incidents/AP-0005-chevy-dealer-chatbot-one-dollar-tahoe.yaml) | 2023-12 | Dealership chatbot agrees to sell a 2024 Chevy Tahoe for $1, "no takesies backsies" | `prompt-injection` | ⬜ low | 🔥 in the wild |
| [AP-0004](incidents/AP-0004-mata-v-avianca-fake-cases.yaml) | 2023-06-22 | Lawyers sanctioned for filing ChatGPT-invented case law (Mata v. Avianca) | `hallucination` | 🟨 medium | 🔥 in the wild |
| [AP-0003](incidents/AP-0003-samsung-source-code-pasted-into-chatgpt.yaml) | 2023-05-02 | Samsung engineers paste confidential source code into ChatGPT; company bans generative AI | `data-exfiltration` | 🟨 medium | 🔥 in the wild |
| [AP-0002](incidents/AP-0002-chatgpt-redis-bug-leaks-chats.yaml) | 2023-03-20 | ChatGPT bug shows users other people's chat titles and some payment details | `isolation-failure` `infra-vuln` | 🟧 high | 🔥 in the wild |
| [AP-0001](incidents/AP-0001-bing-chat-system-prompt-leak.yaml) | 2023-02 | Bing Chat ("Sydney") reveals its hidden system prompt to a simple injection | `prompt-injection` | ⬜ low | 🔥 in the wild |
<!-- END:INCIDENTS -->

## Use the data

Every incident is a YAML file in [`incidents/`](incidents/) validated against
[`schema/incident.schema.json`](schema/incident.schema.json). The combined dataset is published at
[`docs/incidents.json`](docs/incidents.json):

```bash
curl -s https://hasnat23.github.io/agent-postmortems/incidents.json \
  | jq '[.[] | select(.classes | index("prompt-injection"))] | length'
```

Good uses: threat modeling an agent before launch, red-team test cases, security training, slide decks
that need a real example, and evaluating guardrail tools against real attack patterns.

## Contributing

Know an incident that's missing? Open an [issue](https://github.com/hasnat23/agent-postmortems/issues/new?template=new-incident.yml) with a link, or
send a PR with a new YAML file. The bar for inclusion:

- It happened to a real AI system (a product, an agent, an LLM feature), not a hypothetical.
- At least one public, credible source. Primary sources (vendor postmortems, researcher write-ups) preferred.
- Factual, neutral wording. Describe the failure, not the people.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the format. CI validates every entry and checks that every
source link still resolves.

## Related

- [AI Incident Database](https://incidentdatabase.ai/) covers AI harms broadly. This repo focuses on
  agents and LLM apps, with an engineering root cause and mitigation for every entry.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) is the risk list. These are the case studies.
- [mcp-warden](https://github.com/hasnat23/mcp-warden) is a security gateway for MCP that enforces several of the
  mitigations listed here (tool pinning, poisoning scans, secret redaction, audit logs).

## License

Incident data is licensed under [CC BY 4.0](LICENSE-DATA). Code (scripts, site) is [MIT](LICENSE).
Each entry summarizes and links to its original sources; credit for the research belongs to them.
