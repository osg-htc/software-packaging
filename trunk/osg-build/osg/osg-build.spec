
Name:           osg-build
Version:        1.2.6
Release:        1%{?dist}
Summary:        Build tools for the OSG

Group:          System Environment/Tools
License:        Apache 2.0
URL:            https://twiki.grid.iu.edu/bin/view/SoftwareTeam/OSGBuildTools

Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       mock >= 1.0.0
Requires:       rpm-build
Requires:       openssl
Requires:       quilt
Requires:       koji
Requires:       rpmlint

Obsoletes:      vdt-build <= 0.0.17
Provides:       vdt-build = %{version}

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}
See %{url} for details.


%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/koji-tag-checker
%{_bindir}/koji-tag-diff
%{_bindir}/rpm-ripper
%{_bindir}/osg-build-test
%{_bindir}/osg-import-srpm
%{_bindir}/osg-koji
%{_bindir}/osg-promote
%{_bindir}/vdt-build
%dir %{python_sitelib}/osgbuild
%{python_sitelib}/osgbuild/*.py*
%{_datadir}/%{name}/osg-koji-site.conf
%{_datadir}/%{name}/osg-koji-home.conf
%{_datadir}/%{name}/mock-auto.cfg.in
%{_datadir}/%{name}/rpmlint.cfg
%doc %{_docdir}/%{name}/sample-osg-build.ini

%changelog
* Fri Aug 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.6-1
- Add %osg macro
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

