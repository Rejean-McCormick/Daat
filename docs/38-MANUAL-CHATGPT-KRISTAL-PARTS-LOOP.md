# 38 — Operator-mediated ChatGPT loop for source-grounded Kristal *candidates* (DaAT 0.4.4)

**Status: `[TESTED]` offline local prototype, not canonical admission.** This pathway is an **optional user-operated interpretation aid**, not source scraping, a ChatGPT API integration, an approved IK Profile, a Kit receiver, a rights verifier or a semantic recognition authority. It follows the existing DaAT owner-boundary constraints; see `docs/29-PROCESS-AND-HANDOFFS.md` and `AGENTS.md`.

## Why this exists

Medium, PhilPapers, journals, websites, archives and private databases offer different levels of access. An AI may see only public metadata or a short abstract rather than the article itself. DaAT must not pretend that an article was read based on a search result or a guessed URL. Users may legitimately access material through their **own authenticated browser session**, export a permitted representation, or supply a short quotation or summary. DaAT receives only that **explicitly provided** material. Authentication to a provider is handled by the provider/browser; **DaAT never asks for usernames, passwords, cookies or session tokens**.

## Manual loop

1. User reads/accesses source in an ordinary browser or authorized export. For Medium, the user signs into Medium *in the browser*, then copies authorized content to the DaAT interface. For PhilPapers, the user may paste bibliography/abstract metadata; **a bibliographic entry is not the referenced article**.
2. User selects `metadata`, `summary`, `excerpt` or `full_text` based on the material **actually provided**, not what exists somewhere on the Web. Add provider, title, optional URL without credentials, access method and rights/terms declaration. The operator separately acknowledges **lawful use** and **permission to disclose to ChatGPT**. Being logged in is **not** automatic permission to transmit a text to a third-party model.
3. DaAT generates a local prompt containing the supplied text, declared visibility and content digests. A human checks and pastes it into ChatGPT. No network request is made by DaAT.
4. ChatGPT responds with JSON of untrusted possible Kristal *parts* (`claim`, `concept`, `relation_hypothesis`, `question`), each with exact verbatim source excerpts and explicit uncertainties. It may return `unknowns` only.
5. User pastes the JSON into DaAT. DaAT validates **exact citation membership**, source references, hashes, allowed keys, size bounds, and absence of authority fields. It returns a **local draft for human review**, never a Kit import, semantic KQ/KP/KA/KS or canonical Kristal.
6. A qualified downstream review/Kit owner might one day transform approved suggestions to canonical knowledge via an **independently adopted, versioned contract and security flow**. That receiver is NOT implemented here.

### Data flow

```
Source on website / file / app (outside DaAT)
       |
       +--> login in normal browser, if required (never share session)
       |
       v
User-pasted summary/excerpt/full text/authorized export
       |
       v
DaAT offline prompt generator [source scope + provenance + local SHA]
       |                            no automatic transmission
       +--> human reviews and pastes to ChatGPT
                                  |
                        ChatGPT candidate JSON
                                  |
       +<-- human pastes JSON back to DaAT
       |
       v
Strict citation/format verifier (not factual truth verification)
       |
       v
Noncanonical candidate-parts JSON --> human review --> owner-gated future Kit adapter
```

## Windows launch

Double-click `C:\mycode\Interaction-Kernel\Daat\LANCER_DAAT_CHATGPT_LOOP.pyw` with Python/Tkinter installed. This is a native Tk GUI (`.pyw`) and does not open CMD. Workflow: **Sources** tab → **Créer le prompt** → **Copier le prompt** → paste into ChatGPT → copy JSON answer → **Vérifier le JSON** → **Exporter le brouillon privé**. Optionally save/reopen a prompt bundle for later verification. If the response is invalid, use **Prompt de correction** to generate another operator-copied attempt. The app does not persist content unless the user explicitly chooses to save, but the OS clipboard and the ChatGPT conversation may retain copied text. Local file protections on Windows depend on user ACLs and disk encryption; local hashes do not encrypt saved sources. Handle these according to the applicable privacy policy.

## Command line / testing

A synthetic, legally unencumbered sample is provided at `examples/chatgpt_loop_synthetic_input.json` (not a real Medium article or PhilPapers record). `input.json` contains exactly `{"purpose":"...", "sources":[...]}`. Each source contains exactly `provider`, `title`, `locator` (empty allowed), `scope`, `access_method`, `rights_basis`, `text`. Valid scopes: `metadata`, `summary`, `excerpt`, `full_text`. Valid methods: `user_paste`, `manual_browser_copy`, `authorized_export`.

```powershell
py -m daat chatgpt-build-prompt input.json --rights-acknowledged --allow-chatgpt-sharing --out private-prompt-bundle.json
# Manually paste the prompt from the JSON bundle into ChatGPT; save the raw JSON response to answer.json
py -m daat chatgpt-verify-response --bundle private-prompt-bundle.json --response answer.json --out private-draft.json
```

Run CLI from an installed `daat` environment or set `PYTHONPATH=src` from the repository root. The commands never print source contents to the console. They write private files only if requested and refuse replacing an existing output unless `--replace` is explicit.

## Truth and authority boundaries

- A quote is verified for **exact presence in supplied text**, not actual authorship, originality, truth or sufficiency to support the claim. A false interpretation of a true quote can pass this limited check; a human reviewer must inspect it.
- Source digests are **local, untrusted checksums, not publisher signatures**. Rights and scope remain user assertions.
- Summary/excerpt/metadata cannot prove contents of unseen pages. The validator marks each reference as `limited_to_supplied_material`; no fetching is performed to fill gaps.
- Prompt injection through source text is mitigated by explicit instructions and separation, **not prevented by a security sandbox in ChatGPT**. The response is always subjected to deterministic validation.
- Avoid uploading sensitive, proprietary, paywalled or identifiable information without permission for **third-party model processing**, even if you personally may read it.
- No external API tokens, scraping agents, password storage, source-hoster writes, local canonical Kit build, owner release or automatic publishing.
- Up to 6 source chunks per prompt, max 40,000 characters per chunk, 90,000 characters overall, 30 candidate parts and 4 direct excerpts per part. Split longer works into deliberate, independently reviewed batches.
- The tool is general across all source families for which the **user can lawfully provide material**. That does not mean it implements 36 source-specific live connectors.

## Tests and known unqualified paths

`tests/test_chatgpt_loop.py` tests normal operation, summary-only scope, two-source references, corrupted digests, forged citations, injection of authority, extra fields, incorrect IDs, rights/disclosure refusal, duplicate/oversized inputs and CLI round trip. GUI source/response functionality is implemented with Tk; a real interactive Windows smoke test is still required. No actual ChatGPT, Medium, PhilPapers or Kit calls are performed by these tests.

`[BLOCKED]`: owner-adopted receiver profile, real semantic review, rights verification, source custody, authenticated publishing, source-specific retrieval and production controls remain separate milestones.
