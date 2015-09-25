Name:      stashcache
Summary:   StashCache metapackages
Version:   0.5
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch
Source0:   %{name}-%{version}.tar.gz
Source1:   xrootd-stashcache-origin-server.cfg.in
Source2:   xrootd-stashcache-cache-server.cfg.in

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%define originhost_prod stash.opensciencegrid.org
%define originhost_itb  stash-itb.opensciencegrid.org

%description
%{summary}

%package daemon
Group: Grid
Summary: Scripts and configuration for StashCache management

Requires: xrootd-server >= 1:4.1.0
Requires: xrootd-python >= 1:4.2.0
Requires: condor-python >= 8.3.5
Requires: grid-certificates >= 7
%if 0%{?rhel} < 6
Requires: fetch-crl3
%else
Requires: fetch-crl
%endif

%description daemon
%{summary}

%package origin-server
Group: Grid
Summary: Metapackage for the origin server

Requires: xrootd-server >= 1:4.1.0
Requires: %{name}-daemon

%description origin-server
%{summary}

%package cache-server
Group: Grid
Summary: Metapackage for a cache server

Requires: xrootd-server >= 1:4.1.0
Requires: %{name}-daemon

%description cache-server
%{summary}

%prep
%setup -q

%install
mkdir -p %{buildroot}%{_sysconfdir}/xrootd
make install DESTDIR=%{buildroot}
for src in "%{SOURCE1}" "%{SOURCE2}"; do
    dst=$(basename "$src" .cfg.in)
    sed -i -e "s#@LIBDIR@#%{_libdir}#" "$src"
    sed -e "s#@ORIGINHOST@#%{originhost_prod}#" \
        "$src" > "%{buildroot}%{_sysconfdir}/xrootd/${dst}.cfg"
    sed -e "s#@ORIGINHOST@#%{originhost_itb}#" \
        "$src" > "%{buildroot}%{_sysconfdir}/xrootd/${dst}-itb.cfg"
done

%clean
rm -rf %{_buildroot}

%files daemon
%defattr(-,root,root)
%{_sbindir}/stashcache
%{_sysconfdir}/condor/config.d/01-stashcache.conf
%{python_sitelib}/xrootd_cache_stats.py*

%files origin-server
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-origin-server.cfg
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-origin-server-itb.cfg

%files cache-server
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-cache-server.cfg
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-cache-server-itb.cfg

%changelog
* Fri Sep 25 2015 Brian Lin <blin@cs.wisc.edu> 0.5-1
- Use FQDN instead of hostname in stashcache-daemon (SOFTWARE-2049)
- Refuse to start if missing host cert or key (SOFTWARE-2026)
- Fix log message if the xrootd service is already running

* Thu Aug 20 2015 Brian Lin <blin@cs.wisc.edu> 0.4-2
- Fix advertisement to central collector

* Thu Aug 20 2015 Brian Lin <blin@cs.wisc.edu> 0.4-1
- Advertise STASHCACHE_DaemonVersion in MasterAd (SOFTWARE-1971)
- Log daemon activity to /var/log/condor/StashcacheLog
- Use TCP to advertise StashCache ads

* Wed Jul 15 2015 Brian Lin <blin@cs.wisc.edu> 0.3-4
- Merge stashcache and stashcache-daemon packages

* Tue Jul 07 2015 Brian Lin <blin@cs.wisc.edu> 0.3-3
- Advertise stashcache startd and master ads to the central collector (SOFTWARE-1966)

* Tue Jun 30 2015 Brian Lin <blin@cs.wisc.edu> 0.3-2
- Restore ability for the daemon to run on EL5

* Thu Jun 25 2015 Brian Lin <blin@cs.wisc.edu> 0.3-1
- Update the cache query script

* Fri May 29 2015 Brian Lin <blin@cs.wisc.edu> 0.2-1
- Fix Python 2.6isms
- HTCondor heartbeats require at least condor-python 8.3.5

* Thu May 28 2015 Brian Lin <blin@cs.wisc.edu> 0.1-3
- Remove epoch from condor-python requirement

* Thu Apr 23 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 0.1-2.osg
- Renamed stashcache-server to stashcache-cache-server, and stashcache-origin
  to stashcache-origin-server; rename config files to match

* Wed Apr 22 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 0.1-1.osg
- Created metapackages with stub config files

