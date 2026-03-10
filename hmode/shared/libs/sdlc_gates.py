"""
SDLC Gate Checking Utilities

Enforces approval gates across SDLC phases, particularly for design workflows.
"""
# File UUID: 3d7f8a2e-9c4b-4f1a-8e3d-2a6f9b3c7d5e

from pathlib import Path
from typing import Literal, Optional
import yaml
from datetime import datetime


class DesignGateNotApproved(Exception):
    """Raised when attempting to proceed past an unapproved design gate."""
    pass


class ApprovalFileNotFound(Exception):
    """Raised when .project-approvals.yaml is required but not found."""
    pass


GateStatus = Literal['pending', 'approved', 'rejected', 'changes_requested']
GateId = Literal['gate_1_ia', 'gate_2_lofi', 'final_signoff']


def check_design_gate(gate_id: GateId, project_root: Optional[Path] = None) -> bool:
    """
    Check if a design approval gate has been passed.

    Args:
        gate_id: gate_1_ia | gate_2_lofi | final_signoff
        project_root: Path to project root (defaults to current directory)

    Returns:
        True if gate approved or workflow not enabled

    Raises:
        DesignGateNotApproved: If gate not approved with status and instructions
        ApprovalFileNotFound: If approval workflow enabled but file missing
    """
    if project_root is None:
        project_root = Path.cwd()

    approval_file = project_root / '.project-approvals.yaml'

    if not approval_file.exists():
        # No approval workflow enabled - allow passage
        return True

    with open(approval_file) as f:
        approvals = yaml.safe_load(f)

    if not approvals.get('design_workflow', {}).get('enabled'):
        # Workflow not enabled - allow passage
        return True

    # Find the gate
    for gate in approvals['design_workflow']['gates']:
        if gate['gate_id'] == gate_id:
            status = gate['status']

            if status == 'approved':
                return True

            # Gate exists but not approved
            stage_name = gate['stage'].replace('_', ' ').title()
            raise DesignGateNotApproved(
                f"Cannot proceed: Gate {gate_id} ({stage_name}) not approved.\n"
                f"Current status: {status}\n"
                f"Artifacts: {', '.join(gate.get('artifacts', []))}\n"
                f"Feedback: {gate.get('feedback', 'None')}\n\n"
                f"Options:\n"
                f"  [1] Request approval for current stage\n"
                f"  [2] Revise based on feedback\n"
                f"  [3] View approval status"
            )

    # Gate not found - hasn't been reached yet, allow passage
    return True


def update_gate_status(
    gate_id: GateId,
    status: GateStatus,
    approved_by: Optional[str] = None,
    feedback: Optional[list[str]] = None,
    project_root: Optional[Path] = None
) -> None:
    """
    Update the status of a design approval gate.

    Args:
        gate_id: The gate to update
        status: New status
        approved_by: Email/username of approver
        feedback: List of feedback items (for changes_requested)
        project_root: Path to project root (defaults to current directory)
    """
    if project_root is None:
        project_root = Path.cwd()

    approval_file = project_root / '.project-approvals.yaml'

    if not approval_file.exists():
        raise ApprovalFileNotFound(
            f"Approval file not found: {approval_file}\n"
            f"Run initialize_approval_workflow() first"
        )

    with open(approval_file) as f:
        approvals = yaml.safe_load(f)

    # Find and update the gate
    for gate in approvals['design_workflow']['gates']:
        if gate['gate_id'] == gate_id:
            gate['status'] = status

            if status == 'approved':
                gate['approved_by'] = approved_by or 'unknown'
                gate['approved_at'] = datetime.utcnow().isoformat() + 'Z'

            if feedback:
                gate['feedback'] = feedback

            break

    # Write back
    with open(approval_file, 'w') as f:
        yaml.dump(approvals, f, default_flow_style=False, sort_keys=False)


