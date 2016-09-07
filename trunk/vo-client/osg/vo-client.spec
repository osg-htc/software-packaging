Name:           vo-client
Version:        68
Release:        1%{?dist}
Summary:        Contains vomses file for use with user authentication and edg-mkgridmap.conf file that contains configuration information for edg-mkgridmap.

Group:          System Environment/Base
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/osg/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires: grid-certificates >= 7

Source0:        %{name}-%{version}-osg.tar.gz

# See
# https://www.opensciencegrid.org/bin/view/SoftwareTeam/CreateVOClient
# for instructions


%description
%{summary}

%package edgmkgridmap
Summary:	edg-mkgridmap.conf file that contains configuration information for edg-mkgridmap
Group:          system environment/base
Provides:       vo-client-edgmkgridmap = %{version}-%{release}
Provides:       osg-edg-mkgridmap-config = %{version}-%{release}
#Requires:       %{name} = %{version}-%{release}

%description edgmkgridmap
%{summary}


%package -n osg-gums-config
Summary:        a file that contains a template configuration for the gums service
Group:          system environment/base
Requires:       gums-service

%description -n osg-gums-config
%{summary}
Running /usr/bin/gums-create-config on the template
(in %{_sysconfdir}/gums/gums.config.template) will create a usable
configuration file.

%prep

%build


%install
rm -rf $RPM_BUILD_ROOT
tar -xz -C $RPM_BUILD_DIR --strip-components=1 -f %{SOURCE0}
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
mv $RPM_BUILD_DIR/vomses $RPM_BUILD_ROOT/%{_sysconfdir}/
mv $RPM_BUILD_DIR/edg-mkgridmap.conf $RPM_BUILD_ROOT/%{_sysconfdir}/

chmod 644 $RPM_BUILD_ROOT/%{_sysconfdir}/vomses $RPM_BUILD_ROOT/%{_sysconfdir}/edg-mkgridmap.conf

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/
mv $RPM_BUILD_DIR/vomsdir $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/
find $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/vomsdir -type f -exec chmod 644 {} \;
find $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/vomsdir -type d -exec chmod 755 {} \;

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/gums/
mv $RPM_BUILD_DIR/gums.config.template $RPM_BUILD_ROOT/%{_sysconfdir}/gums/gums.config.template
chmod 600 $RPM_BUILD_ROOT/%{_sysconfdir}/gums/gums.config.template


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/vomses
%config(noreplace) %{_sysconfdir}/grid-security/vomsdir

%files edgmkgridmap
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/edg-mkgridmap.conf

