# Evidence Pack Assembler

A defensive cybersecurity and governance tool that assembles audit and risk evidence packages by framework and control.

## Overview

This tool ingests control definitions and evidence records from CSV files, maps evidence to controls, detects stale evidence, identifies missing evidence, and generates comprehensive reports including a Markdown evidence inventory and executive summaries.

## Features

- **CSV Ingestion**: Load control definitions, evidence records, and owner information from CSV files
- **Data Validation**: Validate required columns, data integrity, and business rules
- **Evidence Mapping**: Map evidence records to controls by control ID
- **Staleness Detection**: Identify evidence older than 90 days or missing review dates
- **Gap Analysis**: Identify controls with missing or draft-only evidence
- **Reporting**: Generate detailed Markdown reports and terminal summaries
- **No External Dependencies**: Uses only Python standard library

## Sample Data Structure

### controls.csv
```
framework,control_id,control_title,domain,owner_team,priority
ISO 27001,A.9.1.1,Access control policy,Access Control,Security Team,High
NIST CSF,PR.AC-1,Identifies and manages the creation, change, and deletion of user accounts,Access Control,IT Operations,Medium
```

### evidence.csv
```
evidence_id,control_id,evidence_title,evidence_type,file_reference,owner,status,collected_date,review_date,notes
E001,A.9.1.1,Access Control Policy Document,Policy,docs/policy.pdf,Alice Johnson,valid,2023-01-15,2024-01-15,Annual review completed
E002,PR.AC-1,User Account Management Procedure,Procedure,docs/procedure.pdf,Bob Smith,stale,2023-06-01,2023-06-01,Needs update
```

### owners.csv
```
owner,team,email
Alice Johnson,Security Team,alice@company.com
Bob Smith,IT Operations,bob@company.com
```

## Risk/Evidence Logic

- **Valid Evidence**: Status = 'valid', review date within 90 days
- **Stale Evidence**: Review date older than 90 days
- **At Risk Evidence**: Missing review date
- **Missing Evidence**: Control has no valid evidence
- **Draft Evidence**: Status = 'draft', not considered valid
- **Priority Highlighting**: High-priority controls with missing evidence are flagged

## How to Run

1. Ensure Python 3.6+ is installed
2. Clone or download the project
3. Place your CSV data files in the `data/` directory
4. Run the tool:

```bash
python main.py
```

## Sample Output

```
Evidence Pack Assembler Summary:
Total Controls: 8
Total Evidence Items: 12
Missing Evidence Controls: 2
Stale Evidence Items: 3
Report generated at: output/evidence_inventory.md
```

The Markdown report includes summary metrics, executive summary, priority gaps, stale evidence, unknown control mappings, detailed control-to-evidence mapping table, and remediation recommendations.

## Roadmap

- [ ] Add support for additional file formats (JSON, Excel)
- [ ] Implement automated evidence collection from APIs
- [ ] Add dashboard visualization
- [ ] Integrate with compliance management platforms
- [ ] Add configurable staleness thresholds

## Ethical and Operational Use Note

This tool is designed for defensive cybersecurity and governance purposes. Use responsibly and in accordance with applicable laws and organizational policies. Ensure proper authorization before processing sensitive evidence data.