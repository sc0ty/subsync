{
  cmake,
  pocketsphinx-src,
  stdenv,
  ...
}:
stdenv.mkDerivation {
  pname = "pocketsphinx";
  version = pocketsphinx-src.shortRev;

  src = pocketsphinx-src;

  buildInputs = [cmake];
}
