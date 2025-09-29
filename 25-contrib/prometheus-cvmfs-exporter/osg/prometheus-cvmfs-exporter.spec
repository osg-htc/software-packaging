%define gitname prometheus-cvmfs
Name:           prometheus-cvmfs-exporter
Version:        1.0.0
Release:        1.1%{?dist}
Summary:        Prometheus exporter for CVMFS client monitoring

License:        BSD-3-Clause
URL:            https://github.com/cvmfs-contrib/prometheus-cvmfs
Source0:        %{gitname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros

# Runtime dependencies for the script
Requires:       bash
Requires:       attr
Requires:       bc
Requires:       cvmfs
Requires:       findutils
Requires:       grep
Requires:       coreutils
Requires:       util-linux

# Systemd dependencies
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A Prometheus exporter for monitoring CVMFS (CernVM File System) clients.
This package provides a script that collects metrics from CVMFS repositories
and exposes them in Prometheus format, along with systemd service files
for running the exporter as a service.

The exporter collects various metrics including:
- Cache hit rates and sizes
- Download statistics
- Repository status and configuration
- Proxy usage and performance
- System resource usage by CVMFS processes

%prep
%setup -q -n %{gitname}-%{version}

%build
# Nothing to build - this is a shell script package

%install
# Install using the Makefile
make install DESTDIR=%{buildroot}
make install-systemd DESTDIR=%{buildroot}
# Remove duplicate LICENSE file from doc directory since %license handles it
rm -f %{buildroot}%{_docdir}/%{name}/LICENSE

%post
%systemd_post cvmfs-client-prometheus@.service
%systemd_post cvmfs-client-prometheus.socket

%preun
%systemd_preun cvmfs-client-prometheus@.service
%systemd_preun cvmfs-client-prometheus.socket

%postun
%systemd_postun_with_restart cvmfs-client-prometheus@.service
%systemd_postun_with_restart cvmfs-client-prometheus.socket

%files
%license LICENSE
%{_libexecdir}/cvmfs/cvmfs-prometheus.sh
%{_unitdir}/cvmfs-client-prometheus@.service
%{_unitdir}/cvmfs-client-prometheus.socket

%changelog
* Mon Sep 29 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 1.0.0-1.1
- Build for OSG

* Tue Aug 12 2025 Valentin Volkl <valentin.volkl@cern.ch> - 1.0.0-1
- Initial package release
