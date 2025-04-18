Name:      osg-tested-internal
Summary:   All OSG packages we test (internal use only)
Version:   3.5
Release:   5%{?dist}
License:   Apache 2.0
URL:       http://www.opensciencegrid.org



################################################################################
#
# Common
#
################################################################################
Requires: osg-oasis
%if 0%{?el8}
Requires: osg-wn-client
%endif

%if 0%{?rhel} < 8
Requires: /usr/sbin/condor_master
Requires: yum-utils
Requires: osg-configure-tests

Requires: gratia-probe-condor
Requires: gratia-probe-dcache-storage
Requires: gratia-probe-gridftp-transfer
Requires: gratia-probe-pbs-lsf
Requires: gratia-probe-sge

Requires: gsi-openssh-server
Requires: gsi-openssh-clients

Requires: myproxy
Requires: myproxy-server

Requires: htcondor-ce
Requires: htcondor-ce-client
Requires: htcondor-ce-condor
Requires: htcondor-ce-view

Requires: osg-ce-condor

Requires: osg-gridftp

Requires: torque-server
Requires: torque-mom
Requires: torque-client
Requires: torque-scheduler
Requires: osg-ce-pbs

Requires: singularity

Requires: xrootd-client
Requires: osg-xrootd-standalone

Requires: voms-server
Requires: voms-clients-cpp
Requires: voms-mysql-plugin

Requires: globus-gass-copy-progs
Requires: uberftp



%endif  # %%if 0%%{?rhel} < 8

%if 0%{?rhel} >= 7
# osg-tested-internal packages in el7 don't currently pull in mysql/mariadb
Requires: mariadb-server
%else
Requires: mysql-server
%endif


%description
%{summary}

%install

%files

%changelog
* Tue Aug 04 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.5-5
- Add mysql/mariadb for EL8 (needed by slurmdbd) (SOFTWARE-4204)

* Fri Jul 24 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.5-4
- Add EL8 packages (SOFTWARE-3308)

* Mon Jan 13 2020 Diego Davila <didavila@ucsd.edu> - 3.5-3
- Changing Requires: xrootd and xrootd-lcmaps for osg-xrootd-standalone (SOFTWARE-3964)

* Tue Dec 10 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.5-2
- Add globus-gass-copy-progs and uberftp (SOFTWARE-3945)

* Fri Aug 02 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-1
- Drop rsv for OSG 3.5 (SOFTWARE-3761)

* Tue Jan 22 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4-7
- Rename singularity-runtime requirement to singularity (SOFTWARE-3532)

* Wed May 23 2018 Brian Lin <blin@cs.wisc.edu> - 3.4-6
- Add xrootd-lcmaps (SOFTWARE-3264)

* Tue Sep 19 2017 Edgar Fajardo <emfajard@ucsd.edu> - 3.4-5
- Added singularity-runtime to the requirements (SOFTWARE-2894)

* Fri Jul 14 2017 Edgar Fajardo <emfajard@ucsd.edu> - 3.4-4
- Added the correct name of the gsi-openssh packages

* Fri Jul 14 2017 Edgar Fajardo <emfajard@ucsd.edu> - 3.4-3
- Add gsi-openssh (SOFTWARE-2810)
- Add osg-gridftp (SOFTWARE-2829)

* Thu May 26 2017 Brian Lin <blin@cs.wisc.edu> - 3.4-2
- Add voms-mysql-plugin back for voms-proxy-init testing

* Tue May 23 2017 Brian Lin <blin@cs.wisc.edu> - 3.4-1
- Drop requirements for packages no longer in 3.4 (SOFTWARE-2734)
- Explicitly require mysql-server for VOMS

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

