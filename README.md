# DevSecOps Security Scanning Workflows

This repository contains GitHub Actions workflows for automated security scanning using industry-standard tools: Semgrep, Trivy, and Gitleaks. Results are uploaded to DefectDojo for centralized vulnerability management.

## 🔒 Security Scanners

### 1. Semgrep - Static Application Security Testing (SAST)
- **Purpose**: Identifies security vulnerabilities, bugs, and anti-patterns in source code
- **Coverage**: OWASP Top 10, CWE Top 25, secrets detection, security audit rules
- **Output**: SARIF format uploaded to DefectDojo

### 2. Trivy - Vulnerability Scanner
- **Purpose**: Scans for known vulnerabilities in dependencies, container images, and infrastructure
- **Coverage**: CVE database, security misconfigurations, secrets
- **Output**: SARIF format uploaded to DefectDojo

### 3. Gitleaks - Secret Detection
- **Purpose**: Prevents secrets and sensitive information from being committed to the repository
- **Coverage**: API keys, passwords, tokens, certificates, and other credentials
- **Output**: SARIF format uploaded to DefectDojo

## 🚀 Available Workflows

### Individual Scanners
- `.github/workflows/semgrep.yml` - Semgrep security scanning
- `.github/workflows/trivy.yml` - Trivy vulnerability scanning  
- `.github/workflows/gitleaks.yml` - Gitleaks secret scanning

### Combined Scanner
- `.github/workflows/security-scan.yml` - Runs all three scanners in parallel with matrix strategy

## ⚡ Workflow Triggers

All workflows are triggered by:
- **Push** to `main` and `develop` branches
- **Pull Requests** to `main` and `develop` branches
- **Repository rulesets** (via `repository_dispatch` events)
- **Manual dispatch** (combined workflow supports selective scanner execution)

## 🔧 Configuration Files

### Exclusion Patterns
- `.semgrepignore` - Semgrep exclusion patterns
- `.trivyignore` - Trivy exclusion patterns
- `.gitleaks.toml` - Gitleaks configuration with allowlist patterns

### Common Exclusions
All scanners exclude:
- Vendor directories (`vendor/`, `vendors/`, `node_modules/`)
- Build artifacts (`dist/`, `build/`, `target/`, `bin/`)
- Test files and directories
- Documentation files
- Lock files and generated content
- Media and binary files
- IDE and OS files

## 🎯 Severity-Based Failure Policy

### Workflow Failure Conditions
- **Semgrep**: High or Critical security findings
- **Trivy**: High (CVSS 8.0+) or Critical (CVSS 10.0) vulnerabilities
- **Gitleaks**: Any detected secrets (all findings are considered critical)

### DefectDojo Integration
All scanners output results in SARIF (Static Analysis Results Interchange Format) which:
- Uploads automatically to DefectDojo via REST API
- Provides centralized vulnerability management
- Enables tracking and remediation workflows  
- Supports engagement and product management

## 📊 Pull Request Integration

### Automated Comments
Each workflow automatically comments on pull requests with:
- Summary of findings by severity
- Pass/fail status for each scanner
- Links to detailed results in DefectDojo
- Action items for remediation

### DefectDojo Upload Integration
Results are automatically uploaded to DefectDojo with:
- Engagement and product organization
- Test categorization by scanner type
- Automated tagging and metadata
- Configurable finding closure policies

## 🛠️ Setup Instructions

### 1. Repository Secrets (Required)
```bash
# DefectDojo integration (required)
DEFECTDOJO_URL=https://c9d0c1530abe.ngrok-free.app
DEFECTDOJO_TOKEN=d5ebd60db81a7f286e5953a95deafc4bf7c7459c

# For enhanced Semgrep features (optional)
SEMGREP_APP_TOKEN=your_semgrep_token
```

### 2. Required Permissions
Ensure your repository has these permissions enabled:
- Actions: Read
- Contents: Read  
- Pull requests: Write (for comments)

### 3. Branch Protection (Recommended)
Configure branch protection rules to:
- Require status checks to pass
- Include security scan workflows as required checks
- Prevent merging with high/critical findings

## 🔄 Workflow Execution

### Manual Execution
```bash
# Run all scanners
gh workflow run security-scan.yml

# Run specific scanner
gh workflow run security-scan.yml -f scan_type=semgrep
gh workflow run security-scan.yml -f scan_type=trivy  
gh workflow run security-scan.yml -f scan_type=gitleaks
```

### Repository Ruleset Triggers
```bash
# Trigger via repository dispatch (for rulesets)
gh api repos/{owner}/{repo}/dispatches \
  --method POST \
  --field event_type=security-scan

# Trigger specific scanner
gh api repos/{owner}/{repo}/dispatches \
  --method POST \
  --field event_type=semgrep-scan
```

### Monitoring Results
1. **GitHub Actions Tab**: View workflow execution logs
2. **DefectDojo Dashboard**: Review detailed findings and manage vulnerabilities
3. **Pull Request Comments**: Quick summary and status
4. **Artifacts**: Download detailed reports (30-day retention)

## 📈 Best Practices

### For Developers
1. **Run locally** before pushing:
   ```bash
   # Semgrep
   semgrep scan /src --dataflow-traces --config=auto
   
   # Trivy  
   trivy fs /src --scanners vuln --format sarif
   
   # Gitleaks
   gitleaks dir /src --config .gitleaks.toml
   ```

2. **Address findings promptly**: High/critical issues block merges
3. **Review exclusions**: Ensure they're justified and documented
4. **Keep dependencies updated**: Reduces vulnerability exposure

### For Security Teams
1. **Monitor DefectDojo dashboard** regularly for trends and metrics
2. **Review and update** exclusion patterns periodically
3. **Customize rule sets** based on your tech stack
4. **Set up DefectDojo notifications** for critical findings
5. **Integrate with SIEM/SOAR** tools using DefectDojo APIs
6. **Configure engagement workflows** for proper vulnerability lifecycle management

## 🚨 Troubleshooting

### Common Issues
1. **False Positives**: Add patterns to respective ignore files
2. **Performance**: Adjust exclusion patterns for large repositories
3. **Token Issues**: Verify GITHUB_TOKEN permissions and DefectDojo API token
4. **DefectDojo Upload Failures**: Check API endpoint, authentication, and SARIF format
5. **Product/Engagement Creation**: Ensure DefectDojo has proper product configuration

### Debug Mode
Enable debug logging by setting:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

## 📚 Additional Resources

- [Semgrep Documentation](https://semgrep.dev/docs/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [DefectDojo Documentation](https://defectdojo.github.io/django-DefectDojo/)
- [DefectDojo API Documentation](https://demo.defectdojo.org/api/v2/doc/)
- [GitHub Repository Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets)
- [SARIF Specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)

---

🔐 **Security is everyone's responsibility** - These workflows provide automated guardrails, but secure coding practices and regular security reviews remain essential.
