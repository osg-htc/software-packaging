Name:           vo-client
Version:        43
Release:        2%{?dist}
Summary:        Contains vomses file for use with user authentication and edg-mkgridmap.conf file that contains configuration information for edg-mkgridmap.

Group:          System Environment/Base
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/osg/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       grid-certificates

Source0:        %{name}-%{version}-osg.tar.gz

# Tim's note, 1 November 2012: The process below is probably broken and needs to
# be completely revised; see package README.
# ------------------------------------------------------------------------------
# Steps to make tarball (correctly packaged):
# Get GOC's tarball, vo-client-40.tar.gz
# tar xzf vo-client-40.tar.gz
# cp vomses ./
# cp edg-mkgridmap.conf ./

# Copy over old LSC files form previous tarball. 

# Generate LSC files for new or changed VOs
# /usr/sbin/osg-make-vomsdir --vomsdir vomsdir --vomses vomses --vo VO


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


