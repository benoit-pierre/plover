#! /bin/bash

set -ex

cd "$(dirname "$0")"
. ./PKGBUILD
pkgver="$(git describe --tags | sed -n '/^\([0-9.]\+\)-\([0-9]\+\)-\([0-9a-z]\+\)$/{s//\1.\2.\3/;s/-/./g;p;Q0};Q1')"
src="src/$pkgname-$pkgver"
rm -rf src pkg
mkdir -p "$src"
sed "s/^pkgver=.*\$/pkgver=$pkgver/;s/^_versiondir=.*$/_versiondir=80/" PKGBUILD >PKGBUILD.tmp
(cd "$OLDPWD" && git ls-files -z | xargs -0 cp -a --no-dereference --parents --target-directory="$OLDPWD/$src")
makepkg --clean --noextract -p PKGBUILD.tmp "$@"
rm -f PKGBUILD.tmp
