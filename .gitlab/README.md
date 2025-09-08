# GitLab CI Security Scanning Pipelines

This folder contains GitLab CI/CD pipeline configurations for automated security scanning using Semgrep, Trivy, and Gitleaks.

## 📁 Files Overview

- **`security-scan.yml`** - Combined pipeline with all three scanners
- **`semgrep.yml`** - Individual Semgrep SAST scanning
- **`trivy.yml`** - Individual Trivy vulnerability scanning
- **`gitleaks.yml`** - Individual Gitleaks secret scanning
- **`gitlab-ci-example.yml`** - Example .gitlab-ci.yml configuration

## 🚀 Quick Setup

### Option 1: Combined Pipeline (Recommended)
Copy this to your `.gitlab-ci.yml`:

```yaml
include:
  - local: '.gitlab/security-scan.yml'

variables:
  BLOCKING_MODE: "true"
  SCAN_SEMGREP: "true"
  SCAN_TRIVY: "true"
  SCAN_GITLEAKS: "true"
```

### Option 2: Individual Pipelines
```yaml
include:
  - local: '.gitlab/semgrep.yml'
  - local: '.gitlab/trivy.yml'
  - local: '.gitlab/gitleaks.yml'
```

## ⚙️ Configuration Variables

### Global Variables (set in GitLab CI/CD Variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `BLOCKING_MODE` | `"true"` | Fail pipeline on security findings |
| `SCAN_SEMGREP` | `"true"` | Enable Semgrep scanning |
| `SCAN_TRIVY` | `"true"` | Enable Trivy scanning |
| `SCAN_GITLEAKS` | `"true"` | Enable Gitleaks scanning |

### DefectDojo Integration (Optional)

| Variable | Description |
|----------|-------------|
| `DEFECTDOJO_URL` | DefectDojo server URL |
| `DEFECTDOJO_TOKEN` | DefectDojo API token |

## 🔧 Blocking vs Non-Blocking Modes

### Blocking Mode (Default)
- **Behavior**: Pipeline fails when security issues are found
- **Use case**: Production branches, merge request validation
- **Configuration**: `BLOCKING_MODE: "true"`

### Non-Blocking Mode
- **Behavior**: Pipeline continues even with security issues
- **Use case**: Development branches, informational scanning
- **Configuration**: `BLOCKING_MODE: "false"`

## 🎯 Pipeline Triggers

All pipelines run on:
- **Merge Requests** - Validate security before merging
- **Main/Develop branches** - Continuous security monitoring
- **Manual triggers** - On-demand security scans
- **API triggers** - For integration with external tools

## 📊 Scanner Details

### Semgrep (SAST)
- **Command**: `semgrep --config=auto --sarif --no-git-ignore`
- **Output**: `semgrep.sarif`
- **GitLab Integration**: SAST security reports
- **Detects**: Code vulnerabilities, security anti-patterns

### Trivy (Vulnerability)
- **Command**: `trivy fs --scanners vuln --format sarif`
- **Output**: `trivy-results.sarif`
- **GitLab Integration**: Dependency scanning reports
- **Detects**: Known CVEs in dependencies

### Gitleaks (Secrets)
- **Command**: `gitleaks detect --report-format=sarif`
- **Output**: `gitleaks-results.sarif`
- **GitLab Integration**: Artifact storage
- **Detects**: Hardcoded secrets, API keys, credentials

## 🔄 Usage Examples

### Set Variables in GitLab UI
1. Go to **Settings** > **CI/CD** > **Variables**
2. Add variables:
   ```
   BLOCKING_MODE = true
   DEFECTDOJO_URL = https://your-defectdojo.com
   DEFECTDOJO_TOKEN = your-api-token
   ```

### Manual Pipeline Triggers
```bash
# Trigger with custom variables
curl -X POST \
  -F "token=$CI_TRIGGER_TOKEN" \
  -F "ref=main" \
  -F "variables[BLOCKING_MODE]=false" \
  -F "variables[SCAN_SEMGREP]=true" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/trigger/pipeline"
```

### Conditional Scanning
```yaml
# In your .gitlab-ci.yml
variables:
  SCAN_SEMGREP: "true"
  SCAN_TRIVY: "false"    # Skip Trivy
  SCAN_GITLEAKS: "true"
```

## 📈 GitLab Security Integration

### Security Reports
- **SAST**: Semgrep results appear in GitLab Security Dashboard
- **Dependency Scanning**: Trivy results show vulnerability details
- **Artifacts**: All SARIF files stored for 30 days

### Merge Request Integration
- **Security widgets** show scan results
- **Pipeline status** blocks/allows merging based on blocking mode
- **Artifact downloads** available for detailed analysis

## 🛠️ Customization

### Add Custom Rules
```yaml
# In your pipeline
semgrep:
  extends: .semgrep_template
  script:
    - semgrep --config=custom-rules.yml --sarif --output=semgrep.sarif .
```

### Environment-Specific Configuration
```yaml
# Different blocking behavior per environment
variables:
  BLOCKING_MODE: 
    value: "true"
    description: "Block on security findings"
    
production:
  variables:
    BLOCKING_MODE: "true"   # Always block in production

development:
  variables:
    BLOCKING_MODE: "false"  # Non-blocking in development
```

## 🚨 Troubleshooting

### Common Issues
1. **Pipeline fails immediately**: Check `BLOCKING_MODE` setting
2. **DefectDojo upload fails**: Verify URL and token variables
3. **Scanner not found**: Check image and installation steps
4. **No artifacts**: Verify SARIF file generation

### Debug Mode
Add to any job:
```yaml
variables:
  CI_DEBUG_TRACE: "true"
```

## 🔒 Security Best Practices

1. **Store sensitive variables** in GitLab CI/CD Variables (masked)
2. **Use protected variables** for production environments
3. **Enable pipeline security** in project settings
4. **Review security reports** regularly
5. **Set up notifications** for security issues

---

🔐 **Security scanning is now integrated into your GitLab CI/CD pipeline!**
