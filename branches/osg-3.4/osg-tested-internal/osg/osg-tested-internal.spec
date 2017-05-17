Name:      osg-tested-internal
Summary:   All OSG packages we test (internal use only)
Version:   3.3
Release:   17%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


################################################################################
#
# Common
#
################################################################################
Requires: edg-mkgridmap
Requires: glexec
Requires: /usr/sbin/condor_master
Requires: yum-utils
# https://twiki.grid.iu.edu/bin/view/Documentation/Release3/InstallCvmfs
Requires: osg-oasis
Requires: osg-configure-tests

Requires: gratia-probe-condor
Requires: gratia-probe-glexec
Requires: gratia-probe-dcache-storage
Requires: gratia-probe-gridftp-transfer
Requires: gratia-probe-pbs-lsf
Requires: gratia-probe-sge

Requires: myproxy
Requires: myproxy-server

Requires: osg-gums

Requires: htcondor-ce
Requires: htcondor-ce-client
Requires: htcondor-ce-condor
Requires: htcondor-ce-view

Requires: osg-ce-condor

Requires: torque-server
Requires: torque-mom
Requires: torque-client
Requires: torque-scheduler
Requires: osg-ce-pbs

Requires: rsv

Requires: xrootd
Requires: xrootd-client

Requires: ndt-client

Requires: gratia-service

Requires: osg-voms

# Putting bestman back again in the teest in 2016-Apr-28 - SOFTWARE-2089
Requires: osg-se-bestman
Requires: osg-se-bestman-xrootd

%if 0%{?rhel} == 5
Requires: globus-gram-job-manager-pbs-setup-poll
%endif

%if 0%{?rhel} == 7
# osg-tested-internal packages in el7 don't currently pull in mysql/mariadb
Requires: mariadb-server
%endif

%description
%{summary}


%package gram
Summary:   All OSG packages we test (internal use only) + GRAM
Requires: %{name}
Requires: globus-gatekeeper
Requires: globus-gram-client-tools
Requires: globus-gram-job-manager
Requires: globus-gram-job-manager-fork
Requires: globus-gram-job-manager-fork-setup-poll
Requires: gratia-probe-gram
Requires: globus-gram-job-manager-scripts
Requires: globus-gram-job-manager-condor
Requires: globus-gram-job-manager-pbs-setup-seg


%description gram
%{summary}


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files

%files gram

%changelog
* Wed Apr 5 2017 Brian Lin <blin@cs.wisc.edu> - 3.3-17
- Drop gratia-probe-bdii-status since BDII is no longer available in the OSG

* Fri Oct 2 2016 Brian Lin <blin@cs.wisc.edu> - 3.3-16
- Add htcondor-ce-view (SOFTWARE-2493)

* Mon Sep 19 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-15
- Re-enable osg-voms for EL7 (SOFTWARE-2461)

* Tue Aug 30 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-13
- Add gram subpackage (SOFTWARE-2441)

* Thu Jun 09 2016 Brian Lin <blin@cs.wisc.edu> - 3.3-12
- Re-enable osg-gums for EL7

* Thu Apr 28 2016 Edgar Fajardo <emfajard@ucsd.edu> - 3.3-11
- Put the osg-bestman requirements back for el7 (SOFTWARE-2089)

* Mon Feb 22 2016 Edgar Fajardo <emfajard@ucsd.edu> - 3.3-10
- Drop the gratia-probe-psacct requirements (SOFTWARE-2213)
 
* Thu Feb 18 2016 Brian Lin <blin@cs.wisc.edu> - 3.3-9
- Drop bestman package requirements for el7 (SOFTWARE-2089)

* Tue Feb 16 2016 Brian Lin <blin@cs.wisc.edu> - 3.3-8
- Replace cvmfs-* requirements with osg-oasis metapackage (SOFTWARE-2190)

* Mon Oct 26 2015 Carl Edquist <edquist@cs.wisc.edu> - 3.3-7
- Add bestman package requirements back for el7 (SOFTWARE-2089)

