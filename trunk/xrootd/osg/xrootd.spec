#-------------------------------------------------------------------------------
# We assume the xrootd user when building for the OSG
#-------------------------------------------------------------------------------
%if "0%{?dist}" == "0.osg"
%define _with_xrootd_user 1
%endif

#-------------------------------------------------------------------------------
# Package definitions
#-------------------------------------------------------------------------------
Name:      xrootd
Epoch:     1
Version:   3.1.0
Release:   0.5.rc3%{?dist}%{?_with_xrootd_user:.xu}
Summary:   An eXtended Root Daemon (xrootd)
Group:     System Environment/Daemons
License:   Stanford (modified BSD with advert clause)
URL:       http://xrootd.org/

# git clone http://xrootd.org/repo/xrootd.git xrootd
# cd xrootd
# git-archive master | gzip -9 > ~/rpmbuild/SOURCES/xrootd.tgz
Source0:   xrootd.tar.gz
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: cmake >= 2.8
BuildRequires: readline-devel openssl-devel fuse-devel
BuildRequires: libxml2-devel krb5-devel zlib-devel ncurses-devel

# Perl packaging changed on SLC6 - we require perl-devel to build
%if 0%{?rhel} >= 6
BuildRequires: perl-devel
%endif

%description
%{summary}

#-------------------------------------------------------------------------------
# client
#-------------------------------------------------------------------------------
%package client
Summary: XRootD client
Group:   System Environment/Applications
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
%description client
The XRootD client software.

#-------------------------------------------------------------------------------
# client-devel
#-------------------------------------------------------------------------------
%package client-devel
Summary: Headers for compiling against xrootd-client
Group:   System Environment/Libraries
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: %{name}-libs-devel = %{epoch}:%{version}-%{release}
Requires: %{name}-client = %{epoch}:%{version}-%{release}
%description client-devel
Headers for compiling against xrootd-client

#-------------------------------------------------------------------------------
# fuse
#-------------------------------------------------------------------------------
%package fuse
Summary: XRootD filesystem
Group:   System Environment/Filesystems
Requires: %{name}-client = %{epoch}:%{version}-%{release}
Requires: %{name}-libs   = %{epoch}:%{version}-%{release}
Requires: fuse
%description fuse
Fuse driver for xrootd

#-------------------------------------------------------------------------------
# server
#-------------------------------------------------------------------------------
%package server
Summary: XRootD server
Group:   System Environment/Daemons
Requires: %{name}-libs = %{epoch}:%{version}-%{release}, %{name}-client = %{epoch}:%{version}-%{release}
Obsoletes: xrootd
Requires(post): chkconfig
Requires(preun): chkconfig
# for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts

%description server
XRootD server

#-------------------------------------------------------------------------------
# server-devel
#-------------------------------------------------------------------------------
%package server-devel
Summary: Headers for compiling against xrootd-server
Group:   System Environment/Libraries
Requires: %{name}-server = %{epoch}:%{version}-%{release}
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: %{name}-client = %{epoch}:%{version}-%{release}
Requires: %{name}-libs-devel = %{epoch}:%{version}-%{release}
Requires: %{name}-client-devel = %{epoch}:%{version}-%{release}
Obsoletes: xrootd-devel
%description server-devel
Headers for compiling against xrootd-server

#-------------------------------------------------------------------------------
# libs
#-------------------------------------------------------------------------------
%package libs
Summary: XRootD core libraries
Group:   System Environment/Libraries
%description libs
XRootD core libraries

#-------------------------------------------------------------------------------
# libs devel
#-------------------------------------------------------------------------------
%package libs-devel
Summary: Headers for compiling against xrootd-lib
Group:   System Environment/Libraries
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
%description libs-devel
Headers for compiling against xrootd-libs

#-------------------------------------------------------------------------------
# Build instructions
#-------------------------------------------------------------------------------
%prep
%setup -c -n %{name}

%build
cd %{name}
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr ../
make VERBOSE=1%{?_smp_mflags}

#-------------------------------------------------------------------------------
# Installation
#-------------------------------------------------------------------------------
%install
cd %{name}
cd build
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

