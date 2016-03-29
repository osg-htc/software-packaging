%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib(1)')}
%endif

Summary:   Tests an OSG Software installation
Name:      osg-test
Version:   1.6.0
Release:   1%{?dist}
License:   Apache License, 2.0
Group:     Applications/Grid
Packager:  VDT <vdt-support@opensciencegrid.org>
Source0:   %{name}-%{version}.tar.gz
AutoReq:   yes
AutoProv:  yes
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

Requires: osg-ca-generator

%description
The OSG Test system runs functional integration tests against an OSG Software
installation.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/osg-test
%{_sbindir}/%{name}
%{python_sitelib}/osgtest

%changelog
* Tue Mar 29 2016 Brian Lin <blin@cs.wisc.edu> - 1.6.0-1
- Add option that exits osg-test on first failure (SOFTWARE-2229)
- Create an input file that determines test sequence (SOFTWARE-2228)
- java.verify_ver does not verify java-1.8.0 (SOFTWARE-2212)

* Fri Feb 26 2016 Brian Lin <blin@cs.wisc.edu> - 1.5.3-1
- Drop tarball tests (SOFTWARE-2214)
- Fix PBS test failures due to EPEL update

* Wed Feb 24 2016 Brian Lin <blin@cs.wisc.edu> - 1.5.2-1
- Drop automated tests of Gratia psacct probe (SOFTWARE-2209)
- Drop extra Gratia logging for failed tests
- use '-long' instead of deprecated '-verbose' for condor_status (SOFTWARE-2210)
- Ignore fetch-crl error when it can't get the lastUpdate time
- Remove htcondor-ce-condor requirement for HTCondor-CE setup tests

* Tue Feb 2 2016 Brian Lin <blin@cs.wisc.edu> - 1.5.1-1
- Fix error due to missing gratia outbox dir

* Tue Feb 2 2016 Brian Lin <blin@cs.wisc.edu> - 1.5.0-1
- Use the new osg-ca-generator library
- Add CVMFS and gratia psacct tests back to the nightlies
- Fix 3.1 -> 3.2 cvmfs cleanup failures (SOFTWARE-2131)

* Thu Dec 17 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.4.33-1
- Only remove OSG-Test CA certs if osg-test created them (SOFTWARE-2129)
- Fixes for pbs tests in EL7 (SOFTWARE-2130, SOFTWARE-1996)
- Handle gratia db schema update in 1.16.3+ (SOFTWARE-1932, SOFTWARE-2075)

* Mon Nov 30 2015 Brian Lin <blin@cs.wisc.edu> 1.4.32-1
- Include the failing command in test output (SOFTWARE-1819)
- Fail test if gatekeeper service succeeds but the gatekeeper is not running
- Ignore CRL signature verification failures

* Tue Oct 27 2015 Brian Lin <blin@cs.wisc.edu> 1.4.31-1
- Fix voms and gfal tests to deal with missing "voms-clients" (SOFTWARE-2085)
- Add osg-test-log-viewer
- Fixes for EL7 tests (SOFTWARE-1996)

* Mon Sep 16 2015 Brian Lin <blin@cs.wisc.edu> 1.4.30-1
- Disable SEG on EL5 (SOFTWARE-1929)
- Generalize retriable yum install error for EL7
- Fix osg-configure skips

* Mon Aug 31 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.29-1
- Skip myproxy tests if server fails to start
- Add skip for supported vo RSV probe in case gums-client is not installed
- Fix xrootd service start/stop under EL7 (SOFTWARE-2005)

* Wed Aug 19 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.28-1
- Fix OSG 3.3 release install bug
- Handle mariadb on EL7

* Tue Aug 13 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.27-1
- Skip lfc-multilib test in 3.3 for compatability
- Improvements to bootstrap-osg-test
- Increase debugging level of HTCondor CE

* Tue Jun 30 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.26-1
- Fix RSV version probe assertion
- Add GPG checks back to the OSG 3.3 tests

* Wed May 20 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.25-1
- Add support for OSG 3.3
- Fix torque configuration (SOFTWARE-1899)
- BadSkip HTCondor CE tests if the service failed to start (SOFTWARE-1898)
- Remove osg-configure unit test output that confused our test reporting (SOFTWARE-1818)

