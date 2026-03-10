# Migration Guide: Multi-Context Infrastructure

Integrate multi-context, multi-stage infrastructure into existing CDK projects.

## Overview

**Before:** Single environment structure
```
config/
├── dev.yml
├── stage.yml
└── prod.yml
```

**After:** Multi-context structure
```
config/
├── work/
│   ├── dev.yml
│   ├── stage.yml
│   └── prod.yml
└── personal/
    └── dev.yml
```

## Migration Strategies

### Strategy 1: Automatic Migration (Recommended)

Use the migration script to automate the process:

```bash
# From your project root
make migrate-multi-context CONTEXT=work
```

This will:
1. ✅ Backup existing configs
2. ✅ Create context directory structure
3. ✅ Move existing configs to new location
4. ✅ Update code files (schema.ts, loader.ts, bin/app.ts)
5. ✅ Update Makefile
6. ✅ Preserve existing deployments

### Strategy 2: Manual Migration

Follow these steps to migrate manually.

## Manual Migration Steps

### Step 1: Backup Existing Configuration

```bash
# Create backup
mkdir -p .backup/config
cp -r config/* .backup/config/
cp infra/bin/app.ts .backup/app.ts.bak
cp Makefile .backup/Makefile.bak

echo "✓ Backup created in .backup/"
```

### Step 2: Choose Your Context Name

Decide what context name to use for your existing configs:
- `work` - For work/company projects
- `personal` - For personal projects
- `client-{name}` - For client-specific projects
- `team-{name}` - For team-specific projects

**Example:** We'll use `work` for this guide.

### Step 3: Reorganize Config Directory

```bash
# Create context directory
mkdir -p config/work

# Move existing YAML files
mv config/*.yml config/work/ 2>/dev/null || true

# Verify
ls config/work/
# Should show: dev.yml  stage.yml  prod.yml  (or whatever you had)
```

### Step 4: Update schema.ts

Replace the old schema with the new multi-context version:

```bash
# Download new schema
curl -o config/schema.ts \
  https://raw.githubusercontent.com/your-repo/golden-repos/main/typescript-cdk/config/schema.ts
```

Or manually update `config/schema.ts`:

```typescript
// REMOVE old environment enum:
// export const environments = ['local', 'dev', 'stage', 'prod'] as const;
// export type Environment = (typeof environments)[number];

// ADD new context/stage types:
export type Context = string;
export type Stage = string;

// UPDATE envConfigSchema:
export const envConfigSchema = z.object({
  context: z.string(),      // NEW
  stage: z.string(),        // NEW (was: env)
  account: z.string(),
  region: z.string().default('us-east-1'),
  // ... rest stays the same
});
```

### Step 5: Update loader.ts

Replace with new context-aware loader:

```bash
# Download new loader
curl -o config/loader.ts \
  https://raw.githubusercontent.com/your-repo/golden-repos/main/typescript-cdk/config/loader.ts
```

Or manually update `config/loader.ts`:

**Key changes:**
```typescript
// OLD:
export function loadConfig(env?: Environment): EnvConfig {
  const environment = env ?? getEnvironment();
  const configPath = path.join(__dirname, `${environment}.yml`);
  // ...
}

// NEW:
export function loadConfig(context?: Context, stage?: Stage): EnvConfig {
  const ctx = context ?? getContext();
  const stg = stage ?? getStage();
  const configPath = path.join(__dirname, ctx, `${stg}.yml`);
  // ...
}

// ADD new helper functions:
export function getContext(): Context {
  return process.env.CONTEXT ?? process.env.CDK_CONTEXT ?? 'work';
}

export function getStage(): Stage {
  return process.env.STAGE ?? process.env.CDK_STAGE ?? 'dev';
}

export function listAvailableConfigs(): string { /* ... */ }
export function getDeploymentId(config: EnvConfig): string { /* ... */ }
```

### Step 6: Update bin/app.ts

Update the CDK app entry point:

```typescript
// OLD:
import { loadConfig, getEnvironment } from '../config';
const config = loadConfig();
console.log(`\n🚀 Deploying to: ${config.env.toUpperCase()}`);

// NEW:
import { loadConfig, getContext, getStage } from '../config';
const config = loadConfig();
console.log(`\n🚀 Deploying Infrastructure`);
console.log(`   Context: ${config.context}`);
console.log(`   Stage: ${config.stage}`);
```

### Step 7: Update Makefile

