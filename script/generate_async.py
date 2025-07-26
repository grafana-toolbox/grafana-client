#!/usr/bin/env python
"""
Program to automatically generate asynchronous code from the
synchronous counterpart.

Synopsis:

  # Check if generated code is up-to-date.
  python script/generate_async.py check

  # Generate code.
  python script/generate_async.py format

What does this program does:
- For each module in `grafana_client/elements/*.py`, except `base` and `__init__`:
  Inject async/await keyword in all available methods / client interactions.
- Detect modules no longer in use, and remove them.
- Generate the async top level code based on `elements/__init__.py`.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

BASE_PATH = Path(".." if Path("../grafana_client").exists() else ".")

HERE = Path.cwd().absolute()
PYPROJECT_TOML = HERE / "pyproject.toml"
SOURCE = BASE_PATH / "grafana_client" / "elements"
TARGET = BASE_PATH / "grafana_client" / "elements" / "_async"


def run(action: str):
    """
    Invoke either the `check`, or the `format` subcommand.

    :check:  Create amalgamated tree in temporary directory,
             and compare with original. This is suitable for
             running sanity checks on CI.
    :format: Generate amalgamated async code from synchronous
             reference code.
    """

    run_check = action == "check" or False
    run_format = action == "format" or False

    source = SOURCE
    target = TARGET

    if run_check:
        # Create temporary formatted exemplar for probing it,
        # compare with current state, and croak on deviations.

        # Use this code for `delete=False`.
        # TemporaryDirectory._rmtree = lambda *more, **kwargs: None  # noqa: ERA001

        with TemporaryDirectory() as tmpdir:
            target = Path(tmpdir)
            process(source, target)

            command = f"diff -x __pycache__ -x .ruff_cache -u {TARGET} {target}"
            exitcode = os.system(command)

        if exitcode == 0:
            print(msg("INFO: Async code up-to-date. Excellent."))
        else:
            print(msg("ERROR: Async code not up-to-date. Please run `poe format`."))
            sys.exit(2)

    elif run_format:
        Path(target).mkdir(exist_ok=True)
        process(source, target)

    else:
        raise ValueError("Wrong or missing action, use either `check` or `format`.")


def process(source: Path, target: Path):
    """
    Process files, from input path (source) to output path (target).
    """

    module_processed = []

    print(f"Input path:  {source}")
    print(f"Output path: {target}")

    # for module_path in glob(f"{source}/*.py"):
    for module_path in Path(source).glob("*.py"):
        if module_path.name in ["__init__.py", "base.py"]:
            continue

        print(f"Processing {module_path}...")

        with Path.open(module_path) as fp:
            module_dump = fp.read()

        # Adjust imports.
        for relative_import in [".base", "..client", "..knowledge", "..model"]:
            module_dump = module_dump.replace(f"from {relative_import}", f"from .{relative_import}")

        # Modify function definitions.
        module_dump = re.sub(r"( {4}def )(?!_)", r"    async def ", module_dump)

        # Modify function calls.
        module_dump = re.sub(r"self\.client\.(.+)\(", r"await self.client.\1(", module_dump)
        module_dump = re.sub(r"= self\.(.+)\(", r"= await self.\1(", module_dump)
        module_dump = re.sub(r"send_request\(", r"await send_request(", module_dump)

        # Modify property accesses.
        module_dump = module_dump.replace("self.api.version", "await self.api.version")

        module_processed.append(module_path)
        target_path = Path(str(module_path).replace(str(source), str(target)))
        with Path.open(target_path, "w") as fp:
            fp.write(module_dump)

    relevant_modules = [_.name for _ in module_processed]
    existing_modules = [_.name for _ in Path(target).glob("*.py") if _.name not in ["base.py", "__init__.py"]]

    remove_module_count = 0

    for existing_module in existing_modules:
        if existing_module not in relevant_modules:
            print(f"Removing module {existing_module}...")
            (Path(target) / existing_module).unlink()
            remove_module_count += 1

    if not remove_module_count:
        print("No modules to remove.. pursuing..")

    with Path.open(source / "__init__.py") as fp:
        top_level_content = fp.read()

    print("Updating _async top level import content")

    top_level_content_patch = []

    for line in top_level_content.splitlines():
        if line.startswith("from "):
            if ".base" in line:
                continue

            patch_import_line = ""

            line_split = line.split(" ")

            for idx, word in zip(range(0, len(line_split)), line_split):
                if idx <= 2:
                    patch_import_line += word
                else:
                    patch_import_line += f"{word.replace(',', '')} as Async{word}"

                if idx != len(line_split) - 1:
                    patch_import_line += " "

            line = patch_import_line

        elif line.startswith(" " * 4):
            if "Base" in line:
                continue
            line = line.replace('    "', '    "Async')

        top_level_content_patch.append(line)

    with Path.open(target / "__init__.py", "w") as fp:
        fp.write("\n".join(top_level_content_patch) + "\n")

    # Run Ruff for code formatting, providing the same configuration as the project.
    shutil.copy(PYPROJECT_TOML, f"{target}")
    subprocess.call(["ruff", "format", target])
    subprocess.call(["ruff", "check", "--fix", target])
    Path(f"{target}/pyproject.toml").unlink()


def msg(text: str):
    """
    Return a colorful message, the color is determined by its text.
    """
    green = "\033[92;1m"
    red = "\033[91;1m"
    reset = "\033[0m"
    color = ""
    if text.lower().startswith("info"):
        color = green
    elif text.lower().startswith("error"):
        color = red
    return f"{color}{text}{reset}"


if __name__ == "__main__":
    subcommand = sys.argv[1:] and sys.argv[1] or None
    run(subcommand)
