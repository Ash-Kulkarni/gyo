{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  name = "pyddb dev shell";
  packages = [
    pkgs.python313
    pkgs.nodejs_22
    pkgs.typescript
    pkgs.typescript-language-server
    pkgs.prettierd
    pkgs.uv
    pkgs.cargo
    pkgs.rustc
    pkgs.ruff
    pkgs.mypy
    pkgs.just
  ];
}
