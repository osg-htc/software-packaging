Summary: OASIS-specific configuration
Name: oasis-config
Version: 4
Release: 2%{?dist}
License: ASL 2.0
Group: Applications/Grid
Source0: opensciencegrid.org.pub
Source1: opensciencegrid.org.conf
Source2: oasis.opensciencegrid.org.conf
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: cvmfs
Requires: wget

%description
%{summary}



%prep
exit 0




%build
exit 0








%install
[[ %{buildroot} != / ]] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/cvmfs/keys
mkdir -p %{buildroot}%{_sysconfdir}/cvmfs/domain.d
mkdir -p %{buildroot}%{_sysconfdir}/cvmfs/config.d
install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/cvmfs/keys 
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/cvmfs/domain.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/cvmfs/config.d



%clean
[[ %{buildroot} != / ]] && rm -rf %{buildroot}




%files
%{_sysconfdir}/cvmfs/keys/*
%{_sysconfdir}/cvmfs/domain.d/*
%{_sysconfdir}/cvmfs/config.d/*





%changelog
* Thu Aug 22 2013 Dave Dykstra <dwd@fnal.gov> 4-2
- Move the setting of OASIS_CERTIFICATES to where it more properly belongs
  in new file /etc/cvmfs/config.d/oasis.opensciencegrid.org.conf

* Thu Aug 22 2013 Dave Dykstra <dwd@fnal.gov> 4-1
- Add default setting for OASIS_CERTIFICATES

* Wed Jul 24 2013 Dave Dykstra <dwd@fnal.gov> 3-4
- Remove metapackage designation and specific version requirement on cvmfs.
  Instead a new metapackage osg-oasis has been created.

* Wed Jul 12 2013 Dave Dykstra <dwd@fnal.gov> 3-3
- Require cvmfs 2.1.12

* Wed Jun 26 2013 Dave Dykstra <dwd@fnal.gov> 3-2
- Require latest version of cvmfs

* Wed Jun 26 2013 Dave Dykstra <dwd@fnal.gov> 3-1
- Add BNL stratum 1

* Wed May 29 2013 Dave Dykstra <dwd@fnal.gov> 2-2
- Add --no-proxy to the wget probe in case $http_proxy is somehow set.

* Wed May 29 2013 Dave Dykstra <dwd@fnal.gov> 2-1
- Change from using the stratum 0 to using the GOC stratum 1 and
    the FNAL stratum 1 as servers.  Add logic to compute the best order
    between the servers the first time they are accessed after an rpm
    upgrade, and to store the order in a file.

* Wed Jan 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1-1
- Initial version



# vim:ft=spec
