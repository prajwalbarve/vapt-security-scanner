# VAPT Security Scanner

**Python-based web and API security assessment prototype** exploring automated checks, evidence collection, and the distinction between scanner observations and manually confirmed vulnerabilities.

> **Project status:** Work in progress. This public repository contains early Python scanning scripts and separate prospect-discovery utilities. It does **not** currently contain the newer OWASP ZAP-powered scanner or a complete SQLi/XSS/IDOR testing suite. See [Current capabilities](#current-capabilities) and [Limitations](#limitations).

## Why I built this

Automated scanners are useful for discovering suspicious behavior, but an HTTP 200 response, a reflected payload, or a server error does not automatically prove a security vulnerability. I am building this project to practice web/API assessment workflows, improve detection quality, and document findings in a way that supports **reproducible manual verification**.

**Areas of interest:** web application security, API security, Python automation, OWASP testing methodology, evidence handling, and false-positive analysis.

## Current capabilities

The following checks are implemented in the **public scripts**; each result should be treated as a **candidate finding** until verified:

| Script | Checks implemented | Output |
| --- | --- | --- |
| `scripts/vapt_scanner_actual.py` | Requests for selected configuration paths; basic SQL error/HTTP 500 heuristics; reflected XSS payload checks; responses from selected unauthenticated API paths | `data/vapt_verified_vulnerabilities.json` |
| `scripts/vapt_vulnerability_scanner_strict.py` | Certificate-date inspection; HTTP HEAD requests for selected sensitive paths; checks of selected API paths; identification of publicly reachable admin login pages | `data/vapt_strict_findings.json` |

**Important:** Some early code and output fields use phrases such as “verified,” “critical,” or “100% confidence.” These are **scanner-assigned labels, not independently validated security conclusions**. A successful response, public login page, response keyword, or unencoded reflection is not by itself proof of an exploitable vulnerability.

### Other repository components

This repository also includes experimental prospect-discovery and lead-tracking scripts:

- `scripts/vapt_prospect_scraper.py` and `scripts/vapt_scraper_mumbai.py`: search-based discovery of company websites.
- `scripts/lead_sync_server.py`: a local lead-tracker API (requires Flask, which is **not** currently listed in `requirements.txt`).
- `docs/`: historical documentation for those prospect-discovery utilities.

**Discovering a company website does not authorize scanning it.** Do not treat the bundled lead lists as an approved testing scope.

## How the current prototype works

```text
Authorized test-scope data (JSON)
              |
              v
       Python scan script
              |
              +--> HTTP/HTTPS path and response checks
              +--> Simple injection/reflection indicators
              +--> API response checks
              +--> Optional OpenSSL certificate check (strict script)
              |
              v
       JSON candidate findings
              |
              v
   Manual validation and evidence review
              |
              v
    Confirmed / rejected / informational
```

## Getting started

**Requirements:** Python 3, pip, internet access to an **explicitly authorized** test environment, and OpenSSL in your PATH if using the strict scanner.

```bash
git clone https://github.com/prajwalbarve/vapt-security-scanner.git
cd vapt-security-scanner

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

The current scripts have **no `--target` or `--authorized` CLI option**. They read domain names from `data/vapt_qualified_leads.json` (up to 10 domains for the main scanner; up to 5 for the strict scanner).

Before running either script, **replace the bundled lead list with only assets you own or have written permission to test**. For example, edit `data/vapt_qualified_leads.json` to the following *placeholder* structure, substituting an actual authorized hostname:

```json
[
  {
    "domain": "your-authorized-staging-host.example"
  }
]
```

Then, from the repository root:

```bash
python3 scripts/vapt_scanner_actual.py
# Or run the alternative checks:
python3 scripts/vapt_vulnerability_scanner_strict.py
```

Inspect the resulting JSON in `data/`. Do not interpret the scanner's printed vulnerability counts as confirmed findings without independent verification. Running the scripts sends real HTTP requests; there is currently no rate-limit, scope-enforcement, or written-authorization gate in the code.

## How I evaluate findings

For each potential finding, a defensible verification record should contain:

1. **Scope and authorization:** hostname, test account/role (if applicable), and permitted testing window.
2. **Reproduction:** the exact request, relevant response details, steps, and applicable preconditions (with secrets removed).
3. **Baseline comparison:** expected normal behavior versus the suspicious behavior.
4. **Security impact:** what an unauthorized actor could actually do, established without accessing unrelated user data.
5. **Disposition:** confirmed vulnerability, potential finding requiring more testing, informational observation, or false positive.
6. **Remediation and retest:** an actionable fix and evidence that it resolves the issue.

Examples of checks requiring extra care:

- **SQL injection:** a generic HTTP 500 or the word “SQL” is not proof of injection.
- **XSS:** reflected text is not sufficient; execution and context require safe validation.
- **APIs:** a JSON response without credentials may be intentional if the endpoint serves public information.
- **Admin pages:** an accessible login form is not necessarily a vulnerability.
- **Sensitive paths:** status codes or sizes alone do not establish data exposure.

## Limitations

- No implemented IDOR/BOLA verification in this public snapshot.
- Limited hard-coded paths and input parameters; not comprehensive OWASP Top 10 coverage.
- No authenticated browser workflow, application-specific business-logic tests, or cross-user authorization comparisons.
- Basic error/keyword heuristics can cause both false positives and false negatives.
- The main scanner currently disables TLS certificate verification for several requests; this is **not suitable as a secure default**.
- The strict scanner's certificate-expiry logic is simplistic and should not be used as a reliable expiry assessment.
- Current scripts do not enforce authorized scope or provide rate limiting.
- There are no published automated test results or benchmarked detection metrics in this repository.

## Planned improvements

- Integrate the newer **OWASP ZAP-based scanning workflow** after code review, testing, and removal of sensitive artifacts.
- Add a target-input interface and explicit scope/authorization safeguards.
- Add authorized local test cases for SQLi, XSS, and IDOR/BOLA.
- Separate **candidate findings** from manually **confirmed vulnerabilities** in reports and console output.
- Capture redacted reproduction evidence, structured severity reasoning, and retest status.
- Introduce automated tests, versioned releases, and safer TLS/subprocess handling.

## Responsible use and disclosure

**Use this project only on systems you own or have explicit written authorization to assess.** Avoid disruptive testing and collecting personal or sensitive information. Do not publish credentials, production request bodies, internal endpoints, third-party finding details, or company data.

Some historical JSON files in `data/` contain references to third-party websites. They are **not evidence of testing authorization or confirmed vulnerability** and should be reviewed and sanitized before this project is used as a portfolio demonstration.

## Repository status

This README documents the code currently visible in the public repository, not private or local development versions. Project work is ongoing; technical claims and demonstrations will be updated as tested implementations are published.
