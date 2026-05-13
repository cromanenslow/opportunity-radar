"""Opportunity Radar - Repo 白名单

初始 100 个 TS/Python 高价值 repo。
筛选标准：
- 有 good-first-issue / help-wanted 标签
- 近期有外部 PR 合并
- 有 Sponsors / OpenCollective / 赏金历史
- 有测试套件、CI 配置
"""

from __future__ import annotations
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class WhitelistRepo:
    """白名单 repo 条目"""
    full_name: str
    language: str                     # typescript / python
    stars: int = 0
    description: str = ""
    install_cmd: str = ""             # npm install / pip install -e .
    test_cmd: str = ""                # npm test / pytest
    contrib_guide: str = ""           # CONTRIBUTING.md 链接
    maintainer_response_days: float = 7.0
    ext_pr_merge_rate_90d: float = 0.0
    has_sponsors: bool = False
    has_opencollective: bool = False
    has_algora_tipping: bool = False
    bounty_history: float = 0.0       # 历史赏金总额(USD)
    common_task_types: list[str] = field(default_factory=list)
    notes: str = ""
    priority: int = 0                 # 0=待观察 1=正常 2=高优先


# 初始白名单 - TypeScript 项目 (50个)
TYPESCRIPT_REPOS = [
    WhitelistRepo("vercel/next.js", "typescript", 130000, "The React Framework", "pnpm install", "pnpm test", "", 2, 0.3, True, False, True, 5000, ["bug", "docs", "test"], "大型项目，持续有赏金"),
    WhitelistRepo("facebook/react", "typescript", 230000, "The library for web and native UI", "yarn install", "yarn test", "", 3, 0.15, True, False, False, 2000, ["bug", "rfc", "test"]),
    WhitelistRepo("vuejs/core", "typescript", 48000, "Vue.js core", "pnpm install", "pnpm test", "", 5, 0.2, True, True, False, 1000, ["bug", "docs", "migration"]),
    WhitelistRepo("angular/angular", "typescript", 96000, "Angular framework", "yarn install", "yarn test", "", 4, 0.2, True, False, False, 3000, ["bug", "docs", "test"]),
    WhitelistRepo("sveltejs/svelte", "typescript", 81000, "cybernetically enhanced web apps", "pnpm install", "pnpm test", "", 3, 0.25, True, True, True, 2000, ["bug", "docs"]),
    WhitelistRepo("microsoft/TypeScript", "typescript", 103000, "TypeScript compiler", "npm install", "npm test", "", 7, 0.1, True, False, False, 1000, ["bug", "compiler", "test"]),
    WhitelistRepo("denoland/deno", "typescript", 100000, "A modern runtime for JS and TS", "cargo build", "cargo test", "", 3, 0.15, True, False, True, 3000, ["bug", "feature", "docs"]),
    WhitelistRepo("vitejs/vite", "typescript", 72000, "Next gen frontend tooling", "pnpm install", "pnpm test", "", 2, 0.3, True, True, True, 2000, ["bug", "plugin", "docs"]),
    WhitelistRepo("tailwindlabs/tailwindcss", "typescript", 86000, "A utility-first CSS framework", "npm install", "npm test", "", 2, 0.2, True, True, True, 1500, ["bug", "docs", "config"]),
    WhitelistRepo("prisma/prisma", "typescript", 42000, "Next-gen ORM for Node.js and TypeScript", "npm install", "npm test", "", 3, 0.25, True, False, True, 3000, ["bug", "migration", "schema"]),
    WhitelistRepo("trpc/trpc", "typescript", 36000, "End-to-end typesafe APIs made easy", "pnpm install", "pnpm test", "", 2, 0.3, True, True, True, 1000, ["bug", "docs", "test"]),
    WhitelistRepo("shadcn-ui/ui", "typescript", 82000, "Beautifully designed components", "pnpm install", "pnpm test", "", 2, 0.2, True, False, True, 500, ["docs", "a11y", "component"]),
    WhitelistRepo("nestjs/nest", "typescript", 69000, "A progressive Node.js framework", "npm install", "npm test", "", 4, 0.2, True, True, False, 1000, ["bug", "docs", "module"]),
    WhitelistRepo("nestjs/cli", "typescript", 4000, "Nest CLI tool", "npm install", "npm test", "", 5, 0.3, False, False, False, 200, ["bug", "docs"]),
    WhitelistRepo("typescript-eslint/typescript-eslint", "typescript", 16000, "Monorepo for ESLint types", "npm install", "npm test", "", 3, 0.3, True, True, True, 1000, ["rule", "bug", "docs"]),
    WhitelistRepo("eslint/eslint", "typescript", 25000, "Find and fix problems in JS code", "npm install", "npm test", "", 5, 0.2, True, True, True, 2000, ["rule", "bug", "docs"]),
    WhitelistRepo("prettier/prettier", "typescript", 50000, "Opinionated code formatter", "npm install", "npm test", "", 7, 0.15, True, True, False, 1000, ["bug", "format", "docs"]),
    WhitelistRepo("date-fns/date-fns", "typescript", 34500, "Modern JS date utility library", "npm install", "npm test", "", 5, 0.3, True, True, False, 500, ["bug", "locale", "docs"]),
    WhitelistRepo("vueuse/vueuse", "typescript", 20000, "Collection of Vue composition utilities", "pnpm install", "pnpm test", "", 2, 0.35, True, True, True, 800, ["composable", "bug", "docs"]),
    WhitelistRepo("storybookjs/storybook", "typescript", 85000, "Storybook frontend workshop", "npm install", "npm test", "", 5, 0.2, True, True, True, 2000, ["bug", "addon", "docs"]),
    WhitelistRepo("remix-run/remix", "typescript", 30000, "Build modern web apps with React", "npm install", "npm test", "", 3, 0.25, True, False, True, 1500, ["bug", "loader", "docs"]),
    WhitelistRepo("apollographql/apollo-client", "typescript", 19000, "A fully-featured caching GraphQL client", "npm install", "npm test", "", 7, 0.15, True, False, False, 1000, ["bug", "cache", "docs"]),
    WhitelistRepo("graphql/graphql-js", "typescript", 14000, "The reference implementation of GraphQL", "npm install", "npm test", "", 10, 0.1, True, False, False, 500, ["bug", "spec", "test"]),
    WhitelistRepo("jestjs/jest", "typescript", 44000, "Delightful JS Testing", "npm install", "npm test", "", 10, 0.1, True, False, False, 1000, ["bug", "matcher", "docs"]),
    WhitelistRepo("vitest-dev/vitest", "typescript", 14000, "A Vite-native unit test framework", "pnpm install", "pnpm test", "", 2, 0.35, True, True, True, 800, ["bug", "matcher", "docs"]),
    WhitelistRepo("nuxt/nuxt", "typescript", 55000, "The Intuitive Vue Framework", "pnpm install", "pnpm test", "", 3, 0.25, True, True, True, 2000, ["bug", "module", "docs"]),
    WhitelistRepo("strapi/strapi", "typescript", 65000, "Open-source headless CMS", "npm install", "npm test", "", 5, 0.2, True, False, True, 1500, ["bug", "plugin", "docs"]),
    WhitelistRepo("calcom/cal.com", "typescript", 36000, "Scheduling infrastructure", "yarn install", "yarn test", "", 3, 0.3, True, True, True, 2000, ["bug", "integration", "docs"]),
    WhitelistRepo("supabase/supabase", "typescript", 80000, "The open source Firebase alternative", "npm install", "npm test", "", 3, 0.2, True, True, True, 3000, ["bug", "auth", "docs"]),
    WhitelistRepo("appwrite/appwrite", "typescript", 47000, "Build like a team of hundreds_", "pnpm install", "pnpm test", "", 3, 0.25, True, True, True, 2000, ["bug", "sdk", "docs"]),
    WhitelistRepo("nestjs/nest-cli", "typescript", 3000, "CLI tool for Nest applications", "npm install", "npm test", "", 5, 0.3, False, False, False, 100, ["bug", "schematic"]),
    WhitelistRepo("nrwl/nx", "typescript", 24000, "Smart Monorepos · Fast CI", "npm install", "npm test", "", 4, 0.2, True, False, True, 1500, ["bug", "plugin", "docs"]),
    WhitelistRepo("tannerlinsley/react-query", "typescript", 43000, "Hooks for fetching, caching and updating data", "npm install", "npm test", "", 3, 0.25, True, True, True, 1000, ["bug", "hook", "docs"]),
    WhitelistRepo("colinhacks/zod", "typescript", 36000, "TypeScript-first schema validation", "npm install", "npm test", "", 3, 0.3, True, True, True, 800, ["bug", "schema", "docs"]),
    WhitelistRepo("Effect-TS/effect", "typescript", 8000, "Build type-safe, composable applications", "npm install", "npm test", "", 3, 0.3, True, True, True, 500, ["bug", "effect", "docs"]),
    WhitelistRepo("faker-js/faker", "typescript", 13000, "Generate massive amounts of fake data", "npm install", "npm test", "", 2, 0.35, True, True, True, 500, ["locale", "bug", "docs"]),
    WhitelistRepo("clerk/javascript", "typescript", 5000, "Clerk frontend SDKs", "npm install", "npm test", "", 3, 0.3, True, False, True, 500, ["bug", "sdk", "docs"]),
    WhitelistRepo("redis/ioredis", "typescript", 14000, "A robust, performance-focused Redis client", "npm install", "npm test", "", 5, 0.25, True, True, False, 800, ["bug", "command", "docs"]),
    WhitelistRepo("socketio/socket.io", "typescript", 61000, "Real-time bidirectional event-based communication", "npm install", "npm test", "", 7, 0.15, True, False, False, 500, ["bug", "transport", "docs"]),
    WhitelistRepo("winstonjs/winston", "typescript", 23000, "A logger for just about everything", "npm install", "npm test", "", 10, 0.2, True, True, False, 300, ["bug", "transport", "docs"]),
    WhitelistRepo("pinojs/pino", "typescript", 14000, "Node.js logger with very low overhead", "npm install", "npm test", "", 4, 0.25, True, True, False, 300, ["bug", "transport", "docs"]),
    WhitelistRepo("fastify/fastify", "typescript", 33000, "Fast and low overhead web framework", "npm install", "npm test", "", 3, 0.3, True, True, True, 1000, ["bug", "plugin", "docs"]),
    WhitelistRepo("honojs/hono", "typescript", 23000, "Ultrafast web framework for the edge", "npm install", "npm test", "", 2, 0.35, True, True, True, 500, ["bug", "middleware", "docs"]),
    WhitelistRepo("elysiajs/elysia", "typescript", 11000, "Ergonomic framework for building backend servers", "npm install", "npm test", "", 2, 0.35, True, True, True, 300, ["bug", "plugin", "docs"]),
    WhitelistRepo("openai/openai-node", "typescript", 8000, "Official OpenAI Node.js library", "npm install", "npm test", "", 3, 0.3, True, False, False, 500, ["bug", "api", "docs"]),
    WhitelistRepo("anthropics/anthropic-sdk-typescript", "typescript", 1200, "Official Anthropic TypeScript SDK", "npm install", "npm test", "", 2, 0.4, True, False, False, 300, ["bug", "api", "docs"]),
    WhitelistRepo("langchain-ai/langchainjs", "typescript", 14000, "Build context-aware reasoning applications", "npm install", "npm test", "", 3, 0.25, True, True, True, 1000, ["bug", "chain", "docs"]),
    WhitelistRepo("huggingface/chat-ui", "typescript", 8000, "Open-source codebase for chat interfaces", "npm install", "npm test", "", 4, 0.25, True, False, True, 500, ["bug", "ui", "docs"]),
    WhitelistRepo("dubinc/dub", "typescript", 20000, "Open-source link management infrastructure", "npm install", "npm test", "", 2, 0.3, True, True, True, 1000, ["bug", "api", "docs"]),
    WhitelistRepo("documenso/documenso", "typescript", 9000, "Open-source DocuSign alternative", "npm install", "npm test", "", 3, 0.3, True, True, True, 800, ["bug", "feature", "docs"]),
]

