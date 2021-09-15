#!/bin/bash
set -x
 
apt-get update
apt-get -y install git rsync python3-pip python3-sphinx python3-sphinx-rtd-theme

export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)

make -C docs clean
make -C docs html
 
docroot=`mktemp -d`
rsync -av "docs/_build/html/" "${docroot}/"
 
pushd "${docroot}"
 
git init
git remote add deploy "git@github.com:wemulate/wemulate.git"
git checkout -b gh-pages
 

touch .nojekyll
cat > README.md <<EOF
# GitHub Pages Cache
 
Nothing to see here. The contents of this branch are essentially a cache that's not intended to be viewed on github.com.
 
 
If you're looking to update our documentation, check the relevant development branch's 'docs/' dir.
EOF
 
git add .
 
msg="Updating Docs"
git commit -am "${msg}"
 
git push deploy gh-pages --force

popd

exit 0
