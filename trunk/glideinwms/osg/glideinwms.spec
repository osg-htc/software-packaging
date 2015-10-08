# The following should be either "v2_plus" or "v3_plus"
%define v2_plus 0
%define v3_plus 1

Name:           glideinwms

# Release Candidates NVR format
#%define release 0.1.rc1
# Official Release NVR format
#%define release 1

%if %{v2_plus}
%define version 2.7.2
%define release 1
%define frontend_xml frontend.xml
%define factory_xml glideinWMS.xml
%endif

# ------------------------------------------------------------------------------
# For Release Candidate builds, check with Software team on release string
# ------------------------------------------------------------------------------
%if %{v3_plus}
%define version 3.2.11.2
%define release 4
%define frontend_xml frontend.master.xml
%define factory_xml glideinWMS.master.xml
%endif

Version:        %{version}
Release:        %{release}%{?dist}

Summary:        The VOFrontend for glideinWMS submission host

Group:          System Environment/Daemons
License:        Fermitools Software Legal Information (Modified BSD License)
URL:            http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%define web_dir %{_localstatedir}/lib/gwms-frontend/web-area
%define web_base %{_localstatedir}/lib/gwms-frontend/web-base
%define frontend_dir %{_localstatedir}/lib/gwms-frontend/vofrontend
%define factory_web_dir %{_localstatedir}/lib/gwms-factory/web-area
%define factory_web_base %{_localstatedir}/lib/gwms-factory/web-base
%define factory_dir %{_localstatedir}/lib/gwms-factory/work-dir
%define condor_dir %{_localstatedir}/lib/gwms-factory/condor


#Source0:        http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/glideinWMS_v2_5_1_frontend.tgz
Source:	glideinwms.tar.gz

# How to build tar file
# git clone http://cdcvs.fnal.gov/projects/glideinwms
# cd glideinwms
# git archive v3_0_rc3 --prefix='glideinwms/' | gzip > ../glideinwms.tar.gz
# change v3_0_rc3 to the proper tag in the above line

Source1:        creation/templates/frontend_startup
Source2:        %{frontend_xml}
Source3:        gwms-frontend.conf.httpd
Source4:	%{factory_xml}
Source5:        gwms-factory.conf.httpd
Source6:        creation/templates/factory_startup
Source7:	chksum.sh
Source8:        gwms-frontend.sysconfig
Source9:        gwms-factory.sysconfig

Patch0:         No-collectors-behind-shared-port.patch

%description
This is a package for the glidein workload management system.
GlideinWMS provides a simple way to access the Grid resources
through a dynamic condor pool of grid-submitted resources.
Two packages exist (factory and vofrontend) plus 
dependent condor packages for additional condor customizability.


%package vofrontend
Summary:        The VOFrontend for glideinWMS submission host
Group:          System Environment/Daemons
Provides:	GlideinWMSFrontend = %{version}-%{release}
Obsoletes:	GlideinWMSFrontend < 2.5.1-11
Requires: glideinwms-vofrontend-standalone = %{version}-%{release}
Requires: glideinwms-userschedd = %{version}-%{release}
Requires: glideinwms-usercollector = %{version}-%{release}
Obsoletes: glideinwms-vofrontend-condor < 2.6.2-2
%description vofrontend
The purpose of the glideinWMS is to provide a simple way 
to access the Grid resources. GlideinWMS is a Glidein 
Based WMS (Workload Management System) that works on top of 
Condor. For those familiar with the Condor system, it is used 
for scheduling and job control. 
This package is for a one-node vofrontend install
(userschedd,submit,vofrontend).


%package vofrontend-standalone
Summary:        The VOFrontend for glideinWMS submission host
Group:          System Environment/Daemons
Requires: httpd
# Most functions work with HTCondor 7.8.0 (and newer) 
# gangliad enabled by default requires 8.2 - disable it if you have an older condor
# 8.2.2 should be avoided because incompatible with 8.0
Requires: condor >= 8.2.3
Requires: python-rrdtool
Requires: m2crypto
Requires: javascriptrrd >= 1.1.0

# former osg-client requirements (minus networking stuff)
Requires: globus-common-progs
Requires: globus-gram-client-tools
Requires: globus-gsi-cert-utils-progs
Requires: gsi-openssh-clients
Requires: osg-cert-scripts
Requires: osg-system-profiler
Requires: osg-version
Requires: osg-wn-client
Requires: vo-client

Requires: glideinwms-minimal-condor = %{version}-%{release}
Requires: glideinwms-libs = %{version}-%{release}
Requires: glideinwms-glidecondor-tools = %{version}-%{release}
Requires: glideinwms-common-tools = %{version}-%{release}
#To be added in 2.6.3+ once probe is finished.
#Requires: gratia-probe-gwms
#Requires: vdt-vofrontend-essentials
Requires(post): /sbin/service
Requires(post): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
%description vofrontend-standalone
The purpose of the glideinWMS is to provide a simple way
to access the Grid resources. GlideinWMS is a Glidein
Based WMS (Workload Management System) that works on top of
Condor. For those familiar with the Condor system, it is used
for scheduling and job control.
This package is for a standalone vofrontend install


%package usercollector
Summary:        The VOFrontend glideinWMS collector host
Group:          System Environment/Daemons
Requires: condor >= 7.8.0
Requires: glideinwms-minimal-condor = %{version}-%{release}
Requires: glideinwms-glidecondor-tools = %{version}-%{release}
%description usercollector
The user collector matches user jobs to glideins in the WMS pool.
It can be split off into its own node.


%package userschedd
Summary:        The VOFrontend glideinWMS submission host
Group:          System Environment/Daemons
Requires: condor >= 7.8.0
Requires: glideinwms-minimal-condor = %{version}-%{release}
Requires: glideinwms-glidecondor-tools = %{version}-%{release}
%description userschedd
This is a package for a glideinwms submit host.


%package libs
Summary:        The glideinWMS common libraries.
Group:          System Environment/Daemons
Requires: python-rrdtool
Requires: python-ldap
Requires: m2crypto
%description libs
This is a package provides common libraries used by glideinwms.


%package glidecondor-tools
Summary:        Condor tools useful with the glideinWMS.
Group:          System Environment/Daemons
Requires: glideinwms-libs = %{version}-%{release}
%description glidecondor-tools
This is a package provides common libraries used by glideinwms.


%package minimal-condor
Summary:        The VOFrontend minimal condor config
Group:          System Environment/Daemons
Provides: gwms-condor-config
Requires: glideinwms-condor-common-config = %{version}-%{release}
%description minimal-condor
This is an alternate condor config for just the minimal amount
needed for VOFrontend.


