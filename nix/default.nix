{
  ffmpeg,
  pkg-config,
  pocketsphinx,
  python3Packages,
  version,
  ...
}: let
  inherit (builtins) concatStringsSep;
in
  python3Packages.buildPythonPackage {
    pname = "subsync";
    inherit version;
    format = "other";

    src = ../.;

    buildInputs = [
      ffmpeg
      pkg-config
      pocketsphinx
    ];

    nativeBuildInputs = with python3Packages; [
      pip
      setuptools
      wheel
    ];

    propagatedBuildInputs = with python3Packages; [
      certifi
      cryptography
      pybind11
      pycryptodome
      pysubs2
      pyyaml
      requests
      utils
    ];

    # The tests are for the GUI
    doCheck = false;

    # 'pip install .' takes care of building the package
    buildPhase = "";

    installPhase = ''
      python -m pip install . ${concatStringsSep " " [
        "--no-index"
        "--no-warn-script-location"
        "--prefix=\"$out\""
        "--no-cache"
      ]}
    '';
  }
