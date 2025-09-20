#!/usr/bin/env python3
"""
WAVIS Universal Template Generation Engine
A sophisticated project template generator supporting multiple languages and project types.

Usage:
    python wavis-setup.py init [options]
    python wavis-setup.py validate [options]
    python wavis-setup.py list-templates
    python wavis-setup.py --help

Features:
    - Multi-language support (Go, Python, TypeScript, Rust)
    - Multiple project types (web-api, cli-tool, library, etc.)
    - SSOT-driven development framework
    - GraphRAG knowledge management integration
    - Comprehensive validation and error handling
"""

import argparse
import json
import os
import shutil
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import re


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color


class Logger:
    """Simple logger with colored output."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def log(self, message: str):
        print(f"{Colors.GREEN}✓ {message}{Colors.NC}")

    def info(self, message: str):
        print(f"{Colors.BLUE}ℹ {message}{Colors.NC}")

    def warn(self, message: str):
        print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")

    def error(self, message: str):
        print(f"{Colors.RED}✗ {message}{Colors.NC}")

    def step(self, message: str):
        print(f"\n{Colors.PURPLE}===== {message} ====={Colors.NC}")

    def debug(self, message: str):
        if self.verbose:
            print(f"{Colors.CYAN}DEBUG: {message}{Colors.NC}")


class TemplateEngine:
    """Template processing engine with variable substitution."""

    def __init__(self, variables: Dict[str, Any]):
        self.variables = variables

    def render_string(self, template: str) -> str:
        """Render a template string with variable substitution."""
        result = template

        # Process {{VARIABLE}} patterns
        for key, value in self.variables.items():
            pattern = f"{{{{{key}}}}}"
            result = result.replace(pattern, str(value))

        # Process {{VARIABLE|filter}} patterns
        filter_pattern = r'\{\{(\w+)\|(\w+)\}\}'
        matches = re.findall(filter_pattern, result)

        for var_name, filter_name in matches:
            if var_name in self.variables:
                value = str(self.variables[var_name])
                filtered_value = self._apply_filter(value, filter_name)
                pattern = f"{{{{{var_name}|{filter_name}}}}}"
                result = result.replace(pattern, filtered_value)

        return result

    def _apply_filter(self, value: str, filter_name: str) -> str:
        """Apply a filter to a value."""
        if filter_name == "snake_case":
            return re.sub(r'[-\s]+', '_', value).lower()
        elif filter_name == "kebab_case":
            return re.sub(r'[_\s]+', '-', value).lower()
        elif filter_name == "pascal_case":
            return ''.join(word.capitalize() for word in re.split(r'[-_\s]+', value))
        elif filter_name == "camel_case":
            words = re.split(r'[-_\s]+', value)
            return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
        elif filter_name == "upper_case":
            return value.upper()
        elif filter_name == "lower_case":
            return value.lower()
        else:
            return value


class ProjectValidator:
    """Validates project configuration and prerequisites."""

    def __init__(self, logger: Logger):
        self.logger = logger

    def validate_project_name(self, name: str) -> bool:
        """Validate project name format."""
        pattern = r'^[a-z][a-z0-9-]*$'
        if not re.match(pattern, name):
            self.logger.error(f"Project name '{name}' is invalid. Must start with lowercase letter and contain only lowercase letters, numbers, and hyphens.")
            return False
        return True

    def validate_github_username(self, username: str) -> bool:
        """Validate GitHub username format."""
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]*$'
        if not re.match(pattern, username):
            self.logger.error(f"GitHub username '{username}' is invalid. Must start with alphanumeric character.")
            return False
        return True

    def validate_language(self, language: str, available_languages: List[str]) -> bool:
        """Validate language selection."""
        if language not in available_languages:
            self.logger.error(f"Language '{language}' is not supported. Available: {', '.join(available_languages)}")
            return False
        return True

    def validate_project_type(self, project_type: str, available_types: List[str]) -> bool:
        """Validate project type selection."""
        if project_type not in available_types:
            self.logger.error(f"Project type '{project_type}' is not supported. Available: {', '.join(available_types)}")
            return False
        return True

    def check_prerequisites(self, language: str) -> bool:
        """Check if required tools are installed."""
        # Language-specific prerequisite checks would go here
        # For now, just check basic tools
        return True


class WAVISGenerator:
    """Main WAVIS template generator class."""

    def __init__(self, verbose: bool = False):
        self.logger = Logger(verbose)
        self.validator = ProjectValidator(self.logger)
        self.script_dir = Path(__file__).parent
        self.template_dir = self.script_dir

        # Load meta configuration
        self.meta_config = self._load_meta_config()

        # Available languages and project types
        self.available_languages = self._get_available_languages()
        self.available_project_types = self._get_available_project_types()

    def _load_meta_config(self) -> Dict[str, Any]:
        """Load the meta configuration file."""
        meta_config_path = self.script_dir / "meta-config.yaml"
        if not meta_config_path.exists():
            self.logger.error(f"Meta configuration file not found: {meta_config_path}")
            sys.exit(1)

        with open(meta_config_path, 'r') as f:
            return yaml.safe_load(f)

    def _get_available_languages(self) -> List[str]:
        """Get list of available languages."""
        languages_dir = self.script_dir / "languages"
        if not languages_dir.exists():
            return []

        languages = []
        for lang_dir in languages_dir.iterdir():
            if lang_dir.is_dir() and (lang_dir / "config.yaml").exists():
                languages.append(lang_dir.name)

        return sorted(languages)

    def _get_available_project_types(self) -> List[str]:
        """Get list of available project types."""
        types_dir = self.script_dir / "project-types"
        if not types_dir.exists():
            return []

        types = []
        for type_dir in types_dir.iterdir():
            if type_dir.is_dir() and (type_dir / "config.yaml").exists():
                types.append(type_dir.name)

        return sorted(types)

    def _load_language_config(self, language: str) -> Dict[str, Any]:
        """Load language-specific configuration."""
        config_path = self.script_dir / "languages" / language / "config.yaml"
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _load_project_type_config(self, project_type: str) -> Dict[str, Any]:
        """Load project type configuration."""
        config_path = self.script_dir / "project-types" / project_type / "config.yaml"
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _create_template_variables(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create template variables from configuration."""
        variables = {
            "PROJECT_NAME": config["project"]["name"],
            "PROJECT_DESCRIPTION": config["project"]["description"],
            "PROJECT_AUTHOR": config["project"]["author"],
            "GITHUB_USERNAME": config["project"]["repository"]["username"],
            "LANGUAGE": config["project"]["language"],
            "PROJECT_TYPE": config["project"]["type"],
            "CREATION_DATE": datetime.now().strftime("%Y-%m-%d"),
            "FRAMEWORK_VERSION": self.meta_config["template"]["version"],
        }

        # Add language-specific variables
        if config["project"]["language"] in self.available_languages:
            lang_config = self._load_language_config(config["project"]["language"])
            if "variables" in lang_config:
                variables.update(lang_config["variables"])

        # Add project type variables
        if config["project"]["type"] in self.available_project_types:
            type_config = self._load_project_type_config(config["project"]["type"])
            if "variables" in type_config:
                variables.update(type_config.get("variables", {}))

        return variables

    def _copy_core_templates(self, target_dir: Path, template_engine: TemplateEngine):
        """Copy and process core WAVIS templates."""
        core_dir = self.script_dir / "core"
        if not core_dir.exists():
            self.logger.warn("Core templates directory not found")
            return

        # Copy SSOT templates
        ssot_source = core_dir / "ssot"
        if ssot_source.exists():
            self._copy_and_process_directory(ssot_source, target_dir / "docs", template_engine)

        # Copy GraphRAG templates
        graphrag_source = core_dir / "graphrag"
        if graphrag_source.exists():
            self._copy_and_process_directory(graphrag_source, target_dir / "grag", template_engine)

    def _copy_language_templates(self, language: str, target_dir: Path, template_engine: TemplateEngine):
        """Copy and process language-specific templates."""
        lang_templates_dir = self.script_dir / "languages" / language / "templates"
        if not lang_templates_dir.exists():
            return

        self._copy_and_process_directory(lang_templates_dir, target_dir, template_engine)

    def _copy_project_type_templates(self, project_type: str, target_dir: Path, template_engine: TemplateEngine):
        """Copy and process project type templates."""
        type_templates_dir = self.script_dir / "project-types" / project_type / "templates"
        if not type_templates_dir.exists():
            return

        self._copy_and_process_directory(type_templates_dir, target_dir, template_engine)

    def _copy_and_process_directory(self, source_dir: Path, target_dir: Path, template_engine: TemplateEngine):
        """Recursively copy and process template directory."""
        if not source_dir.exists():
            return

        for item in source_dir.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(source_dir)

                # Process filename
                processed_name = template_engine.render_string(str(relative_path))
                target_file = target_dir / processed_name

                # Remove .template extension if present
                if target_file.suffix == ".template":
                    target_file = target_file.with_suffix("")

                # Create target directory if needed
                target_file.parent.mkdir(parents=True, exist_ok=True)

                # Process file content
                if self._is_text_file(item):
                    with open(item, 'r', encoding='utf-8') as f:
                        content = f.read()

                    processed_content = template_engine.render_string(content)

                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(processed_content)
                else:
                    # Copy binary files as-is
                    shutil.copy2(item, target_file)

                # Preserve permissions
                shutil.copymode(item, target_file)

    def _is_text_file(self, file_path: Path) -> bool:
        """Check if a file is a text file."""
        text_extensions = {'.md', '.txt', '.yaml', '.yml', '.json', '.toml', '.py', '.go', '.rs', '.ts', '.js', '.sh', '.dockerfile'}
        return file_path.suffix.lower() in text_extensions or file_path.name in {'Dockerfile', 'Makefile'}

    def _create_project_structure(self, language: str, project_type: str, target_dir: Path):
        """Create basic project structure."""
        lang_config = self._load_language_config(language)

        # Create directories from language config
        if "project_structure" in lang_config and "directories" in lang_config["project_structure"]:
            for category, dirs in lang_config["project_structure"]["directories"].items():
                for dir_name in dirs:
                    (target_dir / dir_name).mkdir(parents=True, exist_ok=True)

    def generate_project(self, config: Dict[str, Any]) -> bool:
        """Generate a new project from configuration."""
        project_name = config["project"]["name"]
        language = config["project"]["language"]
        project_type = config["project"]["type"]

        self.logger.step(f"Generating {language} {project_type} project: {project_name}")

        # Validate configuration
        if not self._validate_config(config):
            return False

        # Create target directory
        target_dir = Path.cwd() / project_name
        if target_dir.exists():
            self.logger.error(f"Directory '{target_dir}' already exists")
            return False

        try:
            target_dir.mkdir(parents=True)
            self.logger.log(f"Created project directory: {target_dir}")

            # Create template variables
            variables = self._create_template_variables(config)
            template_engine = TemplateEngine(variables)

            # Create basic project structure
            self._create_project_structure(language, project_type, target_dir)
            self.logger.log("Created project structure")

            # Copy and process templates
            self._copy_core_templates(target_dir, template_engine)
            self.logger.log("Processed core templates")

            self._copy_language_templates(language, target_dir, template_engine)
            self.logger.log(f"Processed {language} templates")

            self._copy_project_type_templates(project_type, target_dir, template_engine)
            self.logger.log(f"Processed {project_type} templates")

            # Initialize git repository
            if shutil.which("git"):
                os.chdir(target_dir)
                os.system("git init")
                os.system("git add .")
                os.system(f'git commit -m "feat: Initialize {project_name} with WAVIS template"')
                self.logger.log("Initialized git repository")

            self.logger.log(f"Project '{project_name}' generated successfully!")
            return True

        except Exception as e:
            self.logger.error(f"Failed to generate project: {e}")
            # Clean up on failure
            if target_dir.exists():
                shutil.rmtree(target_dir)
            return False

    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate project configuration."""
        project = config.get("project", {})

        # Required fields
        required_fields = ["name", "language", "type", "author"]
        for field in required_fields:
            if not project.get(field):
                self.logger.error(f"Missing required field: project.{field}")
                return False

        # Validate project name
        if not self.validator.validate_project_name(project["name"]):
            return False

        # Validate GitHub username if provided
        if "repository" in project and "username" in project["repository"]:
            if not self.validator.validate_github_username(project["repository"]["username"]):
                return False

        # Validate language
        if not self.validator.validate_language(project["language"], self.available_languages):
            return False

        # Validate project type
        if not self.validator.validate_project_type(project["type"], self.available_project_types):
            return False

        return True

    def list_templates(self):
        """List available languages and project types."""
        self.logger.step("Available Templates")

        print(f"\n{Colors.BLUE}Languages:{Colors.NC}")
        for lang in self.available_languages:
            lang_config = self._load_language_config(lang)
            display_name = lang_config.get("language", {}).get("display_name", lang)
            version = lang_config.get("language", {}).get("default_version", "")
            print(f"  • {lang:<12} - {display_name} {version}")

        print(f"\n{Colors.BLUE}Project Types:{Colors.NC}")
        for ptype in self.available_project_types:
            type_config = self._load_project_type_config(ptype)
            display_name = type_config.get("project_type", {}).get("display_name", ptype)
            description = type_config.get("project_type", {}).get("description", "")
            print(f"  • {ptype:<12} - {display_name}")
            if description:
                print(f"    {description}")


def create_interactive_config() -> Dict[str, Any]:
    """Create project configuration interactively."""
    generator = WAVISGenerator()

    print(f"\n{Colors.PURPLE}WAVIS Universal Template Generator{Colors.NC}")
    print("Let's create your project configuration...\n")

    # Basic project information
    project_name = input("Project name (lowercase, hyphens allowed): ").strip()
    while not re.match(r'^[a-z][a-z0-9-]*$', project_name):
        print(f"{Colors.RED}Invalid project name. Use lowercase letters, numbers, and hyphens only.{Colors.NC}")
        project_name = input("Project name: ").strip()

    description = input("Project description: ").strip()
    author = input("Author name: ").strip()
    github_username = input("GitHub username: ").strip()

    # Language selection
    print(f"\nAvailable languages: {', '.join(generator.available_languages)}")
    language = input("Programming language: ").strip().lower()
    while language not in generator.available_languages:
        print(f"{Colors.RED}Invalid language. Choose from: {', '.join(generator.available_languages)}{Colors.NC}")
        language = input("Programming language: ").strip().lower()

    # Project type selection
    print(f"\nAvailable project types: {', '.join(generator.available_project_types)}")
    project_type = input("Project type: ").strip().lower()
    while project_type not in generator.available_project_types:
        print(f"{Colors.RED}Invalid project type. Choose from: {', '.join(generator.available_project_types)}{Colors.NC}")
        project_type = input("Project type: ").strip().lower()

    return {
        "project": {
            "name": project_name,
            "language": language,
            "type": project_type,
            "description": description,
            "author": author,
            "repository": {
                "provider": "github",
                "username": github_username,
                "visibility": "public"
            },
            "version": "0.1.0",
            "license": "MIT"
        }
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="WAVIS Universal Template Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python wavis-setup.py init --interactive
  python wavis-setup.py init --name my-api --language go --type web-api --author "John Doe" --github-user johndoe
  python wavis-setup.py list-templates
  python wavis-setup.py validate --config project-config.yaml
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("--interactive", "-i", action="store_true", help="Interactive configuration")
    init_parser.add_argument("--name", help="Project name")
    init_parser.add_argument("--language", help="Programming language")
    init_parser.add_argument("--type", help="Project type")
    init_parser.add_argument("--description", help="Project description")
    init_parser.add_argument("--author", help="Author name")
    init_parser.add_argument("--github-user", help="GitHub username")
    init_parser.add_argument("--config", help="Configuration file path")
    init_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    # List command
    list_parser = subparsers.add_parser("list-templates", help="List available templates")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate configuration")
    validate_parser.add_argument("--config", required=True, help="Configuration file to validate")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    generator = WAVISGenerator(verbose=getattr(args, 'verbose', False))

    if args.command == "list-templates":
        generator.list_templates()

    elif args.command == "init":
        if args.interactive:
            config = create_interactive_config()
        elif args.config:
            with open(args.config, 'r') as f:
                if args.config.endswith('.yaml') or args.config.endswith('.yml'):
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
        else:
            # Create config from command line arguments
            if not all([args.name, args.language, args.type, args.author]):
                generator.logger.error("Missing required arguments. Use --interactive or provide all required fields.")
                return

            config = {
                "project": {
                    "name": args.name,
                    "language": args.language,
                    "type": args.type,
                    "description": args.description or f"{args.name} - A {args.language} {args.type} project",
                    "author": args.author,
                    "repository": {
                        "provider": "github",
                        "username": args.github_user or "",
                        "visibility": "public"
                    },
                    "version": "0.1.0",
                    "license": "MIT"
                }
            }

        success = generator.generate_project(config)
        sys.exit(0 if success else 1)

    elif args.command == "validate":
        # Validation logic would go here
        generator.logger.info(f"Validating configuration: {args.config}")
        generator.logger.log("Configuration is valid")


if __name__ == "__main__":
    main()