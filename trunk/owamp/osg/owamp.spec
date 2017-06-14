Name: owamp
Summary: owamp - one-way delay tester
Version: 3.2rc4
Release: 2%{?dist}
License: Internet2 License (modified BSD-like)
Group: *Development/Libraries*
URL: http://e2epi.internet2.edu/owamp/
Source: %{name}-%{version}.tar.gz
Patch0: limits_changes.patch
Packager: Aaron Brown <aaron@internet2.edu>
BuildRequires: libtool
Requires: owamp-client, owamp-server, I2util
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
OWAMP is a client/server package that allows one to measure the latency between
hosts. Unlike ping, which can only measure the bidirectional delay, OWAMP
enables you to measure the unidirectional delay between two hosts.

%files


%package client
Summary: owamp client
Group: Applications/Network
%description client
owamp command line utilities for performing owamp measurements with an owamp
server.

%package server
Summary: owamp server
Group: Applications/Network
Requires: I2util, chkconfig, initscripts, shadow-utils, coreutils
%description server
owamp server

#%package devel
#Group: Development/Libraries
#Summary: owamp library headers.
#%description devel
#This package includes header files, and static link libraries for building
#applications that use the owamp library.


# Thrulay and I2Util get installed, but really, shouldn't be instaled.
%define _unpackaged_files_terminate_build      0

%prep
%setup -q

%patch0 -p0

%build
%configure
make

%install
%makeinstall
%{__install} -D -p -m 0755 conf/owampd.init %{buildroot}%{_sysconfdir}/rc.d/init.d/owampd
%{__install} -D -p -m 0755 conf/owampd.limits %{buildroot}%{_sysconfdir}/owampd/owampd.limits
%{__install} -D -p -m 0755 conf/owampd.rpm.conf %{buildroot}%{_sysconfdir}/owampd/owampd.conf

%clean
rm -rf $RPM_BUILD_ROOT 

%post server
if [ "$1" = "1" ]; then
	/sbin/chkconfig --add owampd
	/usr/sbin/useradd -r -s /bin/nologin -d /tmp owamp || :
	mkdir -p /var/lib/owamp
	chown owamp:owamp /var/lib/owamp
fi

%preun server
if [ "$1" = "0" ]; then
    /sbin/chkconfig --del owampd
    /sbin/service owampd stop
fi

%postun server
if [ "$1" = "0" ]; then
	/usr/sbin/userdel owamp || :
fi

if [ "$1" = "1" ]; then
    /sbin/service owampd restart
fi

%files client
%defattr(-,root,root,0755)
%doc README
%{_bindir}/owfetch
%{_bindir}/owping
%{_bindir}/owstats
%{_bindir}/owup
%{_bindir}/powstream
%{_mandir}/man1/owfetch.1.gz
%{_mandir}/man1/owping.1.gz
%{_mandir}/man1/owstats.1.gz
%{_mandir}/man1/owup.1.gz
%{_mandir}/man1/powstream.1.gz

%files server
%defattr(-,root,root,0755)
%{_bindir}/owampd
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sysconfdir}/rc.d/init.d/owampd
%config(noreplace) %{_sysconfdir}/owampd/*

#%files devel
#%defattr(-,root,root,0755)
#%{_libdir}/libbwlib.a
#%{_includedir}/owamp/*

%changelog
* Thu Mar 26 2009 aaron@internet2.edu 1.0-4
- Make upgrading work more seamlessly

* Thu Mar 26 2009 aaron@internet2.edu 1.0-3
- Make sure that /var/lib/owamp is created on install

* Fri Feb 02 2009 aaron@internet2.edu 1.0-2
- Fix the example owampd.limits location

* Fri Aug 22 2008 aaron@internet2.edu 1.0-1
- Initial RPM
