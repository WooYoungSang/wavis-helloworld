#!/usr/bin/env python3
"""
Setup script for Demeter WAVIS Framework v1.0
Complete AI-driven development framework
"""

from setuptools import setup, find_packages
import os
import sys
from pathlib import Path

# Ensure we're using Python 3.9+
if sys.version_info < (3, 9):
    print("Demeter WAVIS Framework requires Python 3.9 or higher")
    sys.exit(1)

# Read version from VERSION file
def get_version():
    version_file = Path(__file__).parent / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return "1.0.0"

# Read long description from README
def get_long_description():
    readme_file = Path(__file__).parent / "README.md"
    if readme_file.exists():
        return readme_file.read_text(encoding="utf-8")
    return ""

# Read requirements from requirements.txt
def get_requirements():
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        return requirements_file.read_text().strip().split('\n')
    return [
        "pyyaml>=6.0.0",
        "jinja2>=3.1.0",
        "click>=8.1.0",
        "rich>=13.7.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.0.0",
        "httpx>=0.25.0",
        "aiofiles>=23.0.0",
        "python-multipart>=0.0.6",
    ]

# Find all packages
packages = find_packages(
    where=".",
    include=["demeter*"],
    exclude=["tests*", "examples*", "docs*"]
)

# Package data
package_data = {
    "demeter": [
        "**/*.yaml",
        "**/*.yml",
        "**/*.json",
        "**/*.md",
        "**/*.txt",
        "**/*.sh",
        "**/*.jinja2",
        "**/*.j2",
        "templates/**/*",
        "examples/**/*",
        "docs/**/*",
    ]
}

# Data files
data_files = [
    ("", ["VERSION", "LICENSE", "README.md", "CHANGELOG.md"]),
    ("docs", [
        "docs/API.md",
        "docs/ARCHITECTURE.md",
        "docs/MIGRATION-GUIDE.md"
    ]),
    ("guides", [
        "demeter/guides/getting-started.md",
        "demeter/guides/quick-reference.md"
    ]),
    ("examples", [
        "demeter/examples/complete-workflows.md"
    ]),
]

# Entry points
entry_points = {
    "console_scripts": [
        "demeter=demeter.cli.main:main",
        "demeter-quick-start=demeter.setup.quick_start:main",
        "demeter-dev-cycle=demeter.ai.development_cycle:main",
        "demeter-copy-template=demeter.scripts.copy_template:main",
        "demeter-verify=demeter.verification.verify_all:main",
    ],
    "gui_scripts": [
        "demeter-dashboard=demeter.dashboard.app:main",
    ],
    "demeter.plugins": [
        "base=demeter.plugins.base",
        "ai=demeter.plugins.ai",
        "contracts=demeter.plugins.contracts",
    ],
    "demeter.tech_adapters": [
        "python-fastapi=demeter.adapters.python_fastapi",
        "typescript-nextjs=demeter.adapters.typescript_nextjs",
        "go-gin=demeter.adapters.go_gin",
        "java-spring=demeter.adapters.java_spring",
    ],
}

# Classifiers
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Quality Assurance",
    "Topic :: Software Development :: Testing",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
    "Environment :: Console",
    "Environment :: Web Environment",
    "Framework :: FastAPI",
    "Framework :: Django",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

# Keywords
keywords = [
    "ai-driven-development",
    "ssot",
    "contract-engineering",
    "claude-code",
    "graphrag",
    "development-framework",
    "requirements-management",
    "automated-testing",
    "quality-assurance",
    "project-template",
    "artificial-intelligence",
    "code-generation",
    "development-automation",
]

# Project URLs
project_urls = {
    "Homepage": "https://github.com/wavis-alchemy/demeter",
    "Documentation": "https://github.com/wavis-alchemy/demeter/wiki",
    "Repository": "https://github.com/wavis-alchemy/demeter.git",
    "Bug Tracker": "https://github.com/wavis-alchemy/demeter/issues",
    "Changelog": "https://github.com/wavis-alchemy/demeter/blob/main/CHANGELOG.md",
    "Funding": "https://github.com/sponsors/wavis-alchemy",
    "Release Notes": "https://github.com/wavis-alchemy/demeter/releases",
}

