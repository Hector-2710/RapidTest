# Contributing to RapidTest

Thank you for your interest in contributing to RapidTest! This guide will help you get started.

## Code of Conduct

Please be respectful and constructive. We welcome contributions from everyone.

## Ways to Contribute

- 🐛 **Bug Reports**: Report bugs via GitHub Issues
- 💡 **Feature Requests**: Suggest new features
- 📖 **Documentation**: Improve docs or translate
- 💻 **Code Contributions**: Fix bugs or add features
- 🧪 **Testing**: Add or improve test coverage

## Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/Hector-2710/rapidtest.git
cd rapidtest
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -e .
pip install -e ".[dev]"
```

4. **Run tests**
```bash
pytest
```

## Coding Standards

- Follow **PEP 8** style guidelines
- Use **type hints** where possible
- Keep lines under **88 characters** (enforced by Ruff)
- Add **docstrings** to public functions

### Running Linters

```bash
# Format code
ruff format .

# Check for issues
ruff check .

# Type checking
mypy rapidtest/
```

## Pull Request Process

1. **Create a branch** from `main`
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** and commit with clear messages
```bash
git commit -m "feat: add new feature"
```

3. **Push to your fork** and create a Pull Request
```bash
git push origin feature/your-feature-name
```

4. **Fill out the PR template**:
   - Description of changes
   - Related issue (if any)
   - Testing performed

## Commit Message Convention

We follow [Conventional Commits](https://conventionalcommits.org):

```
<type>: <description>

Types: feat, fix, refactor, test, chore, docs, style
```

Examples:
- `feat: add new HTTP method`
- `fix: resolve connection timeout issue`
- `docs: update API reference`

## Testing

- Write tests for new features
- Ensure existing tests pass
- Test both HTTP and ASGI modes when applicable

```python
# Example test structure
def test_http_get():
    from rapidtest import HTTPTest
    api = HTTPTest(url="http://localhost:8000")
    api.get(path="/health", status=200)
```

## Questions?

- Open a GitHub Discussion for questions
- Tag maintainers for urgent issues

Thank you for contributing to RapidTest! 🎉