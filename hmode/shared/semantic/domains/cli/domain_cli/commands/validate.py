"""Validate command - validate domain schema."""

from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.panel import Panel

from ..registry import Registry

console = Console()


REQUIRED_SECTIONS = ["domain", "entities"]
REQUIRED_DOMAIN_FIELDS = ["name", "version", "description"]


@click.command()
@click.argument("name")
@click.option("--strict", is_flag=True, help="Enable strict validation")
@click.pass_context
def validate(ctx: click.Context, name: str, strict: bool) -> None:
    """Validate a domain schema file.

    NAME is the domain name to validate.

    Checks:
    - Schema file exists and is valid YAML
    - Required sections present (domain, entities)
    - Domain metadata fields (name, version, description)
    - Entity definitions have required properties
    - created_at/updated_at timestamps present (strict mode)
    """
    registry: Registry = ctx.obj["registry"]
    domains_root: Path = ctx.obj["domains_root"]

    # Find schema file
    schema_path = registry.get_domain_schema_path(name)

    if schema_path is None:
        # Check if directory exists but no schema
        domain_dir = domains_root / name
        if domain_dir.exists():
            console.print(f"[red]No schema file found in '{name}/' directory[/red]")
            console.print("Expected: schema.yaml, models.yaml, or {name}.yaml")
        else:
            console.print(f"[red]Domain '{name}' not found[/red]")
        raise SystemExit(1)

    errors: list[str] = []
    warnings: list[str] = []

    # Parse YAML
    try:
        with open(schema_path) as f:
            schema = yaml.safe_load(f)
    except yaml.YAMLError as e:
        console.print(f"[red]Invalid YAML: {e}[/red]")
        raise SystemExit(1)

    if not isinstance(schema, dict):
        console.print("[red]Schema must be a YAML dictionary[/red]")
        raise SystemExit(1)

    # Check required sections
    for section in REQUIRED_SECTIONS:
        if section not in schema:
            errors.append(f"Missing required section: '{section}'")

    # Validate domain metadata
    if "domain" in schema:
        domain_meta = schema["domain"]
        if isinstance(domain_meta, dict):
            for field in REQUIRED_DOMAIN_FIELDS:
                if field not in domain_meta:
                    errors.append(f"Missing domain field: '{field}'")

            # Check name matches directory
            if domain_meta.get("name") != name:
                warnings.append(f"Domain name '{domain_meta.get('name')}' doesn't match directory '{name}'")

            # Check version format
            version = domain_meta.get("version", "")
            if version and not _is_valid_version(version):
                warnings.append(f"Version '{version}' doesn't follow semver format")

    # Validate entities
    if "entities" in schema:
        entities = schema["entities"]
        if isinstance(entities, dict):
            for entity_name, entity_def in entities.items():
                entity_errors = _validate_entity(entity_name, entity_def, strict)
                errors.extend(entity_errors)
        else:
            errors.append("'entities' must be a dictionary")

    # Validate enums (if present)
    if "enums" in schema:
        enums = schema["enums"]
        if enums and isinstance(enums, dict):
            for enum_name, enum_def in enums.items():
                if enum_def and isinstance(enum_def, dict):
                    if "values" not in enum_def:
                        warnings.append(f"Enum '{enum_name}' has no values defined")

    # Show results
    _show_results(name, schema_path, errors, warnings, strict)

    if errors:
        raise SystemExit(1)


def _validate_entity(name: str, definition: dict | None, strict: bool) -> list[str]:
    """Validate a single entity definition."""
    errors = []

    if definition is None:
        errors.append(f"Entity '{name}' has no definition")
        return errors

    if not isinstance(definition, dict):
        errors.append(f"Entity '{name}' must be a dictionary")
        return errors

    # Check for properties
    if "properties" not in definition:
        errors.append(f"Entity '{name}' has no properties")
        return errors

    props = definition.get("properties", {})
    if not isinstance(props, dict):
        errors.append(f"Entity '{name}' properties must be a dictionary")
        return errors

    # Strict mode: check for timestamps
    if strict:
        if "created_at" not in props:
            errors.append(f"Entity '{name}' missing 'created_at' property (strict mode)")
        if "updated_at" not in props:
            errors.append(f"Entity '{name}' missing 'updated_at' property (strict mode)")

    # Check each property has a type
    for prop_name, prop_def in props.items():
        if prop_def and isinstance(prop_def, dict):
            if "type" not in prop_def:
                errors.append(f"Entity '{name}.{prop_name}' missing 'type'")

    return errors


def _is_valid_version(version: str) -> bool:
    """Check if version follows semver format."""
    parts = version.split(".")
    if len(parts) != 3:
        return False
    return all(part.isdigit() for part in parts)


def _show_results(
    name: str,
    path: Path,
    errors: list[str],
    warnings: list[str],
    strict: bool,
) -> None:
    """Show validation results."""
    if errors:
        console.print(Panel(
            "\n".join(f"[red]✗[/red] {e}" for e in errors),
            title=f"[red]Validation Failed: {name}[/red]",
            expand=False
        ))
    elif warnings:
        console.print(Panel(
            "[green]✓ Schema valid[/green]\n\nWarnings:\n" +
            "\n".join(f"[yellow]⚠[/yellow] {w}" for w in warnings),
            title=f"[yellow]{name}[/yellow]",
            expand=False
        ))
    else:
        mode = " (strict)" if strict else ""
        console.print(Panel(
            f"[green]✓ Schema valid{mode}[/green]\n\n"
            f"File: {path.name}",
            title=f"[green]{name}[/green]",
            expand=False
        ))

    if warnings and not errors:
        console.print(f"\n[dim]{len(warnings)} warning(s)[/dim]")
