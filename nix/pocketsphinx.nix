{
  autoreconfHook,
  pkg-config,
  pocketsphinx-src,
  python3,
  sphinxbase,
  stdenv,
  swig2,
  ...
}:
stdenv.mkDerivation {
  pname = "pocketsphinx";
  version = pocketsphinx-src.shortRev;

  src = pocketsphinx-src;

  patches = [./patches/pocketsphinx-distutils.patch];

  autoreconfPhase = ''
    ./autogen.sh
  '';
  nativeBuildInputs = [
    autoreconfHook
    pkg-config
    swig2
    python3
  ];
  propagatedBuildInputs = [
    sphinxbase
  ];

  postFixup = ''
    cp $out/include/pocketsphinx/* $out/include
  '';
}
