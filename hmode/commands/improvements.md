Execute the improvements tracking skill with the provided arguments.

Usage: `/improvements [description] [--priority low|medium|high|urgent] [--status pending|in_progress|completed] [--list]`

Examples:
- `/improvements abstract config`
- `/improvements refactor authentication layer --priority high`
- `/improvements --list`

The skill will:
1. Create a Todo in `project-management/improvements/{project-name}/`
2. Follow task-management domain model
3. Store with UUID, timestamp, status, priority
4. Auto-detect current project from `.project` file

Run the improvements skill:
```bash
python3 shared/skills/improvements.py "$@"
```
