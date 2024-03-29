"""
Script to automatically generate grafana asynchronous code from the
synchronous counterpart.
What does this program do:
- For all module in grafana_client/elements/*.py excepted base and __init__
Inject async/await keyword in all available methods / client interactions.
- Then detect no longer needed module for removal.
- Finally generate the _async top level code based on the elements/__init__.py one.
"""

import os
import re
import subprocess
from glob import glob

BASE_PATH = ".." if os.path.exists("../grafana_client") else "."

if __name__ == "__main__":
    module_processed = []
    module_generated = []

    for module_path in glob(f"{BASE_PATH}/grafana_client/elements/*.py"):
        if "__init__.py" in module_path or "base.py" in module_path:
            continue

        print(f"Processing {module_path}...")

        with open(module_path, "r") as fp:
            module_dump = fp.read()

        module_dump = re.sub(r"( {4}def )(?!_)", r"    async def ", module_dump)

        module_dump = module_dump.replace("self.client.", "await self.client.")

        for relative_import in [".base", "..client", "..knowledge", "..model"]:
            module_dump = module_dump.replace(f"from {relative_import}", f"from .{relative_import}")

        module_dump = module_dump.replace("self.api.version", "await self.api.version")
        module_dump = module_dump.replace("= self.", "= await self.")

        module_processed.append(module_path)
        target_path = module_path.replace("elements/", "elements/_async/")
        module_generated.append(target_path)

        print(f"Writing to {target_path}...")

        with open(module_path.replace("elements/", "elements/_async/"), "w") as fp:
            fp.write(module_dump)

    relevant_modules = [os.path.basename(_) for _ in module_processed]
    existing_modules = [
        os.path.basename(_)
        for _ in glob(f"{BASE_PATH}/grafana_client/elements/_async/*.py")
        if "base.py" not in _ and "__init__.py" not in _
    ]

    remove_module_count = 0

    for existing_module in existing_modules:
        if existing_module not in relevant_modules:
            print(f"Removing module {existing_module}...")
            os.remove(f"{BASE_PATH}/grafana_client/elements/_async/{existing_module}")
            remove_module_count += 1

    if not remove_module_count:
        print("No modules to remove.. pursuing..")

    with open(f"{BASE_PATH}/grafana_client/elements/__init__.py", "r") as fp:
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

    with open(f"{BASE_PATH}/grafana_client/elements/_async/__init__.py", "w") as fp:
        fp.write("\n".join(top_level_content_patch) + "\n")

    subprocess.call(["poe", "format"])
