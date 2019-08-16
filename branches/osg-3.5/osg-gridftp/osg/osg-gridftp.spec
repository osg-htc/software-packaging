Name:      osg-gridftp
Summary:   Standalone OSG GridFTP with LCMAPS VOMS support
Version:   3.5
Release:   3%{?dist}
License:   Apache 2.0
URL:       http://www.opensciencegrid.org


Source1: udt-%{name}.conf

Requires: osg-system-profiler
Requires: globus-gridftp-server-progs
Requires: vo-client
Requires: vo-client-lcmaps-voms
Requires: grid-certificates >= 7
Requires: gratia-probe-gridftp-transfer >= 1.17.0-1
Requires: fetch-crl
Requires: osg-configure-misc
Requires: osg-configure-gratia
Requires: globus-xio-udt-driver

Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)

# This should also pull in lcas, lcmaps, and various plugins
# (basic, proxy verify, posix, etc)

%description
This is a meta package for a standalone GridFTP server with
support for the LCMAPS VOMS authentication method.




%package xrootd
Summary: OSG GridFTP XRootD Storage Element package

Requires: %{name} = %{version}-%{release}
Requires: xrootd-dsi
Requires: xrootd-fuse >= 1:4.1.0
Requires: gratia-probe-xrootd-transfer >= 1.17.0-1
Requires: gratia-probe-xrootd-storage

%description xrootd
This is a meta-package for GridFTP with the underlying XRootD storage element
using the FUSE/DSI module.

%package hdfs
Summary: OSG GridFTP HDFS Storage Element package

Requires: %{name} = %{version}-%{release}
Requires: gridftp-hdfs >= 0.5.4-16

%description hdfs
This is a meta package for a standalone GridFTP server with 
HDFS and GUMS support.

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/gridftp.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/gridftp.d/

%files
%config(noreplace) %{_sysconfdir}/gridftp.d/udt-%{name}.conf

%files xrootd
# This section intentionally left blank

%files hdfs
# This section intentionally left blank

%changelog
* Fri Aug 16 2019 Brian Lin <blin@cs.wisc.edu> - 3.5-3
- Add HDFS sub-package

* Mon Aug 12 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-2
- Bump version to 3.5 (SOFTWARE-3761)

* Wed Mar 07 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.4-7
- Add mistakenly dropped gratia-probe-xrootd-transfer requirement to
  osg-gridftp-xrootd (SOFTWARE-3141)

* Mon Feb 19 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.4-6
- Combine packaging with osg-gridftp-xrootd (SOFTWARE-3141)

* Mon Jan 08 2018 Edgar Fajardo <emfajard@ucsd.edu> - 3.4-5
- Remove osg-version from dependencies (SOFTWARE-2917)

* Wed Nov 15 2017 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.4-4
- Add osg-configure-gratia to dependencies (SOFTWARE-3019)

* Mon Jun 12 2017 Edgar Fajardo <emfajard@ucsd.edu> - 3.4-3
- Add osg-configure-misc to dependencies (SOFTWARE-2758)

* Mon Jun 05 2017 Brian Lin <blin@cs.wisc.edu> - 3.4-2
- Add vo-client-lcmaps-voms deps to osg-gridftp (SOFTWARE-2760)

* Tue May 23 2017 Brian Lin <blin@cs.wisc.edu> 3.4-1
- Rebuild for OSG 3.4

* Thu Aug 25 2016 Carl Edquist <edquist@cs.wisc.edu> - 3.3-3
- drop gums-client dependency (SOFTWARE-2398)
- remove rhel5-specific macros (OSG-3.2 EOL)

* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-2
- Require grid-certificates >= 7 (SOFTWARE-1883)

* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Tue Apr 21 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-11_clipped
- Create clipped version for el7

* Thu Mar 13 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-9
- Add globus-xio-udt-driver dependency for el6, and enable by default in
  /etc/gridftp.d/ (SOFTWARE-1412)

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-8
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-7
- Added dependencies on osg-version and osg-system-profiler

* Fri Nov 3 2011 Doug Strain <dstrain.fnal.gov> - 3.0.0-6
- Added fetch-crl to the requirements

* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-5
- Do not mark this as a noarch package, as we depend directly on a arch-specific RPM.

* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-4
Another update to get Requires right for 32-bit modules

* Fri Aug 26 2011 Doug Strain <dstrain.fnal.gov> 
- Created an initial gridftp-standalone meta package RPM.

