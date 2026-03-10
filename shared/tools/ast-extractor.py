#!/usr/bin/env python3
"""
AST-based code signature extractor using tree-sitter.

Extracts only the public API surface:
- Class names and docstrings
- Function/method signatures (not bodies)
- Type definitions
- Exports

Filters out:
- Implementation details
- Helper/private functions
- Import statements (configurable)
- Comments (except docstrings)
"""

from typing import Optional
from pathlib import Path

# Try to import tree-sitter, gracefully degrade if not available
try:
    import tree_sitter_python as tspython
    import tree_sitter_javascript as tsjavascript
    import tree_sitter_typescript as tstypescript
    from tree_sitter import Language, Parser
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False


def is_private_name(name: str) -> bool:
    """Check if name suggests private/internal (underscore prefix, lowercase helper)."""
    if name.startswith("_"):
        return True
    # Common helper function patterns
    helper_patterns = {"helper", "util", "internal", "impl", "do_", "handle_"}
    return any(p in name.lower() for p in helper_patterns)


def extract_python_signatures(content: str, include_imports: bool = False) -> str:
    """Extract Python signatures using tree-sitter AST."""
    if not TREE_SITTER_AVAILABLE:
        return _fallback_extract(content, "python")

    try:
        PY_LANGUAGE = Language(tspython.language())
        parser = Parser(PY_LANGUAGE)
        tree = parser.parse(bytes(content, "utf8"))

        signatures = []

        def extract_docstring(node) -> Optional[str]:
            """Extract docstring from first child if present."""
            for child in node.children:
                if child.type == "block":
                    for block_child in child.children:
                        if block_child.type == "expression_statement":
                            expr = block_child.children[0] if block_child.children else None
                            if expr and expr.type == "string":
                                doc = content[expr.start_byte:expr.end_byte]
                                # Truncate long docstrings
                                if len(doc) > 200:
                                    doc = doc[:200] + '..."""'
                                return doc
                    break
            return None

        def get_signature_line(node) -> str:
            """Get just the signature line (first line of definition)."""
            start = node.start_byte
            # Find end of first line or colon
            text = content[start:]
            colon_pos = text.find(":")
            newline_pos = text.find("\n")
            if colon_pos != -1:
                end = start + colon_pos + 1
            elif newline_pos != -1:
                end = start + newline_pos
            else:
                end = node.end_byte
            return content[start:end].strip()

        def walk(node, depth=0):
            # Module-level docstring
            if node.type == "module":
                for child in node.children:
                    if child.type == "expression_statement":
                        expr = child.children[0] if child.children else None
                        if expr and expr.type == "string":
                            doc = content[expr.start_byte:expr.end_byte]
                            if len(doc) > 300:
                                doc = doc[:300] + '..."""'
                            signatures.append(f"# Module docstring:\n{doc}\n")
                            break
                    elif child.type not in ("comment",):
                        break

            # Imports (optional)
            if include_imports and node.type in ("import_statement", "import_from_statement"):
                signatures.append(content[node.start_byte:node.end_byte])

            # Class definitions
            elif node.type == "class_definition":
                name_node = node.child_by_field_name("name")
                name = content[name_node.start_byte:name_node.end_byte] if name_node else "?"

                if not is_private_name(name):
                    sig = get_signature_line(node)
                    signatures.append(f"\n{sig}")

                    docstring = extract_docstring(node)
                    if docstring:
                        signatures.append(f"    {docstring}")

                    # Extract method signatures
                    for child in node.children:
                        if child.type == "block":
                            for block_child in child.children:
                                if block_child.type == "function_definition":
                                    method_name_node = block_child.child_by_field_name("name")
                                    method_name = content[method_name_node.start_byte:method_name_node.end_byte] if method_name_node else "?"

                                    # Skip private methods except __init__, __call__, etc.
                                    if method_name.startswith("_") and not method_name.startswith("__"):
                                        continue

                                    method_sig = get_signature_line(block_child)
                                    # Indent method signatures
                                    signatures.append(f"    {method_sig}")

            # Decorated definitions (functions/classes with decorators)
            elif node.type == "decorated_definition":
                # Get the decorator(s)
                decorators = []
                for child in node.children:
                    if child.type == "decorator":
                        dec_text = content[child.start_byte:child.end_byte].strip()
                        decorators.append(dec_text)
                    elif child.type == "function_definition":
                        name_node = child.child_by_field_name("name")
                        name = content[name_node.start_byte:name_node.end_byte] if name_node else "?"

                        if not is_private_name(name):
                            # Add decorators
                            for dec in decorators:
                                signatures.append(f"\n{dec}")
                            sig = get_signature_line(child)
                            signatures.append(sig)

                            docstring = extract_docstring(child)
                            if docstring:
                                signatures.append(f"    {docstring}")
                    elif child.type == "class_definition":
                        # Handle decorated classes
                        name_node = child.child_by_field_name("name")
                        name = content[name_node.start_byte:name_node.end_byte] if name_node else "?"

                        if not is_private_name(name):
                            for dec in decorators:
                                signatures.append(f"\n{dec}")
                            sig = get_signature_line(child)
                            signatures.append(sig)

            # Top-level function definitions (non-decorated)
            elif node.type == "function_definition" and depth <= 1:
                # Check parent isn't a decorated_definition or class
                parent_type = node.parent.type if node.parent else None
                if parent_type not in ("decorated_definition", "block"):
                    name_node = node.child_by_field_name("name")
                    name = content[name_node.start_byte:name_node.end_byte] if name_node else "?"

                    if not is_private_name(name):
                        sig = get_signature_line(node)
                        signatures.append(f"\n{sig}")

                        docstring = extract_docstring(node)
                        if docstring:
                            signatures.append(f"    {docstring}")

            # Type aliases and assignments (often constants/config)
            elif node.type == "type_alias_statement":
                signatures.append(content[node.start_byte:node.end_byte])

            # Global assignments that look like constants (ALL_CAPS)
            elif node.type == "expression_statement" and depth <= 1:
                text = content[node.start_byte:node.end_byte].strip()
                if "=" in text:
                    var_name = text.split("=")[0].strip()
                    # Check if it's a constant (ALL_CAPS) or dataclass
                    if var_name.isupper() or var_name.startswith("@"):
                        if len(text) < 100:
                            signatures.append(text)

            # Recurse into children
            for child in node.children:
                walk(child, depth + 1)

        walk(tree.root_node)
        return "\n".join(signatures)

    except Exception as e:
        return f"# AST extraction failed: {e}\n" + _fallback_extract(content, "python")


