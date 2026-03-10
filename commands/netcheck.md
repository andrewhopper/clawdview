---
uuid: cmd-netcheck-4h5i6j7k
version: 1.0.0
last_updated: 2025-11-13
description: Network diagnostics with DNS, ping, traceroute, ports, SSL, HTTP checks
---

# Network Diagnostics (netcheck)

Comprehensive network troubleshooting tool. Run whenever something can't be accessed or network issues suspected.

## Usage

```bash
# Check a hostname
/netcheck example.com

# Check a URL
/netcheck https://example.com

# Check an IP
/netcheck 8.8.8.8
```

## What It Checks

✅ DNS resolution (nameserver, records, TTL)
✅ IP address with ping statistics
✅ Compressed traceroute
✅ Port connectivity for 22 (SSH), 80 (HTTP), 443 (HTTPS)
✅ SSL/TLS negotiation and certificate
✅ HTTP response codes

---

## Instructions

### Run Python Script

Execute the netcheck.py Python script which performs all diagnostics in a single process (avoids multiple ACL requests):

```bash
TARGET="${1:?Usage: /netcheck <hostname|url>}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/prototypes/proto-015-claude-power-tools/scripts"

# Run Python diagnostics script
python3 "${SCRIPT_DIR}/netcheck.py" "$TARGET"
```

The Python script will:
1. Parse the target (hostname/URL/IP)
2. Run DNS resolution
3. Ping the primary IP
4. Traceroute to target
5. Check ports 22, 80, 443
6. Verify SSL certificate (if 443 open)
7. Test HTTP response
8. Generate formatted markdown report

---

## Network Diagnostics Report Format

```markdown
# Network Diagnostics Report

**Target**: {hostname}
**Analyzed**: {timestamp}

---

## DNS Resolution

**Status**: {✅/❌}
**Hostname**: {hostname}
**Nameserver**: {nameserver from /etc/resolv.conf}

**DNS Records**:
```bash
# Run dig or host command
dig +short {hostname}
# Or fallback to host command
host {hostname}
```

**Result**: {IP addresses}
**TTL**: {TTL value from dig +ttlid}

{If failed: ❌ DNS resolution failed}
{If success: ✅ Resolved to {IP}}

---

## Ping Test

**Status**: {✅/❌}
**Target IP**: {primary_ip}

```bash
# Run ping
ping -c 4 {ip}
```

**Results**:
- Packets: {received}/{sent} received
- Packet Loss: {percentage}%
- Latency: min={min}ms / avg={avg}ms / max={max}ms

{If failed: ❌ No response}
{If success: ✅ Reachable (avg={avg}ms)}

---

## Traceroute (Compressed)

**Status**: {✅/⚠️/❌}
**Total Hops**: {count}

```bash
# Run traceroute with max 15 hops
traceroute -m 15 {hostname}
```

**Key Hops** (first 3 and last 3):

| Hop | Host | IP | Time |
|-----|------|----|------|
| 1 | gateway | 192.168.1.1 | 1.2ms |
| 2 | isp-router | 10.x.x.x | 15ms |
| 3 | ... | ... | ... |
| ... | ... | ... | ... |
| 13 | cdn-edge | x.x.x.x | 45ms |
| 14 | server | x.x.x.x | 48ms |
| 15 | {hostname} | {ip} | 50ms |

{If failed: ❌ Route unavailable}
{If success: ✅ Route established ({hops} hops)}

---

## Port Connectivity

**Status**: Check TCP connectivity

| Port | Service | Status | Open | Response Time | Notes |
|------|---------|--------|------|---------------|-------|
| 22 | SSH | {✅/❌} | {Yes/No} | {ms}ms | {Connection result} |
| 80 | HTTP | {✅/❌} | {Yes/No} | {ms}ms | {Connection result} |
| 443 | HTTPS | {✅/❌} | {Yes/No} | {ms}ms | {Connection result} |

**Port check commands**:
```bash
# Check port 22 (SSH)
timeout 5 bash -c "</dev/tcp/{ip}/22" 2>/dev/null && echo "✅ Port 22 open" || echo "❌ Port 22 closed"

# Check port 80 (HTTP)
timeout 5 bash -c "</dev/tcp/{ip}/80" 2>/dev/null && echo "✅ Port 80 open" || echo "❌ Port 80 closed"

# Check port 443 (HTTPS)
timeout 5 bash -c "</dev/tcp/{ip}/443" 2>/dev/null && echo "✅ Port 443 open" || echo "❌ Port 443 closed"

# Or use nc if available
nc -zv -w 3 {ip} 22 80 443
```

---

## SSL/TLS Certificate

{Only if port 443 is open}

**Status**: {✅/❌}

```bash
# Check SSL certificate
echo | openssl s_client -connect {hostname}:443 -servername {hostname} 2>/dev/null | openssl x509 -noout -text
```

**TLS Version**: {version from openssl output}
**Cipher Suite**: {cipher from openssl output}

**Certificate Details**:
- Issuer: {issuer organization}
- Subject: {common name}
- Valid From: {notBefore date}
- Valid Until: {notAfter date}
- SAN (Subject Alt Names): {DNS names}

**Certificate Check**:
```bash
# Get certificate expiry
echo | openssl s_client -connect {hostname}:443 -servername {hostname} 2>/dev/null | openssl x509 -noout -dates

