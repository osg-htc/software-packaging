#-------------------------------------------------------------------------------
# Package definitions
#-------------------------------------------------------------------------------
Name:      xrootd4
Epoch:     1
Version:   4.0.0
Release:   1.1%{?dist}%{?_with_cpp11:.cpp11}%{?_with_clang:.clang}
Summary:   Extended ROOT file server
Group:     System Environment/Daemons
License:   LGPLv3+
URL:       http://xrootd.org/

# git clone http://xrootd.org/repo/xrootd.git xrootd
# cd xrootd
# git-archive master | gzip -9 > ~/rpmbuild/SOURCES/xrootd.tgz
Source0:   xrootd.tar.gz

BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: cmake
BuildRequires: krb5-devel
BuildRequires: readline-devel
BuildRequires: openssl-devel
BuildRequires: fuse-devel
BuildRequires: libxml2-devel
BuildRequires: krb5-devel
BuildRequires: zlib-devel
BuildRequires: ncurses-devel

# selinux
BuildRequires: checkpolicy

%if %{?fedora}%{!?fedora:0} >= 20
BuildRequires: policycoreutils-python
%else
BuildRequires: policycoreutils
%endif

%if %{?_with_tests:1}%{!?_with_tests:0}
BuildRequires: cppunit-devel
%endif

BuildRequires:	doxygen
BuildRequires:	graphviz
%if "%{?rhel}" == "5"
BuildRequires:	graphviz-gd
%endif

%if %{?_with_clang:1}%{!?_with_clang:0}
BuildRequires: clang
%endif

Requires:	  %{name}-libs        = %{epoch}:%{version}-%{release}
Requires:	  %{name}-client-libs = %{epoch}:%{version}-%{release}
Requires:	  %{name}-server-libs = %{epoch}:%{version}-%{release}
Conflicts:  xrootd
#Added the conflicts statements to prevent old plugins from using xroot4 rpms
Conflicts: xrootd-cmstfc < 1.5.1-7
Conflicts: xrootd-dsi < 3.0.4-12
Conflicts: xrootd-hdfs < 1.8.4-2
Conflicts: xrootd-lcmaps < 0.0.7-6
Conflicts: xrootd-status-probe < 0.0.3-7

Requires(pre):		shadow-utils
Requires(pre):		chkconfig
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description
The Extended root file server consists of a file server called xrootd
and a cluster management server called cmsd.

The xrootd server was developed for the root analysis framework to
serve root files. However, the server is agnostic to file types and
provides POSIX-like access to any type of file.

The cmsd server is the next generation version of the olbd server,
originally developed to cluster and load balance Objectivity/DB AMS
database servers. It provides enhanced capability along with lower
latency and increased throughput.

%define policy_dir /usr/share/selinux/targeted

#-------------------------------------------------------------------------------
# libs
#-------------------------------------------------------------------------------
%package libs
Summary:	Libraries used by xrootd servers and clients
Group:		System Environment/Libraries
Conflicts: xrootd-libs

%description libs
This package contains libraries used by the xrootd servers and clients.

#-------------------------------------------------------------------------------
# devel
#------------------------------------------------------------------------------
%package devel
Summary:	Development files for xrootd
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Conflicts: xrootd-devel

%description devel
This package contains header files and development libraries for xrootd
development.

#-------------------------------------------------------------------------------
# client-libs
#-------------------------------------------------------------------------------
%package client-libs
Summary:	Libraries used by xrootd clients
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Conflicts: xrootd-client-libs

%description client-libs
This package contains libraries used by xrootd clients.

#-------------------------------------------------------------------------------
# client-devel
#-------------------------------------------------------------------------------
%package client-devel
Summary:	Development files for xrootd clients
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Conflicts: xrootd-client-devel

%description client-devel
This package contains header files and development libraries for xrootd
client development.

#-------------------------------------------------------------------------------
# server-libs
#-------------------------------------------------------------------------------
%package server-libs
Summary:	Libraries used by xrootd servers
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Conflicts: xrootd-server-libs

