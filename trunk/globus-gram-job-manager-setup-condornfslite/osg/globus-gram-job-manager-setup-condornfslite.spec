%{!?perl_vendorlib: %global perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)}

Name:           globus-gram-job-manager-setup-condornfslite
Version:        2.0.0
Release:        2%{?dist}
Summary:        Globus Toolkit - Condor NFS lite Job Manager Setup

Group:          Applications/Internet
BuildArch:      noarch
License:        ASL 2.0
URL:            http://www.globus.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source:		Globus-CondorNFSLite-Setup.tar.gz
Patch0:         default_locs.patch

Requires:       globus-gram-job-manager-scripts
Requires:       globus-gass-cache-program >= 2
Requires:       globus-common-setup >= 2
Requires:       globus-gram-job-manager >= 10.59
#BuildRequires:  grid-packaging-tools
#BuildRequires:  globus-core

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world.   This package augments the condor job manager
to use a modified light-weight NFS implementation to share information for
jobs (stdout, stderr, etc).

%prep
%setup -q -n Globus-CondorNFSLite-Setup
%patch0 -p0

%build
#Patch jobmanager file

sed -i "s/MAGIC_VDT_LOCATION\/globus\/libexec/\/usr\/sbin/" globus/etc/grid-services/jobmanager-condornfslite
sed -i "s/MAGIC_VDT_LOCATION\/globus\/etc/\/etc/" globus/etc/grid-services/jobmanager-condornfslite


%install

#Documentation
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 notes.html $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/
install -m 644 globus/lib/perl/Globus/GRAM/JobManager/condornfslite.pm $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/
install -m 755 globus/lib/perl/Globus/GRAM/JobManager/condor_nfslite_job_wrapper.sh $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/globus
install -m 644 globus/share/globus_gram_job_manager/condornfslite.rvf $RPM_BUILD_ROOT%{_datadir}/globus

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-services
install -m 755 globus/etc/grid-services/jobmanager-condornfslite $RPM_BUILD_ROOT%{_sysconfdir}/grid-services/

%files
%{_datadir}/globus/condornfslite.rvf
%{perl_vendorlib}/Globus/GRAM/JobManager/condornfslite.pm
%{perl_vendorlib}/Globus/GRAM/JobManager/condor_nfslite_job_wrapper.sh
%{_docdir}/%{name}-%{version}/notes.html
%{_sysconfdir}/grid-services/jobmanager-condornfslite

