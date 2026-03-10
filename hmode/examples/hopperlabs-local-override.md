# Hopper Labs — Local Override (.claude/CLAUDE.md)

<!-- Example of project-specific overrides for the hopperlabs monorepo. -->
<!-- Copy this to .claude/CLAUDE.md and customize for your project. -->

## Author Context
**Background:** Ex-startup founder & CTO → Startup AI/ML Solutions Architect @ AWS
**Focus:** Rapid prototyping, AI/ML solutions, startup-scale architecture

## AWS Credentials

| Profile | Account | Purpose |
|---------|---------|---------|
| admin-507745175693 | 507745175693 | Personal account (b.lfg.new) |
| default | 108782054816 | Work/bedrock account (aws.demo1983.com) |
- Region: us-east-1

## Overwatch (Local Automation)

**Overwatch** is an autonomous file change automation system with 12 services:

**Quick Commands:**
```bash
bin/overwatch-manager status    # Check all services
bin/overwatch-manager health    # Run health checks
bin/overwatch-manager clean     # Clean zombie processes
bin/start-overwatch             # Start all services
bin/stop-overwatch              # Stop all services
```

**Services:**
| Category | Service | Description |
|----------|---------|-------------|
| Infrastructure | zmq_bus | ZMQ message broker (ports 5555/5556) |
| Infrastructure | events_tee | FIFO→ZMQ bridge for Claude events |
| Publisher | file_watcher | Monitors file changes |
| Subscriber | doc_agent | Auto-updates API docs |
| Subscriber | diagram_gen | Auto-updates architecture diagrams |
| Subscriber | html_gen | Auto-updates project HTML |
| Subscriber | semantic_indexer | Updates semantic search index |
| Subscriber | search_api | Semantic search REST (port 5557) |
| Subscriber | ui_dashboard | Overwatch web UI (port 3456) |

**Configuration:** `config/overwatch-services.yaml`
**Logs:** `logs/overwatch/*.log`

## Monorepo Structure

```
hopperlabs/
├── project-management/
│   ├── ideas/                  # Pre-SDLC ideas
│   ├── DASHBOARD.md            # Live project status
│   └── reports/
├── projects/                   # Active projects (~500+)
│   ├── personal/
│   ├── work/
│   ├── shared/
│   ├── oss/
│   └── unspecified/
├── bin/                        # Monorepo-specific scripts
│   └── overwatch/
├── config/                     # Overwatch config
├── infra/                      # Root infrastructure
└── hmode/                      # Shared methodology (subtree)
```

## Repository Statistics

| Category | Count | Notes |
|----------|-------|-------|
| Total Projects | ~500+ | Across all lifecycle stages |
| Active Projects | ~150 | In active development |
| Semantic Domains | 127 | Reusable domain models |
| Golden Repo Templates | 14 | Project starters by tech |
| Code Standards | 12 | Language/framework specific |
| Slash Commands | 154 | Custom Claude commands |
| Shared Tools | 15+ | Utility libraries & scripts |
| Overwatch Services | 12 | File automation microservices |
