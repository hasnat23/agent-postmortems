# Contributing

Thanks for helping. Every incident makes the next agent a bit safer.

## Quick path: open an issue

Use the [new incident form](https://github.com/hasnat23/agent-postmortems/issues/new?template=new-incident.yml) with a link to a source. A maintainer
will write the entry.

## Full path: send a pull request

1. Copy any file in [`incidents/`](incidents/) to `incidents/AP-XXXX-short-slug.yaml`, where `XXXX` is the
   next free number.
2. Fill in every field. The schema is in [`schema/incident.schema.json`](schema/incident.schema.json) and the
   classes are explained in [TAXONOMY.md](TAXONOMY.md).
3. Regenerate the README table and dataset, then commit everything:

   ```bash
   pip install -r requirements.txt
   python scripts/build.py
   ```

CI runs `python scripts/build.py --check` and checks that every source URL resolves.

## Inclusion bar

- **Real system.** A product, agent, LLM feature or AI infrastructure that real people used. No hypotheticals.
- **Public source.** At least one credible, public link. Prefer the primary source (vendor postmortem,
  advisory, researcher write-up), and add a news article as a second source when there is one.
- **Engineering lesson.** The root cause and mitigations should be concrete enough that an engineer could
  act on them.

## Writing style

- Neutral and factual. Describe what the system did, not how foolish anyone was.
- Don't name private individuals unless they published the incident themselves.
- Use the public disclosure date. Use `YYYY-MM` when the exact day isn't clear.
- Keep the summary to a few sentences, and put every number you state in at least one source.

## Corrections

If an entry is wrong or a vendor has published new details, open an issue or PR with the source. Corrections
are always welcome.
