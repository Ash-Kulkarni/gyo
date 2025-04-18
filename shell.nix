{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  name = "pyddb dev shell";
  packages = [
    pkgs.python313
    pkgs.nodejs_22
    pkgs.typescript-language-server
    pkgs.prettierd
    pkgs.uv
    pkgs.cargo
    pkgs.rustc
    pkgs.ruff
    pkgs.mypy
    pkgs.gum
    pkgs.live-server
  ];

  shellHook = ''
    alias run-server='uv run uvicorn server.main:app --reload'
    alias test-server='uv run pytest'
    alias run-client='uv run live-server --port=8080 client/'
    alias test-client='npx vitest'
  '';
}