def extract_javascript_signatures(content: str, include_imports: bool = False) -> str:
    """Extract JavaScript/TypeScript signatures using tree-sitter AST."""
    if not TREE_SITTER_AVAILABLE:
        return _fallback_extract(content, "javascript")

    try:
        JS_LANGUAGE = Language(tsjavascript.language())
        parser = Parser(JS_LANGUAGE)
        tree = parser.parse(bytes(content, "utf8"))

        signatures = []

        def get_jsdoc(node) -> Optional[str]:
            """Get preceding JSDoc comment if present."""
            # Look for comment node before this one
            if node.prev_sibling and node.prev_sibling.type == "comment":
                comment = content[node.prev_sibling.start_byte:node.prev_sibling.end_byte]
                if comment.startswith("/**"):
                    if len(comment) > 200:
                        comment = comment[:200] + "...*/"
                    return comment
            return None

        def walk(node, depth=0):
            # Imports/exports
            if node.type in ("import_statement", "export_statement"):
                if include_imports or node.type == "export_statement":
                    line = content[node.start_byte:node.end_byte]
                    # Truncate long exports
                    if len(line) > 150:
                        line = line[:150] + "..."
                    signatures.append(line)

            # Function declarations
            elif node.type in ("function_declaration", "generator_function_declaration"):
                name_node = node.child_by_field_name("name")
                name = content[name_node.start_byte:name_node.end_byte] if name_node else "?"

                if not is_private_name(name):
                    jsdoc = get_jsdoc(node)
                    if jsdoc:
                        signatures.append(jsdoc)

                    # Get just signature (up to opening brace)
                    text = content[node.start_byte:node.end_byte]
                    brace_pos = text.find("{")
                    if brace_pos != -1:
                        sig = text[:brace_pos].strip()
                    else:
                        sig = text.split("\n")[0]
                    signatures.append(sig)

            # Class declarations
            elif node.type == "class_declaration":
                name_node = node.child_by_field_name("name")
                name = content[name_node.start_byte:name_node.end_byte] if name_node else "?"

                if not is_private_name(name):
                    jsdoc = get_jsdoc(node)
                    if jsdoc:
                        signatures.append(jsdoc)

                    # Class header
                    text = content[node.start_byte:node.end_byte]
                    brace_pos = text.find("{")
                    if brace_pos != -1:
                        header = text[:brace_pos].strip()
                    else:
                        header = text.split("\n")[0]
                    signatures.append(f"\n{header} {{")

                    # Extract method signatures from class body
                    body = node.child_by_field_name("body")
                    if body:
                        for child in body.children:
                            if child.type == "method_definition":
                                method_name_node = child.child_by_field_name("name")
                                method_name = content[method_name_node.start_byte:method_name_node.end_byte] if method_name_node else "?"

                                if not method_name.startswith("_"):
                                    method_text = content[child.start_byte:child.end_byte]
                                    brace_pos = method_text.find("{")
                                    if brace_pos != -1:
                                        method_sig = method_text[:brace_pos].strip()
                                    else:
                                        method_sig = method_text.split("\n")[0]
                                    signatures.append(f"  {method_sig}")

                    signatures.append("}")

            # Arrow functions assigned to const (common pattern)
            elif node.type == "lexical_declaration":
                text = content[node.start_byte:node.end_byte]
                if "=>" in text or "function" in text:
                    # It's a function assignment
                    first_line = text.split("\n")[0]
                    if not any(p in first_line.lower() for p in ["_", "helper", "internal"]):
                        # Truncate if too long
                        if len(first_line) > 100:
                            first_line = first_line[:100] + "..."
                        signatures.append(first_line)

            # Interface/type definitions (TypeScript in .js with JSDoc)
            elif node.type == "comment":
                text = content[node.start_byte:node.end_byte]
                if "@typedef" in text or "@interface" in text:
                    if len(text) > 200:
                        text = text[:200] + "...*/"
                    signatures.append(text)

            for child in node.children:
                walk(child, depth + 1)

        walk(tree.root_node)
        return "\n".join(signatures)

    except Exception as e:
        return f"// AST extraction failed: {e}\n" + _fallback_extract(content, "javascript")


