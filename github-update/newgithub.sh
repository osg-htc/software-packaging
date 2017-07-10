#!/bin/bash

from=https://vdt.cs.wisc.edu/svn/native/redhat
authors_file=~/authors.txt
workbench=~/git-svn-mirrors/Software-Redhat
to=git@github.com:opensciencegrid/Software-Redhat.git

set -e

svn info "$from"

wget http://vdt.cs.wisc.edu/svn-authors.txt -O "$authors_file"
mkdir -p "$workbench"
git-svn-mirror init --from         "$from" \
                    --to           "$to" \
                    --workbench    "$workbench" \
                    --authors-file "$authors_file"

cd "$workbench"
git fetch || :
git push --force

