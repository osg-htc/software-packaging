#!/bin/bash
authors_file=~/authors.txt
workbench=~/git-svn-mirrors/Software-Redhat

wget http://vdt.cs.wisc.edu/svn-authors.txt -O "$authors_file"
git-svn-mirror update "$workbench"