def extract_typescript_signatures(content: str, include_imports: bool = False) -> str:
    """Extract TypeScript signatures using tree-sitter AST."""
    if not TREE_SITTER_AVAILABLE:
        return _fallback_extract(content, "typescript")

    try:
        TS_LANGUAGE = Language(tstypescript.language_typescript())
        parser = Parser(TS_LANGUAGE)
        tree = parser.parse(bytes(content, "utf8"))

        signatures = []

        def walk(node, depth=0):
            # Imports/exports
            if node.type in ("import_statement", "export_statement"):
                if include_imports or node.type == "export_statement":
                    line = content[node.start_byte:node.end_byte]
                    if len(line) > 150:
                        line = line[:150] + "..."
                    signatures.append(line)

            # Interface declarations
            elif node.type == "interface_declaration":
                name_node = node.child_by_field_name("name")
                name = content[name_node.start_byte:name_node.end_byte] if name_node else "?"

                # Get full interface (usually short enough)
                text = content[node.start_byte:node.end_byte]
                if len(text) > 500:
                    # Truncate long interfaces
                    text = text[:500] + "\n  ...\n}"
                signatures.append(f"\n{text}")

            # Type aliases
            elif node.type == "type_alias_declaration":
                text = content[node.start_byte:node.end_byte]
                if len(text) > 200:
                    text = text[:200] + "..."
                signatures.append(text)

            # Function declarations
            elif node.type in ("function_declaration", "function_signature"):
                name_node = node.child_by_field_name("name")
                name = content[name_node.start_byte:name_node.end_byte] if name_node else "?"

                if not is_private_name(name):
                    text = content[node.start_byte:node.end_byte]
                    brace_pos = text.find("{")
                    if brace_pos != -1:
                        sig = text[:brace_pos].strip()
                    else:
                        sig = text.split("\n")[0]
                    signatures.append(f"\n{sig}")

            # Class declarations
            elif node.type == "class_declaration":
                name_node = node.child_by_field_name("name")
                name = content[name_node.start_byte:name_node.end_byte] if name_node else "?"

                if not is_private_name(name):
                    text = content[node.start_byte:node.end_byte]
                    brace_pos = text.find("{")
                    if brace_pos != -1:
                        header = text[:brace_pos].strip()
                    else:
                        header = text.split("\n")[0]
                    signatures.append(f"\n{header} {{")

                    # Get method signatures
                    body = node.child_by_field_name("body")
                    if body:
                        for child in body.children:
                            if child.type in ("method_definition", "method_signature", "public_field_definition"):
                                child_text = content[child.start_byte:child.end_byte]
                                # Check if private
                                if child_text.strip().startswith("private") or child_text.strip().startswith("_"):
                                    continue
                                brace_pos = child_text.find("{")
                                if brace_pos != -1:
                                    child_sig = child_text[:brace_pos].strip()
                                else:
                                    child_sig = child_text.split("\n")[0].strip()
                                if len(child_sig) > 100:
                                    child_sig = child_sig[:100] + "..."
                                signatures.append(f"  {child_sig}")

                    signatures.append("}")

            # Enum declarations
            elif node.type == "enum_declaration":
                text = content[node.start_byte:node.end_byte]
                if len(text) > 300:
                    text = text[:300] + "\n  ...\n}"
                signatures.append(f"\n{text}")

            for child in node.children:
                walk(child, depth + 1)

        walk(tree.root_node)
        return "\n".join(signatures)

    except Exception as e:
        return f"// AST extraction failed: {e}\n" + _fallback_extract(content, "typescript")


