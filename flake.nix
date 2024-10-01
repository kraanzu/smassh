{
  description = "Flake for Smassh";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        name = "smassh";
        version = "3.1.6";

        pkgs = import nixpkgs {inherit system;};
        python3 = pkgs.python312Packages;

        mainPkgs = with python3; [
          poetry-core
          textual
          click
          platformdirs
          requests
        ];
      in {
        packages.default = python3.buildPythonPackage {
          pname = name;
          version = version;
          src = ./.;
          format = "pyproject";

          nativeBuildInputs = with pkgs; [
            poetry
          ];

          propagatedBuildInputs = mainPkgs;

          pythonRelaxDeps = [
            "textual"
            "tzlocal"
            "platformdirs"
          ];

          doCheck = false;  # no tests
        };

        # Deps: Devshell
        devShell = pkgs.mkShell {
          name = "smassh";
          buildInputs =
            mainPkgs
            ++ (with python3; [
              textual-dev
              pre-commit-hooks
              ruff
            ]);
        };
      }
    );
}