def initialize_approval_workflow(project_root: Optional[Path] = None) -> Path:
    """
    Initialize the approval workflow for a project.

    Creates .project-approvals.yaml with default gate structure.

    Args:
        project_root: Path to project root (defaults to current directory)

    Returns:
        Path to created approval file
    """
    if project_root is None:
        project_root = Path.cwd()

    approval_file = project_root / '.project-approvals.yaml'

    approval_structure = {
        'design_workflow': {
            'enabled': True,
            'gates': [
                {
                    'gate_id': 'gate_1_ia',
                    'stage': 'information_architecture',
                    'status': 'pending',
                    'approved_by': None,
                    'approved_at': None,
                    'artifacts': [],
                    'feedback': []
                },
                {
                    'gate_id': 'gate_2_lofi',
                    'stage': 'lofi_wireframes',
                    'status': 'pending',
                    'approved_by': None,
                    'approved_at': None,
                    'artifacts': [],
                    'feedback': []
                },
                {
                    'gate_id': 'final_signoff',
                    'stage': 'hifi_mockups',
                    'status': 'pending',
                    'approved_by': None,
                    'approved_at': None,
                    'artifacts': [],
                    'feedback': []
                }
            ]
        }
    }

    with open(approval_file, 'w') as f:
        yaml.dump(approval_structure, f, default_flow_style=False, sort_keys=False)

    return approval_file


def get_approval_status(project_root: Optional[Path] = None) -> dict:
    """
    Get the current approval status for all gates.

    Args:
        project_root: Path to project root (defaults to current directory)

    Returns:
        Dictionary with approval status for each gate
    """
    if project_root is None:
        project_root = Path.cwd()

    approval_file = project_root / '.project-approvals.yaml'

    if not approval_file.exists():
        return {'design_workflow': {'enabled': False, 'gates': []}}

    with open(approval_file) as f:
        approvals = yaml.safe_load(f)

    return approvals


def format_approval_status(project_root: Optional[Path] = None) -> str:
    """
    Format approval status as human-readable text.

    Args:
        project_root: Path to project root (defaults to current directory)

    Returns:
        Formatted status string
    """
    status = get_approval_status(project_root)

    if not status['design_workflow']['enabled']:
        return "Design approval workflow: DISABLED"

    output = []
    output.append("═" * 60)
    output.append("  DESIGN APPROVAL STATUS")
    output.append("═" * 60)
    output.append("")

    for gate in status['design_workflow']['gates']:
        stage_name = gate['stage'].replace('_', ' ').title()
        status_icon = {
            'pending': '⏳',
            'approved': '✅',
            'rejected': '❌',
            'changes_requested': '🔄'
        }.get(gate['status'], '❓')

        output.append(f"{status_icon} {stage_name}")
        output.append(f"   Status: {gate['status'].upper()}")

        if gate['approved_by']:
            output.append(f"   Approved by: {gate['approved_by']}")
            output.append(f"   Approved at: {gate['approved_at']}")

        if gate['artifacts']:
            output.append(f"   Artifacts: {', '.join(gate['artifacts'])}")

        if gate['feedback']:
            output.append(f"   Feedback:")
            for item in gate['feedback']:
                output.append(f"     - {item}")

        output.append("")

    return "\n".join(output)


# ============================================================================
# Domain Model Approval Functions
# ============================================================================


class DomainNotApproved(Exception):
    """Raised when attempting to implement unapproved domain model."""
    pass


def check_domain_exists(domain_name: str, project_root: Optional[Path] = None) -> bool:
    """
    Check if domain exists in global registry.

    Args:
        domain_name: Domain to check
        project_root: Path to project root (defaults to current directory)

    Returns:
        True if domain exists and is active
    """
    if project_root is None:
        project_root = Path.cwd()

    registry_path = project_root / 'shared' / 'semantic' / 'domains' / 'registry.yaml'

    if not registry_path.exists():
        raise FileNotFoundError(f"Domain registry not found: {registry_path}")

    with open(registry_path) as f:
        registry = yaml.safe_load(f)

    for domain in registry.get('domains', []):
        if domain['name'] == domain_name and domain['status'] == 'active':
            return True

    return False


