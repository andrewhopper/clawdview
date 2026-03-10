---
name: add-sa-to-accounts
description: Add user as SA to accounts and opportunities for specified companies
tags: [salesforce, accounts, opportunities, macro]
---

# Add SA to Accounts & Opportunities Macro

This macro automates the process of:
1. Finding accounts for specified companies
2. Getting territory information
3. Retrieving all opportunities (open + closed-won)
4. Generating XLSX report with complete data
5. (Manual step) Adding user as SA to accounts and opportunities

## Usage

```bash
/add-sa-to-accounts
```

You'll be prompted for:
- Company names (comma-separated)
- Whether to include closed opportunities

## Process

### 1. Get User Details
```python
user_details = get_my_personal_details()
# Returns: {"alias": "andyhop", "sfdcId": "0050z000008OWntAAG"}
```

### 2. Search Accounts
```python
for company_name in company_names:
    accounts = search_accounts(queryTerm=company_name)
    # User selects the correct account if multiple matches
```

### 3. Get Account Details & Territory
```python
for account_id in account_ids:
    details = fetch_account_details(accountId=account_id)
    # Extracts: name, territory, owner, etc.
```

### 4. Get Opportunities
```python
for account_id in account_ids:
    opps = get_opportunities_for_account(
        accountId=account_id,
        includeClosed=True,  # Include closed-won
        limit=50
    )
    # Filter for: stageName != "Closed Lost"
```

### 5. Generate XLSX Report
Creates spreadsheet with columns:
- Opp ID
- Account ID
- Territory
- Account Name
- Opp Name
- Opp Amount
- Stage

### 6. Manual Steps (AWS Sentral MCP Limitation)

**Important:** The AWS Sentral MCP server does not currently provide tools to:
- Add account team members (SA role)
- Add opportunity team members (SA role)

These must be done manually via Salesforce UI or direct API access.

#### Manual Process:

**For Account Team:**
1. Navigate to Account in Salesforce
2. Go to Account Team section
3. Click "Add Team Member"
4. Select user: `andyhop` (0050z000008OWntAAG)
5. Role: "Solutions Architect"

**For Opportunity Team:**
1. Navigate to Opportunity in Salesforce
2. Go to Opportunity Team section
3. Click "Add Team Member"
4. Select user: `andyhop` (0050z000008OWntAAG)
5. Role: "Solutions Architect"

## Example Output

```
✓ Found 2 accounts:
  - Cohere Health (0010z00001bLn8uAAC)
    Territory: NAMED-AGS-NAMER-United States-UNITED STATES-UNITED STATES-EAST1-BOS-PRT-HCLS1
  - CloudZero (0013800001CB3mFAAT)
    Territory: NAMED-AGS-NAMER-United States-UNITED STATES-UNITED STATES-EAST1-BOS-PRT-CROSS1

✓ Retrieved 70 opportunities (36 Cohere Health, 34 CloudZero)

✓ Report generated: account_opps_report_20251210_111039.xlsx

⚠ Manual steps required:
  [ ] Add andyhop as SA to 2 accounts
  [ ] Add andyhop as SA to 70 opportunities
```

## Report Columns

| Column | Description |
|--------|-------------|
| Opp ID | Salesforce Opportunity ID |
| Account ID | Salesforce Account ID |
| Territory | Full territory path |
| Account Name | Account display name |
| Opp Name | Opportunity name |
| Opp Amount | Opportunity amount ($) |
| Stage | Current opportunity stage |

## Notes

- Only includes opportunities with stage != "Closed Lost"
- Default limit is 50 opportunities per account
- Report saved to: `/Users/andyhop/dev/lab/account_opps_report_TIMESTAMP.xlsx`
- Access denied errors (e.g., Flagship Pioneering) are documented in report

## Future Enhancement Ideas

1. **Bulk API Integration:** Use Salesforce Bulk API to add account/opp team members
2. **Permission Request Automation:** Auto-request access for accounts with permission errors
3. **Stage Filtering:** Allow user to specify which stages to include
4. **CSV Export Option:** Alternative to XLSX for easier parsing
5. **Summary Statistics:** Add summary sheet with totals by account/stage
