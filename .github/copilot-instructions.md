# 🧭 Copilot Guidelines for Secure, Sustainable & High-Quality Python Development

This document defines the mandatory standards for **AI-assisted code generation** (e.g., GitHub Copilot, ChatGPT, OpenAI API, etc.) within this repository.
All automatically generated or supported code contributions must comply with these principles.

---

## 🔒 1. Information Security & Compliance

- **ISO/IEC 27001 & 27002**: Ensure confidentiality, integrity, and availability in all code and architectural decisions.
- **OWASP Top 10**: Code must be resistant to common web application risks (Injection, XSS, CSRF, Insecure Deserialization, etc.).
- **GDPR / Privacy**:
  - Avoid unnecessary collection or storage of personal data.
  - Apply data minimization, pseudonymization, and encryption.
  - Logging must not expose PII or credentials.
- **Secrets Management**:
  - Never hardcode secrets or tokens.
  - Use environment variables or secret managers instead.

---

## 📚 2. Documentation & Traceability

- Every module, class, and function must include clear and up-to-date **docstrings** (PEP 257).
- Each module should start with a **purpose statement** and responsibility summary.
- Comments should explain the **“why”**, not just the “how”.
- Document architecture decisions following **ADR (Architecture Decision Records)**.
- Generate and maintain documentation via **Sphinx**, **MkDocs**, or **pdoc**.

---

## 🧪 3. Testing & Quality Assurance

- Use **pytest** as the default test framework.
- Maintain **≥ 90% coverage**, enforced through CI/CD.
- All security-relevant or business-critical logic must include tests.
- Integration tests required for DB, API, and file operations.
- Static & quality analysis tools:
  - `flake8`, `mypy`, `bandit`, `black`, `isort`.
- Pre-commit hooks via `pre-commit` are mandatory.
- Test reports must pass before merge or release.

---

## ⚙️ 4. Performance & Sustainability

- Code must be optimized for **runtime efficiency** and **low energy usage**:
  - Use optimal algorithmic complexity (prefer O(n) over O(n²)).
  - Apply **lazy loading**, **caching**, and avoid redundant computations.
  - Use **profiling tools** (`cProfile`, `line_profiler`, `memory_profiler`).
- Prefer efficient data structures:
  - `set` for membership checks, `deque` for queues, `dict` for indexed access.
- Use asynchronous or concurrent execution for I/O-heavy tasks.
- Optimize to reduce CPU time and power usage → lower CO₂ footprint.

---

## 🧱 5. Architecture & Scalability

- Follow **Clean Architecture** or **Hexagonal Architecture** principles.
- Maintain **loose coupling** and **single responsibility**.
- Apply **Dependency Injection** and clear layer boundaries.
- Database design:
  - Proper indexing for frequent queries.
  - Normalize data (3NF minimum).
  - Use connection pooling for high-load environments.
- Include **logging** (`structlog`, `loguru`) and **metrics/tracing** (`opentelemetry`).

---

## 🧩 6. Versioning, Branching & Releases

- Use **Semantic Versioning (SemVer 2.0.0)**:
  Format → `MAJOR.MINOR.PATCH` (e.g., `v2.3.1`)
- Branch naming conventions:
  - `feature/x.y.z-short-description`
  - `fix/x.y.z-short-description`
  - `release/x.y.z`
- All release branches must:
  1. Pass CI/CD (tests, security, lint, type-check).
  2. Be tagged automatically by the release workflow.
  3. Include an updated `CHANGELOG.md` and version bump.
- Automated versioning handled via **GitHub Actions** using `semantic-release`.

---

## 🧰 7. Patch-Level, Dependencies & Maintenance

- Regularly audit dependencies:
  - Tools: `pip-audit`, `dependabot`.
  - Allow automatic patch updates only after CI success.
- Lock dependencies precisely in `requirements.txt` or `pyproject.toml`.
- Document all changes in `CHANGELOG.md`.

---

## 📊 8. Observability & Monitoring

- All components must expose:
  - **Structured logging** (JSON preferred).
  - **Metrics endpoints** (Prometheus, OpenTelemetry).
  - **Health checks** for readiness & liveness.
- Use consistent log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).

---

## 💡 9. Software Quality & Governance

- Enforce automated code reviews via GitHub Actions / SonarCloud / Codacy.
- Apply continuous integration & deployment (CI/CD).
- Regularly perform **security & performance audits**.
- Maintain up-to-date architecture diagrams (PlantUML / Mermaid).

---

## ♻️ 10. Sustainability & Responsibility

- Avoid unnecessary dependencies or large frameworks.
- Optimize builds, reuse caches, and parallelize tests to reduce energy use.
- Prefer low-impact compute operations.

---

## ✅ 11. Short Prompt for AI Tools

> Always produce **secure, documented, tested, efficient, and sustainable** Python code.
> Follow **ISO 27001**, **OWASP Top 10**, **GDPR**, **Clean Architecture**, and **Semantic Versioning**.
> Generate code with complete docstrings, tests, and explanations.
> Optimize performance and energy efficiency.
