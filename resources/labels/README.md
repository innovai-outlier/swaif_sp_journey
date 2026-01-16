# UI Label Packs

All UI strings must be sourced from locale label packs.

## Files
- `pt-BR.json` (default)
- Add future locales as `<locale>.json` (e.g., `en-US.json`)

## Conventions
- Use dotted keys (e.g., `auth.login.title`)
- Support interpolation with `{name}` placeholders
- Missing key:
  - render `[[missing.key]]`
  - log warning for dev visibility

## Example
Key: `common.save` => "Salvar"
