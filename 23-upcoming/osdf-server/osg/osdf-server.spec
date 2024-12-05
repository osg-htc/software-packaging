Summary: Service files for Pelican-based OSDF daemons
Name: osdf-server
Version: 7.11.7
Release: 1%{?dist}
License: ASL 2.0
Url: https://github.com/PelicanPlatform/pelican
BuildArch: noarch
#BuildRequires: pelican >= %%{version}
# ^^ does not work: the pelican RPM is missing the SIGMD5 header and cannot be used
#    in a BuildRequires - at least in Koji
Source0: pelican-%{version}.tar.gz
Source1: 20-cache.yaml


# subpackage: A helper macro to get rid of some of the code duplication. This
# expands to the various sections needed for each osdf subpackage. Add the -x
# flag for services that use XRootD (the cache and the origin).

%define subpackage(x) %{expand:
%%package -n %1
Summary: Service file and configuration for %1
Requires: pelican >= %{version}
Requires: /usr/bin/osdf
%{-x:Requires: xrootd-server >= 1:5.7.0}
%{-x:Requires: xrootd-scitokens}
%{-x:Requires: xrootd-voms}
%{-x:Requires: xrootd-multiuser}
%{-x:Requires: xrdcl-pelican}

%%description -n %1
Service file for %1

%%preun -n %1
%%systemd_preun %1.service

%%postun -n %1
systemctl daemon-reload

%%post -n %1
%%systemd_post %1.service
systemctl daemon-reload

%%files -n %1
/usr/lib/systemd/system/%{1}*.service
%%config /etc/pelican/%{1}*.yaml
/usr/share/pelican/config.d/10-osdf-defaults.yaml
%%config(noreplace) /etc/pelican/config.d/15-osdf.yaml
%%config(noreplace) /etc/pelican/config.d/50-webui.yaml
%{-x:%%attr(-,xrootd,xrootd) /var/spool/osdf}
%%dir %%attr(0700,root,root) /var/log/pelican
%%config(noreplace) /etc/logrotate.d/pelican

# kind of a hack
%%if "%{1}" == "osdf-cache"
%%config(noreplace) /etc/pelican/config.d/20-cache.yaml
%%endif

%%triggerin -n %1 -- pelican
systemctl condrestart %1.service

%{-x:%%triggerin -n %1 -- xrootd-server}
%{-x:systemctl condrestart %1.service}
}

# end of subpackage helper macro

%description
Service files for Pelican


%prep
%setup -n pelican-%{version}


%build
exit 0


%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system/
mkdir -p $RPM_BUILD_ROOT/usr/share/pelican/config.d/
mkdir -p $RPM_BUILD_ROOT/etc/pelican/config.d/
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d/
mkdir -p $RPM_BUILD_ROOT/var/spool/osdf
mkdir -p $RPM_BUILD_ROOT/var/log/pelican
install -m 0644 systemd/osdf-*.service          $RPM_BUILD_ROOT/usr/lib/systemd/system/
install -m 0644 systemd/osdf-*.yaml             $RPM_BUILD_ROOT/etc/pelican/
install -m 0644 systemd/10-osdf-defaults.yaml   $RPM_BUILD_ROOT/usr/share/pelican/config.d/
install -m 0644 %{SOURCE1}                      $RPM_BUILD_ROOT/etc/pelican/config.d/
install -m 0644 systemd/examples/15-osdf.yaml   $RPM_BUILD_ROOT/etc/pelican/config.d/
install -m 0644 systemd/examples/50-webui.yaml  $RPM_BUILD_ROOT/etc/pelican/config.d/
install -m 0644 systemd/pelican.logrotate       $RPM_BUILD_ROOT/etc/logrotate.d/pelican


%subpackage osdf-registry

%subpackage osdf-director

%subpackage -x osdf-origin

%subpackage -x osdf-cache




%changelog
* Thu Dec 05 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.11.7-1
- Upgrade to Pelican 7.11.7 (SOFTWARE-6028)

* Tue Nov 05 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.11.1-1
- Upgrade to Pelican 7.11.1 and switch to config.d layout (SOFTWARE-6028)

* Wed Oct 02 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.10.7-1
- Upgrade to Pelican 7.10.7 (SOFTWARE-6004)

* Fri Aug 16 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.9.9-1
- Upgrade to Pelican 7.9.9
- Require pelican version >= service version
- Restart service if pelican or (for xrootd-requiring services) xrootd-server is upgraded
- Require xrootd >= 5.7.0
- Require xrootd-multiuser

* Fri Jul 05 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.9.3-1
- Upgrade to Pelican 7.9.3 (SOFTWARE-5847)
- Require xrootd >= 5.6.9-1.6 for various backports from 5.7.0

* Wed May 22 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.8.3-1
- Upgrade to Pelican 7.8.3 (SOFTWARE-5847)

* Thu May 02 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.7.6-1
- Upgrade to Pelican 7.7.6 (SOFTWARE-5847)
- Add logrotate.conf

* Fri Feb 16 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.5.6-1
- Upgrade to Pelican 7.5.6
- Require xrootd >= 5.6.6 for pelican:// URL support
- Put log files in /var/log/pelican

* Fri Feb 02 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.99-2.1
- Require xrdcl-pelican

* Thu Feb 01 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.99-2
- Prerelease build for 7.5.0; remove pelican-* subpackages and only build osdf-* subpackages

* Mon Jan 29 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.0-5
- Add /var/spool/pelican and /var/spool/osdf directories for the xrootd-based daemons

* Mon Jan 22 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.0-4
- Mark config files as %config(noreplace)

* Mon Jan 22 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.0-3
- Updates to yaml and service files
- Remove redundant *-origin-multiuser services
- Add osdf-cache-public and osdf-origin-public

* Fri Jan 05 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.0-2
- Remove xrootd requirements from registry and director
- Add pelican-osdf-compat requirement to osdf subpackages

* Wed Jan 03 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.0-1
- Add minimum version requirements:
  - xrootd must be 5.6.3 to avoid chunked upload incompatibility
  - pelican must be 7.3.3 to avoid authfile/scitokens.conf parsing issues
- Make origin and origin-multiuser services conflict

* Thu Dec 28 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.2.0-5
- Add missing xrootd-voms dependency
- osdf config improvements

* Fri Dec 22 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.2.0-3
- Add missing xrootd-scitokens dependency
- Flesh out cache and origin configs

* Mon Dec 04 2023 Mátyás Selmeci <matyas@cs.wisc.edu>
- Created


# vim:ft=spec
