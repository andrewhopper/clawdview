# Requirements Excel Generator

**Location:** `shared/artifact-library/requirements-excel-generator.py`

## Purpose
Generate simple and advanced requirements tracking templates with UUIDs, optimized for keyboard navigation.

## Usage

```bash
python requirements-excel-generator.py [output_directory]
```

If no directory specified, creates files in current directory.

## Templates Generated

### 1. REQUIREMENTS-SIMPLE.xlsx
**For:** Quick reviews, stakeholder approvals, fast decision-making

**Columns:**
- Feature
- Approved (Y/N/With Changes)
- Notes
- UUID (auto-generated, at end)

**Features:**
- Color-coded approvals (green=Y, red=N, orange=With Changes)
- Auto-calculating summary stats
- Keyboard optimized (Tab through Feature → Approved → Notes)

**Best for:** Solo decision-making, quick iterations

---

### 2. REQUIREMENTS-ADVANCED.xlsx
**For:** Team collaboration, detailed planning, version tracking

**Columns:**
- Feature Group
- Tags (comma-separated)
- Type (Functional/Non-Functional)
- Requirement
- Must/Nice
- v1/v2/v3 (version markers)
- Decision (Accepted, Revise, Kill, Move to vX)
- Status (Not Started, In Progress, Done, etc.)
- User Feedback
- Revision Notes
- UUID (auto-generated, at end)

**Features:**
- Feature groups for organization
- Tagging system
- Multi-version planning
- Decision workflow tracking
- Summary stats sheet
- Keyboard optimized

**Best for:** Development teams, complex projects, multiple versions

---

## Design Principles

1. **UUID at end** - Out of the way, auto-generated
2. **No Owner column** - For solo developers
3. **Keyboard optimized** - Tab left-to-right, Enter moves down
4. **Color-coded decisions** - Visual clarity
5. **Auto-calculating stats** - No manual counting

## Examples

Generate in current directory:
```bash
python requirements-excel-generator.py
```

Generate in project directory:
```bash
python requirements-excel-generator.py ~/projects/my-app/
```

## Customization

Edit the Python script to:
- Change sample data
- Add/remove columns
- Modify color schemes
- Adjust column widths
- Add more sheets

## Dependencies

```bash
pip install openpyxl
```
