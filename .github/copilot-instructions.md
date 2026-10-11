# Repository Guidelines

## Default behavior

- Do not create, edit, delete, or rename files unless the user explicitly requests an implementation or file change.
- Treat questions as requests for explanation, review, diagnosis, or planning by default.
- When implementation has not been requested, provide explanations, findings, suggested changes, and commands without applying changes.
- If a request is ambiguous between explanation and implementation, ask the user which they prefer.

## When implementation is explicitly requested

- Inspect the relevant files before making changes.
- Make precise, focused changes that address the request and avoid unrelated edits.
- Preserve existing behavior unless the user requests a behavior change.
- Follow existing project patterns and keep changes type-safe.
- Run the smallest relevant tests or validation commands when practical.
- Summarize changed files and validation results afterward.