# 初始白名单 - Python 项目 (50个)
PYTHON_REPOS = [
    WhitelistRepo("django/django", "python", 82000, "The Web framework for perfectionists with deadlines", "pip install -e .", "python -m pytest", "", 3, 0.2, True, False, False, 3000, ["bug", "orm", "docs"]),
    WhitelistRepo("flask-admin/flask-admin", "python", 5700, "Simple and extensible admin interface", "pip install -e .", "pytest", "", 7, 0.3, True, True, False, 300, ["bug", "view", "docs"]),
    WhitelistRepo("fastapi/fastapi", "python", 81000, "Modern, fast web framework for building APIs", "pip install -e .", "pytest", "", 2, 0.35, True, True, True, 2000, ["bug", "docs", "dependency"]),
    WhitelistRepo("pallets/flask", "python", 68000, "The Python micro framework for building web apps", "pip install -e .", "pytest", "", 5, 0.2, True, True, False, 1000, ["bug", "docs", "extension"]),
    WhitelistRepo("celery/celery", "python", 24000, "Distributed Task Queue", "pip install -e .", "pytest", "", 7, 0.2, True, True, False, 800, ["bug", "backend", "docs"]),
    WhitelistRepo("scrapy/scrapy", "python", 53000, "Web scraping framework", "pip install -e .", "pytest", "", 5, 0.25, True, True, False, 500, ["bug", "spider", "docs"]),
    WhitelistRepo("pandas-dev/pandas", "python", 44000, "Flexible and powerful data analysis library", "pip install -e .", "pytest", "", 7, 0.15, True, True, False, 2000, ["bug", "dtype", "docs"]),
    WhitelistRepo("numpy/numpy", "python", 28000, "Fundamental package for array computing", "pip install -e .", "pytest", "", 10, 0.1, True, True, False, 1500, ["bug", "ufunc", "docs"]),
    WhitelistRepo("psf/requests", "python", 52000, "A simple HTTP library for Python", "pip install -e .", "pytest", "", 14, 0.1, True, True, False, 500, ["bug", "adapter", "docs"]),
    WhitelistRepo("urllib3/urllib3", "python", 4000, "HTTP library with thread-safe connection pooling", "pip install -e .", "pytest", "", 5, 0.25, True, True, True, 1000, ["bug", "pool", "docs"]),
    WhitelistRepo("encode/httpx", "python", 13000, "A next generation HTTP client for Python", "pip install -e .", "pytest", "", 3, 0.3, True, True, True, 800, ["bug", "auth", "docs"]),
    WhitelistRepo("python-attrs/attrs", "python", 5200, "Python Classes Without Boilerplate", "pip install -e .", "pytest", "", 5, 0.3, True, True, False, 300, ["bug", "validator", "docs"]),
    WhitelistRepo("pydantic/pydantic", "python", 23000, "Data validation using Python type annotations", "pip install -e .", "pytest", "", 3, 0.3, True, True, True, 1500, ["bug", "schema", "docs"]),
    WhitelistRepo("sqlalchemy/sqlalchemy", "python", 10000, "Database Toolkit for Python", "pip install -e .", "pytest", "", 7, 0.15, True, True, False, 1000, ["bug", "dialect", "docs"]),
    WhitelistRepo("marshmallow-code/marshmallow", "python", 7000, "Object serialization/deserialization library", "pip install -e .", "pytest", "", 5, 0.25, True, True, False, 300, ["bug", "field", "docs"]),
    WhitelistRepo("pytest-dev/pytest", "python", 12000, "The pytest framework", "pip install -e .", "pytest", "", 5, 0.2, True, True, False, 1000, ["bug", "fixture", "docs"]),
    WhitelistRepo("tox-dev/tox", "python", 4000, "Command line driven CI frontend", "pip install -e .", "pytest", "", 5, 0.25, True, True, False, 300, ["bug", "env", "docs"]),
    WhitelistRepo("python-poetry/poetry", "python", 16000, "Python dependency management and packaging", "pip install -e .", "pytest", "", 5, 0.2, True, True, True, 800, ["bug", "lockfile", "docs"]),
    WhitelistRepo("pypa/pip", "python", 30000, "The Python package installer", "pip install -e .", "pytest", "", 10, 0.1, True, True, False, 500, ["bug", "resolver", "docs"]),
    WhitelistRepo("pre-commit/pre-commit", "python", 13000, "A framework for managing git hooks", "pip install -e .", "pytest", "", 5, 0.2, True, True, False, 300, ["bug", "hook", "docs"]),
    WhitelistRepo("home-assistant/core", "python", 75000, "Open source home automation", "pip install -r requirements.txt", "pytest", "", 3, 0.25, True, True, True, 2000, ["integration", "bug", "docs"]),
    WhitelistRepo("scikit-learn/scikit-learn", "python", 60000, "Machine learning in Python", "pip install -e .", "pytest", "", 7, 0.15, True, True, False, 1500, ["bug", "estimator", "docs"]),
    WhitelistRepo("matplotlib/matplotlib", "python", 20000, "Comprehensive library for creating visualizations", "pip install -e .", "pytest", "", 7, 0.15, True, True, False, 800, ["bug", "axes", "docs"]),
    WhitelistRepo("sympy/sympy", "python", 13000, "A computer algebra system written in pure Python", "pip install -e .", "pytest", "", 5, 0.2, True, True, False, 500, ["bug", "function", "docs"]),
    WhitelistRepo("django-rest-framework/django-rest-framework", "python", 28000, "Web APIs for Django", "pip install -e .", "pytest", "", 5, 0.2, True, True, False, 800, ["bug", "serializer", "docs"]),
    WhitelistRepo("encode/django-rest-framework", "python", 28000, "Web APIs for Django (encode fork)", "pip install -e .", "pytest", "", 5, 0.2, True, True, False, 500, ["bug", "serializer", "docs"]),
    WhitelistRepo("tiangolo/full-stack-fastapi-template", "python", 27000, "Full stack, modern web application template", "pip install -e .", "pytest", "", 3, 0.3, True, True, True, 500, ["bug", "template", "docs"]),
    WhitelistRepo("openai/openai-python", "python", 25000, "Official OpenAI Python library", "pip install -e .", "pytest", "", 2, 0.35, True, False, False, 500, ["bug", "api", "docs"]),
    WhitelistRepo("anthropics/anthropic-sdk-python", "python", 4000, "Official Anthropic Python SDK", "pip install -e .", "pytest", "", 2, 0.4, True, False, False, 300, ["bug", "api", "docs"]),
    WhitelistRepo("langchain-ai/langchain", "python", 100000, "Build context-aware reasoning applications", "pip install -e .", "pytest", "", 2, 0.3, True, True, True, 2000, ["bug", "chain", "docs"]),
    WhitelistRepo("streamlit/streamlit", "python", 40000, "A faster way to build and share data apps", "pip install -e .", "pytest", "", 3, 0.25, True, True, True, 1500, ["bug", "widget", "docs"]),
    WhitelistRepo("apache/airflow", "python", 40000, "Platform to programmatically author workflows", "pip install -e .", "pytest", "", 5, 0.15, True, False, False, 1000, ["bug", "operator", "docs"]),
    WhitelistRepo("prefecthq/prefect", "python", 18000, "A workflow orchestration tool", "pip install -e .", "pytest", "", 3, 0.3, True, True, True, 1000, ["bug", "flow", "docs"]),
    WhitelistRepo("dagster-io/dagster", "python", 12000, "An orchestration platform for data assets", "pip install -e .", "pytest", "", 3, 0.3, True, True, True, 800, ["bug", "asset", "docs"]),
    WhitelistRepo("huggingface/transformers", "python", 140000, "State-of-the-art ML for PyTorch, TensorFlow, JAX", "pip install -e .", "pytest", "", 5, 0.15, True, True, True, 3000, ["bug", "model", "docs"]),
    WhitelistRepo("mlflow/mlflow", "python", 19000, "Open source platform for the ML lifecycle", "pip install -e .", "pytest", "", 5, 0.2, True, False, False, 1000, ["bug", "tracking", "docs"]),
    WhitelistRepo("ray-project/ray", "python", 35000, "Unified framework for scaling Python and AI", "pip install -e .", "pytest", "", 5, 0.2, True, True, False, 1500, ["bug", "actor", "docs"]),
    WhitelistRepo("mitmproxy/mitmproxy", "python", 37000, "An interactive TLS-capable intercepting HTTP proxy", "pip install -e .", "pytest", "", 5, 0.2, True, True, False, 1000, ["bug", "addon", "docs"]),
    WhitelistRepo("yt-dlp/yt-dlp", "python", 105000, "A feature-rich command-line audio/video downloader", "pip install -e .", "pytest", "", 2, 0.3, True, True, True, 500, ["bug", "extractor", "docs"]),
    WhitelistRepo("httpie/cli", "python", 35000, "HTTPie — making HTTP requests human-friendly", "pip install -e .", "pytest", "", 5, 0.2, True, True, True, 500, ["bug", "cli", "docs"]),
    WhitelistRepo("seleniumbase/SeleniumBase", "python", 6000, "Python browser automation & testing framework", "pip install -e .", "pytest", "", 2, 0.35, True, True, True, 300, ["bug", "mode", "docs"]),
    WhitelistRepo("PostHog/posthog", "python", 23000, "Open-source product analytics suite", "pip install -e .", "pytest", "", 3, 0.25, True, True, True, 1000, ["bug", "event", "docs"]),
    WhitelistRepo("All-Hands-AI/OpenHands", "python", 45000, "Code less, create more", "pip install -e .", "pytest", "", 2, 0.3, True, True, True, 2000, ["bug", "agent", "docs"]),
    WhitelistRepo("open-webui/open-webui", "python", 80000, "User-friendly AI interface", "pip install -e .", "pytest", "", 2, 0.3, True, True, True, 1000, ["bug", "ui", "docs"]),
    WhitelistRepo("MushroomLabs/Farcaster-Protocol", "python", 5000, "Decentralized social protocol", "pip install -e .", "pytest", "", 3, 0.25, True, True, True, 800, ["bug", "protocol", "docs"]),
    WhitelistRepo("getsentry/sentry-python", "python", 1700, "The official Python SDK for Sentry", "pip install -e .", "pytest", "", 3, 0.3, True, True, False, 500, ["bug", "integration", "docs"]),
    WhitelistRepo("zeromq/pyzmq", "python", 3200, "PyZMQ: Python bindings for ZeroMQ", "pip install -e .", "pytest", "", 5, 0.25, True, True, False, 300, ["bug", "socket", "docs"]),
    WhitelistRepo("python/cpython", "python", 66000, "The Python programming language", "pip install -e .", "python -m test", "", 14, 0.05, True, False, False, 500, ["bug", "stdlib", "docs"]),
    WhitelistRepo("pypa/setuptools", "python", 2400, "Official project repository for setuptools", "pip install -e .", "pytest", "", 7, 0.15, True, True, False, 200, ["bug", "build", "docs"]),
]