%package condor-common-config
Summary:        Shared condor config files
Group:          System Environment/Daemons
%description condor-common-config
This contains condor config files shared between alternate
condor config setups (minimal-condor and factory-condor).


%package common-tools
Summary:        Shared tools
Group:          System Environment/Daemons
%description common-tools
This contains tools common to both the glideinwms factory and vofrontend
standalone packages.


%package factory
Summary:        The Factory for glideinWMS
Group:          System Environment/Daemons
Provides:       GlideinWMSFactory = %{version}-%{release}
Requires: httpd
# We require Condor 7.6.0 (and newer) to support
# condor_advertise -multiple -tcp which is enabled by default
Requires: glideinwms-factory-condor = %{version}-%{release}
Requires: glideinwms-libs = %{version}-%{release}
Requires: glideinwms-glidecondor-tools = %{version}-%{release}
Requires: glideinwms-common-tools = %{version}-%{release}
Requires: condor >= 7.8.0
Requires: python-rrdtool
Requires: python-ldap
Requires: m2crypto
Requires: javascriptrrd >= 1.1.0
Requires(post): /sbin/service
Requires(post): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
%description factory
The purpose of the glideinWMS is to provide a simple way
to access the Grid resources. GlideinWMS is a Glidein
Based WMS (Workload Management System) that works on top of
HTCondor. For those familiar with the Condor system, it is used
for scheduling and job control.


%package factory-condor
Summary:        The GWMS Factory condor config
Group:          System Environment/Daemons
Provides: gwms-factory-config
Requires: glideinwms-condor-common-config = %{version}-%{release}
%description factory-condor
This is a package including condor_config for a full one-node
install of wmscollector + wms factory




%prep
%setup -q -n glideinwms
# Apply the patches
%patch -P 0 -p1
#%patch -P 1 -p1
#%patch -P 2 -p1
#%patch -P 3 -p1

%build
cp %{SOURCE7} .
chmod 700 chksum.sh
./chksum.sh v%{version}-%{release}.osg etc/checksum.frontend "CVS config_examples doc .git .gitattributes poolwatcher factory/check* factory/glideFactory* factory/test* factory/manage* factory/stop* factory/tools creation/create_glidein creation/reconfig_glidein creation/info_glidein creation/lib/cgW* creation/web_base/factory*html creation/web_base/collector_setup.sh creation/web_base/condor_platform_select.sh creation/web_base/condor_startup.sh creation/web_base/create_mapfile.sh creation/web_base/gcb_setup.sh creation/web_base/glexec_setup.sh creation/web_base/glidein_startup.sh creation/web_base/job_submit.sh creation/web_base/local_start.sh creation/web_base/setup_x509.sh creation/web_base/update_proxy.py creation/web_base/validate_node.sh chksum.sh etc/checksum* unittests"
./chksum.sh v%{version}-%{release}.osg etc/checksum.factory "CVS config_examples doc .git .gitattributes poolwatcher frontend/* creation/reconfig_glidein creation/clone_glidein creation/lib/cgW* creation/web_base/factory*html creation/web_base/collector_setup.sh creation/web_base/condor_platform_select.sh creation/web_base/condor_startup.sh creation/web_base/create_mapfile.sh creation/web_base/gcb_setup.sh creation/web_base/glexec_setup.sh creation/web_base/glidein_startup.sh creation/web_base/job_submit.sh creation/web_base/local_start.sh creation/web_base/setup_x509.sh creation/web_base/update_proxy.py creation/web_base/validate_node.sh chksum.sh etc/checksum* unittests"

%install
rm -rf $RPM_BUILD_ROOT

# Set the Python version
%define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%d.%d'%v")

# From http://fedoraproject.org/wiki/Packaging:Python
# Define python_sitelib
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

#Change src_dir in reconfig_Frontend
sed -i "s/WEB_BASE_DIR=.*/WEB_BASE_DIR=\"\/var\/lib\/gwms-frontend\/web-base\"/" creation/reconfig_frontend
sed -i "s/STARTUP_DIR=.*/STARTUP_DIR=\"\/var\/lib\/gwms-frontend\/web-base\"/" creation/reconfig_frontend
sed -i "s/WEB_BASE_DIR=.*/WEB_BASE_DIR=\"\/var\/lib\/gwms-factory\/web-base\"/" creation/reconfig_glidein
sed -i "s/STARTUP_DIR =.*/STARTUP_DIR=\"\/var\/lib\/gwms-factory\/web-base\"/" creation/reconfig_glidein
sed -i "s/STARTUP_DIR =.*/STARTUP_DIR=\"\/var\/lib\/gwms-factory\/web-base\"/" creation/clone_glidein

#Create the RPM startup files (init.d) from the templates
creation/create_rpm_startup . %{SOURCE1} %{SOURCE6}

# install the executables
install -d $RPM_BUILD_ROOT%{_sbindir}
# Find all the executables in the frontend directory
install -m 0500 frontend/checkFrontend.py $RPM_BUILD_ROOT%{_sbindir}/checkFrontend
install -m 0500 frontend/glideinFrontendElement.py $RPM_BUILD_ROOT%{_sbindir}/glideinFrontendElement.py
install -m 0500 frontend/glideinFrontend.py $RPM_BUILD_ROOT%{_sbindir}/glideinFrontend
install -m 0500 frontend/stopFrontend.py $RPM_BUILD_ROOT%{_sbindir}/stopFrontend
install -m 0500 creation/reconfig_frontend $RPM_BUILD_ROOT%{_sbindir}/reconfig_frontend

#install the factory executables
install -m 0500 factory/checkFactory.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 factory/glideFactory.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 factory/glideFactoryEntry.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 factory/glideFactoryEntryGroup.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 factory/manageFactoryDowntimes.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 factory/stopFactory.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 creation/reconfig_glidein $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 creation/clone_glidein $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 creation/info_glidein $RPM_BUILD_ROOT%{_sbindir}/


# install the library parts
# FIXME: Need to create a subdirectory for vofrontend python files
install -d $RPM_BUILD_ROOT%{python_sitelib}
cp -r ../glideinwms $RPM_BUILD_ROOT%{python_sitelib}
# Some of the files are not needed by RPM
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/install
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/doc
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/etc
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/config_examples
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/create_rpm_startup
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/.gitattributes
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/unittests
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/chksum.sh
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/LICENSE.txt
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/ACKNOWLEDGMENTS.txt
# Put in other places
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/web_base
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/add_entry
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/clone_glidein
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/create_condor_tarball
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/create_frontend
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/create_glidein
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/info_glidein
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/reconfig_frontend
rm -f $RPM_BUILD_ROOT%{python_sitelib}/glideinwms/creation/reconfig_glidein


