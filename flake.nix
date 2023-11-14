{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
  };

  nixConfig = {
    extra-trusted-public-keys =
      "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = { self, nixpkgs, devenv, systems, ... }@inputs:
    let forEachSystem = nixpkgs.lib.genAttrs (import systems);
    in {
      devShells = forEachSystem (system:
        let pkgs = nixpkgs.legacyPackages.${system};
        in {
          default = devenv.lib.mkShell {
            inherit inputs pkgs;
            modules =
              let

                py-cord = pkgs.python310Packages.buildPythonPackage rec {
                  pname = "py-cord-dev";
                  version = "2.5.0rc5";
                  src = pkgs.fetchPypi {
                    inherit pname version;
                    sha256 =
                      "sha256-6XtnoObhdrESX5heEeBvIULRWDNiVwfQ6RUlJoTtQJk=";
                  };
                  propagatedBuildInputs = with pkgs.python310Packages; [
                    setuptools_scm
                    typing-extensions
                    aiohttp
                  ];
                  # Disable the tests
                  checkPhase = ''
                    echo
                  '';
                };
                openai =
                  pkgs.python310Packages.callPackage ./dev_dependencies/openai.nix
                    { };

                python = pkgs.python310.withPackages (p: [ openai py-cord ]);
              in
              [{
                # https://devenv.sh/reference/options/

                packages = [ python ];

                pre-commit.hooks = {
                  nixpkgs-fmt.enable = true;
                  tests = {
                    enable = true;
                    name = "python-tests";
                    description = "Run tests";
                    entry = "${python}/bin/python -m unittest discover tests";
                    files = ".$";
                  };
                };
              }];
          };
        });
    };
}