%description server-libs
This package contains libraries used by xrootd servers.

#-------------------------------------------------------------------------------
# server-devel
#-------------------------------------------------------------------------------
%package server-devel
Summary:	Development files for xrootd servers
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-server-libs%{?_isa} = %{epoch}:%{version}-%{release}
Conflicts: xrootd-server-devel

%description server-devel
This package contains header files and development libraries for xrootd
server development.

#-------------------------------------------------------------------------------
# private devel
#-------------------------------------------------------------------------------
%package private-devel
Summary:	Legacy xrootd headers
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Conflicts: xrootd-private-devel

%description private-devel
This package contains some private xrootd headers. The use of these
headers is strongly discouraged. Backward compatibility between
versions is not guaranteed for these headers.

#-------------------------------------------------------------------------------
# client
#-------------------------------------------------------------------------------
%package client
Summary:	Xrootd command line client tools
Group:		Applications/Internet
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Conflicts: xrootd-client

%description client
This package contains the command line tools used to communicate with
xrootd servers.

#-------------------------------------------------------------------------------
# fuse
#-------------------------------------------------------------------------------
%package fuse
Summary:	Xrootd FUSE tool
Group:		Applications/Internet
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	fuse
Conflicts: xrootd-fuse

%description fuse
This package contains the FUSE (file system in user space) xrootd mount
tool.

#-------------------------------------------------------------------------------
# doc
#-------------------------------------------------------------------------------
%package doc
Summary:	Developer documentation for the xrootd libraries
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif

%description doc
This package contains the API documentation of the xrootd libraries.

#-------------------------------------------------------------------------------
# selinux
#-------------------------------------------------------------------------------
%package selinux
Summary:	 SELinux policy extensions for xrootd.
Group:		 System Environment/Base
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch: noarch
%endif
Requires:  policycoreutils
Requires:  selinux-policy-targeted

%description selinux
SELinux policy extensions for running xrootd while in enforcing mode.

#-------------------------------------------------------------------------------
# tests
#-------------------------------------------------------------------------------
%if %{?_with_tests:1}%{!?_with_tests:0}
%package tests
Summary: CPPUnit tests
Group:   Development/Tools
Requires: %{name}-client = %{epoch}:%{version}-%{release}
%description tests
This package contains a set of CPPUnit tests for xrootd.
%endif

#-------------------------------------------------------------------------------
# Build instructions
#-------------------------------------------------------------------------------
%prep
%setup -c -n xrootd

%build
cd xrootd
mkdir build
cd build

%if %{?_with_cpp11:1}%{!?_with_cpp11:0}
export CXXFLAGS=-std=c++11
%endif

%if %{?_with_clang:1}%{!?_with_clang:0}
export CC=clang
export CXX=clang++
%endif

%if %{?_with_tests:1}%{!?_with_tests:0}
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=RelWithDebInfo -DENABLE_TESTS=TRUE ../
%else
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=RelWithDebInfo ../
%endif

make -i VERBOSE=1 %{?_smp_mflags}

checkmodule -M -m -o xrootd.mod ../packaging/common/xrootd.te
semodule_package -o xrootd.pp -m xrootd.mod

cd ..
doxygen Doxyfile

#-------------------------------------------------------------------------------
# Installation
#-------------------------------------------------------------------------------
%install
cd xrootd
cd build
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

