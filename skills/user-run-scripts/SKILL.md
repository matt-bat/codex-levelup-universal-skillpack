---
name: user-run-scripts
description: When enabled by `--ill-run-scripts`, pause before running easily executable scripts and provide exact copy-paste commands with the required working directory for the user to run.
---

# User-Run Scripts

When this mode is on, stop immediately before an easily executable script or shell pipeline would run. Show the complete command, exact working directory, required inputs, and what success output to expect. Wait for the user to run it and return the result before continuing. Keep read-only inspection and commands that are necessary to explain the command separate, and never claim that a command ran when the user ran it.

The mode is explicit and persistent. Toggle it with the exact command `--ill-run-scripts`; the last state is saved in the local preferences file and applies in later conversations until toggled again. A direct instruction in the current prompt takes precedence for that prompt; hosts should record the exact toggle only when the user explicitly toggles the mode.