Add multi-context support to your Makefile:

```makefile
# ADD at top:
CONTEXT ?= work
STAGE ?= dev
DEPLOY_ID := $(CONTEXT)-$(STAGE)

# UPDATE release paths:
RELEASES_DIR := infra/deploys/$(DEPLOY_ID)/releases
RELEASE_DIR := $(RELEASES_DIR)/$(TIMESTAMP)
CURRENT_LINK := infra/deploys/$(DEPLOY_ID)/current
SHARED_DIR := infra/deploys/$(DEPLOY_ID)/shared

# UPDATE deploy command:
infra-deploy:
	@echo "🚀 Deploying Infrastructure"
	@echo "   Context: $(CONTEXT)"
	@echo "   Stage: $(STAGE)"
	@mkdir -p $(RELEASE_DIR) $(SHARED_DIR)
	cd infra && CONTEXT=$(CONTEXT) STAGE=$(STAGE) npx cdk deploy --all ...
```

Or download the full Makefile:

```bash
curl -o Makefile \
  https://raw.githubusercontent.com/your-repo/golden-repos/main/typescript-cdk/Makefile
```

### Step 8: Test the Migration

```bash
# List available configs
make infra-list
# Should show: work: dev, stage, prod

# Test synthesis (doesn't deploy)
CONTEXT=work STAGE=dev npx cdk synth

# Deploy to dev
make infra-deploy CONTEXT=work STAGE=dev
```

### Step 9: Update CI/CD (if applicable)

**GitHub Actions:**
```yaml
# OLD:
- name: Deploy to dev
  run: npm run deploy:dev

# NEW:
- name: Deploy to dev
  run: make infra-deploy CONTEXT=work STAGE=dev
  env:
    CONTEXT: work
    STAGE: dev
```

**GitLab CI:**
```yaml
# OLD:
deploy:dev:
  script:
    - npm run deploy:dev

# NEW:
deploy:dev:
  script:
    - make infra-deploy CONTEXT=work STAGE=dev
  variables:
    CONTEXT: work
    STAGE: dev
```

### Step 10: Update Documentation

Update your project README:

```markdown
## Deployment

Deploy to specific context and stage:

```bash
# Deploy work dev
make infra-deploy CONTEXT=work STAGE=dev

# Deploy work prod
make infra-deploy CONTEXT=work STAGE=prod

