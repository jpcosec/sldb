---
id: track-automation-and-external-surfaces
status: proposed
summary: Bundle effects, capability controls, agent surfaces, and optional UI surfaces after core product authority boundaries are stable.
tags:
- workspace:desk
- artifact:track
- system:sldb
history:
- "2026-07-29: drafted as interstitial planning layer between features and promotable tasks."
references:
- interfaces.md
- libraries_core.md
- docs/architecture/spec2viz/target-runtime.yml
items:
- desk/drawer/features/feature-effect-system-and-automation.md
- desk/drawer/features/feature-security-threat-model-and-capabilities.md
- desk/drawer/features/feature-agent-and-mcp-surface.md
- desk/drawer/features/feature-desktop-or-visual-ui-surface.md
---

# Automation and external surfaces track

## Goal

Group externally visible and externally acting product surfaces that depend on stable capability and authority boundaries.

## Promotion order inside the track

1. Effect system and automation
2. Security threat model and capabilities
3. Agent and MCP surface
4. Desktop or visual UI surface

## Needs design or grounding before promotion

- exact effect-safety bar before agent/UI surfaces
- read vs write capability policy for external consumers
- whether a desktop UI remains committed scope
