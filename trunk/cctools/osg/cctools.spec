Name:           cctools
Summary:        Cooperative Computing Tools
Version:        7.0.14
Release:        1%{?dist}
Group:          Applications/System
License:        GPLv2
URL:            http://ccl.cse.nd.edu/software/
Source0:        http://ccl.cse.nd.edu/software/files/cctools-%{version}-source.tar.gz
BuildRoot:       %{_topdir}/BUILDROOT/

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  m4

#cctools package dependencies
BuildRequires:  fuse-devel
BuildRequires:  python-devel
BuildRequires:  swig
BuildRequires:  libuuid-devel
BuildRequires:  readline-devel
BuildRequires:  zlib-devel
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-Embed
BuildRequires:  cvmfs-devel

#the dependencies of globus-connect-server are complex, and ignored for now.
#BuildRequires:  globus-connect-server

#required by cvmfs-devel
BuildRequires:  openssl-devel

#required by cvmfs applications
BuildRequires:  freetype

Requires(post): info
Requires(preun): info

# cctools 4.4.3 was split into sub-packages; allow for upgrades
Provides:       %{name}-chirp            = %{version}-%{release}
Provides:       %{name}-doc              = %{version}-%{release}
Provides:       %{name}-dttools          = %{version}-%{release}
Provides:       %{name}-makeflow         = %{version}-%{release}
Provides:       %{name}-parrot           = %{version}-%{release}
Provides:       %{name}-resource_monitor = %{version}-%{release}
Provides:       %{name}-sand             = %{version}-%{release}
Provides:       %{name}-wavefront        = %{version}-%{release}
Provides:       %{name}-weaver           = %{version}-%{release}
Provides:       %{name}-work_queue       = %{version}-%{release}

Obsoletes:      %{name}-chirp            < 7.0.9
Obsoletes:      %{name}-doc              < 7.0.9
Obsoletes:      %{name}-dttools          < 7.0.9
Obsoletes:      %{name}-makeflow         < 7.0.9
Obsoletes:      %{name}-parrot           < 7.0.9
Obsoletes:      %{name}-resource_monitor < 7.0.9
Obsoletes:      %{name}-sand             < 7.0.9
Obsoletes:      %{name}-wavefront        < 7.0.9
Obsoletes:      %{name}-weaver           < 7.0.9
Obsoletes:      %{name}-work_queue       < 7.0.9

%description
The Cooperative Computing Tools (%{name}) contains Parrot,
Chirp, Makeflow, Work Queue, SAND, and other software.

%package devel
Summary: CCTools package development libraries
Group: Applications/System

%description devel
The CCTools package static libraries and header files

%prep
%setup -n cctools-%{version}-source -q

%build
./configure --prefix /usr \
	--with-python-path /usr \
	--with-swig-path /usr \
	--with-readline-path /usr \
	--with-zlib-path /usr \
	--with-perl-path /usr \
	--with-cvmfs-path /usr \
	--with-fuse-path /usr \
	--with-uuid-path /usr
make %{?_smp_mflags}

#the globus dependency is too complex and ignored for now. When the globus dependency is ready, just add `--with-globus-path / \` into the `./configure` command.

%install
rm -rf $RPM_BUILD_ROOT
make CCTOOLS_INSTALL_DIR=%{buildroot}/usr install
rm -rf %{buildroot}/usr/etc
mkdir -p %{buildroot}%{_defaultdocdir}/cctools
mv %{buildroot}/usr/doc/* %{buildroot}%{_defaultdocdir}/cctools
rm -rf %{buildroot}/usr/doc
%ifarch x86_64
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/cctools/*
#%{_bindir}/*
%{_datadir}/*
%attr(0755,root,root) %{_bindir}/*

%files devel
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/cctools/COPYING
%{_includedir}/cctools/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/lib64/*.so
%{_libdir}/python*
%{_libdir}/perl*
%attr(0755,root,root) %{_libdir}/*.so
%attr(0755,root,root) %{_libdir}/lib64/*.so


%changelog
* Wed Jun 12 2019 Carl Edquist <edquist@cs.wisc.edu> - 7.0.14-1
- Update to 7.0.14 (SOFTWARE-3710)

* Wed May 22 2019 Carl Edquist <edquist@cs.wisc.edu> - 7.0.13-1
- Update to 7.0.13 (SOFTWARE-3710)

* Mon Apr 01 2019 Carl Edquist <edquist@cs.wisc.edu> - 7.0.11-1
- Update to 7.0.11 (SOFTWARE-3626)

* Tue Feb 26 2019 Carl Edquist <edquist@cs.wisc.edu> - 7.0.9-2
- Update to 7.0.9, add Provides/Obsoletes for upgrades (SOFTWARE-3599)

* Wed Nov 18 2015 Marty Kandes <mkandes@ucsd.edu> - 4.4.3-1
- Updated to version 4.4.3

* Wed Apr 22 2015 Jeff Dost <jdost@ucsd.edu> - 4.4.0-1
- Updated to version 4.4.0, updated xrootd build requirements

* Fri Dec 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 4.1.3-3
- Fix build failure on EL7

* Wed Aug 13 2014 Carl Edquist <edquist@cs.wisc.edu> - 4.1.3-2
- Rebuild against xrootd4-devel

* Mon Apr 21 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 4.1.3-1
- Updated to version 4.1.3

* Mon Jan 06 2014 Edgar Fajardo  <efajardo@cern.ch> - 4.0.2-7
- Addded the obsoletes part to the doc subpackage so a clean upgrade is done in cases users had older versions

* Fri Dec 13 2013 Edgar Fajardo <efajardo@cern.ch> - 4.0.2-6
- Created the doc package to include all html docummentation aswell as the api documentation

* Tue Dec 10 2013 Edgar Fajardo <efajardo@cern.ch> - 4.0.2-4
- Added m4, doxygen and nroff so documentation is built.

* Tue Oct 15 2013 Brian Lin <blin@cs.wisc.edu> - 4.0.2-3
- Introduced to the OSG Software Stack

* Thu Oct 10 2013 Lincoln Bryant <lincolnb@hep.uchicago.edu> - 4.0.2-2
- B. Tovar patched segfault in Makeflow when using Condor submit
- Moved Perl from site_perl to vendor_perl

* Wed Sep 18 2013 Lincoln Bryant <lincolnb@hep.uchicago.edu> - 4.0.2-1
- Rebased to 4.0.2

* Mon Aug 19 2013 Lincoln Bryant <lincolnb@hep.uchicago.edu> - 4.0.1-1
- Added CVMFS and FUSE support.
