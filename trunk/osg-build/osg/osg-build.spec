%global betatag .pre
%global _release 1

Name:           osg-build
Version:        1.8.92
Release:        %{?betatag:0.}%{_release}%{?betatag}%{?dist}
Summary:        Build tools for the OSG

License:        Apache 2.0
URL:            https://twiki.grid.iu.edu/bin/view/SoftwareTeam/OSGBuildTools

Source0:        %{name}-%{version}.tar.gz
Patch0:         koji-hub-testing.patch

BuildArch:      noarch

Requires:       %{name}-base
Requires:       %{name}-mock
Requires:       %{name}-koji


Obsoletes:      vdt-build <= 0.0.17
Provides:       vdt-build = %{version}

%description
%{summary}
See %{url} for details.


%package base
Requires:       git
Requires:       rpm-build
Requires:       quilt
Requires:       rpmlint
Requires:       subversion
Requires:       wget
Requires:       python >= 2.6
Summary:        OSG-Build base package, not containing mock or koji modules or koji-based tools

%description base
%{summary}
Installing this package makes osg-build and osg-import-srpm
available. osg-build can do rpmbuilds and run the lint and quilt
tasks. osg-build-mock is required to use the mock task, and
osg-build-koji is required to use the koji task.


%package mock
Requires:       %{name}-base
Requires:       mock >= 1.0.0
Summary:        OSG-Build Mock plugin, allows builds with mock

%description mock
%{summary}


%package koji
Requires:       %{name}-base
Requires:       openssl
Requires:       koji >= 1.7.0
Summary:        OSG-Build Koji plugin and Koji-based tools

%description koji
%{summary}
Installing this package enables the 'koji' task in osg-build and adds
the following tools:
- koji-blame
- koji-tag-diff
- osg-koji
- osg-promote


%package tests
Requires:       %{name}
Summary:        OSG-Build tests

%description tests
%{summary}


%prep
%setup -q -n %{name}-%{version}

# changes the koji-hub URL to koji-hub-testing.chtc.wisc.edu, for testing only
# % patch0 -p1

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files

