# CE Security Hardening Checklist

- Status: Implementation Guidance
- Edition: CE
- Priority: High
- Audience: CE owners, operators, security reviewers, AI coding agents

Use this checklist before exposing Opstage CE outside a local development machine.

---

## 1. Required Secrets

- [ ] `OPSTAGE_SESSION_SECRET` is random and at least 32 characters.
- [ ] `OPSTAGE_ADMIN_PASSWORD` is changed from examples/placeholders and is at least 12 characters.
- [ ] `.env` is not committed to git.
- [ ] Agent token files are not committed to git.
- [ ] SQLite backups are not committed to git.

---

## 2. HTTPS and Reverse Proxy

- [ ] CE is served behind HTTPS.
- [ ] Reverse proxy preserves `Set-Cookie`.
- [ ] Reverse proxy forwards `X-CSRF-Token`.
- [ ] `OPSTAGE_PUBLIC_BASE_URL` is set to the canonical HTTPS URL when exposed.
- [ ] Secure cookies are enabled when served over HTTPS.

---

## 3. User and Role Management

- [ ] At least two active `owner` users exist for break-glass access.
- [ ] Daily operators use `operator`, not `owner`.
- [ ] Auditors and stakeholders use `viewer`.
- [ ] Disabled users are reviewed periodically.
- [ ] Password reset flow is documented for owners.

---

## 4. Agent Registration and Tokens

- [ ] Registration tokens are short-lived or revoked after use.
- [ ] Raw registration token is copied once and stored securely only when needed.
- [ ] Unused registration tokens are revoked.
- [ ] Revoked/disabled Agents are reviewed periodically.
- [ ] Agent token files have restrictive filesystem permissions.
- [ ] Re-registration process is documented for Agent hosts.

---

## 5. Actions and Commands

- [ ] Destructive actions require confirmation.
- [ ] Action payloads and CommandResults do not expose raw secrets.
- [ ] Large logs/artifacts are not returned inline as CommandResult data.
- [ ] `OPSTAGE_COMMAND_RESULT_MAX_BYTES` is configured appropriately.
- [ ] Operators know how to inspect prepare diagnostics and command failures.

---

## 6. Audit, Metrics, and Diagnostics

- [ ] Audit retention is configured with `OPSTAGE_AUDIT_RETENTION_DAYS`.
- [ ] Audit exports are protected and stored securely.
- [ ] Runtime diagnostics are not exposed without authentication.
- [ ] Metrics are reviewed during incident response.
- [ ] System clocks are synchronized on CE and Agent hosts.

---

## 7. Backups

- [ ] SQLite backups are created regularly.
- [ ] Backups are stored outside the CE host.
- [ ] Backups are encrypted if they contain sensitive operational metadata.
- [ ] Restore has been tested in a disposable environment.
- [ ] Backup retention matches compliance requirements.

---

## 8. Network Exposure

- [ ] CE admin UI is not exposed directly to the public internet unless required.
- [ ] Firewall/security groups restrict access to trusted networks.
- [ ] Agent-to-Backend network path is documented.
- [ ] Cross-network Agent access uses TLS and stable DNS or a controlled tunnel.
