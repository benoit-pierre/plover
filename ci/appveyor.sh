#!/bin/sh

set -e

. ./utils/functions.sh

appveyor_install()
{
  # Setup development environment.
  bootstrap_dev
}

appveyor_before_build()
{
  # Update version number from VCS.
  run "$python" setup.py patch_version
}

appveyor_build_script()
{
  run "$python" setup.py build
}

appveyor_test_script()
{
  run "$python" setup.py test
}

appveyor_after_test()
{
  run "$python" setup.py bdist_win -t -z -i
}

[ $# -eq 1 ]

python='python'

appveyor_"$1"
