Summary: Package for OSG-Configure and associated scripts
Name: osg-configure
Version: 1.8.0
Release: 2%{?dist}
Source0: %{name}-%{version}.tar.gz
License: Apache 2.0
Group: Grid
Prefix: %{_prefix}
BuildArch: noarch
Url: https://github.com/opensciencegrid/osg-configure
Provides: configure-osg
Requires: condor-python


%define gateway_ini %_sysconfdir/osg/config.d/10-gateway.ini
%define gateway_ini_backup /var/lib/misc/10-gateway.ini-backup


%description
%{summary}

%package rsv
Summary: OSG configuration file for RSV
Group: Grid
Provides: configure-osg-rsv
Requires: %name = %version-%release
Requires: %name-gateway
%description rsv
This package includes the ini file for configuring RSV using osg-configure

%package gratia
Summary: OSG configuration file for gratia
Group: Grid
Provides: configure-osg-gratia
Requires: %name = %version-%release
%description gratia
This package includes the ini file for configuring gratia using osg-configure

%package gip
Summary: OSG configuration file for gip
Group: Grid
Provides: configure-osg-gip
Requires: %name = %version-%release
%description gip
This package includes the ini file for configuring gip using osg-configure

%package lsf
Summary: OSG configuration file for lsf
Group: Grid
Provides: configure-osg-lsf
Requires: %name = %version-%release
Requires: %name-gateway
%description lsf
This package includes the ini file for configuring lsf using osg-configure

%package pbs
Summary: OSG configuration file for pbs
Group: Grid
Provides: configure-osg-pbs
Requires: %name = %version-%release
Requires: %name-gateway
%description pbs
This package includes the ini file for configuring pbs using osg-configure

%package condor
Summary: OSG configuration file for condor
Group: Grid
Provides: configure-osg-condor
Requires: %name = %version-%release
Requires: %name-gateway
%description condor
This package includes the ini file for configuring condor using osg-configure

%package sge
Summary: OSG configuration file for sge
Group: Grid
Provides: configure-osg-sge
Requires: %name = %version-%release
Requires: %name-gateway
%description sge
This package includes the ini file for configuring sge using osg-configure

%package monalisa
Summary: Transitional dummy package for OSG 3.2
Group: Grid
Provides: configure-osg-monalisa
%description monalisa
This is an empty package created as a workaround for 3.1->3.2 upgrade issues.
It may safely be removed.

%package ce
Summary: OSG configuration file for CE
Group: Grid
Provides: configure-osg-ce
Requires: %name = %version-%release
Requires: %name-gateway
%description ce
This package includes the ini files for configuring a basic CE using 
osg-configure.  One of the packages for the job manager configuration also 
needs to be installed for the CE configuration.

%package misc
Summary: OSG configuration file for misc software
Group: Grid
Provides: configure-osg-misc
Requires: %name = %version-%release
Requires: lcmaps-db-templates
%description misc
This package includes the ini files for various osg software including
certificates setup, lcmaps, and glexec

%package squid
Summary: OSG configuration file for squid
Group: Grid
Provides: configure-osg-squid
Requires: %name = %version-%release
%description squid
This package includes the ini files for configuring an OSG system to use squid

%package managedfork
Summary: OSG configuration file for managedfork
Group: Grid
Provides: configure-osg-managedfork
Requires: %name = %version-%release
Requires: %name-gateway
%description managedfork
This package includes the ini files for configuring an OSG CE to use
managedfork

%package network
Summary: OSG configuration file for Globus network configuration
Group: Grid
Provides: configure-osg-network
Requires: %name = %version-%release
%description network
This package includes the ini files for configuring network related information
such as firewall ports that globus should use

%package tests
Summary: OSG-Configure unit tests and configuration for unit testing
Group: Grid
Provides: configure-osg-tests
Requires: %name = %version-%release
%description tests
This package includes the ini files and files for unit tests that osg-configure
uses to verify functionality

%package slurm
Summary: OSG configuration file for slurm
Group: Grid
Provides: configure-osg-slurm
Requires: %name = %version-%release
Requires: %name-gateway
%description slurm
This package includes the ini file for configuring slurm using osg-configure

%package bosco
Summary: OSG configuration file for bosco
Group: Grid
Provides: configure-osg-bosco
Requires: %name = %version-%release
Requires: %name-gateway
Requires: condor-bosco
%description bosco
This package includes the ini file for configuring bosco using osg-configure