# Extra requirements
extras_require = {
    "ai": [
        "openai>=1.3.0",
        "anthropic>=0.7.0",
        "tiktoken>=0.5.0",
    ],
    "graphrag": [
        "sentence-transformers>=2.2.0",
        "chromadb>=0.4.0",
        "networkx>=3.1.0",
        "scikit-learn>=1.3.0",
    ],
    "dev": [
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
        "pytest-asyncio>=0.21.0",
        "black>=23.9.0",
        "flake8>=6.1.0",
        "mypy>=1.6.0",
        "pre-commit>=3.4.0",
        "sphinx>=7.2.0",
        "sphinx-rtd-theme>=1.3.0",
    ],
    "database": [
        "sqlalchemy>=2.0.0",
        "alembic>=1.12.0",
        "psycopg2-binary>=2.9.0",
        "redis>=5.0.0",
    ],
    "cloud": [
        "boto3>=1.29.0",
        "azure-identity>=1.14.0",
        "google-cloud-storage>=2.10.0",
    ],
    "monitoring": [
        "prometheus-client>=0.18.0",
        "opentelemetry-api>=1.21.0",
        "opentelemetry-sdk>=1.21.0",
        "structlog>=23.2.0",
    ],
}

# Add 'all' extra that includes everything
extras_require["all"] = [
    dep for deps in extras_require.values() for dep in deps
]

# Custom commands
class DemeterCommand:
    """Base class for custom setup commands"""

    def run(self):
        pass

class InstallDemeterCommand(DemeterCommand):
    """Custom installation command"""

    def run(self):
        print("🌾 Installing Demeter WAVIS Framework v1.0...")
        print("✅ Installation completed!")
        print("")
        print("Next steps:")
        print("1. Run: demeter-quick-start")
        print("2. Follow the interactive setup")
        print("3. Start AI-driven development!")

# Setup configuration
setup(
    # Basic information
    name="demeter-wavis-framework",
    version=get_version(),
    description="Complete AI-driven development framework with SSOT-based requirements management and contract engineering",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",

    # Author information
    author="WAVIS Alchemy",
    author_email="info@wavis-alchemy.com",
    maintainer="Demeter Framework Team",
    maintainer_email="demeter@wavis-alchemy.com",

    # URLs
    url="https://github.com/wavis-alchemy/demeter",
    project_urls=project_urls,

    # Package information
    packages=packages,
    package_data=package_data,
    data_files=data_files,
    include_package_data=True,
    zip_safe=False,

    # Dependencies
    python_requires=">=3.9",
    install_requires=get_requirements(),
    extras_require=extras_require,

    # Entry points
    entry_points=entry_points,

    # Metadata
    license="MIT",
    keywords=keywords,
    classifiers=classifiers,

    # Options
    platforms=["any"],

    # Custom metadata
    options={
        "build_scripts": {
            "executable": "/usr/bin/env python3",
        },
        "egg_info": {
            "tag_build": "",
            "tag_date": False,
        },
    },

    # Scripts
    scripts=[
        "quick-start.sh",
        "demeter/ai/automate-dev-cycle.sh",
        "demeter/scripts/copy-template.sh",
    ],
)

# Post-installation message
def post_install():
    """Post-installation message"""
    print("")
    print("🌾" + "="*60 + "🌾")
    print("   Demeter WAVIS Framework v1.0 Successfully Installed!")
    print("🌾" + "="*60 + "🌾")
    print("")
    print("🚀 Quick Start:")
    print("   demeter-quick-start")
    print("")
    print("🤖 AI Commands (in Claude Code):")
    print("   /ssot-query [feature]")
    print("   /generate-implementation [UoW-ID] --with-tests")
    print("   /verify-contracts --all")
    print("")
    print("📚 Documentation:")
    print("   https://github.com/wavis-alchemy/demeter/wiki")
    print("")
    print("🌾 From Requirements to Reality, Guided by AI 🌾")
    print("")

if __name__ == "__main__":
    # Run post-install message after successful installation
    try:
        post_install()
    except:
        pass