{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    pkgs = nixpkgs.legacyPackages."x86_64-linux";
    darwinPkgs = nixpkgs.legacyPackages."x86_64-darwin";
  in {
    devShells = {
      "x86_64-linux".default =
        import ./shell.nix {inherit pkgs;};

      "x86_64-darwin".default =
        import ./shell.nix {pkgs = darwinPkgs;};
    };
  };
}