def load_whitelist() -> list[WhitelistRepo]:
    """加载白名单"""
    return TYPESCRIPT_REPOS + PYTHON_REPOS


def save_whitelist_csv(repos: list[WhitelistRepo], path: str = "whitelist/repos.csv"):
    """保存为 CSV"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "full_name", "language", "stars", "install_cmd", "test_cmd",
            "maintainer_response_days", "ext_pr_merge_rate_90d",
            "has_sponsors", "has_opencollective", "has_algora_tipping",
            "bounty_history", "common_task_types", "priority"
        ])
        for r in repos:
            writer.writerow([
                r.full_name, r.language, r.stars, r.install_cmd, r.test_cmd,
                r.maintainer_response_days, r.ext_pr_merge_rate_90d,
                r.has_sponsors, r.has_opencollective, r.has_algora_tipping,
                r.bounty_history, "|".join(r.common_task_types), r.priority,
            ])
    print(f"白名单已保存: {path} ({len(repos)} 个 repo)")


def load_whitelist_csv(path: str = "whitelist/repos.csv") -> list[WhitelistRepo]:
    """从 CSV 加载白名单"""
    repos = []
    p = Path(path)
    if not p.exists():
        return load_whitelist()

    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            repos.append(WhitelistRepo(
                full_name=row["full_name"],
                language=row["language"],
                stars=int(row.get("stars", 0)),
                install_cmd=row.get("install_cmd", ""),
                test_cmd=row.get("test_cmd", ""),
                maintainer_response_days=float(row.get("maintainer_response_days", 7)),
                ext_pr_merge_rate_90d=float(row.get("ext_pr_merge_rate_90d", 0)),
                has_sponsors=row.get("has_sponsors", "").lower() in ("true", "1"),
                has_opencollective=row.get("has_opencollective", "").lower() in ("true", "1"),
                has_algora_tipping=row.get("has_algora_tipping", "").lower() in ("true", "1"),
                bounty_history=float(row.get("bounty_history", 0)),
                common_task_types=row.get("common_task_types", "").split("|") if row.get("common_task_types") else [],
                priority=int(row.get("priority", 0)),
            ))
    return repos


if __name__ == "__main__":
    repos = load_whitelist()
    save_whitelist_csv(repos)
    ts = [r for r in repos if r.language == "typescript"]
    py = [r for r in repos if r.language == "python"]
    print(f"TypeScript: {len(ts)} 个 | Python: {len(py)} 个 | 总计: {len(repos)} 个")
