{
  inputs = {
    nixpkgs = {
      type = "github";
      owner = "NixOS";
      repo = "nixpkgs";
      ref = "nixos-unstable";
    };

    # srcs
    pocketsphinx-src = {
      type = "github";
      owner = "cmusphinx";
      repo = "pocketsphinx";
      ref = "last-pre-1.0";
      flake = false;
    };
    sphinxbase-src = {
      type = "github";
      owner = "cmusphinx";
      repo = "sphinxbase";
      # Latest commit (deprecated)
      rev = "617e53691889336a482631380f75b453445d0dae";
      flake = false;
    };
  };

  outputs = {
    self,
    nixpkgs,
    pocketsphinx-src,
    sphinxbase-src,
  }: let
    supportedSystems = ["x86_64-linux"];

    perSystem = attrs:
      nixpkgs.lib.genAttrs supportedSystems (system: let
        pkgs = nixpkgs.legacyPackages.${system};
      in
        attrs system pkgs);
  in {
    packages = perSystem (system: pkgs: let
      mkDate = longDate: (pkgs.lib.concatStringsSep "-" [
        (builtins.substring 0 4 longDate)
        (builtins.substring 4 2 longDate)
        (builtins.substring 6 2 longDate)
      ]);
      date = mkDate (self.lastModifiedDate or "19700101");
    in {
      sphinxbase = pkgs.callPackage ./nix/sphinxbase.nix {inherit sphinxbase-src;};
      pocketsphinx = pkgs.callPackage ./nix/pocketsphinx.nix {
        inherit (self.packages.${system}) sphinxbase;
        inherit pocketsphinx-src;
      };

      subsync = pkgs.callPackage ./nix {
        version = date;
        inherit (self.packages.${system}) sphinxbase pocketsphinx;
      };

      default = self.packages.${system}.subsync;
    });

    formatter = perSystem (_: pkgs: pkgs.alejandra);

    devShells = perSystem (_: pkgs: {
      default = pkgs.mkShell {
        packages = with pkgs; [
          alejandra
          # ... more dev packages
        ];
      };
    });
  };
}
