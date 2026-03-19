---
name: kicad-cli-automation
description: KiCad CLI Automation
---

# KiCad CLI Automation Skill

## Overview
This skill teaches you how to orchestrate the `kicad-cli` tool using the local Docker environment to automate essential KiCad tasks without opening the GUI. You will use this skill when executing operations like exporting schematics, generating BOMs, running DRC checks, and exporting manufacturing files (Gerber/Drill) or 3D models.

## Pre-requisites & Environment
- **Docker Command**: All KiCad CLI commands MUST be executed through the Docker container to ensure the correct environment and dependencies.
- **Project Structure**: Always locate the `.kicad_pro`, `.kicad_sch`, and `.kicad_pcb` files within the workspace before running commands.
- **Output Directories**: Unless specified otherwise, save all exported files to an `exports/` folder within the project directory.

## Core Commands & Workflows

### 1. Schematic Operations (`kicad-cli sch`)
Used for operations on `.kicad_sch` files.

#### PDF Export
Generates a PDF of the schematic. Useful for documentation and review.
```bash
# Example
docker run --rm -v $(pwd):/workdir kicad_image kicad-cli sch export pdf --output exports/schematic.pdf project_name.kicad_sch
```

#### BOM (Bill of Materials) Export
Extracts the BOM in XML or CSV format.
```bash
# Example (XML)
docker run --rm -v $(pwd):/workdir kicad_image kicad-cli sch export bom --output exports/bom.xml project_name.kicad_sch

# Example (CSV/TXT using BOM scripts - might require specific python scripts within the container/workspace)
docker run --rm -v $(pwd):/workdir kicad_image kicad-cli sch export netlist --format kicadxml --output project.xml project_name.kicad_sch
```

#### Schematic DRC (Design Rule Check) / ERC (Electrical Rules Check)
Verifies if the schematic has any electrical errors.
```bash
# Example
docker run --rm -v $(pwd):/workdir kicad_image kicad-cli sch drc --output exports/erc_report.txt project_name.kicad_sch
```

### 2. PCB Operations (`kicad-cli pcb`)
Used for operations on `.kicad_pcb` files.

#### Gerber Export (Manufacturing)
Exports Gerber files needed by PCB manufacturers (JLCPCB, PCBWay, etc.).
```bash
# Example
docker run --rm -v $(pwd):/workdir kicad_image kicad-cli pcb export gerber --output exports/gerbers/ project_name.kicad_pcb
```

#### Drill Files Export
Exports drill (Excellon) files, usually required alongside Gerbers.
```bash
# Example
docker run --rm -v $(pwd):/workdir kicad_image kicad-cli pcb export drill --output exports/gerbers/ project_name.kicad_pcb
```

#### PCB PDF Export
Generates a PDF of the PCB layers.
```bash
# Example (exporting all layers)
docker run --rm -v $(pwd):/workdir kicad_image kicad-cli pcb export pdf --output exports/pcb_layers.pdf project_name.kicad_pcb
```

#### PCB DRC (Design Rule Check)
Verifies if the PCB layout violates any design rules.
```bash
# Example
docker run --rm -v $(pwd):/workdir kicad_image kicad-cli pcb drc --output exports/drc_report.txt project_name.kicad_pcb
```

#### 3D Model Export (STEP)
Exports a 3D STEP model of the assembled PCB.
```bash
# Example
docker run --rm -v $(pwd):/workdir kicad_image kicad-cli pcb export step --output exports/board_3d.step project_name.kicad_pcb
```

## Best Practices
1. **Always use Absolute Paths or reliable Relative Paths**: When mapping volumes in run_command `-v $(pwd):/workdir` ensure the paths point to the correct project root.
2. **Handle Warnings/Errors**: After running a DRC/ERC, use `cat` or `Get-Content` to read the generated report and summarize the findings for the user.
3. **Zipping Manufacturing Files**: Manufacturers usually require a `.zip` file containing Gerbers and Drills. After generating them, you can zip the folder: `Compress-Archive -Path exports/gerbers/* -DestinationPath exports/manufacturing_files.zip`.
