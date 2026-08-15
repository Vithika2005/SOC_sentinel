# Brute Force / Credential Stuffing Response

## Trigger conditions
- Repeated failed login attempts against the same account or from the same
  source IP within a short window (SentinelX default: 5+ failures in 10 minutes).
- Failed attempts spread across many accounts from a single source IP
  (credential stuffing pattern) rather than one account being targeted.

## Immediate containment
1. Rate-limit or temporarily block the source IP at the reverse proxy (nginx) / WAF.
2. If a specific account is targeted, force a password reset and invalidate
   existing sessions for that account.
3. If MFA is not already enforced for the affected account, require it before
   the account can be used again.

## Investigation
- Pull auth-service logs for the affected account/IP over the preceding 24h.
- Check whether any attempt succeeded (a successful login mixed in with
  failures is a much higher-severity finding than failures alone).
- Cross-reference the source IP against known malicious-IP threat feeds.

## Escalation criteria
- Any successful login following a failure streak -> escalate to critical,
  treat as a probable account compromise, not just an attempted one.
- Attempts distributed across 10+ accounts from one IP -> likely automated
  credential stuffing, escalate for infrastructure-level blocking, not just
  per-account remediation.

## Related MITRE technique
T1110 (Brute Force)
