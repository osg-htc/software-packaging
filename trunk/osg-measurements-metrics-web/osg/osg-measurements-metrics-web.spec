%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           osg-measurements-metrics-web
Version:        1.2
Release:        9%{?dist}
Summary:        OSG Measurements and Metrics web and database

Group:          Applications/System
License:        Apache 2.0
URL:            http://t2.unl.edu/documentation/gratia_graphs
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-setuptools
Requires:       graphtool >= 0.6.4 
Requires:	MySQL-python 
Requires:	python-sqlite 
Requires:	python-cheetah 
Requires:	/usr/bin/ldapsearch 
Requires:	python-cherrypy >= 3.1.2 
Requires:	python-ZSI 
Requires: 	python-setuptools 
Requires: 	osg-measurements-metrics-db 
%if 0%{?el5}
Requires:	python-simplejson 
%endif
Requires:	gratia-probe-common   
Requires:	gratia-probe-services




%description
GratiaWeb installation package for web

%prep
%setup -q


%build
cp setup/setup_Web.py ./setup.py
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build



%install
rm -rf $RPM_BUILD_ROOT


%{__python} setup.py install --skip-build --root %{buildroot}

install -d %{buildroot}/%{_initrddir}
mv %{buildroot}/etc/init.d/GratiaWeb %{buildroot}/%{_initrddir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/GratiaWeb/*
%config %{_sysconfdir}/wlcg_email.conf.rpmnew
%config %{_sysconfdir}/access.db
%config %{_sysconfdir}/osg_graphs.conf
%{_sysconfdir}/cron.d/*
%{_sysconfdir}/logrotate.d/*
%{_initrddir}/*


%{python_sitelib}/*




%changelog

* Thu Jul 25 2013 William B Hurst <wbhurst@cse.unl.edu>
- Modification made to resolve GOC ticket 15719:
- 'Unable to retrieve transfer data for USCMS-FNAL-WC1-SE'
- file modified: src/gratia/config/generic_queries.xml
- query name modified: 'summary'; change made was to
- remove 'Unknown|unknown' from pre-populated:
- 'exclude-vo' field

* Thu Jul 11 2013 William B Hurst <wbhurst@cse.unl.edu>
- Modifications to resolve GratiaWeb-38 'Disable
- Authentication Warnings': were achieved by commenting
- out /src/gratia/templates files: bysite.tmpl, byvo.tmpl,
- main.tmpl in the initial 'is_authenticated' section

* Wed Jul 10 2013 William B Hurst <wbhurst@cse.unl.edu>
- updated version release to 1.2-7
- Modifications made in response to GratiaWeb-39
- 'Disable Monitoring Pages'. The files touched
- by these changes are src/gratia/web/__init__.py and
- src/gratia/web/navigate.py; then the various
- setup/*.cfg files for the 'release' change.

* Mon Jul 8 2013 William B Hurst <wbhurst@cse.unl.edu>
- updated version release to 1.2-6
- updated config/GratiaWeb
- - GratiaWeb-34: exit 0 --> exit $? 
- updated osg-measurements-metrics-web-spec
- - Requires: python-json --> python-simplejson
- updated setup/setup_Web.cfg 
- - requires = python-jason --> python-simplejson
- updated src/gratia/web/__init__.py
- - GratiaWeb-35: added new function 'NotContainsRegex'
- - and supporting code to use new function to test
- - filter_dict['facility'] & and filter_dict['vo'] 

* Thu Jun 13 2013 William B Hurst <wbhurst@cse.unl.edu>
- updated version release to 1.2-5
- modified gratia_bar_queries.xml and wlcg_reporting.tmpl.
- wlcg_reporting.tmpl was changed to modify column order
- of WLCG plege information reports. The 
- gratia_bar_queries.xml file was modified as first step
- in responding to Gratia REQUEST-56.

* Mon Jun 03 2013 William B Hurst <wbhurst@cse.unl.edu>
- revised apel_url in src/gratia/web/jot_reporting.py and
- src/gratia/web/wlc_reporting.py for accessing data

* Tue May 28 2013 William B Hurst <wbhurst@cse.unl.edu>
- added gratia_reporting.py and jot_reporting.py changes
- exclude-vo = 'Unknown' and kicked up release by one

* Thu May 23 2013 William B Hurst <wbhurst@cse.unl.edu>
- primarily modified code in response to GRATIA-108
- gratia-fix-unknown-vo. A request to revise filter
- exclude-vo to 'Unknown|unknown|other'. The remaining
- changes included small change to wlcg_json_data.py
- implementing simplejson.loads(s).

* Thu May 3 2013 William B Hurst <wbhurst@cse.unl.edu>
- updated changelog

- commit 3e9338c4f40cd220d4fbfe6fcf43cfe313523269
- code modifications to rename and utilize lower case file names 
- for 'osg-measurements-metrics-[db/web].spec' files

* Thu May 2 2013 William B Hurst <wbhurst@cse.unl.edu>
- commit 066c6bdcb64066bd91184e305b10706c43485be2
- modifications made to present a repository version change.

* Thu May 2 2013 William B Hurst <wbhurst@cse.unl.edu>
- commit 84756816b656593e4502689bcc165e1a39736ffa
- (https://jira.opensciencegrid.org/browse/GRATIAWEB-32)
- Modifications made in order to comply with the requested changes 
- specified in Jira GRATIAWEB-32; 
- 1) Create new Campus Page, 
- 2) Copy all graphs Pilot Page, -
- 3) Remove all to campus from original Pilot and Campus accounting page.

* Thu May 2 2013 William B Hurst <wbhurst@cse.unl.edu>
- commit a8365c313de0e2cb722407a42c6c90000c2699de
- (https://jira.opensciencegrid.org/browse/GRATIAWEB-33)
- Changes made in order to comply with jira GRATIAWEB-33 ticket; 
- requesting 'Factory Frontend Accounting' be changed to 'GlideinWMS Monitoring'

* Thu May 2 2013 William B Hurst <wbhurst@cse.unl.edu>
- commit 11bffdc21ac187f385a5461fcfcb86c22cb0caf9
- change made to fix problems with lower case file
- and directory names that led to installation failure.

* Mon Feb 18 2013 Ashu Guru <aguru2@unl.edu>
- Added the Under Construction and BatchPilot 
- (https://jira.opensciencegrid.org/browse/GRATIAWEB-28)

* Thu Jan 10 2013 Derek Weitzel <dwetizel@cse.unl.edu> - 1.1-4
- Fixing initrd dir

* Thu Jan 10 2013 Derek Weitzel <dweitzel@cse.unl.edu> - 1.1-3
- Fixing sysconfdir in the spec file

* Thu Jan 10 2013 Derek Weitzel <dwetizel@cse.unl.edu> - 1.1-2
- Updating datarootdir to multi-platform version datadir

* Thu Jan 10 2013 Derek Weitzel <dweitzel@cse.unl.edu> - 1.1-1
- Update to 1.1

* Mon Jun 28 2012 Ashu Guru <aguru2@unl.edu>
- Updated for gratia_data.cron emitting error email on gratiaweb-itb.grid.iu.edu
- (https://jira.opensciencegrid.org/browse/SOFTWARE-684)

* Mon Jun 28 2012 Ashu Guru <aguru2@unl.edu>
- Updated for fixing number of days in pie chart
- (https://jira.opensciencegrid.org/browse/GRATIAWEB-17)

* Mon May 31 2012 Ashu Guru <aguru2@unl.edu>
- Updated for fixing the number of bins and days of bar chart report issue
- (https://jira.opensciencegrid.org/browse/GRATIAWEB-17)

* Thu Apr 5 2012 Ashu Guru <aguru2@unl.edu>
- Top Pull Downs on the Gratia Web Interface 
- (http://jira.opensciencegrid.org/browse/GRATIAWEB-14)

* Wed Apr 4 2012 Ashu Guru <aguru2@unl.edu>
- Gratia/WLCG interface/reporting of Tier1/2 sites changes required due to new APEL SSM interface 
- (https://jira.opensciencegrid.org/browse/METRICS-10)

