# UAV Deconflict — Remaining Work

## Current preserved milestone

The project currently has a verified strategic UAV deconfliction engine with:

- mission/flight models;
- trajectory interpolation;
- spatial and temporal conflict analysis;
- CLI execution;
- JSON reporting;
- static 2D visualization;
- animated 2D visualization;
- interactive 3D visualization support;
- automated tests.

## Verified acceptance

At the Kunj Vault preservation checkpoint:

- pytest: 16/16 PASS
- CLI end-to-end: PASS
- report.json generation: PASS
- demo_paths.png generation: PASS
- animation.mp4 generation: PASS
- scenario runner: exits successfully

## Known future work

This list is not a full product backlog.

When the project is resumed:

1. decide whether to rename the GitHub repository from `flybeast01`;
2. add real committed scenario JSON fixtures if scenario regression coverage is required;
3. review and validate `src/server.py` as part of the intended public scope;
4. evaluate packaging and dependency pinning;
5. review coordinate/reference-frame assumptions and document them clearly;
6. review scalability for larger multi-UAV traffic sets;
7. prepare polished demo evidence and portfolio case study;
8. execute the complete C01-C26 project-completion contract before declaring 100% completion.

## Preservation rule

Do not add unrelated feature work during the current Kunj Vault pass.
