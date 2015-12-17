Summary: osg-pki-tools
Name: osg-pki-tools
Version: 1.2.14
Release: 1%{?dist}
Source: OSGPKITools-%{version}.tar.gz
License: Apache 2.0
Group: Grid
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: python
Requires: m2crypto
Requires: python-simplejson
%if 0%{?rhel} < 6
Requires: python-ssl
%endif

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}

%package tests
Summary: tests for osg-pki-tools
Requires: %{name} = %{version}
# Requires: python-scripttest
# ^ Leaving this behind for future reference. 'scripttest' is not available
# as an RPM package, and must be installed via pip or easy_install
Group: Grid

%description tests
tests for osg-pki-tools

%prep
%setup -n OSGPKITools-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=%{buildroot}
rm -f %{buildroot}%{python_sitelib}/*.egg-info || :
install -d %{buildroot}%{_bindir}
install -m 755 -t %{buildroot}%{_bindir}    \
    osgpkitools/osg-cert-request            \
    osgpkitools/osg-cert-retrieve           \
    osgpkitools/osg-cert-revoke             \
    osgpkitools/osg-gridadmin-cert-request  \
    osgpkitools/osg-user-cert-renew         \
    osgpkitools/osg-user-cert-revoke
install -d %{buildroot}%{_sysconfdir}/osg
install -m 644 osgpkitools/pki-clients.ini %{buildroot}%{_sysconfdir}/osg
mv -f %{buildroot}%{python_sitelib}/tests %{buildroot}%{python_sitelib}/osgpkitools/tests
install -d %{buildroot}%{_defaultdocdir}/%{name}-%{version}
install -m 644 -t %{buildroot}%{_defaultdocdir}/%{name}-%{version} CHANGELOG.txt LICENSE.txt README.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{python_sitelib}/osgpkitools
%{python_sitelib}/osgpkitools/*.py*
/usr/bin/*
%dir %{_sysconfdir}/osg
%config(noreplace) %{_sysconfdir}/osg/pki-clients.ini
%{_defaultdocdir}/%{name}-%{version}/*

%files tests
%defattr(-,root,root)
%dir %{python_sitelib}/osgpkitools/tests
%{python_sitelib}/osgpkitools/tests/*


%changelog
* Thu Dec 17 2015 Brian Lin <blin@cs.wisc.edu> - 1.2.14-1
- Accept hostname aliases in cert requests (SOFTWARE-2114)
- Refactor tests (SOFTWARE-2120)

* Thu Dec 10 2015 Brian Lin <blin@cs.wisc.edu> - 1.2.13-1
- Certificate requests fail without setting the CSR version (SOFTWARE-1936)

* Tue Mar 31 2015 Brian Lin <blin@cs.wisc.edu> - 1.2.12-1
- Fix to osg-user-cert-renew using old SSL protocols
- Check write permissions of output dir before renewing certs

* Fri Oct 24 2014 Brian Lin <blin@cs.wisc.edu> - 1.2.11-1
- Fix to avoid SSLv3 due to the POODLE vulnerability

* Tue Aug 19 2014 Brian Lin <blin@cs.wisc.edu> - 1.2.10-1
- Catch uncaught exceptions when missing request VO (SOFTWARE-1584)

* Mon Aug 18 2014 Brian Lin <blin@cs.wisc.edu> - 1.2.9-1
- Add ability to revoke specific certs by serial ID (SOFTWARE-1494)

* Tue Jun 17 2014 Brian Lin <blin@cs.wisc.edu> - 1.2.8-1
- Change required options in retrieve/revoke tools to be required args (SOFTWARE-1500)
- Fix redundant input param when providing CSR (SOFTWARE-1502)

* Wed Mar 05 2014 Brian Lin <blin@cs.wisc.edu> - 1.2.7-1
- Fix osg-user-cert-renew error on EL5

* Tue Feb 25 2014 Brian Lin <blin@cs.wisc.edu> - 1.2.6-1
- Pull PKCS12 files from OIM (SOFTWARE-1229)
- Add ability to add CC's to the GOC ticket when requesting certs (SOFTWARE-1318)
- Fix VO option when requesting a new cert (SOFTWARE-1386)

* Thu Nov 21 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.5-1
- Handle blank lines in hostfile for osg-gridadmin-cert-request (SOFTWARE-1271)
- Fix bugs in exception handling (SOFTWARE-1201)

* Fri Nov 07 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.4-1
- Handle all IO errors

* Mon Oct 28 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.3-1
- Handle no such file/directory errors explicitly

* Thu Oct 17 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.2-1
- Improve exception handling when typos occur on the command-line (SOFTWARE-1183)

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.1-4
- Add documentation

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.1-3
- Bump to rebuild

* Thu Jun 27 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.1-2
- Bump to rebuild with fixed source

* Tue Jun 25 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.1-1
- New version 1.2.1

* Thu Jun 13 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.0-3
- New version 1.2
- Fix ConnectAPI imports in osg-cert-request and osg-cert-retrieve
- Fix exception handling

* Thu Mar 28 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1.0-3
- Rebuild with fix to scripts to look for pki-clients.ini in /etc/osg

* Wed Mar 27 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1.0-2
- Make source tarball from 1.1 tag
- Remove upstreamed patches

* Wed Feb 06 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1.0-1
- Version update
- Add python-ssl dependency on el5
- Fix sitelib
- Fix imports

* Thu Oct 04 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.3-1
- Version update

* Fri Sep 28 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.2-1
- Version update

* Thu Sep 27 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.1-1
- Version update
- Add python-simplejson dependency
- Move unit tests
- Rename and move OSGPKIClients.ini
- Remove python-argparse dependency for tests

* Tue Sep 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-4
- Add m2crypto dependency
- Add OSGPKIClients.ini

* Mon Sep 24 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-3
- Use correct sources
- Remove patches, since they're upstream

* Fri Sep 14 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-2
- Fix imports
- Fix os.system calls
- Catch SystemExit

* Thu Sep 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-1
- Initial packaging

