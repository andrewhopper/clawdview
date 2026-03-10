#!/bin/bash
# File UUID: 2f7e9c3a-1b4d-4e8f-9c2a-5d6e7f8a9b0c

# SSM Parameter Migration Script
#
# Migrates existing SSM parameters to standardized hierarchical namespace.
# Follows pattern: /{account-type}/{environment}/{project}/{category}/{key}
#
# Usage:
#   ./shared/tools/migrate-ssm-params.sh [--dry-run]

set -euo pipefail

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "🔍 DRY RUN MODE - No changes will be made"
fi

REGION="${AWS_REGION:-us-east-1}"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
  echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
  echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
  echo -e "${RED}✗${NC} $1"
}

migrate_param() {
  local old_name=$1
  local new_name=$2

  # Get parameter details
  local param_json
  if ! param_json=$(aws ssm get-parameter --name "$old_name" --with-decryption --region "$REGION" 2>/dev/null); then
    log_error "Failed to read: $old_name"
    return 1
  fi

  local value=$(echo "$param_json" | jq -r '.Parameter.Value')
  local type=$(echo "$param_json" | jq -r '.Parameter.Type')

  # Check if new parameter already exists
  if aws ssm get-parameter --name "$new_name" --region "$REGION" &>/dev/null; then
    log_warning "Already exists: $new_name (skipping)"
    return 0
  fi

  if [[ "$DRY_RUN" == true ]]; then
    log_info "Would migrate:"
    echo "  From: $old_name"
    echo "  To:   $new_name"
    echo "  Type: $type"
    return 0
  fi

  # Create new parameter
  if aws ssm put-parameter \
    --name "$new_name" \
    --value "$value" \
    --type "$type" \
    --description "Migrated from $old_name" \
    --region "$REGION" \
    --overwrite &>/dev/null; then
    log_success "Migrated: $old_name → $new_name"
  else
    log_error "Failed to create: $new_name"
    return 1
  fi
}

# Migration rules

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  SSM Parameter Migration to Hierarchical Namespace"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Migrate /gocoder/dev/* → /work/dev/gocoder/*
echo "1️⃣  Migrating GoCoder dev environment..."
echo ""

gocoder_dev_params=$(aws ssm get-parameters-by-path --path /gocoder/dev --recursive --region "$REGION" --query 'Parameters[].Name' --output text 2>/dev/null || echo "")

for param in $gocoder_dev_params; do
  # Extract path after /gocoder/dev/
  suffix=${param#/gocoder/dev/}
  new_param="/work/dev/gocoder/$suffix"
  migrate_param "$param" "$new_param"
done

# 2. Migrate /gocoder/work/dev/* → /work/dev/gocoder/* (inconsistent depth)
echo ""
echo "2️⃣  Migrating GoCoder work-dev environment..."
echo ""

gocoder_work_dev_params=$(aws ssm get-parameters-by-path --path /gocoder/work/dev --recursive --region "$REGION" --query 'Parameters[].Name' --output text 2>/dev/null || echo "")

for param in $gocoder_work_dev_params; do
  suffix=${param#/gocoder/work/dev/}
  new_param="/work/dev/gocoder/$suffix"
  migrate_param "$param" "$new_param"
done

# 3. Migrate /hopperlabs/shared/* → /work/* (account-level shared)
echo ""
echo "3️⃣  Migrating HopperLabs shared to account-level..."
echo ""

hopperlabs_shared_params=$(aws ssm get-parameters-by-path --path /hopperlabs/shared --recursive --region "$REGION" --query 'Parameters[].Name' --output text 2>/dev/null || echo "")

for param in $hopperlabs_shared_params; do
  suffix=${param#/hopperlabs/shared/}
  new_param="/work/$suffix"
  migrate_param "$param" "$new_param"
done

# 4. Migrate /hopperlabs/projects/* → /work/prod/{project}/*
echo ""
echo "4️⃣  Migrating HopperLabs projects to production..."
echo ""

hopperlabs_project_params=$(aws ssm get-parameters-by-path --path /hopperlabs/projects --recursive --region "$REGION" --query 'Parameters[].Name' --output text 2>/dev/null || echo "")

for param in $hopperlabs_project_params; do
  suffix=${param#/hopperlabs/projects/}
  # Extract project name (first segment)
  project=$(echo "$suffix" | cut -d'/' -f1)
  category=$(echo "$suffix" | cut -d'/' -f2-)
  new_param="/work/prod/$project/$category"
  migrate_param "$param" "$new_param"
done

# 5. Migrate story-wizard work environment
echo ""
echo "5️⃣  Migrating Story Wizard work environment..."
echo ""

story_wizard_params=$(aws ssm get-parameters-by-path --path /story-wizard/work --recursive --region "$REGION" --query 'Parameters[].Name' --output text 2>/dev/null || echo "")

for param in $story_wizard_params; do
  suffix=${param#/story-wizard/work/}
  new_param="/work/prod/story-wizard/$suffix"
  migrate_param "$param" "$new_param"
done

# 6. Migrate ppm work/prod
echo ""
echo "6️⃣  Migrating PPM work/prod environment..."
echo ""

ppm_params=$(aws ssm get-parameters-by-path --path /ppm/work/prod --recursive --region "$REGION" --query 'Parameters[].Name' --output text 2>/dev/null || echo "")

for param in $ppm_params; do
  suffix=${param#/ppm/work/prod/}
  new_param="/work/prod/ppm/$suffix"
  migrate_param "$param" "$new_param"
done

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Migration Complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [[ "$DRY_RUN" == true ]]; then
  log_warning "This was a DRY RUN - no changes were made"
  log_info "Run without --dry-run to apply changes"
else
  log_success "All parameters migrated successfully"
  log_warning "Old parameters are still in place"
  log_info "After verifying new parameters work, delete old ones with:"
  echo "  aws ssm delete-parameter --name <old-param-name>"
fi

echo ""
