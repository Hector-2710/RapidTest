j# Agent Instructions for Commit Messages

## Overview

Genera mensajes de commit siguiendo la convención Conventional Commits con emojis.

## Reglas de Tipos

| Tipo | Emoji |
|------|-------|
| feat | ✨ |
| refactor | ✅ |
| test | 🧩 |
| fix | 🐛 |
| chore | 🔍 |
| docs | 📝 |
| style | 💅🏻 |

## Formato

```
{emoji} {tipo}: {descripcion corta en infinitivo}
```

## Ejemplos

```
🐛 fix: replace manual string formatting with urllib.parse.urlencode
✨ feat: add user authentication endpoint
✅ refactor: simplify connection error handling in utils.py
🧩 test: add integration tests for token endpoint
🔍 chore: update dependencies in requirements.txt
📝 docs: update README with new features
💅🏻 style: remove unnecessary whitespace in Test.py
```

## Cuando Aplicar

Después de completar cualquier cambio en archivos, antes de finalizar la sesión o cuando el usuario pide guardar/cancelar cambios.