# configuration stuff
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/*

# var paths
mkdir -p $RPM_BUILD_ROOT%{_var}/log/%{name}
mkdir -p $RPM_BUILD_ROOT%{_var}/run/%{name}
mkdir -p $RPM_BUILD_ROOT%{_var}/spool/%{name}

# init stuff
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}

%if %{?_with_xrootd_user:1}%{!?_with_xrootd_user:0}
cat packaging/rhel/xrootd.sysconfig | sed -e 's/XROOTD_USER=daemon/XROOTD_USER=xrootd/g' \
  -e 's/XROOTD_GROUP=daemon/XROOTD_GROUP=xrootd/g' > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
%else
install -m 644 packaging/rhel/xrootd.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
%endif


install -m 755 packaging/rhel/cmsd.init $RPM_BUILD_ROOT%{_initrddir}/cmsd
install -m 755 packaging/rhel/frm_purged.init $RPM_BUILD_ROOT%{_initrddir}/frm_purged
install -m 755 packaging/rhel/frm_xfrd.init $RPM_BUILD_ROOT%{_initrddir}/frm_xfrd
install -m 755 packaging/rhel/xrootd.init $RPM_BUILD_ROOT%{_initrddir}/xrootd

%if 0%{?rhel} < 5
install -m 755 packaging/rhel/xrootd.functions-slc4 $RPM_BUILD_ROOT%{_initrddir}/xrootd.functions
%else
install -m 755 packaging/rhel/xrootd.functions $RPM_BUILD_ROOT%{_initrddir}/xrootd.functions
%endif

install -m 644 packaging/common/xrootd-clustered.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/xrootd-clustered.cfg
install -m 644 packaging/common/xrootd-standalone.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/xrootd-standalone.cfg

%clean
rm -rf $RPM_BUILD_ROOT

#-------------------------------------------------------------------------------
# Install rc*.d links
#-------------------------------------------------------------------------------
%post server
/sbin/ldconfig
/sbin/chkconfig --add xrootd
/sbin/chkconfig --add cmsd
/sbin/chkconfig --add frm_purged
/sbin/chkconfig --add frm_xfrd

#-------------------------------------------------------------------------------
# Add a new user and group if necessary
#-------------------------------------------------------------------------------
%if %{?_with_xrootd_user:1}%{!?_with_xrootd_user:0}
%pre server
getent group xrootd >/dev/null || groupadd -r xrootd
getent passwd xrootd >/dev/null || \
       useradd -r -g xrootd -c "XRootD runtime user" \
       -s /sbin/nologin -d /etc/xrootd xrootd
exit 0
%endif

#-------------------------------------------------------------------------------
# Handle deinstallation of the server
#-------------------------------------------------------------------------------
%preun server
if [ "$1" = "0" ]; then
    /sbin/service xrootd stop >/dev/null 2>&1
    /sbin/service cmsdd stop >/dev/null 2>&1
    /sbin/service frm_purged stop >/dev/null 2>&1
    /sbin/service frm_xfrd stop >/dev/null 2>&1
    /sbin/chkconfig --del xrootd
    /sbin/chkconfig --del cmsd
    /sbin/chkconfig --del frm_purged
    /sbin/chkconfig --del frm_xfrd
fi

#-------------------------------------------------------------------------------
# Handle upgrade
#-------------------------------------------------------------------------------
%postun server
/sbin/ldconfig
if [ "$1" -ge "1" ] ; then
    /sbin/service xrootd condrestart >/dev/null 2>&1 || :
    /sbin/service cmsd condrestart >/dev/null 2>&1 || :
    /sbin/service frm_purged condrestart >/dev/null 2>&1 || :
    /sbin/service frm_xfrd condrestart >/dev/null 2>&1 || :
fi

#-------------------------------------------------------------------------------
# Add a new user and group if necessary
#-------------------------------------------------------------------------------
%if %{?_with_xrootd_user:1}%{!?_with_xrootd_user:0}
%pre fuse
getent group xrootd >/dev/null || groupadd -r xrootd
getent passwd xrootd >/dev/null || \
       useradd -r -g xrootd -c "XRootD runtime user" \
       -s /sbin/nologin -d /etc/xrootd xrootd
exit 0
%endif

%post client
/sbin/ldconfig

%postun client
/sbin/ldconfig

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

#-------------------------------------------------------------------------------
# Files
#-------------------------------------------------------------------------------
%files libs
%defattr(-,root,root,-)
%{_libdir}/libXrdSec*.so*
%{_libdir}/libXrdCrypto*.so*
%{_libdir}/libXrdUtils.so*
%{_libdir}/libXrdMain.so*

%files libs-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/XrdVersion.hh
%{_includedir}/%{name}/XrdSec
%{_includedir}/%{name}/XrdSecsss
%{_includedir}/%{name}/XrdCrypto
%{_includedir}/%{name}/XrdSut
%{_includedir}/%{name}/XrdNet
%{_includedir}/%{name}/XrdOuc
%{_includedir}/%{name}/XrdSys
%{_includedir}/%{name}/Xrd
%{_includedir}/%{name}/XProtocol

%files client
%defattr(-,root,root,-)
%{_libdir}/libXrdClient*.so*
%{_libdir}/libXrdPosix.so*
%{_libdir}/libXrdPosixPreload.so*
%{_libdir}/libXrdFfs.so*
%{_libdir}/XrdClientAdmin.pm
%{_bindir}/xprep
%{_bindir}/xrd
%{_bindir}/xrdcp
%{_bindir}/xrdgsiproxy
%{_bindir}/xrdstagetool
%doc %{_mandir}/man1/xprep.1.gz
%doc %{_mandir}/man1/xrd.1.gz
%doc %{_mandir}/man1/xrdadler32.1.gz
%doc %{_mandir}/man1/xrdcp.1.gz
%doc %{_mandir}/man1/xrdstagetool.1.gz
%doc %{_mandir}/man1/xrdgsiproxy.1.gz

%files client-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/XrdClient
%{_includedir}/%{name}/XrdPosix
%{_includedir}/%{name}/XrdFfs

%files fuse
%defattr(-,root,root,-)
%{_bindir}/xrootdfs
%doc %{_mandir}/man1/xrootdfs.1.gz

%if %{?_with_xrootd_user:1}%{!?_with_xrootd_user:0}
%attr(-,xrootd,xrootd) %dir %{_sysconfdir}/%{name}/
%else
%attr(-,daemon,daemon) %dir %{_sysconfdir}/%{name}/
%endif


%files server
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
%{_bindir}/xrdadler32
%{_bindir}/XrdCnsd
%{_bindir}/xrdpwdadmin
%{_bindir}/xrdsssadmin
%{_bindir}/xrootd
%{_libdir}/libXrdBwm.so*
%{_libdir}/libXrdPss*.so*
%{_libdir}/libXrdOfs*.so*
%{_libdir}/libXrdServer.so*
%doc %{_mandir}/man8

%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%if %{?_with_xrootd_user:1}%{!?_with_xrootd_user:0}
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/%{name}/xrootd-clustered.cfg
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/%{name}/xrootd-standalone.cfg
%attr(-,xrootd,xrootd) %dir %{_var}/log/%{name}
%attr(-,xrootd,xrootd) %dir %{_var}/run/%{name}
%attr(-,xrootd,xrootd) %dir %{_var}/spool/%{name}
%else
%config(noreplace) %{_sysconfdir}/%{name}/xrootd-clustered.cfg
%config(noreplace) %{_sysconfdir}/%{name}/xrootd-standalone.cfg
%attr(-,daemon,daemon) %dir %{_var}/log/%{name}
%attr(-,daemon,daemon) %dir %{_var}/run/%{name}
%attr(-,daemon,daemon) %dir %{_var}/spool/%{name}
%endif

%{_datadir}/%{name}/utils
%{_initrddir}/%{name}
%{_initrddir}/cmsd
%{_initrddir}/frm_xfrd
%{_initrddir}/frm_purged
%{_initrddir}/xrootd
%{_initrddir}/xrootd.functions

%files server-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/XrdAcc
%{_includedir}/%{name}/XrdBwm
%{_includedir}/%{name}/XrdCms
%{_includedir}/%{name}/XrdOfs
%{_includedir}/%{name}/XrdOss
%{_includedir}/%{name}/XrdPss
%{_includedir}/%{name}/XrdFrc
%{_includedir}/%{name}/XrdSfs
%{_includedir}/%{name}/XrdCks

#-------------------------------------------------------------------------------
# Changelog
#-------------------------------------------------------------------------------
%changelog
* Tue Oct 05 2011 Lukasz Janyst <ljanyst@cern.ch> 3.1.0-0.rc1
- bump the version to 3.1.0-rc1

* Tue Apr 11 2011 Lukasz Janyst <ljanyst@cern.ch> 3.0.3-1
- the first RPM release - version 3.0.3
- the detailed release notes are available at:
  http://xrootd.org/download/ReleaseNotes.html
