# Failure taxonomy

Each incident has one or more classes. They describe **how** the failure happened, so one incident
often has several (a prompt injection that leads to data exfiltration is both).

| Class | Meaning |
|---|---|
| <a id="destructive-action"></a>`destructive-action` | The agent deleted, overwrote or modified something it should not have, such as files, databases, emails or infrastructure. |
| <a id="excessive-agency"></a>`excessive-agency` | The agent held more permissions, tools or autonomy than the task needed, which turned a mistake or an attack into real damage (OWASP LLM06). |
| <a id="prompt-injection"></a>`prompt-injection` | Instructions from untrusted content (web pages, issues, emails, forms, logs) or from a user overrode the intended behavior. |
| <a id="tool-poisoning"></a>`tool-poisoning` | Malicious or changed tool metadata (MCP tool descriptions, server configs) steered the model, or a tool server itself was malicious. |
| <a id="data-exfiltration"></a>`data-exfiltration` | Private data left its trust boundary, through a tool call, a rendered link or image, a comment, or a third-party service. |
| <a id="supply-chain"></a>`supply-chain` | A compromised or malicious package, extension, rules file or release reached users of an AI tool, or AI tooling was the target of the payload. |
| <a id="hallucination"></a>`hallucination` | Fabricated facts, policies, citations or package names were acted on, with real consequences. |
| <a id="unsafe-output-handling"></a>`unsafe-output-handling` | Model output was rendered, fetched or executed without validation, such as markdown images to arbitrary URLs or `exec()` on generated code (OWASP LLM05). |
| <a id="memory-poisoning"></a>`memory-poisoning` | Untrusted content wrote to the assistant's persistent memory and affected later sessions. |
| <a id="isolation-failure"></a>`isolation-failure` | Data crossed tenant or user boundaries because of a bug in the AI feature or its infrastructure. |
| <a id="sandbox-escape"></a>`sandbox-escape` | An agent reached systems outside the environment it was meant to be confined to. |
| <a id="infra-vuln"></a>`infra-vuln` | A classic software vulnerability (RCE, missing auth, default credentials) in AI tooling or infrastructure. |
| <a id="model-behavior"></a>`model-behavior` | A model or prompt update changed behavior in a harmful way, such as sycophancy or abusive replies. |
| <a id="misuse"></a>`misuse` | Attackers deliberately used AI agents as a tool to attack others. |

## Severity

- **critical**: large-scale data exposure, remote code execution, or irreversible loss of production data.
- **high**: sensitive data exposed or high-impact actions possible, for a meaningful group of users.
- **medium**: limited exposure, or real financial, legal or reputational cost.
- **low**: embarrassing or noisy, with little lasting harm.

## Status

- **in-the-wild**: real users, systems or organizations were harmed or exposed.
- **research**: demonstrated by researchers and disclosed, usually patched, with no confirmed victims.