%files tests
%{_bindir}/osg-build-test
%dir %{python_sitelib}/osgbuild/test
%{python_sitelib}/osgbuild/test/*.py*

%files base
%{_bindir}/%{name}
%{_bindir}/osg-import-srpm
%{_bindir}/vdt-build
%dir %{python_sitelib}/osgbuild
%{python_sitelib}/osgbuild/__init__.py*
%{python_sitelib}/osgbuild/constants.py*
%{python_sitelib}/osgbuild/error.py*
%{python_sitelib}/osgbuild/fetch_sources.py*
%{python_sitelib}/osgbuild/git.py*
%{python_sitelib}/osgbuild/importer.py*
%{python_sitelib}/osgbuild/main.py*
%{python_sitelib}/osgbuild/srpm.py*
%{python_sitelib}/osgbuild/svn.py*
%{python_sitelib}/osgbuild/utils.py*
%{_datadir}/%{name}/rpmlint.cfg
%doc %{_docdir}/%{name}/sample-osg-build.ini

%files mock
%{python_sitelib}/osgbuild/mock.py*

%files koji
%{_bindir}/koji-blame
%{_bindir}/koji-tag-diff
%{_bindir}/osg-koji
%{_bindir}/osg-promote
%{python_sitelib}/osgbuild/clientcert.py*
%{python_sitelib}/osgbuild/kojiinter.py*
%{python_sitelib}/osgbuild/promoter.py*
%{_datadir}/%{name}/osg-koji-site.conf
%{_datadir}/%{name}/osg-koji-home.conf
%{_datadir}/%{name}/promoter.ini


%changelog
* Wed Apr 26 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.8.92-0.1
(prerelease)
- Make koji and mock optional modules that can be shipped as separate
  subpackages and will be loaded if necessary. (SOFTWARE-2671)
- Improve `osg-build --help` text to be more consistent and show default
  values for options. (SOFTWARE-2558)
- Drop Python 2.4 compatibility
- Add support for OSG 3.4 (SOFTWARE-2693)
- Add new .source file syntax to fetch sources directly from Git repos
  (SOFTWARE-2689)
- Drop EL 5 packaging

* Tue Apr 04 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.8.1
- Set 'use_old_ssl=True' in template user config to work around SOFTWARE-2616

* Wed Feb 01 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.8.0
- Use koji 1.11 on CSL systems and update template config to koji 1.7+ version
  (adds dependency on koji >= 1.7) (SOFTWARE-2566)
- Remove broken --mock-config=AUTO (autogenerating a mock config from a template)
- Fix KeyError on non-RHEL-like systems (e.g. Fedora)
- Improve explanatory text in osg-koji setup (SOFTWARE-2455)

* Thu Sep 01 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.7.1-1
- Don't print "Implicitly building for el..." message unless in verbose mode
- Add update action (--update or -U) to osg-import-srpm
- Some internal cleanup

* Mon Aug 08 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.7.0-1
- Add three-way diff support to osg-import-srpm
- Make osg-build log messages look nicer by replacing the
  'LOGLEVEL:osg-build:' prefix with a plain ' >> '
- Remove broken test_mock_auto_cfg
- Tweak language in osg-import-srpm when creating .source files
- Add subversion and git as requirements

* Mon Jun 27 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.6.4-1
- Rename koji-hub.batlab.org to koji.chtc.wisc.edu (SOFTWARE-2175)
- Do not enforce vcs branch checks for scratch builds (SOFTWARE-1876)

* Tue Apr 12 2016 Matyas Selmeci <matyas@cs.wisc.edu> 1.6.3-1
- include CILogon-OSG CA cert in CA bundle created by `osg-koji setup' (SOFTWARE-2273)

* Fri Feb 19 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6.2-1
- Change osg-promote table layout to put build first (SOFTWARE-2116)

* Mon Aug 17 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6.1-1
- Change promotion aliases testing, prerelease, and contrib to point to 3.3 instead of 3.2
- Fix unit tests to work with new default dvers
- Drop upstreamed patches

* Wed Aug 12 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6.0-3
- Change default dvers for building out of trunk to be el6 and el7 (instead of el5 and el6)

* Tue Aug 04 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6.0-2
- Change default dvers for upcoming* promotion routes to be el6 and el7 (instead of el5 and el6)

* Thu Jul 30 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6.0-1
- Add promotion routes for goc repos (SOFTWARE-1969)
- Read promotion route definitions from an ini file instead of guessing from available Koji tags
- Fix promotion problems for repos with different supported dvers (SOFTWARE-1988)
- Fix promotion route for contrib to go from development instead of testing

* Wed Jul 08 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.0-3
- Fix ambiguity with 'upcoming' promotion route

* Tue Jul 07 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.0-2
- Allow promotion to upcoming-prerelease for osg-promote

* Thu Jul 02 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.0-1
- Build for el6 and el7 for OSG 3.3 by default (instead of el5 and el6) (SOFTWARE-1902)
- Allow promotion to prerelease for osg-promote

* Thu Apr 23 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.4-2
- Fix missing import (SOFTWARE-1870)

* Wed Apr 1 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.4-1
- Add log line with destination SRPM path for osg-build prebuild
- Increase max retries for watching koji tasks
- Actually ignore target-arch on non-scratch builds
- Fix a few NameErrors in osg-import-srpm
- Add some hackery to keep osg-promote working even after the 3.3 tags have
  been created

* Wed Dec 17 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.3-1
- Add retry loop to watching tasks (SOFTWARE-1343)
- Allow --target-arch option on scratch koji builds (SOFTWARE-1629)
- Handle mixed git/svn directories (SOFTWARE-1247)
- Update usage text

* Mon Dec 01 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.2-1
- Don't require a cert when doing a mock build using a koji config
- Change contrib promotion route to go from testing to contrib instead of
  development to contrib (SOFTWARE-1682)
- Use current dir as package dir if not specified (SOFTWARE-1424)

* Tue Sep 30 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.4.1-1
- Do not promote EL7 unless --el7 flag is passed (SOFTWARE-1586)
- Add --background option for koji builds to lower priority (SOFTWARE-1609)
- Exit nonzero if watched builds fail

* Mon Aug 11 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.0-1
- EL7 support
- Removed koji-tag-checker

* Mon Jun 23 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.3.8-1
- Add koji-blame, a tool for listing koji tagging history (SOFTWARE-1113)

* Tue May 6 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.3.7-2
- Fix race conditions in osg-koji setup (SOFTWARE-1466)

* Mon Apr 7 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.3.6-1
- osg-koji setup no longer downloads deprecated DOEGrids certs (SOFTWARE-1437)
- Tweak client.crt creation in osg-koji setup to insert newline between cert
  and key and convert line endings

* Fri Mar 21 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.3.5-2
- Allow multiple routes separated by commas in '-r', for osg-promote
  and fix usage message (SOFTWARE-1390)
- Add repo hints for 'condor' and 'perfsonar' repos (SOFTWARE-1413, SOFTWARE-1392)
- Fix SVN URL handling so that you can specify an SVN URL to build from
  instead of a package directory (SOFTWARE-1278)
- Fix osg-promote misdetecting repo tag on packages with a dot in the release
  number (e.g. 1.11) (SOFTWARE-1420)
- Remove logic dealing with the koji tag renaming for osg-next (SOFTWARE-1416)
- Minor bugfixes

* Tue Feb 25 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.3.4-1
- change 'contrib' promotion path to go from development -> contrib instead
  of testing -> contrib, per the new osg-contrib policy  (SOFTWARE-1405)

* Fri Feb 14 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.3.3-3.untagme
- Add koji-hub-testing.patch

* Mon Jan 27 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.3.3-2
- Make client cert check Python 2.4-compatible (SOFTWARE-1366)
- Allow simultaneous promotions to multiple routes (e.g. both 3.1-testing and 3.2-testing) in osg-promote (SOFTWARE-1289)
- Refactoring and unit tests for osg-promote

* Wed Dec 11 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.2-1
- Add grid proxy support to osg-koji setup (SOFTWARE-1287)
- Check client cert for expiration before use (SOFTWARE-1288)
- Remove long-deprecated 'allbuild' task
- Add support for --repo=internal in branches/osg-internal (SOFTWARE-1258)

* Tue Oct 22 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.1-2
- bugfixes for osg-next support

* Mon Oct 21 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.0-1
- osg-next support

* Mon Aug 26 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.8-1
- Support for hcc repos and new koji tag names added to osg-promote (contributed by Brian Bockelman)

* Mon Aug 19 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.7-1
- Add git support (contributed by Brian Bockelman)

* Fri Aug 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.6-1
- Add %%osg macro
- Shorten arguments to rpmbuild

* Fri Feb 15 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.5-1
- Add --upcoming flag to osg-build koji
- Code cleanup
- Fix for SOFTWARE-936

* Thu Feb 14 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1.2.4-2
- Bump to rebuild

* Wed Jan 23 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1.2.4-1
- Updated osg-koji to include DigiCert CA certs in the CA bundle that its setup task generates (SOFTWARE-860)

* Mon Sep 24 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.3-1
- Python 2.4 compatibility fixes
- Added --getfiles option to koji scratch build

* Thu Aug 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.2-1
- osg-promote bugfixes
- 'quilt' task result directory changed to '_quilt' instead of '_final_srpm_contents'

* Thu Jul 12 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.1-1
- mock task bugfixes

* Fri May 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.0-1
- Add promotion script "osg-promote"
- Rewrite koji task to use the functions in the koji library instead of making callouts to the shell

* Tue Feb 21 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1.5-1
- Fixed logging bug

* Fri Feb 17 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1.4-1
- Don't check for outdated svn checkout if we're not using koji

* Thu Feb 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1.3-1
- Changed koji task to build for both el5 and el6 by default
- Added --koji-tag-and-target (--ktt) option as a shorthand for specifying both --koji-tag and --koji-target
- Common usage patterns added to usage message
- Config file bugfixes
- Added 'koji-tag-checker' script which checks for builds that are in both el5 and el6 tags

* Fri Jan 27 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1.2-1
- SOFTWARE-449 snuck back in. Fixed it.

* Fri Jan 27 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1.1-1
- el5/el6 macros fixed

* Thu Jan 26 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1.0-2
- Fixed SVN out-of-date check

* Thu Jan 26 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1.0-1
- allbuild task added
- Major refactoring/reorganization

* Thu Jan 19 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.4-2
- 'mock' requirement changed to 'mock >= 1.0.0'

* Wed Jan 18 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.4-1
- Added el6 support

* Fri Jan 06 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.3-1
- Fix for SOFTWARE-449

* Thu Jan 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.2-1
- Fix for SOFTWARE-444

* Tue Dec 20 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.1-1
- Fix for SOFTWARE-431

* Wed Dec 14 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.0-1
- Version bumped to 1.0.0
- Added osg-build-test script for running unit tests.
- Fixed prepare task bug.

* Fri Dec 09 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.3.1-1
- osg-koji changed to use ~/.koji directory if it exists and ~/.osg-koji doesn't.
- Some refactoring and bugfixes of prebuild step.
- Added Alain Roy's koji-tag-diff script

* Wed Dec 07 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.3.0-1
- Removed deprecated tasks 'batlab' and 'push'.
- Removed deprecated support for builds using the 'osg/root' layout.
- Added error when attempting to do Koji builds using rpmbuild 4.8+ (RHEL6).
- Major refactoring of mock and koji tasks.
- Added 'quilt' task, dependency on quilt.
- Added koji builds directly from subversion.
- Added koji dependency.
- Removed createrepo dependency.

* Thu Nov 17 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.23-1
- Added osg-koji wrapper script

* Thu Oct 06 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.22-1
- Minor tweaks to rpm-ripper

* Thu Oct 06 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.21-1
- Added --nowait tag for koji task
- Added rpm-ripper and osg-import-srpm scripts

* Wed Aug 24 2011 <matyas@cs.wisc.edu> - 0.0.20-1
- Added ability to pass koji tag and koji target on the command line or in
  the config file.

* Mon Aug 15 2011 <matyas@cs.wisc.edu> - 0.0.19-1
- Added 'prepare' task (Software-149).
- Code cleanup. Logging, error handling tweaks.

* Thu Aug 11 2011 <matyas@cs.wisc.edu> - 0.0.18-1
- Renamed vdt-build to osg-build.
- Moved supporting python files to their own subdirectory.
- vdtkoji.conf moved to /usr/share/osg-build instead of being mixed in with the
  .py files (and renamed to osg-koji.conf).
- Added osg-minefield repository to the mock config.
- Fixed logging (-v/-q weren't being obeyed).

* Wed Aug 10 2011 <matyas@cs.wisc.edu> - 0.0.17-1
- Removed push-rpm-to-vdt script.
- Added koji-el5-osg-development repo (SOFTWARE-139).
- Code cleanup.
- Added detection of koji login from CN.
- Made noarch rpms get copied to i386 and x86_64 repos, instead of being copied
  to a noarch repo and symlinked to the arch-specific ones, to fit with how
  mash does it.
- Removed koji code from batlab task.

* Mon Aug 08 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.16-1
- Fixed bug detecting group memebership in mock task.
- Fixed koji task using '.' as the package name if '.' is given as the package
  dir.

* Fri Aug 05 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.15-1
- VDTBuildMockConfig bug fixes
- Added 'koji' task

* Mon Aug 01 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.14-2
- Dead code/comment removal

* Fri Jul 29 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.14-1
- Some code cleanup and bugfixes. Automatic koji importing and tagging
  added to platform-post.py

* Fri Jul 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.13-1
- Added configurable dist tag

* Fri Jul 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.12-1
- KeyError on target_arch fix for mock task
- SystemExit exception fixed

* Fri Jul 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.11-1
- os.path.walk bugfix for push task

* Fri Jul 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.10-1
- More descriptive error messages.
- --target-arch bug fix for mock task

* Thu Jul 21 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.9-1
- Mock config fixes.
- Changed distro tag to .osg

* Wed Jul 20 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.8-1
- Made submit-01.batlab.org be the default submit host.
- Added push-rpm-to-vdt script

* Wed Jul 20 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.7-1
- Fixed cfg_dir variable not defined error in mock task

* Wed Jul 20 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.6-1
- Made -m AUTO the default. Made -m AUTO use a different config file for
  mock >= 0.8

* Tue Jul 19 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.5-1
- Bugfixes for batlab task to make it work with mock as it is installed in batlab.org.
- createrepo added to requires.

* Mon Jul 18 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 0.0.4-4
- Added mock and rpm-build to requires

* Mon Jul 18 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.0.4-3
- Small bugfixes.

* Mon Jul 18 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.0.4-2
- Changed autogenerated mock config to use centos repos until I have a working sl5 mock conf file.

* Mon Jul 18 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.0.4-1
- Implemented batlab builds
- *.py files moved to python_sitelib. sample ini file moved to /usr/share/doc

* Fri Jul 15 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.0.3-2
- Fixed SOFTWARE-21

* Fri Jul 15 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.0.3-1
- Various bugfixes (SOFTWARE-{14,15,16})

* Thu Jul 14 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.0.2-1
- Python rewrite

* Thu Jul  7 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-2
- Made vdt-build obey our own packaging guidelines.

* Fri Jul  1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-1
- Created an initial vdt-build RPM for ease-of-use
- Contains RPM::Toolbox::Spec for now.