# configuration stuff
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/*

# var paths
mkdir -p $RPM_BUILD_ROOT%{_var}/log/xrootd
mkdir -p $RPM_BUILD_ROOT%{_var}/run/xrootd
mkdir -p $RPM_BUILD_ROOT%{_var}/spool/xrootd

# init stuff
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xrootd
mkdir -p $RPM_BUILD_ROOT%{_initrddir}

install -m 644 packaging/rhel/xrootd.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/xrootd

install -m 755 packaging/rhel/cmsd.init $RPM_BUILD_ROOT%{_initrddir}/cmsd
install -m 755 packaging/rhel/frm_purged.init $RPM_BUILD_ROOT%{_initrddir}/frm_purged
install -m 755 packaging/rhel/frm_xfrd.init $RPM_BUILD_ROOT%{_initrddir}/frm_xfrd
install -m 755 packaging/rhel/xrootd.init $RPM_BUILD_ROOT%{_initrddir}/xrootd
install -m 755 packaging/rhel/xrootd.functions $RPM_BUILD_ROOT%{_initrddir}/xrootd.functions

# logrotate
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -p -m 644 packaging/common/xrootd.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/xrootd

install -m 644 packaging/common/xrootd-clustered.cfg $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd-clustered.cfg
install -m 644 packaging/common/xrootd-standalone.cfg $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd-standalone.cfg

# client plug-in config
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/client.plugins.d
install -m 644 packaging/common/client-plugin.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/client.plugins.d/client-plugin.conf.example

# client config
install -m 644 packaging/common/client.conf $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/client.conf

# documentation
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
cp -pr doxydoc/html %{buildroot}%{_docdir}/%{name}-%{version}

# selinux
mkdir -p ${RPM_BUILD_ROOT}%{policy_dir}
install -m 644 build/xrootd.pp ${RPM_BUILD_ROOT}%{policy_dir}

%clean
rm -rf $RPM_BUILD_ROOT

#-------------------------------------------------------------------------------
# RPM scripts
#-------------------------------------------------------------------------------
%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post   client-libs -p /sbin/ldconfig
%postun client-libs -p /sbin/ldconfig

%post   server-libs -p /sbin/ldconfig
%postun server-libs -p /sbin/ldconfig

%pre

getent group xrootd >/dev/null || groupadd -r xrootd
getent passwd xrootd >/dev/null || \
       useradd -r -g xrootd -c "XRootD runtime user" \
       -s /sbin/nologin -d %{_localstatedir}/spool/xrootd xrootd
exit 0

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add xrootd
    /sbin/chkconfig --add cmsd
    /sbin/chkconfig --add frm_purged
    /sbin/chkconfig --add frm_xfrd
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service xrootd stop >/dev/null 2>&1 || :
    /sbin/service cmsd stop >/dev/null 2>&1 || :
    /sbin/service frm_purged stop >/dev/null 2>&1 || :
    /sbin/service frm_xfrd stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del xrootd
    /sbin/chkconfig --del cmsd
    /sbin/chkconfig --del frm_purged
    /sbin/chkconfig --del frm_xfrd
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service xrootd condrestart >/dev/null 2>&1 || :
    /sbin/service cmsd condrestart >/dev/null 2>&1 || :
    /sbin/service frm_purged condrestart >/dev/null 2>&1 || :
    /sbin/service frm_xfrd condrestart >/dev/null 2>&1 || :
fi

#-------------------------------------------------------------------------------
# Add a new user and group if necessary
#-------------------------------------------------------------------------------
%pre fuse
getent group xrootd >/dev/null || groupadd -r xrootd
getent passwd xrootd >/dev/null || \
       useradd -r -g xrootd -c "XRootD runtime user" \
       -s /sbin/nologin -d %{_localstatedir}/spool/xrootd xrootd
exit 0

#-------------------------------------------------------------------------------
# Selinux
#-------------------------------------------------------------------------------
%post selinux
semodule -i %{policy_dir}/xrootd.pp
semodule -R

%postun selinux
semodule -R

#-------------------------------------------------------------------------------
# Files
#-------------------------------------------------------------------------------
%files
%defattr(-,root,root,-)
%{_bindir}/cconfig
%{_bindir}/cmsd
%{_bindir}/cns_ssi
%{_bindir}/frm_admin
%{_bindir}/frm_purged
%{_bindir}/frm_xfragent
%{_bindir}/frm_xfrd
%{_bindir}/mpxstats
%{_bindir}/wait41
%{_bindir}/XrdCnsd
%{_bindir}/xrdpwdadmin
%{_bindir}/xrdsssadmin
%{_bindir}/xrootd
%{_mandir}/man8/cmsd.8*
%{_mandir}/man8/cns_ssi.8*
%{_mandir}/man8/frm_admin.8*
%{_mandir}/man8/frm_purged.8*
%{_mandir}/man8/frm_xfragent.8*
%{_mandir}/man8/frm_xfrd.8*
%{_mandir}/man8/mpxstats.8*
%{_mandir}/man8/XrdCnsd.8*
%{_mandir}/man8/xrdpwdadmin.8*
%{_mandir}/man8/xrdsssadmin.8*
%{_mandir}/man8/xrootd.8*
%{_datadir}/xrootd
%{_initrddir}/*
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/xrootd/xrootd-clustered.cfg
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/xrootd/xrootd-standalone.cfg
%attr(-,xrootd,xrootd) %dir %{_var}/log/xrootd
%attr(-,xrootd,xrootd) %dir %{_var}/run/xrootd
%attr(-,xrootd,xrootd) %dir %{_var}/spool/xrootd
%config(noreplace) %{_sysconfdir}/sysconfig/xrootd
%config(noreplace) %{_sysconfdir}/logrotate.d/xrootd

%files libs
%defattr(-,root,root,-)
%{_libdir}/libXrdAppUtils.so.*
%{_libdir}/libXrdCksCalczcrc32.so.*
%{_libdir}/libXrdCrypto.so.*
%{_libdir}/libXrdCryptoLite.so.*
%{_libdir}/libXrdCryptossl.so.*
%{_libdir}/libXrdSec*.so.*
%{_libdir}/libXrdUtils.so.*
# Some of the libraries are used as plugins - need the .so symlink at runtime
%{_libdir}/libXrdCksCalczcrc32.so
%{_libdir}/libXrdCryptossl.so
%{_libdir}/libXrdSec*.so

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/xrootd
%{_includedir}/xrootd/XProtocol
%{_includedir}/xrootd/Xrd
%{_includedir}/xrootd/XrdCks
%{_includedir}/xrootd/XrdNet
%{_includedir}/xrootd/XrdOuc
%{_includedir}/xrootd/XrdSec
%{_includedir}/xrootd/XrdSys
%{_includedir}/xrootd/XrdVersion.hh
%{_includedir}/xrootd/XrdVersionPlugin.hh
# These libraries are not used as plugins
%{_libdir}/libXrdAppUtils.so
%{_libdir}/libXrdCrypto.so
%{_libdir}/libXrdCryptoLite.so
%{_libdir}/libXrdUtils.so

%files client-libs
%defattr(-,root,root,-)
%{_libdir}/libXrdCl.so.*
%{_libdir}/libXrdClient.so.*
%{_libdir}/libXrdFfs.so.*
%{_libdir}/libXrdPosix.so.*
%{_libdir}/libXrdPosixPreload.so.*
%{_sysconfdir}/xrootd/client.plugins.d/client-plugin.conf.example
%config(noreplace) %{_sysconfdir}/xrootd/client.conf
# Some of the libraries are used as plugins - need the .so symlink at runtime
%{_libdir}/libXrdPosixPreload.so

%files client-devel
%defattr(-,root,root,-)
%{_includedir}/xrootd/XrdCl
%{_includedir}/xrootd/XrdClient
%{_includedir}/xrootd/XrdPosix
# These libraries are not used as plugins
%{_libdir}/libXrdCl.so
%{_libdir}/libXrdClient.so
%{_libdir}/libXrdFfs.so
%{_libdir}/libXrdPosix.so

%files server-libs
%defattr(-,root,root,-)
%{_libdir}/libXrdBwm.so.*
%{_libdir}/libXrdPss.so.*
%{_libdir}/libXrdOfs.so.*
%{_libdir}/libXrdServer.so.*
%{_libdir}/libXrdXrootd.so.*
%{_libdir}/libXrdFileCache.so.*
%{_libdir}/libXrdHttp.so.*
# Some of the libraries are used as plugins - need the .so symlink at runtime
%{_libdir}/libXrdBwm.so
%{_libdir}/libXrdPss.so
%{_libdir}/libXrdXrootd.so
%{_libdir}/libXrdFileCache.so
%{_libdir}/libXrdHttp.so

%files server-devel
%defattr(-,root,root,-)
%{_includedir}/xrootd/XrdAcc
%{_includedir}/xrootd/XrdCms
%{_includedir}/xrootd/XrdOss
%{_includedir}/xrootd/XrdSfs
%{_includedir}/xrootd/XrdXrootd
%{_includedir}/xrootd/XrdHttp
# These libraries are not used as plugins
%{_libdir}/libXrdOfs.so
%{_libdir}/libXrdServer.so

%files private-devel
%defattr(-,root,root,-)
%{_includedir}/xrootd/private

%files client
%defattr(-,root,root,-)
%{_bindir}/xprep
%{_bindir}/xrd
%{_bindir}/xrdadler32
%{_bindir}/xrdcopy
%{_bindir}/xrdcp
%{_bindir}/xrdcp-old
%{_bindir}/xrdfs
%{_bindir}/xrdgsiproxy
%{_bindir}/xrdstagetool
%{_mandir}/man1/xprep.1*
%{_mandir}/man1/xrd.1*
%{_mandir}/man1/xrdadler32.1*
%{_mandir}/man1/xrdcopy.1*
%{_mandir}/man1/xrdcp.1*
%{_mandir}/man1/xrdcp-old.1*
%{_mandir}/man1/xrdfs.1*
%{_mandir}/man1/xrdgsiproxy.1*
%{_mandir}/man1/xrdstagetool.1*

%files fuse
%defattr(-,root,root,-)
%{_bindir}/xrootdfs
%{_mandir}/man1/xrootdfs.1*
%dir %{_sysconfdir}/xrootd

%files doc
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}

%if %{?_with_tests:1}%{!?_with_tests:0}
%files tests
%defattr(-,root,root,-)
%{_bindir}/text-runner
%{_libdir}/libXrdClTests.so
%{_libdir}/libXrdClTestsHelper.so
%{_libdir}/libXrdClTestMonitor.so
%endif

%files selinux
%defattr(-,root,root)
%{policy_dir}/xrootd.pp

#-------------------------------------------------------------------------------
# Changelog
#-------------------------------------------------------------------------------
%changelog
* Thu Jun 5 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:4.0.0-1.1
- First packaging of the official release 4.0.0

* Fri May 16 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:4.0.0-3.rc1
- First package on the osg repo of xrootd4. Release candidate 1.
- Added the conflict statements for the xrootd plugins version not yet build with xrootd4.

* Tue Apr 01 2014 Lukasz Janyst <ljanyst@cern.ch>
- correct the license field (LGPLv3+)
- rename to xrootd4
- add 'conflicts' statements
- remove 'provides' and 'obsoletes'

* Mon Mar 31 2014 Lukasz Janyst <ljanyst@cern.ch>
- Add selinux policy

* Fri Jan 24 2014 Lukasz Janyst <ljanyst@cern.ch>
- Import XrdHttp

* Fri Jun 7 2013 Lukasz Janyst <ljanyst@cern.ch>
- adopt the EPEL RPM layout by Mattias Ellert

* Tue Apr 2 2013 Lukasz Janyst <ljanyst@cern.ch>
- remove perl

* Thu Nov 1 2012 Justin Salmon <jsalmon@cern.ch>
- add tests package

* Fri Oct 21 2011 Lukasz Janyst <ljanyst@cern.ch> 3.1.0-1
- bump the version to 3.1.0

* Mon Apr 11 2011 Lukasz Janyst <ljanyst@cern.ch> 3.0.3-1
- the first RPM release - version 3.0.3
- the detailed release notes are available at:
  http://xrootd.org/download/ReleaseNotes.html
