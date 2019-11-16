#!/bin/sh

set -euo pipefail

BASE=$(realpath $(dirname "$0")/..)
BUILD="$BASE/build/dmg"
DIST="$BASE/dist"
RESOURCES="$BASE/resources"
VERSION=$(python -c "import subsync; print(subsync.version()[0] or '0.0.0')")
APP="subsync.app"
TARGET="$DIST/subsync-${VERSION}-mac-x86_64.dmg"
UPGRADE="$DIST/subsync-${VERSION}-mac-x86_64.zip"

PATH="$PATH:$(dirname $0)"

test -e "$BUILD" && rm -rf "$BUILD"
test -e "$TARGET" && rm -f "$TARGET"
mkdir -p "$BUILD"
mkdir -p "$DIST"
cp -r "$DIST/$APP" "$BUILD"

create-dmg \
	--volname "subsync installer" \
	--volicon "$RESOURCES/icon.icns" \
	--window-pos 300 200 \
	--window-size 700 500 \
	--icon-size 150 \
	--icon "$APP" 200 200 \
	--hide-extension "$APP" \
	--app-drop-link 450 200 \
	--no-internet-enable \
	"$TARGET" "$BUILD"


mkpackage "$UPGRADE" \
	--id="subsync/mac-x86_64" \
	--version="$VERSION" \
	--install="install.sh" \
	--stdin="install.sh" \
	--file="$TARGET" \
	<< END
#!/bin/sh
hdiutil attach -readonly $(basename $TARGET)
END
