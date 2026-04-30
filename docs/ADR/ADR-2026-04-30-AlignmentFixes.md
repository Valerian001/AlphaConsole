# ADR-2026-04-30-AlignmentFixes: System Alignment & Responsiveness Fixes

## Status
Approved

## Context
The "Alpha System Alignment Review Report" (2026-04-30) identified critical blockers in mobile responsiveness and documentation sync (SEO/Typography). The current console layout is fixed for desktop and does not comply with the design tokens or typography specifications.

## Decision
1.  **Typography**: Replace `Geist Mono` with `JetBrains Mono` in `layout.tsx` to align with the technical specs.
2.  **Design Tokens**: Update `--border-muted` in `globals.css` from `rgba(255, 255, 255, 0.05)` to the spec-defined `#262626`.
3.  **SEO Metadata**: Update `layout.tsx` with accurate project metadata (Title: "AlphaConsole | Multi-Agent Orchestration", Description: "Advanced control plane for autonomous multi-agent systems").
4.  **Mobile Responsiveness**:
    *   Implement a hamburger menu for viewport widths `< 768px`.
    *   Convert the fixed sidebar into a collapsible/mobile-responsive component.
    *   Ensure the `UtilityPanel` is hidden or toggleable on mobile to preserve screen real estate.
5.  **Documentation Sync**: Ensure all changes are reflected in the `docs/` folder as per user rules.

## Consequences
*   **Pros**: Full alignment with architectural and design specs. Improved usability on mobile devices. Better SEO/Discovery.
*   **Cons**: Increased UI complexity to handle multiple layout states.