* Thu Mar 05 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.24-1
- Fix install/update failures involving 3.1 due to new xrootd-compat packages in EPEL
- Fix cleanup bug for tests with extra repos
- Add gfal2-plugin-file requirement to gfal2 tests (SOFTWARE-1799)
- Fix fetch-crl whitelist bug (SOFTWARE-1780)

* Wed Feb 04 2015 Brian Lin <blin@cs.wisc.edu> - 1.4.23-1 
- Whitelist gratia-dCache and fetch-crl network failures (SOFTWARE-1748, SOFTWARE-1613)
- Fix skip mechanic of job tests (SOFTWARE-1730)
- Add support for secure passwords with -s/--securepass (SOFTWARE-644)
- Install Java according to the TWiki documentation (SOFTWARE-1720)

* Tue Jan 06 2015 Tim Cartwright <cat@cs.wisc.edu> - 1.4.22-1
- Small tweaks to HTCondor CE tests based on automated test results

* Mon Dec 22 2014 Tim Cartwright <cat@cs.wisc.edu> - 1.4.21-1
- Improve timeout semantics for yum installs & updates (per command)
- Add tests for job environment variables in routine job tests

* Wed Dec 10 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.20-1
- Fix for cleanup tests trying to remove pre-installed packages

* Wed Dec 03 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.19-1
- Improvements to update and cleanup tests for EL5
- Additional changes for EL7 support
- Fix for intermittent failure of condor_ce_ping tests

* Thu Oct 30 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.18-2
- Fix configuration bug that caused osg-test to error out

* Thu Oct 30 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.18-1
- Fix various tests to work with EL7
- Add gfal2 tests (SOFTWARE-1603)
- Add ability to specify multiple update repos

* Wed Sep 03 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.17-1
- Add oasis-config tests (SOFTWARE-901)
- Add condor_ce_trace tests against PBS (SOFTWARE-1459)
- Disable osg-release on EL7
- Fix xrootd4 cleanup errors

* Wed Aug 20 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.16-1
- Add osg-info-services tests
- Update xrootd tests to work with xrootd4 (SOFTWARE-1558)
- Prep work for EL7 (SOFTWARE-1579)

* Tue Jun 3 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.15-1
- Fix error with removing user (SW-1345)
- Add condor_ce_ping test (SW-1458)
- Restored files get restored with original owner/group
- Add more messages to retry list

* Tue May 6 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.14-1
- Add GUMS and HTCondor-CE tests (SOFTWARE-696, SOFTWARE-13338)
- Clean up osg-configure test (SOFTWARE-710)
- Split out lcg-utils tests
- Double gratia test timeouts 

* Mon Apr 7 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.13-1
- Add manual option and speed up fetch-crl tests
- Add lcg-utils tests
- Fixes to myproxy and cleanup tests

* Fri Mar 21 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.12-1
- Allow package cleanup to be retried
- Rebuild to fix dirty source from previous version

* Fri Mar 21 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.11-1
- Include the myproxy configuration file
- Add more retriable messages to yum commands

* Thu Mar 20 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1.4.10-1
- Added the myproxy tests (SOFTWARE-1414)
 
* Tue Mar 04 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.9-1
- Add password to usercert (SOFTWARE-1377)
- Fix condor_ce_trace test (SOFTWARE-1338)
- Update gratia probe dependencies (SOFTWARE-1375)
- Add more errors to yum retry

* Mon Feb 03 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.8-1
- Add retries to package updates
- Use SHA2 CAs/usercerts and test RFC proxies (SOFTWARE-1371)
- Add badskips to globus-job-run tests (SOFTWARE-1363)
- Add preliminary htcondor-ce tests (SOFTWARE-1338)
- Skip osg-configure-cemon tests in OSG 3.2

* Fri Jan 24 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.7-1
- Add retries to package installs
- Downgrade packages that were updated in installation
- Fix bug in osg-release upgrades

* Wed Jan 08 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.6-1
- Increase VOMS admin timeouts
- Clean yum cache after updating osg-release
- Better messages for failed installs

* Tue Dec 17 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.5-1
- Improve yum installation and cleanup

* Mon Nov 25 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.4-1
- All proxies created are now 1024 bits
- Add blahp test and updated PBS setup test accordingly
- Add support for testing updates between OSG versions

* Wed Oct 30 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.3-1
- Add gratia-probe-sge tests
- Add BeStMan debugging
- Additional MySQL backup fixes