def check_domain_approval(domain_name: str, project_root: Optional[Path] = None) -> bool:
    """
    Check if domain has been approved for use in this project.

    Args:
        domain_name: Domain to check
        project_root: Path to project root (defaults to current directory)

    Returns:
        True if approved or already in registry

    Raises:
        DomainNotApproved: If domain not found or not approved
    """
    if project_root is None:
        project_root = Path.cwd()

    # First check global registry
    try:
        if check_domain_exists(domain_name, project_root):
            return True
    except FileNotFoundError:
        pass

    # Check project-specific approvals
    approval_file = project_root / '.project-approvals.yaml'

    if not approval_file.exists():
        raise DomainNotApproved(
            f"Domain '{domain_name}' not found in registry and no project approvals exist.\n"
            f"Required workflow:\n"
            f"  1. Check shared/semantic/domains/registry.yaml\n"
            f"  2. Research external sources (schema.org, GitHub)\n"
            f"  3. Propose domain model (YAML)\n"
            f"  4. Request human approval\n"
            f"  5. Implement after approval"
        )

    with open(approval_file) as f:
        approvals = yaml.safe_load(f)

    for approval in approvals.get('domain_approvals', []):
        if approval['domain'] == domain_name and approval['status'] == 'approved':
            return True

    raise DomainNotApproved(
        f"Domain '{domain_name}' not approved.\n"
        f"Check registry: shared/semantic/domains/registry.yaml\n"
        f"Or run domain approval workflow"
    )


def update_domain_approval(
    domain_name: str,
    status: GateStatus,
    version: str = "1.0.0",
    entities: Optional[list[str]] = None,
    primitives: Optional[list[str]] = None,
    research_sources: Optional[list[str]] = None,
    approved_by: Optional[str] = None,
    feedback: Optional[list[str]] = None,
    project_root: Optional[Path] = None
) -> None:
    """
    Update or create domain approval entry.

    Args:
        domain_name: Domain being approved
        status: Approval status
        version: Domain version
        entities: List of entity names
        primitives: List of primitive names
        research_sources: List of research sources
        approved_by: Email/username of approver
        feedback: List of feedback items
        project_root: Path to project root (defaults to current directory)
    """
    if project_root is None:
        project_root = Path.cwd()

    approval_file = project_root / '.project-approvals.yaml'

    if not approval_file.exists():
        approvals = {'design_workflow': {'enabled': False, 'gates': []}, 'domain_approvals': []}
    else:
        with open(approval_file) as f:
            approvals = yaml.safe_load(f)

    if 'domain_approvals' not in approvals:
        approvals['domain_approvals'] = []

    # Find or create approval entry
    domain_approval = None
    for approval in approvals['domain_approvals']:
        if approval['domain'] == domain_name:
            domain_approval = approval
            break

    if domain_approval is None:
        domain_approval = {
            'domain': domain_name,
            'version': version,
            'status': status,
            'proposed_at': datetime.utcnow().isoformat() + 'Z',
            'entities': entities or [],
            'primitives': primitives or [],
            'research_sources': research_sources or [],
            'files': [],
            'feedback': feedback or []
        }
        approvals['domain_approvals'].append(domain_approval)
    else:
        domain_approval['status'] = status
        if entities:
            domain_approval['entities'] = entities
        if primitives:
            domain_approval['primitives'] = primitives
        if research_sources:
            domain_approval['research_sources'] = research_sources
        if feedback:
            domain_approval['feedback'] = feedback

    if status == 'approved':
        domain_approval['approved_at'] = datetime.utcnow().isoformat() + 'Z'
        domain_approval['approved_by'] = approved_by or 'unknown'

    # Write back
    with open(approval_file, 'w') as f:
        yaml.dump(approvals, f, default_flow_style=False, sort_keys=False)