%files -n osg-gums-config
%defattr(-,root,root,-)
%attr(0600,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/gums/gums.config.template

%changelog
* Wed Sep 07 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 68-1
- Update to vo-client 68 (SOFTWARE-2445)
  - Added project8

* Mon Jul 25 2016 Carl Edquist <edquist@cs.wisc.edu> - 67-1
- Corrected edg-mkgridmap.config for ILC (SOFTWARE-2402)

* Wed May 04 2016 Carl Edquist <edquist@cs.wisc.edu> - 66-1
- Update to vo-client 66 (SOFTWARE-2316)
  - LZ, DREAM, CIGI, SURAGRID Update to CILogon
  - OSG IU VOMS Removal
  - COMPBIOGRID Removal
  - NEES VO Removal

* Fri Apr 01 2016 Carl Edquist <edquist@cs.wisc.edu> - 65-2
- Update DN/CA for osg/voms1.opensciencegrid.org (SOFTWARE-2265)

* Thu Mar 31 2016 Carl Edquist <edquist@cs.wisc.edu> - 65-1
- Update to vo-client 65 (SOFTWARE-2265)
  - Added SuperCDMS VO
  - Update HCC & GLOW DNs
  - Update 11 voms1.fnal.gov DNs

* Mon Feb 22 2016 Carl Edquist <edquist@cs.wisc.edu> - 64-1
- Update to vo-client 64 (SOFTWARE-2218)
  - New VOMS servers DNs for DOSAR, SBGrid, NYSGRID

* Fri Jan 29 2016 Carl Edquist <edquist@cs.wisc.edu> - 63-1
- Update to vo-client 63 (SOFTWARE-2186)
  - Drop UC3 and osgcrossce VOs
  - Transition OSG VO to CILogon OSG CA
  - Change DN of VOMS servers for Star, Gluex, MIS, & osgedu VOs

* Mon Jan 11 2016 Carl Edquist <edquist@cs.wisc.edu> - 62-2
- Update FNAL VOMS Server CA (SOFTWARE-2154)

* Wed Jan 06 2016 Carl Edquist <edquist@cs.wisc.edu> - 62-1
- Update to vo-client 62 (SOFTWARE-2154)
  - Update FNAL VOMS Server DN
  - Drop LIGO VO

* Fri Aug 07 2015 Carl Edquist <edquist@cs.wisc.edu> - 61-1
- Update to vo-client 61 (SOFTWARE-1993)
  - Added DUNE VO

* Tue Jul 07 2015 Carl Edquist <edquist@cs.wisc.edu> - 60-1
- Update to vo-client 60 (SOFTWARE-1967)
  - Added LZ VO

* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 59-2
- Require grid-certificates >= 7 (SOFTWARE-1883)

* Fri May 15 2015 Carl Edquist <edquist@cs.wisc.edu> - 59-1
- Update to vo-client 59 (SOFTWARE-1747)
  - Restructured/removed various Fermilab entries from gums template
  - Removed ATLAS VOMS server vo.racf.bnl.gov
  - Removed GPN, Superbvo VOs
  - Updated nysgrid VOMS address to NYSGRID

* Thu Dec 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 58-3
- Fix https:/// in url (SOFTWARE-1711)

* Thu Dec 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 58-2
- Bring .lsc files up to date (SOFTWARE-1711)

* Wed Dec 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 58-1
- Update to vo-client 58 (SOFTWARE-1711)
  - Added Fermilab Analysis Role
  - Removed all old CERN VOMS addresses
  - Replaced old {lcg-,}voms.cern.ch with {lcg-,}voms2.cern.ch

* Thu Nov 06 2014 Carl Edquist <edquist@cs.wisc.edu> - 57-1
- Update to vo-client 57 (SOFTWARE-1657)
  - Switched voms.cern.ch to voms2.cern.ch
  - Vomses additions for atlas, cms, alice, ops, geant4

* Mon Aug 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 56-1
- Update to vo-client 56 (SOFTWARE-1562)
  - Remove I2U2 VO
  - Remove (lcg-)voms2.cern.ch servers for atlas & cms

* Tue Jul 01 2014 Carl Edquist <edquist@cs.wisc.edu> - 55-1
- Update to vo-client 55 (SOFTWARE-1528)
  - Add snoplus.snolab.ca VO
  - Remove Engage VO
  - Cleanup:
    - Update all outdated LSC files (including dosar)
    - Fix DN mismatches in vomses
    - Remove old LSC files no longer in vomses

* Fri May 23 2014 Carl Edquist <edquist@cs.wisc.edu> - 54-1
- Update to vo-client 54 (SOFTWARE-1491)
  - Add missing LSC files for voms2.cern.ch and lcg-voms2.cern.ch

* Thu May 08 2014 Carl Edquist <edquist@cs.wisc.edu> - 53-1
- Update to vo-client 53 (SOFTWARE-1473)
  - Modify CMS VOMS Address in GUMS Template
  - Modify ILC VOMS Address in GUMS Template and vomses file
  - Modify CompBioGrid vomses entry

* Mon Feb 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 52-1
- Update to vo-client 52 (SOFTWARE-1444)
  - Add New Sub-VOs Lariat, Gendetrd, Lar1, and Okra
  - New stanzas for Production Analysis and Glidein roles in gums template
  - New VOMS Servers at CERN
  - Removed Dayabay VO

* Mon Feb 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 51-1
- Update to vo-client 51 (SOFTWARE-1372)
  - VOs hosted by Fermilab VOMS server transitioned to DigiCert certificates
  - voms.fnal.gov was replaced by voms1/2.fnal.gov
  - voms.opensciencegrid.org replaced by voms1/2.opensciencegrid.org
  - Reference to GOC VOMS server corrected in gums template
  - SBGrid LSC file updated for new DigiCert certificate

* Fri Jan 10 2014 Carl Edquist <edquist@cs.wisc.edu> - 50-2
- Remove trailing slash from atlas/ in edg-mkgridmap.conf (SOFTWARE-1344)

* Tue Jan 07 2014 Carl Edquist <edquist@cs.wisc.edu> - 50-1
- Update to vo-client 50 (SOFTWARE-1344)
  - Add vo.cta.in2p3.fr VO
  - Add xenon-biggrid.nl VO
  - OSGCrossCE Configuration Change

* Wed Nov 06 2013 Carl Edquist <edquist@cs.wisc.edu> - 49-1
- Update to vo-client 49 (SOFTWARE-1248)

* Fri Oct 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 48-1
- Update to vo-client 48 (SOFTWARE-1216)

* Tue Sep 03 2013 Brian Lin <blin@cs.wisc.edu> - 47-1
- Updated to vo-client 47:
  - Add OSG Cross CE VO
  - Change SBGrid VOMS Certificate
  - Change GLOW VOMS Certificate

* Fri Aug 02 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 46-1
- Updated to vo-client 46:
  - Remove NWICG VO
  - Add ENMR VO
  - Add Darkside VO
  - Change VOMS URL for NYSGRID
  - Add production role for Belle VO

* Tue Jul 02 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 45-1
- Updated to vo-client v45:
  - Add GLAST VO
  - Add Auger VO
  - Remove NEBioGrid VO

* Fri Mar 29 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 44-1
- Updated to vo-client v44.

* Thu Nov 01 2012 Tim Cartwright <cat@cs.wisc.edu> - 43-2
- Swapped in the gums.config.template file from John Weigand (see SOFTWARE-824).

* Tue Oct 30 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 43-1
- Updated to vo-client v43.

* Tue Jul 17 2012 Alain Roy <roy@cs.wisc.edu> - 42-2
- Fixed LSC file for OSG VO.

* Mon Jun 18 2012 Alain Roy <roy@cs.wisc.edu> - 42-1
- Updated to vo-client v42. Fixed LSST GUMS template and added COUPP sub-vo.

* Tue Apr 24 2012 Alain Roy <roy@cs.wisc.edu> - 41-3
- Adjusted VOMS server URLs for default GUMS config to work with latest GUMS. 

* Mon Apr 23 2012 Alain Roy <roy@cs.wisc.edu> - 41-2
- Fixed LSST URL

* Wed Mar 18 2012 Alain Roy <roy@cs.wisc.edu> - 41-1
- Updated to match GOC's new v41 release. 
- Added lsst 
- Updated VOMS hostname for Alice

* Wed Mar 14 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 40-4
- osg-edg-mkgridmap-config renamed back to vo-client-edgmkgridmap to solve yum dependency resolution issues.

* Wed Mar 07 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 40-3
- Rename vo-client-edgmkgridmap to osg-edg-mkgridmap-config; remove vo-client dependency
- Add osg-gums-config

* Thu Nov 10 2011 Alain Roy <roy@cs.wisc.edu> - 40-2
- Fixed LSC file for LIGO

* Thu Oct 27 2011 Alain Roy <roy@cs.wisc.edu> - 40-1
- Updated to version 40 of the vo-client. Adds lbne & alice

* Wed Aug 10 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 38-8
- Depend on virtual dependency grid-certificates, not specific package.

* Wed Aug 03 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-7
- Fixed engage's lsc file

* Fri Jul 22 2011 Igor Sfiligoi <isfiligoi@ucsd.edu> - 38-6
- Change RPM to extract directly from the upstream tarball
- Expect the vomsdir to be in the upstream tarball

* Thu Jul 21 2011 Neha Sharma <neha@fnal.gov> - 38-5
- Modified the directory structure. Only needs files at top level

* Wed Jul 20 2011 Neha Sharma <neha@fnal.gov> - 38-4
- Added vo-client-edgmkgridmap

* Tue Jul 19 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-3
- Removed vdt-make-vomsdir.  It now has it's own rpm

* Mon Jul 18 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-2
- Added vdt-make-vomsdir and cleaned up packaging

* Fri Jul 15 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-1
- Initial build of vo-client


