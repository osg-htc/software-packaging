Summary: Tools and utilities for the CREAM service
Name: glite-ce-cream-utils
Version: 1.3.5
Release: 1.1%{?dist}%{!?dist:.el5}
License: Apache Software License
Vendor: EMI
URL: http://glite.cern.ch/
Group: System Environment/Libraries
BuildRequires: cmake, docbook-style-xsl, libxslt
Obsoletes: lcg-info-dynamic-software
Provides: lcg-info-dynamic-software
AutoReqProv: yes
Source: %{name}.tar.gz

%global debug_package %{nil}

%description
This package contains a set of executables called by the CREAM service

%prep
 
%setup -c -q

%build
cmake -DCMAKE_INSTALL_PREFIX:string=%{buildroot} %{_builddir}/%{name}-%{version}
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make install
ln -sf /usr/libexec/glite-ce-glue1-applicationsoftware-env %{buildroot}/usr/libexec/lcg-info-dynamic-software


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir /etc/glite-ce-glue2/
%config(noreplace) /etc/glite-ce-glue2/glite-ce-glue2.conf.template
%dir /etc/glite-ce-dbtool
%config(noreplace) /etc/glite-ce-dbtool/creamdb_min_access.conf.template
%dir /etc/%{name}
%config(noreplace) /etc/%{name}/glite_cream_load_monitor.conf
/usr/bin/*
/usr/libexec/*
%attr(750,root,root) /usr/sbin/JobDBAdminPurger.sh
%doc /usr/share/man/man1/*.1.gz

%changelog
* Fri Jul 22 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.3.5-1.1
- Remove BuildArch line that was keeping it from building for all arches in
  Koji

* Mon Dec 15 2014 CREAM group <cream-support@lists.infn.it> - 1.3.5-1
- Changes for bug https://issues.infn.it/jira/browse/CREAM-106

* Mon Jun 30 2014 CREAM group <cream-support@lists.infn.it> - 1.3.4-1
- Changes for bug https://issues.infn.it/jira/browse/CREAM-149

* Fri May 30 2014 CREAM group <cream-support@lists.infn.it> - 1.3.3-1
- Fixed bug: https://issues.infn.it/jira/browse/CREAM-135

* Tue Jun 25 2013 CREAM group <cream-support@lists.infn.it> - 1.3.2-2
- Internal restructuring