# Install the init.d
install -d  $RPM_BUILD_ROOT/%{_initrddir}
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/gwms-frontend
install -m 0755 %{SOURCE6} $RPM_BUILD_ROOT/%{_initrddir}/gwms-factory

# Install the web directory
install -d $RPM_BUILD_ROOT%{frontend_dir}
install -d $RPM_BUILD_ROOT%{web_base}
install -d $RPM_BUILD_ROOT%{web_dir}
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/
install -d $RPM_BUILD_ROOT%{web_dir}/stage/
install -d $RPM_BUILD_ROOT%{web_dir}/stage/group_main
install -d $RPM_BUILD_ROOT%{factory_dir}
install -d $RPM_BUILD_ROOT%{factory_web_base}
install -d $RPM_BUILD_ROOT%{factory_web_dir}
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/
install -d $RPM_BUILD_ROOT%{factory_web_dir}/stage/
install -d $RPM_BUILD_ROOT%{factory_dir}/lock
install -d $RPM_BUILD_ROOT%{condor_dir}


install -d $RPM_BUILD_ROOT%{web_dir}/monitor/lock
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/jslibs
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/total
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/group_main
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/group_main/lock
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/group_main/total
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/lock
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/jslibs
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/total
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/group_main
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/group_main/lock
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/group_main/total

install -m 644 creation/web_base/nodes.blacklist $RPM_BUILD_ROOT%{web_dir}/stage/nodes.blacklist
install -m 644 creation/web_base/nodes.blacklist $RPM_BUILD_ROOT%{web_dir}/stage/group_main/nodes.blacklist

# Install the logs
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-frontend/frontend
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-frontend/group_main
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-factory
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-factory/server
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-factory/server/factory
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-factory/client
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/gwms-factory/client-proxies


# Install frontend temp dir, for all the frontend.xml.<checksum>
install -d $RPM_BUILD_ROOT%{frontend_dir}/lock
#install -d $RPM_BUILD_ROOT%{frontend_dir}/monitor
#install -d $RPM_BUILD_ROOT%{frontend_dir}/monitor/group_main
install -d $RPM_BUILD_ROOT%{frontend_dir}/group_main
install -d $RPM_BUILD_ROOT%{frontend_dir}/group_main/lock
#install -d $RPM_BUILD_ROOT%{frontend_dir}/group_main/monitor

install -m 644 creation/web_base/frontendRRDBrowse.html $RPM_BUILD_ROOT%{web_dir}/monitor/frontendRRDBrowse.html
install -m 644 creation/web_base/frontendRRDGroupMatrix.html $RPM_BUILD_ROOT%{web_dir}/monitor/frontendRRDGroupMatrix.html  
install -m 644 creation/web_base/frontendStatus.html $RPM_BUILD_ROOT%{web_dir}/monitor/frontendStatus.html 
install -m 644 creation/web_base/frontend/index.html $RPM_BUILD_ROOT%{web_dir}/monitor/
install -m 644 creation/web_base/factory/index.html $RPM_BUILD_ROOT%{factory_web_dir}/monitor/
cp -arp creation/web_base/factory/images $RPM_BUILD_ROOT%{factory_web_dir}/monitor/
cp -arp creation/web_base/frontend/images $RPM_BUILD_ROOT%{web_dir}/monitor/

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
# Install the frontend config dir
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-frontend
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-frontend/frontend.xml
install -m 0644 %{SOURCE8} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/gwms-frontend

# Install the factory config dir
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-factory
install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-factory/glideinWMS.xml
install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/gwms-factory

