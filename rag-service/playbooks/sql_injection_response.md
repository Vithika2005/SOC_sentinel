# SQL Injection Response

## Trigger conditions
- AppSec scanner (e.g. Semgrep) flags a SQLi-vulnerable code path, or
- Runtime WAF/API gateway logs show a request payload matching known SQLi
  patterns (e.g. `' OR 1=1`, stacked queries, comment-based bypasses).

## Immediate containment
1. If runtime exploitation is suspected (not just a static-analysis finding),
   block the source IP at the WAF/reverse proxy immediately.
2. Check whether the vulnerable endpoint touches sensitive tables (auth,
   payment, PII). If so, treat as a potential data-exposure incident, not
   just a code-quality finding.
3. If the endpoint is actively being exploited, consider taking it offline
   or routing it through a stricter WAF rule until patched.

## Remediation
- Require parameterized queries / ORM usage (e.g. SQLAlchemy) instead of
  raw string-built SQL for the affected code path.
- Add or update a Semgrep rule so the same pattern is caught in CI before
  it reaches production again.

## Investigation
- Review application logs for the affected endpoint for any successful
  queries containing injection payloads, not just blocked/flagged ones.
- Check database audit logs (if enabled) for anomalous query patterns
  around the same time window.

## Escalation criteria
- Evidence of successful data exfiltration -> escalate to critical, treat
  as a confirmed breach, notify per your incident response / disclosure policy.

## Related references
OWASP A03:2021 (Injection), MITRE T1190 (Exploit Public-Facing Application)