* Wed Oct 16 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.2-1
- MySQL backup bug fixes

* Wed Oct 16 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.1-1
- Preserve old MySQL data and restore them on test completion

* Fri Oct 11 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.0-1
- Add creation of OSG CA/CRL and ability to sign host certs

* Wed Oct 9 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.3.7-1
- Reliability improvements to Gratia tests
- Fixed a file reading bug in monitor_file()
- Added a missing import in the timeout handler
- Removed --quiet option to rpm --verify
- Merge EL5 get_package_envra() fix from the ca-certs branch
- Made the global timeout value a config file option

* Thu Oct 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.6-2
- Bump release for 3.2 testing -- no functional change

* Fri Sep 27 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.3.6-1
- Fixed package requirements on two RSV tests

* Thu Sep 26 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.3.5-1
- Many small fixes, especially for VM universe tests

* Fri Sep 20 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.4-1
- Add Java7 specific installation logic

* Fri Sep 20 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.3-1
- New version: fix GUMS tests, add global timeout, add java-version RSV probe
- Fix for monitoring a file that has been log rotated

* Wed Sep 04 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.2-1
- Add GUMS and tarball tests

* Thu Aug 22 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.1-1
- Fix bug where certain config file options weren't being read

* Wed Aug 21 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.0-1
- Add support for a configuration file

* Mon Aug 12 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.11-1
- Added gratia probe tests
- Fixed bestman test bugs

* Mon Jul 22 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.10-1
- New version: Made improvements to core and files library

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9-3
- rebuilt

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9-2
- Bump to rebuild

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9-1
- Fix CVMFS test to work with new CVMFS 2.1

* Fri May 23 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.8-1
- Fix glexec create create user proxy test

* Thu May 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.7-1
- Fix lockfile name for HTCondor 7.8.8

* Wed Apr 10 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.6-1
- New version: Add tests for update installations

* Mon Jan 14 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.5-1
- New version: OkSkip/BadSkip test statuses; updated epel-release-6 rpm filename

* Fri Dec 21 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.4-2
- Remove python-nose dependency

* Wed Dec 19 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.4-1
- New version: some xrootd and fetch-crl test fixes 

* Tue Nov 13 2012 Doug Strain <dstrain@fnal.gov> - 1.2.3-1
- New Version to correct xrootd tests (SL6 GSI now working)

* Wed Oct 17 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.2-1
- New version of upstream software

* Tue Jul 31 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.1-1
- New version of upstream software: new RSV tests; cleanup fix

* Tue Jun 19 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.2.0-1
- New version of upstream software: better backups, more tests

* Wed May 09 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.1.1-1
- New version of upstream software: improve cleanup, fix RSV test

* Mon Apr 23 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.1.0-1
- New version of upstream software: LOTS of new tests, library code

* Wed Mar 14 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.0.1-1
- New version of upstream software: Bug fixes

* Thu Feb 23 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.0.0-1
- New version of upstream software: Fix cert hashes and bootstrap script

* Tue Feb 21 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.12-1
- New version of upstream software: Cleanup bug, new CA certificate hashes

* Mon Feb 20 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.11-1
- New version of upstream software: Fixed bug when tailing files

* Fri Feb 17 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.10-1
- New version of upstream software: Fixed install target

* Fri Feb 17 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.9-1
- New version of upstream software: New library, gLExec tests.
- First release to be built for EL 5 and 6.

* Thu Jan 19 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.8-1
- New version of upstream software: UberFTP tests, small bug fixes.

* Wed Dec 21 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.7-1
- New version of upstream software: VOMS tests; *many* other improvements.

* Tue Nov 16 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.6-1
- New version of upstream software: Better logging and first VOMS-related tests.

* Tue Nov 08 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.5-1
- New version of upstream software: Added GRAM tests.

* Mon Sep 26 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.4-1
- New version of upstream software.

* Thu Sep 15 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.3-1
- Skip the uninstall command when there are no RPMs to remove.

* Thu Sep 15 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.2-1
- Added a command-line option to add extra Yum repos when installing
- Removed the extraneous (and occasionally invalid) user password
- Tightened the verify options for epel- and osg-release

* Mon Sep 12 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.1-2
- Added the python-nose dependency

* Fri Sep 09 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.1-1
- Initial release