# Check status
make infra-status CONTEXT=work STAGE=dev
```

## Migration Validation Checklist

After migration, verify:

- [ ] Config files moved to `config/{context}/` directory
- [ ] `schema.ts` updated with `context` and `stage` fields
- [ ] `loader.ts` updated to load from context/stage paths
- [ ] `bin/app.ts` updated to use new loader
- [ ] Makefile supports `CONTEXT=` and `STAGE=` parameters
- [ ] `make infra-list` shows available configs
- [ ] `CONTEXT=work STAGE=dev npx cdk synth` works
- [ ] Test deployment succeeds
- [ ] Stack names include context and stage: `app-work-dev-Api`
- [ ] Resources tagged with Context and Stage
- [ ] Deployment history in `infra/deploys/{context}-{stage}/`
- [ ] CI/CD updated (if applicable)
- [ ] Documentation updated

## Rollback Plan

If migration fails, rollback to original state:

```bash
# Restore configs
rm -rf config/work config/personal
cp -r .backup/config/* config/

# Restore code files
cp .backup/app.ts.bak infra/bin/app.ts
cp .backup/Makefile.bak Makefile

# Re-deploy with original setup
npm run deploy:dev  # or whatever your original command was
```

## Common Issues

### Issue: "Configuration file not found"

**Symptom:**
```
Configuration file not found: config/work/dev.yml
```

**Solution:**
```bash
# Check if configs were moved correctly
ls config/work/

# If empty, restore from backup
cp .backup/config/*.yml config/work/
```

### Issue: "Invalid configuration for work/dev"

**Symptom:**
```
Configuration validation failed for work/dev
```

**Solution:**
Config files are missing `context` and `stage` fields (loader adds them automatically, but check schema validation).

### Issue: Stack names changed

**Symptom:**
CDK tries to create new stacks instead of updating existing ones.

**Solution:**
Stack names now include context and stage. Two options:

**Option A: Import existing stacks**
```bash
# Import existing stack into new name
make infra-import STACK=MyApp-dev-Api
```

**Option B: Keep old stack names temporarily**

Edit `config/loader.ts`:
```typescript
// Temporarily use old naming
export function getStackName(config: EnvConfig, stackName: string): string {
  const prefix = config.stackPrefix ?? config.projectName;
  // OLD format (temporary):
  return `${prefix}-${config.stage}-${stackName}`;
  // NEW format (migrate later):
  // return `${prefix}-${config.context}-${config.stage}-${stackName}`;
}
```

### Issue: Deployment history lost

**Symptom:**
Can't see old releases after migration.

**Solution:**
Old releases are still in `infra/deploys/releases/`. Move them to new location:

```bash
# Move old releases to work-dev
mkdir -p infra/deploys/work-dev/releases
mv infra/deploys/releases/* infra/deploys/work-dev/releases/

# Update current symlink
ln -sfn releases/$(ls -t infra/deploys/work-dev/releases | head -1) \
  infra/deploys/work-dev/current
```

## Advanced: Migrating Multiple Environments

If you have multiple environments and want different contexts:

**Example:** Split dev/stage to work, prod to client-acme

```bash
# Create contexts
mkdir -p config/work config/client-acme

# Split environments
mv config/dev.yml config/work/
mv config/stage.yml config/work/
mv config/prod.yml config/client-acme/

# Update client-acme/prod.yml
# Change account ID, domains, etc.
```

Then deploy:
```bash
make infra-deploy CONTEXT=work STAGE=dev
make infra-deploy CONTEXT=client-acme STAGE=prod
```

## Migration Automation Script

For multiple projects, use the migration script:

```bash
#!/bin/bash
# migrate-to-multi-context.sh

CONTEXT=${1:-work}

echo "🚀 Migrating to multi-context infrastructure"
echo "   Target context: $CONTEXT"

# 1. Backup
mkdir -p .backup/config
cp -r config/* .backup/config/
echo "✓ Backup created"

# 2. Create context directory
mkdir -p config/$CONTEXT

# 3. Move configs
mv config/*.yml config/$CONTEXT/ 2>/dev/null
echo "✓ Configs moved to config/$CONTEXT/"

# 4. Download new files
curl -sL https://raw.githubusercontent.com/your-repo/golden-repos/main/typescript-cdk/config/schema.ts \
  -o config/schema.ts
curl -sL https://raw.githubusercontent.com/your-repo/golden-repos/main/typescript-cdk/config/loader.ts \
  -o config/loader.ts
curl -sL https://raw.githubusercontent.com/your-repo/golden-repos/main/typescript-cdk/Makefile \
  -o Makefile
echo "✓ Updated core files"

# 5. Update app.ts
sed -i.bak 's/getEnvironment/getContext, getStage/g' infra/bin/app.ts
echo "✓ Updated app.ts"

# 6. Test
make infra-list
echo ""
echo "✓ Migration complete!"
echo ""
echo "Next steps:"
echo "1. Test synthesis: CONTEXT=$CONTEXT STAGE=dev npx cdk synth"
echo "2. Test deploy: make infra-deploy CONTEXT=$CONTEXT STAGE=dev"
```

Save as `migrate-to-multi-context.sh` and run:

```bash
chmod +x migrate-to-multi-context.sh
./migrate-to-multi-context.sh work
```

## Next Steps After Migration

1. **Add Personal Context** (if needed):
   ```bash
   mkdir config/personal
   cp config/work/dev.yml config/personal/dev.yml
   # Edit personal/dev.yml with personal account ID
   ```

2. **Add Blue/Green Stages** (if needed):
   ```bash
   cp config/work/prod.yml config/work/blue.yml
   cp config/work/prod.yml config/work/green.yml
   # Edit domains: blue.example.com, green.example.com
   ```

3. **Clean Up Old Deployment History**:
   ```bash
   # After verifying migration works
   rm -rf .backup/
   ```

4. **Update Team Documentation**:
   - Share new deployment commands
   - Update runbooks
   - Update CI/CD pipelines

## Summary

Multi-context migration provides:

✅ **Backward compatible** - Existing deployments continue working  
✅ **Gradual adoption** - Migrate one environment at a time  
✅ **Safe rollback** - Backup allows instant rollback  
✅ **No downtime** - Deployments continue during migration  
✅ **Flexible naming** - Use any context and stage names  

---

**Need help?** Check the main [MULTI_CONTEXT.md](MULTI_CONTEXT.md) documentation or create an issue.
