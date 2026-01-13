
Multi-Database Data Governance Monitor

This repository manages Data Quality (DQ) across three siloed databases to ensure KYC/KYB compliance.

## Architecture
- **Platform_Core**: User accounts and profile data.
- **Identity_Vault**: Sensitive KYC verification and PII.
- **Corporate_Registry**: KYB business entity data.

## How it works
1. `data_quality_checks.sql` identifies mismatches between the three sources.
2. `dq_monitor_alert.py` automates the checking process
