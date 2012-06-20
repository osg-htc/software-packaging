Name:      dcache-gratia-probe 
Summary:   dcache-gratia-probe
Version:   3.0.0
Release:   2%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
#from vdt
Requires: gratia-probe-dcache-transfer 
Requires: gratia-probe-dcache-storage
Requires: osg-ca-certs
Requires: osg-vo-map
Requires: gums-client 
#from epel
Requires: fetch-crl 

%description
%{summary}
meta package to install gratia-probe-dCache-transfer and gratia-probe-dCache-storage packages


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files



%changelog
* Mon Aug 22 2011 Tanya Levshina <tlevshin.fnal.gov> - 3.0.0-2
change the name of dcache gratia probes (from dCache to dcache)


* Thu Aug 18 2011 Tanya Levshina <tlevshin.fnal.gov> 
- Created an initial dCache-gratia-probe RPM.

