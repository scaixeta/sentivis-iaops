---
name: kicad-schema-manager
description: KiCad Schema Manager
---

# KiCad Schema Manager Skill

## Overview
This skill empowers you to read, understand, parse, and manipulate KiCad project files (`.kicad_sch`, `.kicad_pcb`, and `.kicad_pro`), effectively bridging the gap between raw hardware design files and the agent's logic. You will use this skill to extract information about electronic components (Resistors, Capacitors, ICs, Connectors), generate reports based on the schematics, or even perform automated modifications (via scripts) when requested by the Solution Architect.

## Core Concepts & File Formats
You are working with KiCad 7/8+ files, which are S-Expression based. These files are human-readable and easily parseable texts, though they can be large.

### `.kicad_pro` (Project File)
This file holds the project's global settings, active libraries, and general configuration. It's usually a small JSON-like or S-Expression file detailing paths to schematic symbols and footprint libraries.
**Use case**: Checking project dependencies before parsing schematics.

### `.kicad_sch` (Schematic File)
This file contains the logical representation of the circuit.
- **Symbols (`symbol`)**: Represents components (e.g., `R` for Resistor, `C` for Capacitor, `U` for IC).
  - Every symbol has properties like `Reference` (R1, C1), `Value` (10k, 100nF), `Datasheet`, and `Footprint`.
- **Wires (`wire`) & Junctions (`junction`)**: Connect symbols together.
- **Labels (`label`, `global_label`)**: Name nets (wires) for easier connection across sheets.
**Use case**: Extracting a list of all components (BOM mapping) or tracing logic paths.

### `.kicad_pcb` (PCB File)
This file contains the physical layout of the circuit board.
- **Footprints (`footprint`)**: The physical representation of a component (e.g., `Resistor_SMD:R_0805_2012Metric`). Matches the `Reference` from the schematic (R1).
- **Tracks (`segment`, `arc`, `via`)**: The copper traces connecting footprints.
- **Zones (`zone`)**: Copper fills (usually for GND or VCC planes).
**Use case**: Verifying physical constraints, checking component placement, or generating precise manufacturing reports.

## Workflows & Scripts

### 1. Extracting Component Information (Parsing `.kicad_sch`)
When asked "Identify all components in this project" or "List all resistors":
1. Open the primary `.kicad_sch` file.
2. Search for the `(symbol ...)` blocks.
3. Extract the `Reference` (e.g., `(property "Reference" "R1" ...)`) and the `Value` (e.g., `(property "Value" "10k" ...)`).
4. Extract the `Footprint` property if available, to understand the physical package.
5. Compile this into a Markdown table or a structured list for the user.

### 2. Identifying Empty Values or Missing Footprints
This is crucial before sending a board to manufacturing.
1. Scan the schematic for any component where `Value` is exactly `~` or empty.
2. Scan for missing `Footprint` properties.
3. Generate an "Action Required" list for the user, highlighting components like `C5` that lack a value or a physical footprint.

### 3. Modifying Properties (Scripting Approach)
If the user asks to "Change all 10k resistors to 4.7k":
- **Avoid simple Find & Replace** if possible, as it might corrupt the S-expressions.
- **Write a quick Python script** to parse the schematic (using regex or specialized libraries like `kicad-python` or `sexpdata` if available), locate instances where `Reference` starts with `R` AND `Value` is `10k`, change the `Value` to `4.7k`, and save the file.
- **Always backup** the file before running a modification script (e.g., `cp project.kicad_sch project.kicad_sch.bak`).

### 4. PCB Footprint Analysis
If the user asks "Are all components SMD?":
1. Open the `.kicad_pcb` file.
2. Scan the `(footprint ...)` blocks.
3. Look at the footprint names/paths (e.g., `Resistor_SMD:` vs `Resistor_THT:`).
4. Summarize the percentage or list the through-hole (THT) components versus Surface Mount (SMD) components.

### 5. Orchestration (Docker Integration)
Remember that to generate formal BOMs, Netlists, or DRC reports from these files, you should use the `kicad-cli-automation` skill via Docker, rather than parsing it manually. Manual parsing is for quick lookups, specific component modifications, or generating custom structural reports (like "List all ICs and their datasheets").
