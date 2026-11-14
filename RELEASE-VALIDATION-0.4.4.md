# DaAT 0.4.4 — ChatGPT manual source-to-candidate loop validation

## Baseline and change scope

- Baseline: DaAT 0.4.3 from `DaAT_DaAT_Diag_UPDATE_DROP_C_MYCODE_2026-11-14.zip` (user conversation artifact).
- Scope: DaAT repository only (`C:\mycode\Interaction-Kernel\Daat`). No external owner repositories modified.
- New: operator-operated Tk `.pyw` launcher, offline ChatGPT prompt builder, strict citation-bound JSON response verifier, correction prompt and CLI.
- Sources: user-supplied text, summary, excerpt, bibliography metadata or locally authorized export. No scraping, account logins, network API or automatic sending.
- Output: pending-human-review **noncanonical candidate parts**. No Kit import, KQ/KP/KA/KS, publication, source-rights verification or custody.

## Executed validation in this environment

- `PYTHONPATH=src python -m pytest -q` — **209 tests passed**, including **34 new ChatGPT-loop tests** (count includes parametrized cases).
- `python tools/check_markdown_links.py` — **129 relative Markdown links validated**.
- `python tools/verify_manifest.py --write` and `python tools/verify_manifest.py` — source release manifest created and verified (local SHA-256 only).
- `PYTHONPATH=src python -m daat --help` — both new CLI commands available.
- `.pyw` files compiled successfully with `py_compile` (syntax/import check).
- CLI end-to-end synthetic test: explicitly gated input → offline prompt bundle → simulated model JSON → exact-citation checked draft; malicious/invalid cases rejected.

## Unexecuted / blocked

- Native Windows Tk GUI smoke test (not possible in this Linux container); run on user's Windows installation.
- Actual interactive ChatGPT dialogue; model compliance, citation factuality and semantic correctness unqualified.
- Authentication and source permissions for Medium, PhilPapers and other providers: outside DaAT, no browser automation.
- Owner semantic review, authorized IK transport, Kit receiver, canonical build and publication: blocked pending adopted contracts and owner testing.

## Security and privacy notes

- Separate explicit local user assertions are required for source use and for disclosure to ChatGPT.
- No credentials, browser cookies, local session access or background network calls in this feature.
- Prompt and saved bundle **contain source text**. Keep private; Windows ACL and encryption are controlled by the operator's environment. Local SHA-256 checks are not signatures or encryption.
- Source text is untrusted; model prompt injection cannot be eliminated by prompting. The verifier checks bounded JSON structure and exact citation existence; human reviewers must evaluate truth, rights, context and semantics.
