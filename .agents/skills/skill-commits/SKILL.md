---
name: skill-commits
description: |
  Conventional commit messages with emojis. Use when: user asks for commit message,
  finishing changes, or asks to save/confirm work. Generates formatted commit messages.
license: MIT
metadata:
  author: rapidtest
  version: "1.0.0"
---

# Skill: Commit Messages

Cada vez que hagas un cambio en un archivo y esté terminado, necesitas dar un mensaje para el commit que siga estas reglas.

## Reglas

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
```

## Cuando aplicar

- Después de completar cualquier cambio en archivos
- Antes de finalizar la sesión
- Cuando el usuario pide guardar o confirmar cambios
