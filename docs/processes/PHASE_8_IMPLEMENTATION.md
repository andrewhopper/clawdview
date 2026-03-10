### Phase 8: IMPLEMENTATION 💻 (WRITE CODE + RUN TESTS!)
**Goal:** Build the prototype to pass the tests
**Output:** `prototypes/proto-name-xxxxx-NNN-name/src/` with all source code + updated README
**Title:** `# Stage 8 - Implementation`

**Activities:**
- **START FROM GOLDEN REPO** - Copy appropriate template from `hmode/shared/golden-repos/` as foundation
- Write implementation code to make scenarios pass (BDD implementation phase)
- Run scenarios continuously during development
- Refactor as needed while keeping scenarios passing
- Add missing scenarios if gaps discovered during implementation
- **README.md** - Must include: purpose, tech stack, setup instructions, BDD test commands, phase status

---

**🏆 GOLDEN REPOS - Start Every Project Right**

Before writing code, copy the appropriate template from `hmode/shared/golden-repos/`:

| Project Type | Template | Key Features |
|--------------|----------|--------------|
| **Python CLI/Script** | `python-script/` | Typer CLI, structlog, pydantic-settings, pytest |
| **Python API** | `python-fastapi/` | FastAPI, middleware, CORS, health checks, OpenAPI |
| **Python Library** | `python-general/` | Pydantic models, Result pattern, structured logging |
| **Node.js Backend** | `typescript-nodejs/` | Pino logging, Zod config, Vitest, ESM |
| **Next.js App** | `typescript-nextjs/` | App Router, Tailwind, React Testing Library |
| **React Components** | `typescript-react/` | Vite library mode, hooks, component patterns |
| **Vite App** | `typescript-vite/` | Vanilla TS, DOM utils, Result type |
| **Email Templates** | `typescript-email/` | React Email, Resend, preview server |
| **AWS Infrastructure** | `typescript-cdk/` | CDK, YAML configs, multi-env, BaseStack pattern |

**Usage:**
```bash
# Copy template to new prototype
cp -r hmode/shared/golden-repos/python-fastapi/* prototypes/proto-my-api-xxxxx-001/

# Or for TypeScript projects
cp -r hmode/shared/golden-repos/typescript-nextjs/* prototypes/proto-my-app-xxxxx-001/
```

**All templates include:**
- ✅ Structured logging (structlog/pino)
- ✅ Configuration management (pydantic-settings/zod)
- ✅ Test setup (pytest/vitest)
- ✅ Type safety (mypy/TypeScript strict)
- ✅ Linting (ruff/eslint)

---

**BDD Workflow:**
1. Pick failing scenario (Given/When/Then)
2. Implement step definitions if not stubbed
3. Write minimal code to make scenario pass
4. Run `npm run test:bdd` → verify passing
5. Refactor if needed while keeping scenarios green
6. Repeat until all scenarios pass

---

**Track A (Basic) Implementation:**
- Run Cucumber BDD smoke scenarios after each major feature
- Fix broken scenarios immediately (fast feedback loop)
- LLM uses Gherkin scenario output to guide implementation
- Focus: Working code, basic quality, stakeholder-readable tests

**Track B (Comprehensive) Implementation:**
- Run full BDD scenario suite after each module/feature completion
- Maintain 50-70% coverage throughout development
- Add unit tests for step definitions alongside implementation
- Fix ALL failing scenarios before moving to next feature
- Generate HTML reports after test runs
- Focus: Production quality, regression protection, shareable reports

---

**🚨 ENFORCEMENT:**
- **Track A:** Smoke scenarios MUST pass before phase transition
- **Track B:** All scenarios MUST pass, coverage target met before phase transition
- **ALL PROJECTS:** MUST include startup automation script (see Startup Script Requirement below)
- **BDD Testing:** See `hmode/shared/standards/testing/BDD_TESTING_GUIDE.md` for Cucumber setup

**Startup Script Requirement:**

Every project MUST include a single-command startup script that:

1. **Starts all required services** (database, backend, frontend, workers, etc.)
2. **Seeds database with placeholder data** (if applicable)
3. **Configures test environment** (ports, env vars, dependencies)
4. **Verifies environment readiness** (health checks, connectivity)

**Implementation Options:**

**Option A: Shell Script** (`start-dev.sh` or `start-test.sh`)
```bash
#!/bin/bash
# Start all services for testing
docker-compose up -d postgres redis
npm run db:seed
npm run dev
```

**Option B: Package.json Script** (`npm run start:test`)
```json
{
  "scripts": {
    "start:test": "run-p db:start db:seed dev",
    "db:start": "docker-compose up -d postgres",
    "db:seed": "node scripts/seed-db.js",
    "dev": "vite"
  }
}
```

**Option C: Makefile** (`make start-test`)
```makefile
start-test:
	docker-compose up -d
	npm run db:seed
	npm run dev
```

**Requirements:**
- ✅ Single command starts entire test environment
- ✅ Idempotent (safe to run multiple times)
- ✅ Seeds database with realistic placeholder data
- ✅ Documented in README.md with usage instructions
- ✅ Works on fresh clone (no manual setup required)

**Placeholder Data Requirements:**
- Sufficient for testing all features (users, products, transactions, etc.)
- Realistic (proper formats, relationships, edge cases)
- Deterministic (same data each run for consistent tests)
- Fast to seed (<10 seconds for most projects)

**Test Credentials Management:**
- **ALL test login credentials MUST be documented in `test_guide.md`** in project root
- Include username/email, password, role/permissions
- Document which features each test account can access
- Never commit real credentials (test accounts only)
- Example format:
  ```markdown
  ## Test Accounts

  **Admin User:**
  - Email: admin@test.local
  - Password: Admin123!
  - Access: Full system access

  **Regular User:**
  - Email: user@test.local
  - Password: User123!
  - Access: Limited to own resources
  ```

**Documentation Required in README.md:**
```markdown
## Quick Start

# Start entire test environment (includes DB seeding)
npm run start:test

# Or using shell script
./start-dev.sh

# Or using make
make start-test
```

**Exit:** All scenarios pass (per track), features implemented, code runs, README complete with BDD commands, startup script created and documented

