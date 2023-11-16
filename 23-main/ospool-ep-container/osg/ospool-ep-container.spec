%define osgver 23

Name: ospool-ep-container
Version: 1.0
Release: 5%{?dist}
Summary: Systemd service for the OSPool Backfill Container

License: Unknown
URL: https://github.com/opensciencegrid/osgvo-docker-pilot


Source0: ospool-ep-container.service
Source1: start_ospool_ep_container.sh
Source2: ospool-ep-container.cfg

BuildArch: noarch
Requires: /usr/bin/docker systemd

%description
Systemd service for the OSPool Backfill Container

%prep
exit 0

%build
# Set the docker image to the appropriate osg version
sed -i "s/%%{OSGVER}/%{osgver}/" %{SOURCE1}

%install

mkdir -p %{buildroot}/usr/lib/systemd/system %{buildroot}/etc/osg %{buildroot}/usr/sbin
mv %{SOURCE0} %{buildroot}/usr/lib/systemd/system
mv %{SOURCE1} %{buildroot}/usr/sbin
mv %{SOURCE2} %{buildroot}/etc/osg/

%files
%defattr(0644,root,root,-)
/usr/lib/systemd/system/ospool-ep-container.service
%config(noreplace) /etc/osg/ospool-ep-container.cfg 
%attr(0755,root,root) /usr/sbin/start_ospool_ep_container.sh

%changelog

* Tue Nov 14 2023 Matt Westphall <westphall@wisc.edu> 1.0-1
- Initial version
