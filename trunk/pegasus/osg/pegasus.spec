Name:           pegasus
Version:        4.6.1
Release:        1.1%{?dist}
Summary:        Workflow management system for HTCondor, grids, and clouds
Group:          Applications/System
License:        ASL 2.0
URL:            http://pegasus.isi.edu/
Packager:       Pegasus Development Team <pegasus-support@isi.edu>

Source:         pegasus-source-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-root

# Some OSG Software changes below to use Java 7
BuildRequires:  ant, ant-apache-regexp, java7-devel, gcc, groff, python-devel, gcc-c++, make, asciidoc, libxslt, fop, python-setuptools, openssl-devel
Requires:       java7 >= 1:1.7.0, python >= 2.4, condor >= 7.6, graphviz

# Added by OSG Software, so that all builds and binaries work on el5 and el6
%if 0%{?rhel} < 7
BuildRequires:  ant-nodeps
%endif
BuildRequires:  jpackage-utils, /usr/share/java-1.7.0
Requires:       jpackage-utils, /usr/lib/java-1.7.0, /usr/share/java-1.7.0

%define sourcedir %{name}-source-%{version}

%description
The Pegasus project encompasses a set of technologies that
help workflow-based applications execute in a number of
different environments including desktops, campus clusters,
grids, and now clouds. Scientific workflows allow users to
easily express multi-step computations. Once an application
is formalized as a workflow the Pegasus Workflow Management
Service can map it onto available compute resources and
execute the steps in appropriate order.


%prep
%setup -q -n %{sourcedir}

%build
ant dist-release

# strip executables                                                                                                                               
strip dist/pegasus-%{version}/bin/pegasus-cluster
strip dist/pegasus-%{version}/bin/pegasus-kickstart
strip dist/pegasus-%{version}/bin/pegasus-keg

%install
rm -Rf %{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}

cp -aR dist/pegasus-%{version}/etc/* %{buildroot}/%{_sysconfdir}/%{name}/
cp -aR dist/pegasus-%{version}/bin/* %{buildroot}/%{_bindir}/
cp -aR dist/pegasus-%{version}/lib* %{buildroot}/usr/
cp -aR dist/pegasus-%{version}/share/* %{buildroot}/%{_datadir}/

# rm unwanted files                                                                                                                               
rm -f %{buildroot}/%{_bindir}/keg.condor
rm -f %{buildroot}/%{_datadir}/%{name}/java/COPYING.*
rm -f %{buildroot}/%{_datadir}/%{name}/java/EXCEPTIONS.*
rm -f %{buildroot}/%{_datadir}/%{name}/java/LICENSE.*
rm -f %{buildroot}/%{_datadir}/%{name}/java/NOTICE.*

%clean
ant clean
rm -Rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/
%{_bindir}/*
%{_libdir}/pegasus
%{_libdir}/python*
%{_datadir}/doc/%{name}
%{_datadir}/man/man1/*
%{_datadir}/%{name}


%changelog
* Fri Apr 22 2016 Edgar Fajardo <efajardo@physics.ucsd.edu> -4.6.1-1.1
- Bumped to version 4.6.1 - SOFTWARE-2286
* Thu Oct 02 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 4.3.1-1.3
- Remove ant-nodeps buildrequire on EL7

* Wed Nov 27 2013 Tim Cartwright <cat@cs.wisc.edu> 4.3.1-1.2
- Rebuild with unified spec file across OSG 3.1 and 3.2
- Tweaked arrangement of requires lines to ease comparisons against original

* Tue Nov 26 2013 Edgar Fajardo <efajardo@cern.ch> 4.3.1-1.1
- Used the new upstream source rpm 4.3.1 that includes the patch so the code is compatible with python2.4
- Changed the Requires and BuildRequires section so it enforces Java 7
- Added the CLASSPATH hack to the build section

* Mon Nov 25 2013 Pegasus Development Team <pegasus-support@isi.edu> 4.3.1
- 4.3.1 automatic build

* Wed Nov 20 2013 Edgar Fajardo <efajardo@cern.ch> 4.3.0-2.1
- Changed the Requires and BuildRequires section so it enforces Java 7
- Added the CLASSPATH hack to the build section
- Added the patch0 so the code is compatible with python2.4

* Wed Oct 23 2013 Mats Rynge <rynge@isi.edu> 4.3.0
- 4.3.0 release

* Tue May 07 2013 Carl Edquist <edquist@cs.wisc.edu> - 4.2.0-1.2
- Require missing java dir names instead of workaround package

* Tue Apr 09 2013 Brian Lin <blin@cs.wisc.edu> 4.2.0-1.1
- Change dependencies to use and build against java7

* Wed Mar 13 2013 Mats Rynge <rynge@isi.edu> 4.2.1cvs
- 4.2.1cvs release

* Fri Jan 11 2013 Mats Rynge <rynge@isi.edu> 4.2.0
- 4.2.0 release

* Tue Feb 7 2012 Mats Rynge <rynge@isi.edu> 4.1.0
- 4.1.0 release

* Tue Feb 7 2012 Mats Rynge <rynge@isi.edu> 4.0.0cvs-1
- Preparing for 4.0.0
- Added graphviz-gd as dep

* Mon Aug 29 2011 Mats Rynge <rynge@isi.edu> 3.2.0cvs-1
- Moved to 3.2.0cvs which is FHS compliant

* Fri Jul 22 2011 Doug Strain <dstrain@fnal.gov> 3.0.3-2
- Fixing common.pm
- Adding g++ to dependencies

* Wed Jul 20 2011 Doug Strain <dstrain@fnal.gov> 3.0.3-1
- Initial creation of spec file
- Installs into /usr/share/pegasus-3.0.3
- Binaries into /usr/bin
