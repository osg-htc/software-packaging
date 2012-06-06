Summary: CernVM File System Server Utilities
Name: cvmfs-server
Version: 2.0.13
Release: 1
Source0: cvmfs-%{version}.tar.gz
Group: System/Filesystems
License: Copyright (c) 2009, CERN.  Distributed unter the BSD License.
Requires: httpd cvmfs-keys >= 1.1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig
BuildRequires: openssl-devel
%{?el5:BuildRequires: buildsys-macros}
Requires: bash
Requires: coreutils
Requires: grep
Requires: gawk
Requires: sed
Requires: perl
Requires: sudo
Requires: psmisc
Requires: autofs
Requires: fuse
Requires: curl
Requires: attr
# Account for different package names
%if 0%{?suse_version}
Requires: aaa_base
Requires: glibc
Requires: insserv
Requires: util-linux
Requires: pwdutils
Requires(preun): aaa_base insserv
%else
Requires: chkconfig
Requires: glibc-common
Requires: initscripts
Requires: which
Requires: shadow-utils
Requires(post): chkconfig 
Requires(preun): chkconfig initscripts
%endif

%description
HTTP File System for Distributing Software to CernVM.
See http://cernvm.cern.ch
%prep
%setup -q -n cvmfs-%{version}

%build
./configure --enable-sqlite3-builtin --enable-libcurl-builtin --enable-zlib-builtin --disable-cvmfs --prefix=/usr
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
install -D -m 755 add-ons/cvmfs-lvmrotate $RPM_BUILD_ROOT/usr/bin/cvmfs-lvmrotate

%post
/sbin/chkconfig --add cvmfsd

%preun
if [ $1 -eq 0 ]; then
  /sbin/service cvmfsd stop &>/dev/null
  /sbin/chkconfig --del cvmfsd
fi

%files
%defattr(-,root,root)
/usr/bin/cvmfs_sync.bin
/usr/bin/cvmfs_zpipe
/usr/bin/cvmfs_sign
/usr/bin/cvmfs_clgcmp
/usr/bin/cvmfs-sync
/usr/bin/cvmfsd_ctrl
/usr/bin/cvmfs-lvmrotate
/usr/bin/cvmfs_decrypt
/usr/bin/cvmfs_lscat
/usr/bin/cvmfs_mkkey
/usr/bin/cvmfs_unsign
/etc/init.d/cvmfsd
/usr/bin/cvmfs_pull
/usr/bin/cvmfs_scrub
/usr/bin/cvmfs_snapshot
/usr/bin/cvmfs_server
/etc/cvmfs/cgi-bin/replica.cgi
/etc/cvmfs/etc.httpd.conf.d.replica.conf
%config /etc/cvmfs/server.conf 
%config /etc/cvmfs/replica.conf
%doc /usr/share/doc/cvmfs-%{version}/COPYING
%doc /usr/share/doc/cvmfs-%{version}/AUTHORS
%doc /usr/share/doc/cvmfs-%{version}/README
%doc /usr/share/doc/cvmfs-%{version}/NEWS
%doc /usr/share/doc/cvmfs-%{version}/ChangeLog
%doc /usr/share/doc/cvmfs-%{version}/FAQ
%doc /usr/share/doc/cvmfs-%{version}/INSTALL
