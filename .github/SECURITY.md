# Security Policy for CopyrightScan-Delisting-Analysis-Python-Project

As an Apex Authority project, security is treated as a non-negotiable, first-class citizen, adhering to the **Zero-Defect** mandate. This repository strictly follows modern Python security practices using the **uv**, **Ruff**, and **Pytest** toolchains, integrating security scanning into the CI/CD pipeline defined in `.github/workflows/ci.yml`.

## 1. Supported Versions

We actively support and maintain security updates for the primary branch (main) targeting **Python 3.11 and 3.12**.

Security patches are prioritized immediately for the latest stable release.

## 2. Reporting a Vulnerability

We greatly appreciate the diligence of security researchers. To report a potential vulnerability in this repository, please follow the structured process outlined below, respecting the **Responsible Disclosure** principle.

1.  **DO NOT** file a public Issue or Pull Request detailing the vulnerability.
2.  Use the designated **Private Channel** or report directly via the GitHub Security Advisory system.
3.  If you must use GitHub features, open a **private security disclosure** report (if available to your account type).
4.  Alternatively, email the primary maintainer: `chirag127@users.noreply.github.com` (please include `[SECURITY]` in the subject).

### Disclosure Timeline

We commit to the following timeline upon receiving a valid report:

| Stage | Target Response Time |
| :--- | :--- |
| Acknowledgment | Within 24 hours |
| Triage & Confirmation | Within 72 hours |
| Patch Development | Dependent on Severity (See Below) |
| Public Disclosure | Coordinated with the reporter, typically 7 days post-patch deployment |

## 3. Security Practices & Automated Scanning

To ensure integrity, the following automated security measures are enforced in our Continuous Integration process (`.github/workflows/ci.yml`):

*   **Dependency Scanning:** We utilize tools integrated via **uv** to check for known CVEs in declared dependencies (`requirements.txt` or equivalent). This runs on every push.
*   **Static Analysis (SAST):** **Ruff** is configured with security-focused rules (`q` prefix) to detect potential vulnerabilities, unsafe code patterns, and secrets exposure before merging.
*   **Secret Scanning:** GitHub's native Secret Scanning is enabled and configured to block commits containing hardcoded credentials or API keys.

## 4. Vulnerability Severity Matrix

Severity dictates the urgency of patching and disclosure.

| Severity | Description | Remediation SLA (Internal) |
| :--- | :--- | :--- |
| **Critical** | Remote Code Execution (RCE), full data compromise, dependency chain leading to RCE. | Immediate Hotfix (Within 12 hours) |
| **High** | Sensitive data exposure (non-RCE), unauthorized access to system functionality. | Within 3 Days |
| **Medium** | Denial of Service (DoS) vectors, logic flaws impacting analysis integrity. | Within 7 Days |
| **Low** | Informational findings, minor input validation issues without immediate exploit path. | Next Scheduled Release Cycle |

## 5. Dependencies and Third-Party Code

We rigorously adhere to the principles outlined in our customized **AGENTS.md** regarding external dependencies:

*   Only dependencies available via PyPI and managed by **uv** are permitted.
*   Any external dependency must be reviewed against current licensing requirements (**CC BY-NC 4.0** for this project).
*   Dependencies imported must not violate the DRY/YAGNI principles by duplicating existing functionality.

By using this project, you agree to treat any discovered vulnerabilities with the same level of professional disclosure.