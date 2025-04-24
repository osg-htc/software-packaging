# pam_oauth2_device version
%define _version 0.1.3.chtc
%define _lib /lib64


Name:    pamoauth2device
Version: %{_version}
Release: 1%{?dist}
Summary: PAM module for OAuth 2.0 Device flow
License: Apache-2.0
URL:     https://github.com/stfc/pam_oauth2_device/
Source0: pam_oauth2_device-v%{_version}.tar.gz


# List of build-time dependencies:
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: libcurl-devel
BuildRequires: openldap-devel
BuildRequires: pam-devel


# List of runtime dependencies:
Requires: curl
Requires: openldap-clients


%description
PAM module that allows authentication against external OpenID Connect
identity provider using OAuth 2.0 Device Flow.


%prep
%setup -q -n pam_oauth2_device-v%{_version}


%build
make


%install
mkdir -p ${RPM_BUILD_ROOT}%{_lib}/security
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/pam_oauth2_device
install pam_oauth2_device.so ${RPM_BUILD_ROOT}%{_lib}/security
cp config_template.json ${RPM_BUILD_ROOT}%{_sysconfdir}/pam_oauth2_device/config.json


%check
# no test.


%files
%doc LICENSE README.md
%{_lib}/security/pam_oauth2_device.so
%config(noreplace) %{_sysconfdir}/pam_oauth2_device/config.json


%changelog
* Mon Aug 7 2023 Brian Lin <blin@cs.wisc.edu> - 0.1.3.chtc
- Allow the name claim to be configurable (INF-748)

* Mon Aug 2 2021 Brian Bockelman <bbockelman@morgridge.org> - 0.1.2.chtc
- Add support for the device code flow for test.cilogon.org

* Thu Aug 13 2020 Will Furnell <will.furnell@stfc.ac.uk> - 0.1
- Revamped completely for STFC use

* Thu Nov 21 2019 Jaroslaw Surkont <jaroslaw.surkont@unibas.ch> - 0.1.1-1
- Add username_attribute to config (#7)
- Add client authentication to device endpoint (#6)

* Fri Aug 09 2019 Jaroslaw Surkont <jaroslaw.surkont@unibas.ch> - 0.1.0-1
- first build for pamoauth2device.