# Verify certificate
echo | openssl s_client -connect {hostname}:443 -servername {hostname} 2>/dev/null | grep -E "Verify return code"
```

{If valid: ✅ Certificate valid}
{If expired/invalid: ❌ Certificate issue: {error}}

---

## HTTP Response

**Status**: {✅/⚠️/❌}

```bash
# Check HTTP response (follow redirects)
curl -sL -w "\nHTTP_CODE:%{http_code}\nTIME_TOTAL:%{time_total}\nCONTENT_TYPE:%{content_type}\n" \
  -o /dev/null \
  https://{hostname}

# Or detailed with headers
curl -sI https://{hostname}
```

**HTTP Status**: {status_code} {status_text}
- ✅ 2xx: Success
- ⚠️ 3xx: Redirect
- ❌ 4xx: Client error
- ❌ 5xx: Server error

**Response Details**:
- Response Time: {time_total}ms
- Content-Type: {content_type}
- Server: {server header}

**Redirects** (if any):
- 301: {url1} → {url2}
- 302: {url2} → {url3}

{If failed: ❌ HTTP request failed: {error}}
{If success: ✅ HTTP {code} ({time}ms)}

---

## Summary

| Check | Status | Details |
|-------|--------|---------|
| DNS Resolution | {✅/❌} | {IP or error} |
| Ping | {✅/❌} | {avg latency or failure} |
| Traceroute | {✅/⚠️/❌} | {hops or issue} |
| SSH (22) | {✅/❌} | {open/closed} |
| HTTP (80) | {✅/❌} | {open/closed} |
| HTTPS (443) | {✅/❌} | {open/closed} |
| SSL/TLS | {✅/❌} | {valid or error} |
| HTTP Response | {✅/⚠️/❌} | {status code} |

**Overall Status**: {✅ All checks passed / ⚠️ Some issues / ❌ Major issues}

---

## Common Issues Detected

{Analyze results and provide diagnostics}

**DNS Issues**:
- ❌ DNS resolution failed → Check nameserver, try 8.8.8.8
- ⚠️ High TTL → DNS changes take longer to propagate

**Connectivity Issues**:
- ❌ 100% packet loss → Host unreachable, check routing
- ⚠️ High latency (>100ms) → Network congestion or distant server
- ❌ Traceroute timeout → Firewall blocking ICMP

**Port Issues**:
- ❌ Port 443 closed → HTTPS not available, check firewall
- ❌ Port 80 closed → HTTP not available
- ❌ Port 22 closed → SSH access blocked

**SSL Issues**:
- ❌ Certificate expired → Renew certificate
- ❌ Certificate name mismatch → Check SAN includes hostname
- ❌ Self-signed certificate → Not trusted by browsers

**HTTP Issues**:
- ❌ 404 Not Found → Resource doesn't exist
- ❌ 500 Server Error → Application error
- ❌ Connection refused → Service not running
- ⚠️ Too many redirects → Redirect loop

---

## Recommended Actions

Based on failures, provide specific fixes:

**If DNS fails**:
```bash
# Test with Google DNS
dig @8.8.8.8 {hostname}

# Check /etc/hosts for conflicts
grep {hostname} /etc/hosts
```

**If ping fails but DNS works**:
```bash
# Check if ICMP is blocked (try TCP ping)
timeout 3 bash -c "</dev/tcp/{ip}/443"

# Check routing
ip route get {ip}
```

**If SSL fails**:
```bash
# Test SSL manually
openssl s_client -connect {hostname}:443 -servername {hostname}

# Check certificate chain
curl -vI https://{hostname}
```

**If HTTP fails**:
```bash
# Test with curl verbose
curl -v https://{hostname}

# Check specific HTTP method
curl -X GET -I https://{hostname}
```

---

*Generated by netcheck v1.0.0*
```

---

## Implementation Notes

**Tools Used**:
- `dig` or `host` - DNS resolution
- `ping` - ICMP connectivity
- `traceroute` - Route tracing
- `bash` `/dev/tcp` - Port checking
- `nc` (netcat) - Alternative port checking
- `openssl s_client` - SSL/TLS verification
- `curl` - HTTP testing

**Fallbacks**:
- If `dig` unavailable → use `host`
- If `traceroute` unavailable → use `tracepath`
- If `nc` unavailable → use `bash /dev/tcp`

**Error Handling**:
- Timeout all commands (5-10s max)
- Continue on partial failures
- Mark unavailable checks as ⚠️
- Provide actionable error messages

---

## Step-by-Step Execution

1. **Extract hostname** from target
2. **DNS check**: `dig +short {hostname}`
3. **Get primary IP** from DNS result
4. **Ping test**: `ping -c 4 {ip}`
5. **Traceroute**: `traceroute -m 15 {hostname}` (compress output)
6. **Port checks**: Test 22, 80, 443 using `/dev/tcp` or `nc`
7. **SSL check**: `openssl s_client` if 443 open
8. **HTTP check**: `curl -sL -w` for status and timing
9. **Format report** with all results
10. **Provide diagnostics** based on failures

---

## Example Outputs

**Healthy site**:
```
All checks: ✅
DNS: ✅ example.com → 93.184.216.34
Ping: ✅ 15ms avg
Ports: ✅ 80, 443 open
SSL: ✅ Valid (expires 2025-12-01)
HTTP: ✅ 200 OK (250ms)
```

**DNS failure**:
```
DNS: ❌ NXDOMAIN - domain doesn't exist
→ Check domain spelling
→ Try: dig @8.8.8.8 example.com
```

**Port blocked**:
```
Port 443: ❌ Connection timeout
→ Firewall blocking HTTPS
→ Check security group rules
```

**SSL issue**:
```
SSL: ❌ Certificate expired (2025-01-15)
→ Renew certificate with Let's Encrypt
→ certbot renew
```

Run all checks, present comprehensive report, use emojis for status, provide actionable fixes.
