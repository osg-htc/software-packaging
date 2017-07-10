## github-update

Updates the opensciencegrid/Software-Redhat GitHub repository, which is a mirror of the native/redhat tree in SVN.

## Requirements

* an SSH deploy key
* Ruby
* git-svn-mirror (avail. as a RubyGem)

## Usage

1. Set up the SSH deploy key and test it.
2. Edit the paths in `newgithub.sh` and run it once. This initializes a local mirror to periodically update and push to GitHub.
3. Edit the paths in `updategithub.sh` and set it to be run automatically - SystemD service file provided.