%package infoservices
Summary: OSG configuration file for the osg info services
Group: Grid
Provides: configure-osg-infoservices
Requires: %name = %version-%release
Requires: %name-gip
%description infoservices
This package includes the ini file for configuring the osg info services using osg-configure

%package gateway
Summary: OSG configuration file for job gateways (globus-gatekeeper / htcondor-ce)
Group: Grid
Provides: configure-osg-gateway
Requires: %name = %version-%release
%description gateway
This package includes the ini file for configuring the job gateways
(globus-gatekeeper or htcondor-ce) using osg-configure

%package cemon
Summary: Transitional dummy package for OSG 3.2
Group: Grid
Provides: configure-osg-cemon
Requires: %name
%description cemon
This is an empty package created as a workaround to OSG 3.1->3.2 upgrade issues.
It may safely be removed once the upgrade is finished.


%prep
%setup

%build
%{__python} setup.py build

%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/condor-ce/config.d
touch $RPM_BUILD_ROOT/etc/condor-ce/config.d/50-osg-configure.conf
mkdir -p $RPM_BUILD_ROOT/var/log/osg/
touch $RPM_BUILD_ROOT/var/log/osg/osg-configure.log
mkdir -p $RPM_BUILD_ROOT/var/lib/osg
touch $RPM_BUILD_ROOT/var/lib/osg/osg-attributes.conf
touch $RPM_BUILD_ROOT/var/lib/osg/osg-local-job-environment.conf
touch $RPM_BUILD_ROOT/var/lib/osg/osg-job-environment.conf
touch $RPM_BUILD_ROOT/var/lib/osg/globus-firewall
mkdir -p $RPM_BUILD_ROOT/etc/profile.d/
touch $RPM_BUILD_ROOT/etc/profile.d/osg.sh
touch $RPM_BUILD_ROOT/etc/profile.d/osg.csh
mkdir -p $(dirname $RPM_BUILD_ROOT/%gateway_ini_backup)
touch $RPM_BUILD_ROOT/%gateway_ini_backup

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{python_sitelib}/*
/usr/sbin/*
%ghost /var/log/osg/osg-configure.log
%ghost /var/lib/osg/osg-attributes.conf
%ghost /var/lib/osg/osg-local-job-environment.conf
%ghost /var/lib/osg/osg-job-environment.conf
%ghost /etc/condor-ce/config.d/50-osg-configure.conf

%files rsv
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/30-rsv.ini

%files gratia
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/30-gratia.ini

%files gip
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/30-gip.ini

%files lsf
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-lsf.ini

%files pbs
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-pbs.ini

%files condor
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-condor.ini

%files sge
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-sge.ini

%files bosco
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-bosco.ini


%files ce
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/40-localsettings.ini
%config(noreplace) %{_sysconfdir}/osg/config.d/40-siteinfo.ini
%config(noreplace) %{_sysconfdir}/osg/config.d/10-storage.ini
%config(noreplace) %{_sysconfdir}/osg/grid3-locations.txt

%files misc
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/10-misc.ini

%files squid
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/01-squid.ini

%files monalisa
# This section intentionally left blank

%files managedfork
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/15-managedfork.ini

%files network
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/40-network.ini
%ghost /var/lib/osg/globus-firewall
%ghost %{_sysconfdir}/profile.d/osg.sh
%ghost %{_sysconfdir}/profile.d/osg.csh

%files infoservices
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/30-infoservices.ini

%files tests
%defattr(-,root,root)
/usr/share/osg-configure/*

%files slurm
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-slurm.ini

%files gateway
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/10-gateway.ini
%ghost %gateway_ini_backup

%files cemon
# This section intentionally left blank


# 1.0.62-1 and up use HTCondor-CE as the default gateway, but we don't want to
# change it for users upgrading from old versions so backup and restore
# 10-gateway.ini when upgrading from an old version.

# The backup file has a fixed name because it needs to be the same in both the
# pre scriptlet and the triggerun scriptlet.
%pre gateway
if [ $1 -gt 1 ]; then # upgrading
    %__rm -f  %gateway_ini_backup  ||  :
    %__cp -fp  %gateway_ini  %gateway_ini_backup  ||  :
fi

%triggerun gateway -- %name-gateway < 1.0.62-1
if [ $1 -gt 0 ]; then # upgrading, not uninstalling
    %__mv -f  %gateway_ini_backup  %gateway_ini  ||  :
fi



%changelog
* Sun May 28 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 1.8.0-2
- bump to rebuild with fixed tarball

* Sun May 28 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 1.8.0-1
- Reject empty allowed_vos (SOFTWARE-2703)
- Turn missing OSG_APP into a warning instead of an error (SOFTWARE-2674)
- Get default allowed_vos from voms-mapfiles/banfiles if using vomsmap auth (SOFTWARE-2670)

* Mon Apr 24 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 1.7.0-1
- Drop GIP/OSG-Info-Services support (SOFTWARE-2644)
- Make absence of user-vo-map file non-fatal (SOFTWARE-2696)
- Create /etc/lcmaps.db from template and add voms-mapfile support (SOFTWARE-2601)
  (adds dependency on lcmaps-db-templates (SOFTWARE-2692)

* Wed Mar 29 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6.2-1
- Fix info-services unit tests (SOFTWARE-2655)

* Mon Jan 30 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6.1-1
- Fix osg-configure -v for Resource Entry sections (SOFTWARE-2562)

* Tue Jan 24 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6.0-1
- Improve Resource Entry section (SOFTWARE-2562)
-  require 'queue'
-  add template in comments
-  add cpucount and maxmemory attributes
-  add subclusters and vo_tag attributes

* Tue Dec 27 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.4-1
- Don't require attributes in Resource Entry sections that aren't used in AGIS or the CE collector (SOFTWARE-2554)

* Mon Nov 28 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.3-1
- Quote settings written to Gratia probe configs (SOFTWARE-2311)

* Thu Nov 10 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.2-1
- Bugfix for 1.5.1 release (SOFTWARE-2478)

* Mon Nov 07 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.1-1
- Bugfix for 1.5.0 release (SOFTWARE-2478)

* Fri Oct 28 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.0-1
- Add "Resource Entry" as alias for "Subcluster" in 30-gip.ini (SOFTWARE-2478)

* Thu Aug 04 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.2-2
- Require condor-python (SOFTWARE-2420)

* Thu Jul 28 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.2-1
- Fix unit test TestMisc.testValidSettings() to use a gums_host that
  always resolves (SOFTWARE-2406)

* Wed Jun 22 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.1-1
- Set OSG_CONFIGURED=true for BOSCO HTCondor-CEs (SOFTWARE-2360)
- Add edit_lcmaps_db option to prevent changes to lcmaps.db (SOFTWARE-2321)
- Validate gums host (SOFTWARE-2319)
- Set BOSCO_RMS and BOSCO_ENDPOINT for use in BOSCO job routes (SOFTWARE-2366)

* Wed Apr 20 2016 Matyas Selmeci <matyas@cs.wisc.edu> 1.4.0-1
- Relax checks on non-site-controlled hosts (SOFTWARE-2123)
- Remove umask check and always use 022 for umask (SOFTWARE-2276)
- Consistenly quote values in blah.config (SOFTWARE-2226)
- Remove email domain check (SOFTWARE-2271)
- Set GRIDMAP in HTCondor-CE configuration if using gridmap auth
  (SOFTWARE-2244)
- Set authorization method in lcmaps.db (SOFTWARE-1723)
- Fix GIP tests failing if a CE is not installed (SOFTWARE-2224)
- Fix RSV probes not being enabled if gram_ce_hosts in UNAVAILABLE
  (SOFTWARE-2266)
- Add slurm_cluster to 20-slurm.ini (SOFTWARE-2264)

* Thu Mar 31 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.3.0-2
- Fix installation of SSH keys in BOSCO support (SOFTWARE-2188)

* Tue Mar 29 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.3.0-1
- Add Bosco support (SOFTWARE-2188)

* Fri Feb 19 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.2.6-1
- Add SGE settings to /etc/blah.config (SOFTWARE-2189)

* Thu Nov 19 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.2.5-1.osg
- Remove deprecated ReSS support (SOFTWARE-2103)

* Tue Nov 10 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.2.4-1.osg
- Do not look up offline ReSS servers (SOFTWARE-2102)

* Wed Oct 21 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.2.3-1.osg
- Run condor_ce_reconfig after generating the job attribute files, so the
  changes get picked up (SOFTWARE-2058)

* Fri Sep 25 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.2.2-1.osg
- Fix DeprecationWarning in resource catalog code (SOFTWARE-2031)

* Thu Sep 10 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.2.1-1.osg
- Fix wrong permissions in created files (SOFTWARE-2022)

* Mon Aug 24 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.2.0-2.osg
- Support IPv6 addresses in config files (SOFTWARE-1952)
- Add default for AllowedVOs for CE Collector (SOFTWARE-1895)

* Mon Jul 27 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.1.1-1.osg
- Fix spurious 'None' values in the job environment (SOFTWARE-1968)

* Tue Jun 23 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.1.0-1.osg
- Switch to Semantic Versioning
- Support Zabbix consumers in RSV (SOFTWARE-1923)
  (contributed by Trey Dockendorf)
- Improve handling of app_dir and data_dir settings (SOFTWARE-1946)
- Add sentinel value to HTCondor CE config (SOFTWARE-1954)
- Removed cemon code (SOFTWARE-1955)


* Tue May 26 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.72-1.osg
- Make osg-configure-info-services require osg-configure-gip (SOFTWARE-1911)
- Do not require subcluster sections in gip config if CE not installed (SOFTWARE-1912)
- Remove gateway-type patches (in upstream) (SOFTWARE-1918)

* Sun Apr 26 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.71-1.osg
- Handle multiple spaces in user-vo-map (SOFTWARE-1873)
- Fix broken link in job-environment.conf files (SOFTWARE-1834)
- Set lsf_confpath in /etc/blah.config (SOFTWARE-1843)
- Add default for MaxWallTime for CE Collector (SOFTWARE-1872)

* Tue Apr 07 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.70-1.osg
- Do not require the HTCondor Python bindings; handle their absence gracefully (SOFTWARE-1869)

* Mon Mar 30 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.69-2.osg
- Require the HTCondor Python bindings

* Mon Mar 30 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.69-1.osg
- Fix edg-mkgridmap path (SOFTWARE-1841)
- Use SCHEDD_ATTRS instead of SCHEDD_EXPRS (SOFTWARE-1838)
- Add warning if OSG_ResourceCatalog overridden (SOFTWARE-1847)
- Write blah_disable_wn_proxy_renewal=yes to blah config if not using Condor as the batch system (SOFTWARE-1803)

* Thu Feb 19 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.68-1
- Allow max_wall_time to be 0 or unspecified (SOFTWARE-1779)

* Fri Jan 23 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.67-1
- Reload condor and condor-ce configs if we change them (SOFTWARE-1732)
- Fix various bugs related to checking PER_JOB_HISTORY_DIR in the gratia config (SOFTWARE-1735)
- Look at COLLECTOR_PORT when setting JOB_ROUTER_SCHEDD2_POOL (SOFTWARE-1744)
- Warn about /etc/condor/config.d not being searched by Condor configuration (SOFTWARE-1746)
- Allow admins to specify queue and extra transforms in the resource ads for htcondor-ce (SOFTWARE-1759)
- Parallelize CRL downloads

* Mon Dec 15 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.66-1
- Fix test failures caused by default job gateway change (SOFTWARE-1703)
- Change generated job transform expressions to make compatibility aliases for job attributes (SOFTWARE-1727)

* Thu Dec 11 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.65-1
- Make run-osg-configure-tests return nonzero on failure (SOFTWARE-1703)

* Fri Nov 21 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.64-1
- Add MaxWallTime attribute to OSG_ResourceCatalog entries (SOFTWARE-1692)

* Mon Nov 17 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.63-2
- Prepend "TARGET." to terms in generated requirements expression so we can
  match against it (SOFTWARE-1688)
- Add AllowedVOs attribute to OSG_ResourceCatalog entries (SOFTWARE-1688)

* Thu Nov 13 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.62-3
- Tweaks to default gateway upgrade hack (SOFTWARE-1653)

* Mon Nov 10 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.62-1
- Change default gateway type to HTCondor-CE (SOFTWARE-1653)
- Remove upstreamed patches

* Mon Nov 3 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.61-5
- Fix bug in setting blah.config binpaths (SOFTWARE-1625)
- Fix PBS configuration bug which caused the 10-gateway.ini settings to be ignored

* Mon Oct 27 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.0.61-1
- Remove ce_collectors patch (in upstream)
- Make gratia configuration not require Condor to be started before running (SOFTWARE-1564)
- Advertise subcluster attributes in condor-ce schedd ads (SOFTWARE-1633)
- Set binpaths in /etc/blah.config (SOFTWARE-1625)
- Increase other attribute limits in GipConfiguration module (SOFTWARE-1638)

* Wed Oct 1 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.60-2
- Add patch to fix ce_collectors special values

* Tue Sep 30 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.60-1
- Remove SOFTWARE-1567 patch (in upstream)
- Work for Phase 1 of the HTCondor-CE Info-Services project:
    - Advertise some OSG-CE attributes in HTCondor-CE (SOFTWARE-1592)
    - Set CONDOR_VIEW_HOST in HTCondor-CE configs (SOFTWARE-1615)
- Increase core count limit in Gip configuration module (SOFTWARE-1605)
- Skip CEMon configuration of CEMon is missing

* Tue Sep 02 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.59-2
- Add patch to not try to mess with grid3-locations.txt if OSG_APP is UNSET (SOFTWARE-1567)

* Fri Aug 22 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.59-1
- Remove SOFTWARE-771 patch (in upstream)
- Allow unsetting OSG_APP by setting app_dir to a special 'UNSET' value (SOFTWARE-1567)

* Tue Aug 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.58-3
- Improve phrasing of warning message when OSG_JOB_CONTACT cannot be set because no batch system modules exist/are enabled (SOFTWARE-771)
- Mark the config file that gets created in /etc/condor-ce/config.d as a ghost file so it gets properly removed (SOFTWARE-1551)

* Wed Jul 30 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.58-1
- Since job environment attributes may be mapped to more than one section/option, display a list on error (SOFTWARE-1537)
- Don't require OSG_JOB_CONTACT if (a) there's no place to specify it (i.e. no jobmanager module is enabled) or (b) gram is disabled (SOFTWARE-771)
- Only set PATH if using htcondor-ce with condor (SOFTWARE-1554)

* Tue Jul 29 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.57-1
- Change error when no batch system is set to be configured into a warning (SOFTWARE-771)
- Improve error messages for missing job environment attributes (SOFTWARE-1537)
- Improve HTCondor-CE configuration for the Condor batch system (SOFTWARE-1551)
- Set PATH in osg-job-environment.conf (SOFTWARE-1554)

* Fri Jun 20 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.56-1
- Create service keys from host keys if desired (SOFTWARE-422)
- Fix bug in detection of installed Gratia probes (SOFTWARE-1518)

* Fri May 30 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.55-2
- Fix typo in 20-config.ini (SOFTWARE-1475)

* Thu May 22 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.55-1
- New version 1.0.55 (SOFTWARE-1482) with these changes:
-   Fix warnings when adding wlcg_* attributes to the [Site Information] section (SOFTWARE-1486)
-   Add setting for SGE configuration location (SOFTWARE-1481)
-   Fix path for SGE Gratia ProbeConfig file (SOFTWARE-1479)
-   Improve error message when condor_location is set wrong (SOFTWARE-1475)
-   Support one site with multiple CE types on different hosts (SOFTWARE-1471)
-   Remove monalisa module (SOFTWARE-1465)

* Mon May 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.54-3
- Create dummy osg-configure-cemon subpackage on el6 too (SOFTWARE-1468)
- Remove the obsoletes line for osg-configure-cemon.

* Mon May 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.54-2
- Added an obsoletes for osg-configure-cemon (SOFTWARE-1468)
- Also added a dummy osg-configure-cemon subpackage because the obsoletes doesn't work properly on el5

* Fri May 02 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.54-1
- Rename 'htcondor_ce_gateway_enabled' to 'htcondor_gateway_enabled' (SOFTWARE-1446)

* Thu May 01 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.53-1
- Rename 10-ce.ini to 10-gateway.ini and place it in a separate subpackage
- Fix semantics of listing enabled gateway services

* Wed Apr 23 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.52-1
- Ignore some fetch-crl errors the user has no control over (SOFTWARE-1428)
- Add run-osg-configure-tests script to run all the unit tests (SOFTWARE-710)
- Improve support for configuring RSV to use HTCondor-CE; add 10-ce.ini to
  choose between GRAM and HTCondor-CE (SOFTWARE-1446)

* Mon Feb 24 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.0.51-1
- Info-services fixes, unit tests and new config file 30-infoservices.ini (SOFTWARE-1276)

* Mon Feb 03 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.50-1
- Error in listing enabled services 

* Mon Jan 28 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.49-1
- Fix unit test reliance on cemon config test files

* Mon Jan 28 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.48-1
- Add support for osg infoservice
- Better checks in  gratia condor probe

* Thu Oct 24 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.47-1
- Fix for hostname identification on CentOS 6
- Fixes for bugs in condor-cron id fixes

* Thu Oct 17 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.46-1
- Allow sge binary location to be specified
- Give better error messages when options are missing
- Add requires in sub-rpms for osg-configure main rpm
- Check and fix condor-cron ids for RSV

* Wed Sep 16 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.45-1
- Update unit tests for http proxy validation

* Wed Sep 16 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.44-1
- Change http proxy validation per dicussions with Brian and Tim

* Wed Sep 9 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.43-1
- Fix gratia configuration errors for slurm configuration
- Update squid location checks 

* Wed Sep 9 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.42-1
- Fix gratia configuration errors for slurm/sge

* Wed Sep 4 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.41-1
- Added missing config files for unit tests
- Temporarily disable unit test for unused functionality

* Tue Sep 3 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.40-1
- Fix gratia condor probe configuration
- Fix breakage when variable substitution across files or bad variable
  substitution is present
- Add unit tests for above issue

* Thu Aug 29 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.39-1
- Fix squid unit test

* Thu Aug 29 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.38-1
- Add unit tests for squid location check
- Fixes for squid location check

* Fri Aug 23 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.37-1
- Unit test fixes
- Test squid location

* Mon Aug 19 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.36-1
- Multiple bug fixes
- Add Slurm gratia support

* Mon Aug 5 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.35-1
- Fix error message when ram_mb is too high

* Fri Aug 2 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.34-1
- Add unit tests for spaces in ini files

* Thu Aug 1 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.33-1
- Fixes for lines with spaces at beginning of sections in ini files
- Increase the allowed memory to 512GB per node in GIP sanity checks

* Thu Apr 25 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.30-1
- Remove duplicate and broken check for SGE log files

* Tue Apr 9 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.29-1
- Fix SGE unit test errors

* Tue Apr 9 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.28-1
- Fix SGE verification issue 
- Removed stray character in 20-lsf.ini file

* Fri Apr 5 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.27-1
- More fixes for LSF gratia probe configuration

* Fri Mar 29 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.26-1
- Fixes for LSF gratia probe configuration

* Thu Mar 28 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.25-1
- Use log_directory for LSF instead of accounting_log_directory

* Wed Mar 27 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.24-1
- Added support for configuring gratia LSF module

* Wed Mar 19 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.23-1
- Added multiple fixes for LSF

* Wed Feb 20 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.22-1
- Added support for fetch-crl3 if present

* Mon Feb 04 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.21-1
- Added support for SLURM and unit tests for SLURM

* Thu Jan 10 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.20-1
- Multiple clean ups in unit tests
- Add --enabled-services argument to retun a list of services configured

* Tue Dec 04 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.19-1
- Fix localsettings configuration (add getAttributes back)
- Fix gratia unit tests due to change in test configs
- Clean up unit test code based on pylint output

* Tue Dec 04 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.18-1
- Don't configure metric probe in gratia test configs

* Tue Dec 04 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.17-1
- Fix for SOFTWARE-859 / GOC-12974 
- Multiple cleanups and fixes based on pylint analysis

* Thu Nov 15 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.16-1
- Fixes for software-811, software-834 
- Code cleanups based on pylint

* Thu Aug 08 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.15-1
- Update tests for storage
- Incorporate SGE fixes
- Add support for sites without OSG_DATA or which dynamically set OSG_WN_TMP
- Fix various bugs reported by Patrick @ UTA

* Thu Jun 14 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.14-1
- Update tests and fix some minor bugs

* Thu Jun 14 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.13-1
- Fix network state file checking
- Update logging in unit tests

* Fri Jun 8 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.12-1
- Include a few test related changes that were accidentally left out of the
  previous release

* Fri Jun 8 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.11-1
- Allow WN_TMP to be left blank
- Don't require globus port state files to be present
- Updates to test packaging and cleanups

* Mon Jun 4 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.10-1
- Don't try to get rsv user uid, gid in __init__

* Fri Jun 1 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.8-1
- Multiple fixes

* Wed May 2 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.8-1
- Fix for SOFTWARE-597
- Fix for SOFTWARE-599 
- Added tests subpackage to distribute tests
- Added fixes for gip configuration issue Alain ran into

* Mon Apr 23 2012 Alain Roy <roy@cs.wisc.edu> 1.0.7-2
- Patched to fix SOFTWARE-637 (incorrectly setting accounting dir for PBS)
- Added proper setup for Gratia Metric probe -SWK
- Added new RSV option - legacy_proxy -SWK

* Wed Mar 14 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.7-1
- Fix for Software-552
- Implemented Software-568
- Fixes and changes suggested by Alain
- Unit test updates

* Wed Feb 29 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.6-1
- Add support for configuring gratia condor and pbs probes
- Fix missing newline in message when -d is used

* Thu Feb 23 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.5-1
- Cleaned up pbs and lsf config scripts to remove unused home settings
- Removed itb entries from cemon ini file
- Fixed gip errors when on a standalone RSV install

* Tue Feb 21 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.4-1
- Fixed a bug in RSV configuration that prevented the use of user proxies.

* Fri Jan 27 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.3-1
- Minor tweak to let configuration continue if grid3-locations isn't present
- Remove seg_enabled option from condor jobmanager section, it's not used or
  supported by globus condor lrm

* Fri Jan 20 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.2-1
- Minor bug fix for condor_location knob in 30-rsv.ini

* Fri Jan 20 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.1-1
- Added condor_location knob for RSV to specify non-standard installs.

* Tue Jan 17 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.0-1
- Added support for network/firewall configuration
- Improved error reporting 
- Bug fixes for error reporting

* Wed Jan 11 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.7.4-1
- Added configuration for osg-cleanup scripts

* Thu Jan 05 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.7.3-1
- Added support for globus job manager config
- Added support for updating lcmaps.db and gums-client.properties files
- Added support for configuring SEG for job managers that support it
- Improved error reporting
- Internal refactoring done to improve maintainability

* Fri Dec 30 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.7.2-1
- Improved RSV configuration

* Wed Dec 7 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.7.1-1
- Fix the default location of the condor_config file
- Update ini comments to point to correct documentation

* Mon Dec 1 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.7.0-1
- Fix fetching VO names from user-vo-map file

* Mon Nov 21 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.9-1
- Update defaults for rsv certs

* Thu Nov 17 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.8-1
- Fix bugs in configuring gratia probes

* Mon Nov 8 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.7-1
- Update to 0.6.7 to incorporate a variety of bug fixes
- Add support for configuring authentication methods

* Mon Oct 31 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.6-1
- Update to 0.6.6 to fix setting default job manager
- Update config files to use DEFAULT instead of UNAVAILABLE where appropriate

* Wed Oct 26 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.6.5-1
- Fixed a few RSV configuration issues.

* Tue Oct 25 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.4-1
- Writing to osg attributes file and update to 0.6.4

* Fri Oct 21 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.3-1
- Fix a few bugs and update to 0.6.3

* Fri Oct 21 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.2-1
- Added support for accept_limited in all job managers

* Thu Oct 20 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.1-1
- Added bugfixes dealing with managed fork configuration

* Thu Oct 20 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.0-1
- Added configuration of globus job manager for managed fork 
- Fixed unit tests for RSV

* Mon Oct 10 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.5.10-1
- Added configuration of glite-ce-monitor

* Mon Sep 26 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.5.8-1
- Fixed a bug in RSV configuration of gridftp hosts

* Tue Sep 13 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.5.7-1
- Fixed a bug in RSV configuration of Gratia Metric ProbeConfig

* Fri Sep 09 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.5.5-1
- Fixed a bug in rsv configuration when meta directory is not present

* Thu Sep 8 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.5.4-1
- Update to 0.5.4
- Add more subpackages for config files

* Mon Aug 26 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.5.2-1
- Update to 0.5.2
- Let config files reside in /etc/osg/config.d
- Make output files in /var/lib/osg ghost files

* Mon Aug 1 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.5.1-1
- Update to 0.5.1
- Add symlink for config.ini
- Make output files in /var/lib/osg ghost files

* Mon Jul 25 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.5.0-1
- Update to 0.5.0

* Mon Jul 25 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.0.4-1
- Update to 0.0.4

* Mon Jul 25 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.0.3-1
- Update to 0.0.3
- Fix python_sitelab declaration
- Use %{__python} instead of python

* Fri Jul  22 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.2-2
- Include .pyo files in files

* Fri Jul  22 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.2-1
- Created initial configure-osg rpm using real source 

* Thu Jul  21 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.1-1
- Created an initial osg-configure RPM 