def _fallback_extract(content: str, lang: str) -> str:
    """Fallback heuristic extraction when tree-sitter unavailable."""
    lines = content.split("\n")
    important = []

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and pure comments
        if not stripped or stripped.startswith("#") and not stripped.startswith("# "):
            continue

        # Keep class/function definitions
        if any(stripped.startswith(kw) for kw in (
            "class ", "def ", "async def ",  # Python
            "function ", "async function ", "export ", "interface ", "type ",  # JS/TS
            "pub fn ", "fn ", "struct ", "enum ", "impl ",  # Rust
            "func ",  # Go
        )):
            important.append(line)

        # Keep decorators
        elif stripped.startswith("@"):
            important.append(line)

        # Truncate at reasonable length
        if len(important) >= 60:
            important.append("# ... (truncated)")
            break

    return "\n".join(important)


def extract_signatures(path: Path, content: str, include_imports: bool = False) -> str:
    """Extract signatures based on file extension."""
    suffix = path.suffix.lower()

    if suffix == ".py":
        return extract_python_signatures(content, include_imports)
    elif suffix in (".js", ".jsx", ".mjs"):
        return extract_javascript_signatures(content, include_imports)
    elif suffix in (".ts", ".tsx", ".mts"):
        return extract_typescript_signatures(content, include_imports)
    else:
        # Fallback for other languages
        return _fallback_extract(content, "unknown")


def get_extractor_status() -> dict:
    """Return status of AST extractors."""
    return {
        "tree_sitter_available": TREE_SITTER_AVAILABLE,
        "supported_languages": ["python", "javascript", "typescript"] if TREE_SITTER_AVAILABLE else [],
        "fallback_languages": ["python", "javascript", "typescript", "rust", "go"],
    }