* Mon Oct 19 2015 Carl Edquist <edquist@cs.wisc.edu> - 3.3-6
- Add mariadb-server requirement for el7 (SOFTWARE-1996)

* Tue Sep 15 2015 Brian Lin <blin@cs.wisc.edu> 3.3-5
- Fix pbs-setup-poll package name

* Fri Sep 11 2015 Brian Lin <blin@cs.wisc.edu> 3.3-4
- Install globus-grid-job-manager-pbs-setup-poll for EL5 (SOFTWARE-1929)

* Fri Aug 21 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-3
- Actually include torque

* Fri Aug 21 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-2
- Install more el7 packages now that we have more:
  - torque and osg-ce-pbs
  - xrootd and xrootd-client
  - ndt-client
- Remove the %%if 0%%{?rhel} == 7 section: all packages within it are now brought in by the common packages

* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Wed Apr 22 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2-10
- Add rsv and osg-ce-condor to el7

* Fri Mar 27 2015 Carl Edquist <edquist@cs.wisc.edu> - 3.2-9
- Change cvmfs-keys requirement to cvmfs-config (SOFTWARE-1848)

* Tue Mar 03 2015 Brian Lin <blin@cs.wisc.edu> 3.2-8
- Change xrootd requirements to reflect reversion to old package name

* Fri Oct 31 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2-7
- Add lcas-lcmaps-gt4-interface to RHEL 7

* Mon Oct 20 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2-6
- Move htcondor-ce to common now that it builds on EL7

* Thu Oct 09 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2-5
- Add RHEL 7 and non-RHEL 7 sections

* Mon Aug 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.2-4
- update xrootd requirements to xrootd4

* Mon Apr 21 2014 Brian Lin <blin@cs.wisc.edu> - 3.2-3
- Re-add htcondor-ce requirements

* Tue Apr 1 2014 Brian Lin <blin@cs.wisc.edu> - 3.2-2
- Remove htcondor-ce requirements until htcondor-ce tests are fixed in osg-test

* Wed Mar 19 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 3.2-1
- Add myproxy and my proxy requirements.
- Change of version from 1 to 3.2 and release from 19 to 1

* Mon Feb 17 2014 Brian Lin <blin@cs.wisc.edu> - 1-19
- Add htcondor-ce requirements

* Tue Oct 22 2013 Brian Lin <blin@cs.wisc.edu> - 1-18
- Add gratia-probe-sge 

* Wed Sep 25 2013 Tim Cartwright <cat@cs.wisc.edu> - 1-17
- Add ndt-client to eliminate a skipped test

* Wed Aug 28 2013 Brian Lin <blin@cs.wisc.edu> - 1-16
- Add osg-gums

* Thu Aug 01 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1-15
- Add /usr/sbin/condor_master so we get 'condor' and not 'empty-condor'

* Thu Aug 01 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1-14
- Add gratia-service and several probes

* Thu Apr 04 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1-13
- xrootd-server renamed to xrootd to match renaming in xrootd 3.3.1

* Tue Jun 26 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-12
- Add cvmfs-keys

* Sat Jun 09 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-11
- Re-add osg-configure-tests

* Thu Jun 07 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-10
- Add cvmfs

* Mon May 21 2012 Alain Roy <roy@cs.wisc.edu> - 1-9
- Dropped osg-configure-tests because the new version isn't ready for osg-release.

* Thu May 17 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-8
- Add xrootd-server and xrootd-client

* Thu May 17 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-7
- Add osg-configure-tests and pbs/torque rpms

* Tue Apr 24 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-6
- Add osg-se-bestman-xrootd, rsv

* Mon Apr 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-5
- bestman2-* packages replaced with osg-se-bestman

* Mon Apr 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-4
- Added all packages we test on RHEL 5 to RHEL 6, now that they're ready
- Added bestman2

* Fri Apr 06 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-3
- Removed lfc-python from list; has depsolver issues
- Added yum-utils

* Thu Apr 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-2
- Removed multilib testing of lfc-python* from RHEL 5
- Fixed syntax for multilib testing of lfc-python for RHEL 6

* Thu Apr 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-1
- Created

