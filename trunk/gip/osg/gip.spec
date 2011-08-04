Summary: Generic Information Provider
Name: gip
Version: 1.3.0alpha2
Release: 4%{?dist}
License: TODO
Group: Applications/Grid
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
#Packager: VDT <vdt-support@opensciencegrid.org>
#BuildRequires: 
Requires: python
#Requires:           initscripts
#Requires(post):     chkconfig, /sbin/ldconfig
#Requires(preun):    chkconfig
#Requires(postun):   /sbin/ldconfig
AutoReq: yes
AutoProv: yes

Source0: %{name}-%{version}.tgz
Patch0: dir_locations.patch

%description

The Open Science Grid (OSG) Generic Information Provider (GIP) is a core part of the OSG Information Infrastructure.
The GIP is a grid information service that aggregates static and dynamic resource information for use with 
LDAP-based information systems.  It produces information based on the GLUE schema.  This information
then can be sent via external services to information collection servers such as

%prep
%setup -q
%patch0 -p0

%install
rm -rf %{buildroot}

# Set the Python version
%define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%d.%d'%v")

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

install -d %{buildroot}%{python_sitelib}
cp -a gip/lib/python/* %{buildroot}%{python_sitelib}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libexecdir}/%{name}/plugins
install -d %{buildroot}%{_libexecdir}/%{name}/providers
install -d %{buildroot}%{_libexecdir}/%{name}

install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}/ldif.d
install -d %{buildroot}/var/cache/%{name}

install -m 644 gip/etc/logging.conf %{buildroot}%{_sysconfdir}/%{name}
cp -a gip/plugins %{buildroot}%{_libexecdir}/%{name}
cp -a gip/providers %{buildroot}%{_libexecdir}/%{name}
cp -a gip/templates %{buildroot}%{_datadir}/%{name}
rm %{buildroot}%{_datadir}/%{name}/templates/Questions.py

cp gip/libexec/* %{buildroot}%{_libexecdir}/%{name}
# If we don't remove the .py extension, RPM will automatically compile these.
for i in `ls %{buildroot}%{_libexecdir}/%{name}/providers/*.py`; do
    without_py=`echo $i | sed 's|.py||'`
    mv $i $without_py
done
# We want to be able to import osg_info_wrapper
mv %{buildroot}%{_libexecdir}/%{name}/osg_info_wrapper.py %{buildroot}%{python_sitelib}/
# Remove deprecated cruft:
rm %{buildroot}%{_libexecdir}/%{name}/*.py
rm %{buildroot}%{_libexecdir}/%{name}/*.pyc

cp gip/bin/* %{buildroot}%{_bindir}
rm %{buildroot}%{_bindir}/gip-validator.py
rm %{buildroot}%{_bindir}/TestRunner.py
rm %{buildroot}%{_bindir}/run_gip.sh.se_only.example

install -d %{buildroot}%{_libexecdir}/%{name}/plugins
install -d %{buildroot}%{_libexecdir}/%{name}/providers

mkdir -p $RPM_BUILD_ROOT/var/log/%{name}

touch $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/%{name}.conf
touch $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/add-attributes.conf
touch $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/alter-attributes.conf
touch $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/remove-attributes.conf

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libexecdir}/%{name}osg-info-wrapper
%attr(744,root,root) %{_libexecdir}/%{name}/providers/*
%{python_sitelib}/*
%{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/gip.conf
%config(noreplace) %{_sysconfdir}/%{name}/alter-attributes.conf
%config(noreplace) %{_sysconfdir}/%{name}/add-attributes.conf
%config(noreplace) %{_sysconfdir}/%{name}/remove-attributes.conf
%config(noreplace) %{_sysconfdir}/%{name}/logging.conf
%config(noreplace) %{_sysconfdir}/%{name}/ldif.d
%attr(-, daemon, daemon) /var/log/%{name}
%attr(-, daemon, daemon) /var/cache/%{name}

%clean
rm -rf %buildroot

%define _unpackaged_files_terminate_build 1

%changelog
* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.0alpha2-4
- Fix ownership of files.

* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.0alpha2-3
- Improve FHS compliance.

* Fri Jul 22 2011 Burt Holzman <burt@fnal.gov> - 1.3.0alpha2-2
- Added description and cleaned up specfile

* Wed Jul 20 2011 Burt Holzman <burt@fnal.gov> 1.3.0alpha2-1
- Initial build


