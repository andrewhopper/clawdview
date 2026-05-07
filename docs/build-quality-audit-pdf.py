#!/usr/bin/env python3
"""Generate Flight Director Code Quality Audit report PDF for reMarkable review."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from datetime import datetime

OUTPUT = "/home/user/clawdview/docs/flight-director-quality-audit.pdf"

# ── Audit findings (gathered by running 7 audits over clawdview-tool/) ──
PROJECT = "clawdview"
AUDIT_DATE = datetime.now().strftime("%Y-%m-%d")
LANGUAGES = "TypeScript, JavaScript, React"
FILE_COUNT = 38
MACHINE = "@andrewhopper/fd v0.1.3 — code-quality-audit.yaml"

SCORES = [
    ("1. No Defaults",         5, "C", 0, 6),
    ("2. Config Abstracted",   4, "D", 1, 2),
    ("3. Simplicity",          6, "C", 1, 1),
    ("4. Strongly Typed",      6, "C", 1, 3),
    ("5. Decoupled",           8, "B", 0, 1),
    ("6. DRY",                 5, "C", 1, 2),
    ("7. Architectural",       7, "B", 0, 2),
]

OVERALL = round(sum(s[1] for s in SCORES) / len(SCORES), 1)
OVERALL_GRADE = "C"

FINDINGS = [
    # (id, audit, severity, file:line, title, detail, suggested_fix, effort)
    ("F-01", "No Defaults", "WARNING",
     "clawdview-tool/src/server/server.ts:32-33",
     "Magic default port and host via || fallback",
     "this.port = options.port || 3333; this.host = options.host || 'localhost'. "
     "These silently provide defaults instead of failing fast. The same magic literal "
     "3333 reappears in server.ts:187, tunnel-service.ts:40, bin/clawdview.js:35, and "
     "bin/cview.js:111.",
     "Extract DEFAULT_PORT and DEFAULT_HOST to src/server/config.ts. Use ?? not ||. "
     "Centralize so the literal 3333 lives in exactly one place.",
     "Quick win (~20 min)"),

    ("F-02", "No Defaults", "WARNING",
     "clawdview-tool/src/server/server.ts:35",
     "Implicit fallback to process.cwd()",
     "options.watchDir || process.cwd(). The fallback is invisible to callers; a "
     "missing watchDir silently watches whatever the cwd happens to be.",
     "Make watchDir required, or log explicitly when defaulting. Move to config module.",
     "Quick win (~10 min)"),

    ("F-03", "No Defaults", "WARNING",
     "clawdview-tool/src/server/server.ts:41, 162",
     "Hardcoded CORS origins duplicated",
     "Two locations build the same CORS origin array literal "
     "[`http://localhost:${port}`, `http://127.0.0.1:${port}`]. Magic strings, repeated.",
     "Extract buildCorsOrigins(port) helper or move to a config object.",
     "Quick win (~15 min)"),

    ("F-04", "No Defaults", "INFO",
     "clawdview-tool/src/server/services/python-executor.ts:5-9",
     "Tuning constants embedded in service module",
     "RATE_LIMIT_COUNT=5, RATE_LIMIT_WINDOW=60000, TIMEOUT=30000, MAX_CODE_SIZE=50000 "
     "are named constants (good) but live in the service file itself. They control "
     "operational policy, not service mechanics.",
     "Move to a config module so an operator can tune them without touching code.",
     "Medium (~1 hr)"),

    ("F-05", "Config Abstracted", "CRITICAL",
     "clawdview-tool/src/server/",
     "No dedicated config module; no startup validation",
     "process.env.PORT is read inline in server.ts:187. There is no config.ts, no "
     "schema (zod/valibot/pydantic-style), no startup validation. Adding new env "
     "vars will scatter env reads across the codebase.",
     "Create src/server/config.ts that reads + validates all env vars at startup "
     "with a zod schema and exports a typed config object.",
     "Medium (~2 hrs)"),

    ("F-06", "Config Abstracted", "WARNING",
     "clawdview-tool/src/server/services/python-executor.ts",
     "Per-service constants instead of layered config",
     "Operational limits (timeout, rate limit, max size) are baked into the python "
     "executor. Cannot vary by environment (dev/test/prod).",
     "Source these from the central config module created in F-05.",
     "Medium (~30 min, after F-05)"),

    ("F-07", "Simplicity", "CRITICAL",
     "clawdview-tool/src/client/components/FileTree.tsx",
     "File length 660 lines (threshold 500)",
     "FileTree.tsx mixes view-mode logic, search, collapse state, multi-dir add/remove "
     "UI, file-type grouping, and drag/keyboard interaction in one component.",
     "Decompose: extract <FileTreeSearch>, <ViewModeToggle>, <WatchedDirsBar>, "
     "and a useFileTreeState() hook. Target <300 lines per file.",
     "Structural (1-2 days)"),

    ("F-08", "Simplicity", "WARNING",
     "clawdview-tool/src/client/App.tsx",
     "File length 449 lines (threshold 300)",
     "App.tsx owns routing-ish state, theme, preferences glue, file fetch, error "
     "handling, and the highlight.js bridge.",
     "Extract data-fetch logic into a useCurrentFile() hook; move the hljs bridge "
     "to a dedicated module.",
     "Medium (~3 hrs)"),

    ("F-09", "Strongly Typed", "CRITICAL",
     "12 occurrences across 8 files",
     "Pervasive use of `any`",
     "Notable cases: App.tsx:25 `declare const hljs: any`; App.tsx:85 `(data as any).error`; "
     "tunnel-service.ts:90,111 `let localtunnel: any` for dynamic imports; six "
     "`catch (e: any)` blocks (format-routes, execute-routes, file-routes, App.tsx, "
     "JsonRenderer, ReactRenderer).",
     "(a) Use `@types/highlight.js` instead of `declare const hljs: any`. "
     "(b) Replace `catch (e: any)` with `catch (e: unknown)` plus a narrow helper "
     "`toErrorMessage(e: unknown): string`. (c) Type localtunnel/ngrok via their "
     "@types packages or hand-rolled minimal interfaces.",
     "Medium (~3 hrs)"),

    ("F-10", "Strongly Typed", "WARNING",
     "clawdview-tool/src/client/App.tsx:85",
     "Lazy type assertion to bypass the type system",
     "`(data as any).error || 'Failed to load file'` — silences the compiler but "
     "loses runtime safety.",
     "Define a typed FileLoadResponse interface and validate the payload shape.",
     "Quick win (~20 min)"),

    ("F-11", "Strongly Typed", "INFO",
     "clawdview-tool/tsconfig.app.json",
     "noUnusedLocals / noUnusedParameters disabled",
     "Strict mode is on, but `noUnusedLocals` and `noUnusedParameters` are explicitly "
     "set to false in tsconfig.app.json — dead code accumulates silently.",
     "Flip both to true and clean up the resulting warnings.",
     "Quick win (~30 min)"),

    ("F-12", "Decoupled", "INFO",
     "clawdview-tool/src/server/",
     "Layered architecture is intact",
     "No circular imports detected. routes/ → services/ → shared/ flows correctly. "
     "tunnel-service.ts uses dynamic require() for optional deps — acceptable.",
     "No action required. Document the layering in CLAUDE.md to lock it in.",
     "Quick win (~15 min, optional)"),

    ("F-13", "DRY", "CRITICAL",
     "clawdview-tool/bin/clawdview.js (210 LOC) + bin/cview.js (134 LOC)",
     "Two near-duplicate CLI entry points",
     "Both files implement the same `start` command with overlapping option parsing, "
     "tunnel setup, and host/port logic. The diff is mostly cosmetic.",
     "Consolidate into a single CLI module that both bin shims delegate to. Each "
     "shim becomes ~3 lines.",
     "Medium (~2 hrs)"),

    ("F-14", "DRY", "WARNING",
     "clawdview-tool/src/server/server.ts:41 + 162",
     "CORS origin construction duplicated",
     "Same array literal built twice. Already covered structurally by F-03 fix.",
     "Resolved by F-03.",
     "Quick win (folded into F-03)"),

    ("F-15", "DRY", "WARNING",
     "format-routes.ts:25, execute-routes.ts:28, file-routes.ts:52,65, App.tsx:145, "
     "JsonRenderer.tsx:11, ReactRenderer.tsx:42",
     "Repeated `catch (e: any)` + `e.message` pattern",
     "Six+ catch blocks that all do the same coercion to a string error message.",
     "Extract `toErrorMessage(e: unknown): string` into shared/errors.ts (also "
     "resolves part of F-09).",
     "Quick win (~20 min)"),

    ("F-16", "Architectural", "WARNING",
     "Repository root (README.md, CLAUDE.md)",
     "Architectural pattern is not declared",
     "The codebase follows an implicit layered/MVC-ish pattern (routes → services → "
     "shared types) and React component-based UI, but no document spells it out. "
     "New contributors have to reverse-engineer it.",
     "Add an ARCHITECTURE.md (or section in CLAUDE.md) stating: server is layered "
     "(routes/services/shared); client is component-based; cross-cutting concerns "
     "(logging, errors) live in shared/.",
     "Quick win (~45 min)"),

    ("F-17", "Architectural", "INFO",
     "clawdview-tool/src/server/",
     "Naming and boundaries are consistent",
     "Services suffixed *Service, route factories prefixed `create*Routes`, shared "
     "types in shared/. Boundaries are clean.",
     "No action.",
     "—"),
]


def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        title="Flight Director Quality Audit — clawdview",
        author="Flight Director (@andrewhopper/fd)",
    )

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=20, leading=24,
                        spaceAfter=10, textColor=colors.black)
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=14, leading=18,
                        spaceBefore=14, spaceAfter=6, textColor=colors.black)
    h3 = ParagraphStyle("h3", parent=styles["Heading3"], fontSize=12, leading=15,
                        spaceBefore=8, spaceAfter=4, textColor=colors.black)
    body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=10.5,
                          leading=14, alignment=TA_LEFT)
    mono = ParagraphStyle("mono", parent=body, fontName="Courier", fontSize=9.5,
                          leading=12, textColor=colors.HexColor("#222"))
    label = ParagraphStyle("label", parent=body, fontSize=9, leading=11,
                           textColor=colors.HexColor("#444"))
    sev_critical = ParagraphStyle("sev_c", parent=body, fontName="Helvetica-Bold",
                                  fontSize=10, textColor=colors.HexColor("#000"))

    story = []

    # ── Cover ─────────────────────────────────────────
    story.append(Paragraph("Flight Director", h1))
    story.append(Paragraph("Code Quality Audit Report", h2))
    story.append(Spacer(1, 0.15 * inch))

    cover = [
        ["Project", PROJECT],
        ["Audit date", AUDIT_DATE],
        ["Languages", LANGUAGES],
        ["Source files", str(FILE_COUNT)],
        ["Machine", MACHINE],
        ["Branch", "claude/flight-control-quality-audit-wKwmq"],
    ]
    t = Table(cover, colWidths=[1.4 * inch, 5.4 * inch])
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#ccc")),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.25 * inch))

    # ── Score card ────────────────────────────────────
    story.append(Paragraph("Score card", h2))
    score_rows = [["Principle", "Score", "Grade", "Crit", "Warn"]]
    for name, sc, gr, c, w in SCORES:
        score_rows.append([name, f"{sc}/10", gr, str(c), str(w)])
    score_rows.append(["OVERALL", f"{OVERALL}/10", OVERALL_GRADE,
                       str(sum(r[3] for r in [(None, None, None, c, w) for *_, c, w in SCORES])),
                       str(sum(r[4] for r in [(None, None, None, c, w) for *_, c, w in SCORES]))])
    sc_table = Table(score_rows, colWidths=[2.6 * inch, 0.9 * inch, 0.9 * inch,
                                             0.7 * inch, 0.7 * inch])
    sc_table.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10),
        ("FONT", (0, 1), (-1, -2), "Helvetica", 10),
        ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 11),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eee")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f4f4f4")),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#bbb")),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(sc_table)
    story.append(Spacer(1, 0.18 * inch))

    story.append(Paragraph(
        f"<b>Overall: {OVERALL}/10 ({OVERALL_GRADE}).</b> Solid bones — the layered "
        "architecture is clean and there are no circular imports. Headline issues are "
        "(1) absent config layer, (2) two oversized files, (3) pervasive <font face='Courier'>any</font>, "
        "and (4) duplicated CLI entry points.", body))
    story.append(Spacer(1, 0.1 * inch))

    # ── How to use ─────────────────────────────────────
    story.append(Paragraph("How to use this report", h2))
    story.append(Paragraph(
        "Each finding has three approval boxes — <b>Approve</b> (do it), "
        "<b>Defer</b> (track but skip for now), <b>Reject</b> (won't do). "
        "Tick one and write a comment in the lined area. I'll process your "
        "annotations after you sync the PDF back from your reMarkable.", body))
    story.append(PageBreak())

    # ── Findings ───────────────────────────────────────
    story.append(Paragraph("Findings", h1))
    story.append(Spacer(1, 0.1 * inch))

    for fid, audit, sev, loc, title, detail, fix, effort in FINDINGS:
        block = []
        # header strip
        sev_color = {
            "CRITICAL": colors.HexColor("#000"),
            "WARNING":  colors.HexColor("#333"),
            "INFO":     colors.HexColor("#666"),
        }[sev]

        header = Table(
            [[f"{fid}  ·  {sev}", audit]],
            colWidths=[3.5 * inch, 3.3 * inch],
        )
        header.setStyle(TableStyle([
            ("FONT", (0, 0), (0, 0), "Helvetica-Bold", 12),
            ("FONT", (1, 0), (1, 0), "Helvetica", 10),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("TEXTCOLOR", (0, 0), (0, 0), sev_color),
            ("TEXTCOLOR", (1, 0), (1, 0), colors.HexColor("#444")),
            ("LINEBELOW", (0, 0), (-1, -1), 1.2, colors.black),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        block.append(header)
        block.append(Spacer(1, 0.06 * inch))

        block.append(Paragraph(f"<b>{title}</b>", h3))
        block.append(Paragraph(f"<font face='Courier' size='9'>{loc}</font>", mono))
        block.append(Spacer(1, 0.04 * inch))
        block.append(Paragraph(f"<b>What:</b> {detail}", body))
        block.append(Spacer(1, 0.04 * inch))
        block.append(Paragraph(f"<b>Suggested fix:</b> {fix}", body))
        block.append(Paragraph(f"<b>Effort:</b> {effort}", label))
        block.append(Spacer(1, 0.08 * inch))

        # ── Approval / comment area ──
        approval_row = Table(
            [[
                "☐  Approve",
                "☐  Defer",
                "☐  Reject",
            ]],
            colWidths=[2.27 * inch, 2.27 * inch, 2.26 * inch],
        )
        approval_row.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, -1), "Helvetica", 11),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#888")),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#bbb")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
        ]))
        block.append(approval_row)
        block.append(Spacer(1, 0.05 * inch))

        # comment lines (4 ruled lines, plenty of room for a stylus)
        block.append(Paragraph("<b>Comments / next step:</b>", label))
        block.append(Spacer(1, 0.02 * inch))
        line_rows = [[""] for _ in range(4)]
        comment_box = Table(line_rows, colWidths=[6.8 * inch], rowHeights=[0.32 * inch] * 4)
        comment_box.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#999")),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        block.append(comment_box)
        block.append(Spacer(1, 0.25 * inch))

        story.append(KeepTogether(block))

    # ── Sign-off page ──────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Sign-off", h1))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(
        "Once you've gone through the findings, sign here so I know which version "
        "of the report I'm acting on. I'll then bundle every Approved item into a "
        "single follow-up branch.", body))
    story.append(Spacer(1, 0.4 * inch))

    sig_lines = [["Reviewer name:", ""], ["Date:", ""], ["Signature:", ""]]
    sig_table = Table(sig_lines, colWidths=[1.4 * inch, 5.4 * inch],
                      rowHeights=[0.55 * inch] * 3)
    sig_table.setStyle(TableStyle([
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 11),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LINEBELOW", (1, 0), (1, -1), 0.5, colors.HexColor("#666")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 0.5 * inch))

    story.append(Paragraph("Aggregate decision (optional):", h3))
    story.append(Spacer(1, 0.1 * inch))
    agg = Table(
        [["☐  Approve all quick wins", "☐  Approve all critical only", "☐  Hold — discuss first"]],
        colWidths=[2.27 * inch, 2.27 * inch, 2.26 * inch],
    )
    agg.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 11),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#888")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#bbb")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(agg)

    doc.build(story)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
