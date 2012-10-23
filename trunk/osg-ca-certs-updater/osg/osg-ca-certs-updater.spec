
Name:           osg-ca-certs-updater
Version:        0.2
Release:        1%{?dist}
Summary:        Automatic CA certs updates for OSG

Group:          System Environment/Tools
License:        Apache 2.0

Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       /usr/bin/repoquery

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}


%prep
%setup -q

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/%{_localstatedir}/{lock/subsys,lib}
touch %{buildroot}/%{_localstatedir}/lock/subsys/%{name}-cron
touch %{buildroot}/%{_localstatedir}/lib/%{name}-lastrun

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_initrddir}/%{name}-cron
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%ghost %{_localstatedir}/lock/subsys/%{name}-cron
%ghost %{_localstatedir}/lib/%{name}-lastrun
%doc %{_mandir}/man8/%{name}.8*
%doc %{_defaultdocdir}/%{name}-%{version}/README*

%changelog
* Tue Oct 23 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 0.2-1
- Handle bad logfile name gracefully

* Tue Oct 23 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 0.1-1
- First release