# Install the web base
cp -r creation/web_base/* $RPM_BUILD_ROOT%{web_base}/
cp -r creation/web_base/* $RPM_BUILD_ROOT%{factory_web_base}/
rm -rf $RPM_BUILD_ROOT%{web_base}/CVS

# Install condor stuff
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor/ganglia.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor/certs
#make sure this (new) file exists, can be deprecated in gwms 2.7 or so
touch install/templates/90_gwms_dns.config
install -m 0644 install/templates/00_gwms_factory_general.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/00_gwms_general.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/01_gwms_factory_collectors.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/01_gwms_collectors.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/01_gwms_ganglia.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/02_gwms_factory_schedds.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/02_gwms_schedds.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/03_gwms_local.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/11_gwms_secondary_collectors.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/90_gwms_dns.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/01_gwms_metrics.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/ganglia.d/
install -m 0644 install/templates/condor_mapfile $RPM_BUILD_ROOT%{_sysconfdir}/condor/certs/
install -m 0644 install/templates/privsep_config $RPM_BUILD_ROOT%{_sysconfdir}/condor/

#Install condor schedd dirs
for schedd in "schedd_glideins2" "schedd_glideins3" "schedd_glideins4" "schedd_glideins5" "schedd_jobs2"; do
	install -d $RPM_BUILD_ROOT/var/lib/condor/$schedd
	install -d $RPM_BUILD_ROOT/var/lib/condor/$schedd/execute
	install -d $RPM_BUILD_ROOT/var/lib/condor/$schedd/lock
	install -d $RPM_BUILD_ROOT/var/lib/condor/$schedd/procd_pipe
	install -d $RPM_BUILD_ROOT/var/lib/condor/$schedd/spool
done


# Install tools
install -d $RPM_BUILD_ROOT%{_bindir}
# Install the tools as the non-*.py filenames
for file in tools/[!_]*.py; do
   newname=`echo $file | sed -e 's/.*\/\(.*\)\.py/\1/'`
   cp $file $RPM_BUILD_ROOT%{_bindir}/$newname
done
for file in factory/tools/[!_]*; do
   if [ -f "$file" ]; then
      newname=`echo $file | sed -e 's/\(.*\)\.py/\1/'`
      newname=`echo $newname | sed -e 's/.*\/\(.*\)/\1/'`
      cp $file $RPM_BUILD_ROOT%{_bindir}/$newname
   fi
done
cp creation/create_condor_tarball $RPM_BUILD_ROOT%{_bindir}

# Install glidecondor
install -m 0755 install/glidecondor_addDN $RPM_BUILD_ROOT%{_sbindir}/glidecondor_addDN
install -m 0755 install/glidecondor_createSecSched $RPM_BUILD_ROOT%{_sbindir}/glidecondor_createSecSched
install -m 0755 install/glidecondor_createSecCol $RPM_BUILD_ROOT%{_sbindir}/glidecondor_createSecCol

# Install checksum file
install -m 0644 etc/checksum.frontend $RPM_BUILD_ROOT%{frontend_dir}/checksum.frontend
install -m 0644 etc/checksum.factory $RPM_BUILD_ROOT%{factory_dir}/checksum.factory

#Install web area conf
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/gwms-frontend.conf
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/gwms-factory.conf

%if %{v3_plus}
install -d $RPM_BUILD_ROOT%{web_base}/../creation
install -d $RPM_BUILD_ROOT%{web_base}/../creation/templates
install -d $RPM_BUILD_ROOT%{factory_web_base}/../creation
install -d $RPM_BUILD_ROOT%{factory_web_base}/../creation/templates
install -m 0644 creation/templates/factory_initd_startup_template $RPM_BUILD_ROOT%{factory_web_base}/../creation/templates/
install -m 0644 creation/templates/frontend_initd_startup_template $RPM_BUILD_ROOT%{web_base}/../creation/templates/
%endif

%post vofrontend-standalone
# $1 = 1 - Installation
# $1 = 2 - Upgrade
# Source: http://www.ibm.com/developerworks/library/l-rpm2/

fqdn_hostname=`hostname -f`
frontend_name=`echo $fqdn_hostname | sed 's/\./-/g'`_OSG_gWMSFrontend

sed -i "s/FRONTEND_NAME_CHANGEME/$frontend_name/g" %{_sysconfdir}/gwms-frontend/frontend.xml
sed -i "s/FRONTEND_HOSTNAME/$fqdn_hostname/g" %{_sysconfdir}/gwms-frontend/frontend.xml

# If the startup log exists, change the ownership to frontend user
# Ownership was fixed in v3.2.4 with the init script templates rewrite
if [ -f %{_localstatedir}/log/gwms-frontend/frontend/startup.log ]; then
    chown frontend.frontend %{_localstatedir}/log/gwms-frontend/frontend/startup.log
fi

/sbin/chkconfig --add gwms-frontend
if [ ! -e %{frontend_dir}/monitor ]; then
    ln -s %{web_dir}/monitor %{frontend_dir}/monitor
fi

%post factory

fqdn_hostname=`hostname -f`
sed -i "s/FACTORY_HOSTNAME/$fqdn_hostname/g" %{_sysconfdir}/gwms-factory/glideinWMS.xml
if [ "$1" = "1" ] ; then
    if [ ! -e %{factory_dir}/monitor ]; then
        ln -s %{factory_web_dir}/monitor %{factory_dir}/monitor
    fi
    if [ ! -e %{factory_dir}/log ]; then
        ln -s %{_localstatedir}/log/gwms-factory %{factory_dir}/log
    fi
fi

%pre vofrontend-standalone
# Add the "frontend" user and group if they do not exist
getent group frontend >/dev/null || groupadd -r frontend
getent passwd frontend >/dev/null || \
       useradd -r -g frontend -d /var/lib/gwms-frontend \
	-c "VO Frontend user" -s /sbin/nologin frontend
# If the frontend user already exists make sure it is part of frontend group
usermod --append --groups frontend frontend >/dev/null

%pre factory
# Add the "gfactory" user and group if they do not exist
getent group gfactory >/dev/null || groupadd -r gfactory
getent passwd gfactory >/dev/null || \
       useradd -r -g gfactory -d /var/lib/gwms-factory \
	-c "GlideinWMS Factory user" -s /sbin/nologin gfactory
# If the gfactory user already exists make sure it is part of gfactory group
usermod --append --groups gfactory gfactory >/dev/null

# Add the "frontend" user and group if they do not exist
getent group frontend >/dev/null || groupadd -r frontend
getent passwd frontend >/dev/null || \
       useradd -r -g frontend -d /var/lib/gwms-frontend \
	-c "VO Frontend user" -s /sbin/nologin frontend
# If the frontend user already exists make sure it is part of frontend group
usermod --append --groups frontend frontend >/dev/null

%preun vofrontend-standalone
# $1 = 0 - Action is uninstall
# $1 = 1 - Action is upgrade

if [ "$1" = "0" ] ; then
    /sbin/chkconfig --del gwms-frontend
fi

if [ "$1" = "0" ]; then
    # Remove the symlinks
    rm -f %{frontend_dir}/frontend.xml
    rm -f %{frontend_dir}/monitor
    rm -f %{frontend_dir}/group_main/monitor

    # A lot of files are generated, but rpm won't delete those
#    rm -rf %{_datadir}/gwms-frontend
#    rm -rf %{_localstatedir}/log/gwms-frontend/*
fi

%preun factory
if [ "$1" = "0" ] ; then
    /sbin/chkconfig --del gwms-factory
fi
if [ "$1" = "0" ]; then
    rm -f %{factory_dir}/log
    rm -f %{factory_dir}/monitor
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files vofrontend
   
%files common-tools
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/glidein_cat
%attr(755,root,root) %{_bindir}/glidein_gdb
%attr(755,root,root) %{_bindir}/glidein_interactive
%attr(755,root,root) %{_bindir}/glidein_ls
%attr(755,root,root) %{_bindir}/glidein_ps
%attr(755,root,root) %{_bindir}/glidein_status
%attr(755,root,root) %{_bindir}/glidein_top
%attr(755,root,root) %{_bindir}/wmsTxtView
%attr(755,root,root) %{_bindir}/wmsXMLView
%{python_sitelib}/glideinwms/tools
%{python_sitelib}/glideinwms/creation/__init__.py
%{python_sitelib}/glideinwms/creation/__init__.pyc
%{python_sitelib}/glideinwms/creation/__init__.pyo
%{python_sitelib}/glideinwms/creation/lib/cWConsts.py
%{python_sitelib}/glideinwms/creation/lib/cWConsts.pyc
%{python_sitelib}/glideinwms/creation/lib/cWConsts.pyo
%{python_sitelib}/glideinwms/creation/lib/cWDictFile.py
%{python_sitelib}/glideinwms/creation/lib/cWDictFile.pyc
%{python_sitelib}/glideinwms/creation/lib/cWDictFile.pyo
%{python_sitelib}/glideinwms/creation/lib/cWParams.py
%{python_sitelib}/glideinwms/creation/lib/cWParams.pyc
%{python_sitelib}/glideinwms/creation/lib/cWParams.pyo
%{python_sitelib}/glideinwms/creation/lib/cWParamDict.py
%{python_sitelib}/glideinwms/creation/lib/cWParamDict.pyc
%{python_sitelib}/glideinwms/creation/lib/cWParamDict.pyo
%{python_sitelib}/glideinwms/creation/lib/xslt.py
%{python_sitelib}/glideinwms/creation/lib/xslt.pyc
%{python_sitelib}/glideinwms/creation/lib/xslt.pyo
%{python_sitelib}/glideinwms/creation/lib/__init__.py
%{python_sitelib}/glideinwms/creation/lib/__init__.pyc
%{python_sitelib}/glideinwms/creation/lib/__init__.pyo

%files factory
%defattr(-,gfactory,gfactory,-)
%doc LICENSE.txt
%doc ACKNOWLEDGMENTS.txt
%doc doc
%attr(755,root,root) %{_bindir}/analyze_entries
%attr(755,root,root) %{_bindir}/analyze_frontends
%attr(755,root,root) %{_bindir}/analyze_queues
%attr(755,root,root) %{_bindir}/cat_MasterLog
%attr(755,root,root) %{_bindir}/cat_StartdHistoryLog
%attr(755,root,root) %{_bindir}/cat_StartdLog
%attr(755,root,root) %{_bindir}/cat_StarterLog
%attr(755,root,root) %{_bindir}/cat_XMLResult
%attr(755,root,root) %{_bindir}/cat_logs
%attr(755,root,root) %{_bindir}/configGUI
%attr(755,root,root) %{_bindir}/convert_factory_2to3.sh
%attr(755,root,root) %{_bindir}/convert_factory_2to3.xslt
%attr(755,root,root) %{_bindir}/convert_factory_rrds_2to3.sh
%attr(755,root,root) %{_bindir}/create_condor_tarball
%attr(755,root,root) %{_bindir}/entry_ls
%attr(755,root,root) %{_bindir}/entry_q
%attr(755,root,root) %{_bindir}/entry_rm
%attr(755,root,root) %{_bindir}/extract_EC2_Address
%attr(755,root,root) %{_bindir}/find_StartdLogs
%attr(755,root,root) %{_bindir}/find_ids_not_published
%attr(755,root,root) %{_bindir}/find_logs
%attr(755,root,root) %{_bindir}/find_matching_ids
%attr(755,root,root) %{_bindir}/find_missing_ids
%attr(755,root,root) %{_bindir}/find_new_entries
%attr(755,root,root) %{_bindir}/find_partial_matching_ids
%attr(755,root,root) %{_bindir}/gwms-logcat.sh
%attr(755,root,root) %{_bindir}/infosys_lib
%attr(755,root,root) %{_bindir}/manual_glidein_submit
%attr(755,root,root) %{_bindir}/proxy_info
%attr(755,root,root) %{_sbindir}/checkFactory.py
%attr(755,root,root) %{_sbindir}/stopFactory.py
%attr(755,root,root) %{_sbindir}/glideFactory.py
%attr(755,root,root) %{_sbindir}/glideFactoryEntry.py
%attr(755,root,root) %{_sbindir}/glideFactoryEntryGroup.py

%if %{?rhel}%{!?rhel:0} == 5
%attr(755,root,root) %{_sbindir}/checkFactory.pyc
%attr(755,root,root) %{_sbindir}/checkFactory.pyo
%attr(755,root,root) %{_sbindir}/glideFactory.pyc
%attr(755,root,root) %{_sbindir}/glideFactory.pyo
%attr(755,root,root) %{_sbindir}/glideFactoryEntry.pyc
%attr(755,root,root) %{_sbindir}/glideFactoryEntry.pyo
%attr(755,root,root) %{_sbindir}/glideFactoryEntryGroup.pyc
%attr(755,root,root) %{_sbindir}/glideFactoryEntryGroup.pyo
%attr(755,root,root) %{_sbindir}/manageFactoryDowntimes.pyc
%attr(755,root,root) %{_sbindir}/manageFactoryDowntimes.pyo
%attr(755,root,root) %{_sbindir}/stopFactory.pyc
%attr(755,root,root) %{_sbindir}/stopFactory.pyo
%endif
%attr(755,root,root) %{_sbindir}/info_glidein
%attr(755,root,root) %{_sbindir}/manageFactoryDowntimes.py
%attr(755,root,root) %{_sbindir}/reconfig_glidein
%attr(755,root,root) %{_sbindir}/clone_glidein
%attr(-, root, root) %dir %{_localstatedir}/lib/gwms-factory
%attr(-, root, root) %{_localstatedir}/lib/gwms-factory/client-proxies
%attr(-, gfactory, gfactory) %{factory_web_dir}
%attr(-, gfactory, gfactory) %{factory_web_base}

%if %{v3_plus}
%attr(-, gfactory, gfactory) %{factory_web_base}/../creation
%endif
%attr(-, gfactory, gfactory) %{factory_dir}
%attr(-, gfactory, gfactory) %dir %{condor_dir}
%attr(-, root, root) %dir %{_localstatedir}/log/gwms-factory
%attr(-, root, root) %dir %{_localstatedir}/log/gwms-factory/client
%attr(-, gfactory, gfactory) %{_localstatedir}/log/gwms-factory/server
%{python_sitelib}/glideinwms/creation/lib/cgWConsts.py
%{python_sitelib}/glideinwms/creation/lib/cgWConsts.pyc
%{python_sitelib}/glideinwms/creation/lib/cgWConsts.pyo
%{python_sitelib}/glideinwms/creation/lib/cgWCreate.py
%{python_sitelib}/glideinwms/creation/lib/cgWCreate.pyc
%{python_sitelib}/glideinwms/creation/lib/cgWCreate.pyo
%{python_sitelib}/glideinwms/creation/lib/cgWDictFile.py
%{python_sitelib}/glideinwms/creation/lib/cgWDictFile.pyc
%{python_sitelib}/glideinwms/creation/lib/cgWDictFile.pyo
%{python_sitelib}/glideinwms/creation/lib/cgWParamDict.py
%{python_sitelib}/glideinwms/creation/lib/cgWParamDict.pyo
%{python_sitelib}/glideinwms/creation/lib/cgWParamDict.pyc
%{python_sitelib}/glideinwms/creation/lib/cgWParams.py
%{python_sitelib}/glideinwms/creation/lib/cgWParams.pyc
%{python_sitelib}/glideinwms/creation/lib/cgWParams.pyo
%if %{v3_plus}
%{python_sitelib}/glideinwms/creation/templates/factory_initd_startup_template
%endif
%{python_sitelib}/glideinwms/factory
%{_initrddir}/gwms-factory
%config(noreplace) %{_sysconfdir}/httpd/conf.d/gwms-factory.conf
%attr(-, gfactory, gfactory) %dir %{_sysconfdir}/gwms-factory
%attr(-, gfactory, gfactory) %config(noreplace) %{_sysconfdir}/gwms-factory/glideinWMS.xml
%config(noreplace) %{_sysconfdir}/sysconfig/gwms-factory

%files vofrontend-standalone
%defattr(-,frontend,frontend,-)
%doc LICENSE.txt
%doc ACKNOWLEDGMENTS.txt
%doc doc
%attr(755,root,root) %{_sbindir}/checkFrontend
%attr(755,root,root) %{_sbindir}/glideinFrontend
%attr(755,root,root) %{_sbindir}/glideinFrontendElement.py*
%attr(755,root,root) %{_sbindir}/reconfig_frontend
%attr(755,root,root) %{_sbindir}/stopFrontend
%attr(-, frontend, frontend) %dir %{_localstatedir}/lib/gwms-frontend
%attr(-, frontend, frontend) %{web_dir}
%attr(-, frontend, frontend) %{web_base}
%attr(-, frontend, frontend) %{frontend_dir}
%attr(-, frontend, frontend) %{_localstatedir}/log/gwms-frontend
%{python_sitelib}/glideinwms/frontend
%{python_sitelib}/glideinwms/creation/lib/cvWConsts.py
%{python_sitelib}/glideinwms/creation/lib/cvWConsts.pyc
%{python_sitelib}/glideinwms/creation/lib/cvWConsts.pyo
%{python_sitelib}/glideinwms/creation/lib/cvWCreate.py
%{python_sitelib}/glideinwms/creation/lib/cvWCreate.pyc
%{python_sitelib}/glideinwms/creation/lib/cvWCreate.pyo
%{python_sitelib}/glideinwms/creation/lib/cvWDictFile.py
%{python_sitelib}/glideinwms/creation/lib/cvWDictFile.pyc
%{python_sitelib}/glideinwms/creation/lib/cvWDictFile.pyo
%{python_sitelib}/glideinwms/creation/lib/cvWParamDict.py
%{python_sitelib}/glideinwms/creation/lib/cvWParamDict.pyc
%{python_sitelib}/glideinwms/creation/lib/cvWParamDict.pyo
%{python_sitelib}/glideinwms/creation/lib/cvWParams.py
%{python_sitelib}/glideinwms/creation/lib/cvWParams.pyc
%{python_sitelib}/glideinwms/creation/lib/cvWParams.pyo
%if %{v3_plus}
%{python_sitelib}/glideinwms/creation/templates/frontend_initd_startup_template
%endif
%{_initrddir}/gwms-frontend
%config(noreplace) %{_sysconfdir}/httpd/conf.d/gwms-frontend.conf
%attr(-, frontend, frontend) %dir %{_sysconfdir}/gwms-frontend
%attr(-, frontend, frontend) %config(noreplace) %{_sysconfdir}/gwms-frontend/frontend.xml
%config(noreplace) %{_sysconfdir}/sysconfig/gwms-frontend
%if %{v3_plus}
%attr(-, frontend, frontend) %{web_base}/../creation
%endif


%files factory-condor
%config(noreplace) %{_sysconfdir}/condor/config.d/00_gwms_factory_general.config
%config(noreplace) %{_sysconfdir}/condor/config.d/01_gwms_factory_collectors.config
%config(noreplace) %{_sysconfdir}/condor/config.d/02_gwms_factory_schedds.config
%config(noreplace) %{_sysconfdir}/condor/privsep_config
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_glideins2
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_glideins3
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_glideins4
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_glideins5

%files usercollector
%config(noreplace) %{_sysconfdir}/condor/config.d/01_gwms_collectors.config
%config(noreplace) %{_sysconfdir}/condor/config.d/01_gwms_ganglia.config
%config(noreplace) %{_sysconfdir}/condor/config.d/11_gwms_secondary_collectors.config
%config(noreplace) %{_sysconfdir}/condor/ganglia.d/01_gwms_metrics.config

%files userschedd
%config(noreplace) %{_sysconfdir}/condor/config.d/02_gwms_schedds.config
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_jobs2

%files libs
%{python_sitelib}/glideinwms/__init__.py
%{python_sitelib}/glideinwms/__init__.pyc
%{python_sitelib}/glideinwms/__init__.pyo
%{python_sitelib}/glideinwms/lib

%files glidecondor-tools
%attr(755,root,root) %{_sbindir}/glidecondor_addDN
%attr(755,root,root) %{_sbindir}/glidecondor_createSecSched
%attr(755,root,root) %{_sbindir}/glidecondor_createSecCol

%files minimal-condor
%config(noreplace) %{_sysconfdir}/condor/config.d/00_gwms_general.config
%config(noreplace) %{_sysconfdir}/condor/config.d/90_gwms_dns.config

%files condor-common-config
%config(noreplace) %{_sysconfdir}/condor/config.d/03_gwms_local.config
%config(noreplace) %{_sysconfdir}/condor/certs/condor_mapfile

%changelog
* Thu Oct 08 2015 Matyas Selmeci <matyas@cs.wisc.edu> - 3.2.11.2-4
- Don't put collectors behind shared port (needed for HTCondor 8.4.0) (SOFTWARE-2015)

* Mon Oct 05 2015 Carl Edquist <edquist@cs.wisc.edu> - 3.2.11.2-2
- Repartition subpackages to avoid overlapping files (SOFTWARE-2015)

* Fri Sep 18 2015 Parag Mhashilkar <parag@fnal.gov> - 3.2.11.2-1
- Glideinwms v3.2.11.2 release
- Release Notes: http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/doc.v3_2_11_2/history.html

* Wed Sep 02 2015 Parag Mhashilkar <parag@fnal.gov> - 3.2.11.1-1
- Glideinwms v3.2.11.1 release
- Release Notes: http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/doc.v3_2_11_1/history.html

* Thu Aug 20 2015 Parag Mhashilkar <parag@fnal.gov> - 3.2.11-1
- Glideinwms v3.2.11 release
- Release Notes: http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/doc.v3_2_11/history.html

* Thu Aug 13 2015 Parag Mhashilkar <parag@fnal.gov> - 3.2.11-0.2.rc2
- Glideinwms v3.2.11 rc2 release
- Release Notes: http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/doc.v3_2_11/history.html

* Wed Aug 12 2015 Parag Mhashilkar <parag@fnal.gov> - 3.2.11-0.1.rc1
- Glideinwms v3.2.11 rc1 release
- Release Notes: http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/doc.v3_2_11/history.html

* Thu Jul 16 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.2.10-1.1.osg
- vofrontend-standalone: Replace osg-client dep with most of osg-client's
  contents (except the networking stuff), since osg-client has been dropped in
  OSG 3.3

* Mon Jun 01 2015 Parag Mhashilkar <parag@fnal.gov> - 3.2.10-1
- Glideinwms v3.2.10 release
- Release Notes: http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/doc.prd/history.html

* Fri May 08 2015 Parag Mhashilkar <parag@fnal.gov> - 3.2.9-1
- Glideinwms v3.2.9 release
- Release Notes: http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/doc.prd/history.html

* Thu May 07 2015 Parag Mhashilkar <parag@fnal.gov> - 3.2.9-0.2.rc2
- Glideinwms v3.2.9 rc2 release

* Fri Apr 24 2015 Parag Mhashilkar <parag@fnal.gov> - 3.2.9-0.1.rc1
- Glideinwms v3.2.9 rc1 release

* Tue Dec 30 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.8-1
- Glideinwms v3.2.8 release

* Mon Dec 29 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.8-0.2.rc1
- Fixed install location of 01_gwms_metrics.config to /etc/condor/ganglia.d

* Mon Dec 22 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.8-0.1.rc1
- Glideinwms v3.2.8 rc1 release

* Wed Nov 6 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.7.2-1
- Glideinwms v3.2.7.2 release
- Sets MASTER.USE_SHARED_PORT in schedd's config to support HTCondor v8.2.3

* Wed Nov 5 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.7.1-1
- Glideinwms v3.2.7.1 release

* Tue Oct 14 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.7-1
- Glideinwms v3.2.7 release

* Mon Oct 8 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.7-0.2.rc2
- Glideinwms v3.2.7 rc2 release

* Mon Oct 6 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.7-0.1.rc1
- Glideinwms v3.2.7 rc1 release
- Disabled secondarsy schedd in the frontend configuration
- Added python-ldap as dependency to glideinwms-libs and glideinwms-factory

* Fri Jul 25 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.6-1
- Glideinwms v3.2.6 release

* Fri Jul 25 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.6-0.3.rc3
- Glideinwms v3.2.6 rc3 release
- Reverted group name in default dir ownership but we now explicitly make gfactory and fronend users part of the gfactory and frontend group respectively

* Fri Jul 18 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.6-0.2.rc2
- Glideinwms v3.2.6 rc2 release

* Wed Jul 9 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.6-0.1.rc1
- Glideinwms v3.2.6 rc1 release
- Removed the group name in the default dir ownership for factory and frontend

* Wed Jun 25 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.5.1-2
- Added GOC factory info in the factory config template

* Mon Jun 23 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.5.1-1
- Glideinwms v3.2.5.1 release

* Mon May 19 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.5-1
- Glideinwms v3.2.5 release

* Tue May 13 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.5-0.3.rc3
- Glideinwms v3.2.5 rc3 release

* Mon May 5 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.5-0.2.rc2
- Glideinwms v3.2.5 rc2 release

* Fri May 2 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.5-0.1.rc1
- Glideinwms v3.2.5 rc1 release
- Change the default trust_domain in frontend.xml from OSG to grid

* Mon Apr 28 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.4-3
- Fix the ownership of startup.log file for frontend in post script
- Changed the javascriptrrd dependency to be 1.1.0+ for frontend as well

* Mon Apr 16 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.4-2
- Changed the javascriptrrd dependency to be 1.1.0+

* Mon Apr 14 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.4-1
- Glideinwms v3.2.4 release
- Unified the factory and frontend startup scripts in rpm and tarball versions from common templates

* Mon Feb 03 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.3-1
- Glideinwms v3.2.3 release
- Final release does not include support for HTCondor CE rsl

* Wed Jan 22 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.3-0.3.rc3
- Support for HTCondor CE rsl and improvements to Frontend

* Wed Jan 15 2014 Parag Mhashilkar <parag@fnal.gov> - 3.2.3-0.2.rc2
- Bug fixes to factory log cleanup

* Tue Dec 17 2013 Parag Mhashilkar <parag@fnal.gov> - 3.2.3-0.1.rc1
- New features and bug fixes
- Added clone_glidein tool

* Mon Oct 28 2013 Parag Mhashilkar <parag@fnal.gov> - 3.2.1-0.1.rc2
- Added gwms-frontend and gwms-factory files in /etc/sysconfig in the respective rpms
- Added new files, xslt.* to the list for respective rpms

* Thu Oct 10 2013 Parag Mhashilkar <parag@fnal.gov> - 3.2.0-3
- Changed Requires (dependencies) to insure that the entire set of glideinwms rpms is updated as a set.

* Thu Oct 10 2013 Parag Mhashilkar <parag@fnal.gov> - 3.2.0-2
- Fixed the NVR int the rpm version as per the convention

* Mon Sep 09 2013 John Weigand <weigand@fnal.gov> - 2.7.2-0.1.rc3
- No code changes from rc2. Just a change to Requires (dependencies) to insure that the entire set of glideinwms rpms is updated as a set.

* Mon Aug 26 2013 Parag Mhashilkar <parag@fnal.gov> - 3.2-0.2.rc2
- Updated the frontend.xml and added update_proxy.py while generating the checksum for the version

* Mon Aug 26 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.2-0.1.rc2
- Add update_proxy.py while generating the checksum for the version

* Wed Jun 5 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.1-1.1
- Check existence of link before creating it to avoid scriptlet error.

* Mon May 13 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.1-0.rc1.4
- Removed libs directory from the vofrontend-standalone and added glideinwms-libs as its dependency.

* Fri May 10 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.1-0.rc1.3
- Reverted the changes made in 2.7.1-0.rc1.2. Removed condor_q as a requirement whereever we require condor as this creates more conflicts.

* Thu May 9 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.1-0.rc1.2
- Added condor_q as a requirement whereever we require condor to force same dependecny behavior in RHEL 5 and 6

* Wed May 8 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.1-0.rc1.1
- Added 11_gwms_secondary_collectors to respective condor rpms and glidecondor_addSecCol to the tools rpm

* Fri Apr 29 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.0-0.4
- Added missing glideinwms/__init__ to the glideinwms-libs.

* Fri Apr 26 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.0-0.3
- Further refactoring of packages.
- Added new packages glideinwms-glidecondor-tools and its dependancy glideinwms-libs
- Removed files provided by glideinwms-minimal-condor from file list of glideinwms-usercollector and glideinwms-userschedd and make usercollector and userschedd depend on the minimal-condor

* Fri Apr 26 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.0-0.2
- Added glidecondor_addDN to factory, vofrontend-standalone, minimal-condor, userschedd, usercollector packages

* Tue Apr 2 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.0-0.0
- Added missing library files creation/lib/__init__ to the frontend rpm

* Wed Feb 20 2013 Parag Mhashilkar <parag@fnal.gov> - 2.7.0-0.rc1.0
- Updated the checksum creation to sort the info
- Changes to file list based on the python libraries

* Fri Jan 4 2013 Doug Strain <dstrain@fnal.gov> - 2.6.3-0.rc2.6
- Update to 2.6.3 rc2 release candidate
- Adding factory tools scripts and their python libraries
- Adding condor_create_tarball
- Adding frontend/factory index page.

* Thu Nov 8 2012 Doug Strain <dstrain@fnal.gov> - 2.6.2-2
- Improvements recommended by Igor to modularize glideinwms

* Wed Nov 2 2012 Doug Strain <dstrain@fnal.gov> - 2.6.2-1
- Glideinwms 2.6.2 Release

* Thu Sep 20 2012 Doug Strain <dstrain@fnal.gov> - 2.6.1-2
- Added GRIDMANAGER_PROXY_REFRESH_TIME to condor config

* Mon Aug 20 2012 Doug Strain <dstrain@fnal.gov> - 2.6.1-0.rc2
- Added JOB_QUEUE_LOG to the schedd condor configs
- updated to 2.6.1 release candidate

* Fri Aug 3 2012 Doug Strain <dstrain@fnal.gov> - 2.6.0-3
- Updating to new release 
- Changing the schedd configs to work with both wisc and osg condor rpms

* Wed Jun 13 2012 Doug Strain <dstrain@fnal.gov> - 2.6.0-rc1
- Updating to new release candidate

* Fri Apr 27 2012 Doug Strain <dstrain@fnal.gov> - 2.5.7-4
- Changed ownership of frontend.xml to frontend user
- Changed ownership of glideinwms.xml to gfactory user
- This allows writeback during upgrade reconfigs

* Fri Apr 27 2012 Doug Strain <dstrain@fnal.gov> - 2.5.7-3
- Changed frontend init.d script to reconfig as frontend user

* Mon Apr 9 2012 Doug Strain <dstrain@fnal.gov> - 2.5.7-2
- Updating sources for v2.5.7
- Splitting DAEMON LIST to appropriate config files

* Fri Mar 16 2012 Doug Strain <dstrain@fnal.gov> - 2.5.6-1
- Updating sources for v2.5.6

* Tue Feb 21 2012 Doug Strain <dstrain@fnal.gov> - 2.5.5-7alpha
- Adding factory RPM and v3 support
- Updating to also work on sl7
- Also added support for v3.0.0rc3 with optional define

* Thu Feb 16 2012 Doug Strain <dstrain@fnal.gov> - 2.5.5-1 
- Updating for v2.5.5 

* Tue Jan 10 2012 Doug Strain <dstrain@fnal.gov> - 2.5.4-7
- Adding condor_mapfile to minimal

* Mon Jan 9 2012 Doug Strain <dstrain@fnal.gov> - 2.5.4-6
- Changing directories per Igors request
-- changing directories to /var/lib
- Splitting condor config into separate package
- Fixing web-area httpd

* Thu Jan 5 2012 Doug Strain <dstrain@fnal.gov> - 2.5.4-2
- Updating for 2.5.4 release source and fixing eatures for BUG2310
-- Split directories so that the web area is in /var/www

* Thu Dec 29 2011 Doug Strain <dstrain@fnal.gov> - 2.5.4-1
- Using release source and fixing requested features for BUG2310
-- Adding user/group correctly
-- Substituting hostname name automatically

* Fri Dec 09 2011 Doug Strain <dstrain@fnal.gov> - 2.5.4-0.pre2
- Added glidecondor_addDN to vofrontend package

* Thu Nov 10 2011 Doug Strain <dstrain@fnal.gov> - 2.5.4-0.pre1 
- Update to use patched 2.5.3 
- Pushed patches upstream
- Made the package glideinwms with subpackage vofrontend

* Thu Nov 10 2011 Doug Strain <dstrain@fnal.gov> - 2.5.3-3
- Update to 2.5.3
- Updated condor configs to match ini installer
- Updated frontend.xml to not check index.html
- Updated init script to use "-xml" flag

* Mon Oct 17 2011 Burt Holzman <burt@fnal.gov> - 2.5.2.1-1
- Update to 2.5.2.1

* Tue Sep 06 2011 Burt Holzman <burt@fnal.gov> - 2.5.2-5
- Fix reference to upstream tarball

* Tue Sep 06 2011 Burt Holzman <burt@fnal.gov> - 2.5.2-4
- Add RPM to version number in ClassAd

* Tue Sep 06 2011 Burt Holzman <burt@fnal.gov> - 2.5.2-3
- Fixed glideinWMS versioning advertisement

* Wed Aug 31 2011 Burt Holzman <burt@fnal.gov> - 2.5.2-2
- Fixed file location for frontend_support.js

* Wed Aug 13 2011 Burt Holzman <burt@fnal.gov> - 2.5.2-1
- Update to glideinWMS 2.5.2

* Tue Aug 02 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 2.5.1-13
- Made vdt-repo compatible

* Tue Apr 05 2011 Burt Holzman 2.5.1-10
- Update frontend_startup script to better determine frontend name
- Move user-editable configuration items into 02_frontend-local.config

* Tue Mar 22 2011 Derek Weitzel 2.5.1-8
- Change condor config file name to 00_frontend.config
- Separated definition of collectors into 01_collectors.config

* Fri Mar 11 2011 Burt Holzman 	 2.5.1-1
- Include glideinWMS 2.5.1
- Made all the directories independent of the frontend name

* Mon Mar 10 2011 Derek Weitzel  2.5.0-11
- Changed the frontend.xml to correct the web stage directory

* Mon Mar 10 2011 Derek Weitzel  2.5.0-9
- Made the work, stage, monitor, and log directory independent of the frontend name.
- Frontend name is now generated at install time

* Mon Feb 13 2011 Derek Weitzel  2.5.0-6
- Made rpm noarch
- Replaced python site-packages more auto-detectable

* Mon Feb 09 2011 Derek Weitzel  2.5.0-5
- Added the tools to bin directory

* Mon Jan 24 2011 Derek Weitzel  2.5.0-4
- Added the tools directory to the release

* Mon Jan 24 2011 Derek Weitzel  2.5.0-3
- Rebased to official 2.5.0 release.

* Thu Dec 16 2010 Derek Weitzel  2.5.0-2
- Changed GlideinWMS version to branch_v2_4plus_igor_ucsd1

* Fri Aug 13 2010 Derek Weitzel  2.4.2-2
- Removed port from primary collector in frontend.xml
- Changed GSI_DAEMON_TRUSTED_CA_DIR to point to /etc/grid-security/certificates 
  where CA's are installed.
- Changed GSI_DAEMON_DIRECTORY to point to /etc/grid-security.  This is 
  only used to build default directories for other GSI_* 
  configuration variables.
- Removed the rm's to delete the frontend-temp and log directories at uninstall,
  they removed files when updating, not wanted.  Let RPM handle those.

