{
  autoreconfHook,
  bison,
  pkg-config,
  python3,
  sphinxbase-src,
  stdenv,
  swig2,
  ...
}:
stdenv.mkDerivation {
  name = "sphinxbase";
  version = sphinxbase-src.shortRev;

  src = sphinxbase-src;

  buildInputs = [bison pkg-config python3 swig2];
  nativeBuildInputs = [autoreconfHook];

  autoreconfPhase = ''
    ./autogen.sh
  '';

  postFixup = ''
    cp $out/include/sphinxbase/* $out/include/
  '';
}
