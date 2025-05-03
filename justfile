just:
  just --list

run-server:
    uv run uvicorn server.main:app --reload --use-colors

test-server:
    uv run pytest

run-client:
    npx vite --port=8080 client/

test-client:
    npx vitest
