import tomlkit

import argparse
import os
import sys
from typing import Union, AnyStr, IO
from pathlib import Path

def pyproject_toml() -> Path:
    installation_dir = Path(__file__).parent
    return installation_dir/"static"/"pyproject.toml"

def static_pyproject() -> tomlkit.TOMLDocument:
    static_pyproject = pyproject_toml()
    with open(static_pyproject, "r") as f:
        base_pyproject = tomlkit.parse(f.read())

    return base_pyproject

class Pyproject:
    def __init__(self, project_name: str):
        self.document = static_pyproject()

        self.project = self.document["project"]
        self.project_name = project_name
        self.dependencies: list[str] = []
        self.optional_dependencies: dict[str, list[str]] = self._setup_optional_dependencies()

        self._version = "0.1.0"

    def _setup_optional_dependencies(self):
        self.project["optional-dependencies"] = tomlkit.table()
        return self.project["optional-dependencies"]

    def add_dependencies(self, *dependencies: str):
        for dependency in set(dependencies):
            self.dependencies.append(dependency)

    def add_optional_dependencies(self, namespace: str, dependencies: list[str]):
        self.optional_dependencies[namespace] = []
        for dependency in dependencies:
            self.optional_dependencies[namespace].append(dependency)

    def version(self, version: str):
        self._version = version

    def build(self):
        self.project["name"] = self.project_name  # type: ignore
        self.project["dependencies"] = self.dependencies  # type: ignore
        self.project["optional-dependencies"] = self.optional_dependencies  # type: ignore
        self.project["version"] = self._version  #type: ignore

        return self.document

    def write_to(self, out: Union[str, Path, IO[str]]):
        contents = self.build()
        if isinstance(out, str) or isinstance(out, Path):
            with open(out, "w") as pyproject_file:
                tomlkit.dump(contents, pyproject_file)
        else:
            tomlkit.dump(contents, out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="Name of your project")
    parser.add_argument("-v", type=str, required=False, help="Version number of your project")
    parser.add_argument("-d", "--deps", type=str, nargs="*", help="Dependencies to add")
    parser.add_argument("-o", "--optional-deps", type=str, action="append", nargs="*", help="Optional dependencies, first parameter is the namespace (such as 'dev')")
    parser.add_argument("--defaults", action="store_true", help="Apply defaults")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    current_directory = Path(".")
    if not args.dry_run:
        if len(os.listdir(current_directory)) != 0:
            print("Current directory is not empty; exiting...", file=sys.stderr)
            sys.exit(1)
        else:
            package_name = args.name.replace("-", "_")
            package_path = current_directory/"src"/package_name

            os.makedirs(package_path)
            (package_path/"main.py").touch()
            (package_path/"__init__.py").touch()

    pyproject = Pyproject(args.name)
    if args.v:
        pyproject.version(args.v)
    if args.deps:
        pyproject.add_dependencies(*args.deps)
    if args.optional_deps:
        for optional_dep_namespace in args.optional_deps:
            namespace, *deps = optional_dep_namespace
            pyproject.add_optional_dependencies(namespace, deps)
    if args.defaults:
        pyproject.add_dependencies("pydantic", "requests")
        pyproject.add_optional_dependencies("dev", ["pytest", "pyfakefs", "pytest-mock"])

    if args.dry_run:
        pyproject.write_to(sys.stdout)
    else:
        pyproject.write_to(current_directory/"pyproject.toml")

if __name__ == "__main__":
    main()
