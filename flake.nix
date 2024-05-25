{
  description = "Python venv development template";

  inputs = {
    utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    utils,
    ...
  }:
    utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
      pythonPackages = pkgs.python311Packages; # or any other python version
    in {
      devShells.default = pkgs.mkShell {
        name = "python-venv";
        venvDir = "./.venv";
        buildInputs = [

          # We need this for numpy and opencv to run
          # this is because we are not using the nixpkgs libraries
          # but the libraries are installed through pip to have
          # a more up-to-date version and to have the ability to
          # install other packages that are not in nixpkgs
          # It's also more consistant with non nix users
          pkgs.zlib
          pkgs.libGL
          pkgs.glib

          # You need the following only if you are on wayland
          pkgs.xorg.libX11
          pkgs.xorg.libxcb
          pkgs.xorg.libICE
          pkgs.xorg.libSM
          pkgs.xorg.libXext

          # A Python interpreter including the 'venv' module is required to bootstrap
          # the environment.
          pythonPackages.python

          # This executes some shell code to initialize a venv in $venvDir before
          # dropping into the shell
          pythonPackages.venvShellHook

          # Those are dependencies that we would like to use from nixpkgs, which will
          # add them to PYTHONPATH and thus make them accessible from within the venv.
          # pythonPackages.opencv4
        ];

        # Run this command, only after creating the virtual environment
        postVenvCreation = ''
          unset SOURCE_DATE_EPOCH
          pip install -r requirements.txt
        '';

        # FOR WAYLAND USERS
        # Opencv does not officially support wayland, so we need to set the
        # QT_QPA_PLATFORM to xcb to make it work
        QT_QPA_PLATFORM="xcb";
        # Make libraries avaiable for pip installed modules
        # You don't need the xorg libs if you are not on wayland
        LD_LIBRARY_PATH = "${pkgs.zlib}/lib:${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.libGL}/lib:${pkgs.glib.out}/lib:${pkgs.xorg.libX11}/lib:${pkgs.xorg.libxcb}/lib:${pkgs.xorg.libICE}/lib:${pkgs.xorg.libSM}/lib:${pkgs.xorg.libXext}/lib";

        
        # Now we can execute any commands within the virtual environment.
        # This is optional and can be left out to run pip manually.
        postShellHook = ''
          # allow pip to install wheels
          unset SOURCE_DATE_EPOCH
        '';
      };
    });
}
