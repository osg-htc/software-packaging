Summary: osg-pki-tools
Name: osg-pki-tools
Version: 1.2.1
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{python_sitelib}/osgpkitools
%{python_sitelib}/osgpkitools/*.py*
/usr/bin/*
%dir %{_sysconfdir}/osg
%config(noreplace) %{_sysconfdir}/osg/pki-clients.ini

%files tests
%defattr(-,root,root)
%dir %{python_sitelib}/osgpkitools/tests
%{python_sitelib}/osgpkitools/tests/*


%changelog
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

