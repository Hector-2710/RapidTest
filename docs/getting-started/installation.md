# Installation

## Requirements

RapidTest requires Python 3.7 or higher.

## Install from PyPI

The easiest way to install RapidTest is using pip:

```bash
pip install rapidtest
```

## Manual Dependencies

If you prefer to install dependencies manually:

```bash
pip install requests faker
```

## Verify Installation

Test your installation by running:

```python
from rapidtest import Test

# This should work without errors
tester = Test(url="https://httpbin.org")
print("RapidTest installed successfully!")
```
