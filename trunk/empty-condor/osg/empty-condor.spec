Name:           empty-condor
Version:        1.1
Release:        2%{?dist}
Summary:        An empty Condor package

Group:          Applications/System
License:        Unknown
URL:            http://vdt.cs.wisc.edu

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# This fulfills depenendencies for most OSG packages that depend on Condor
Provides:       condor
Conflicts:      /usr/sbin/condor_master

# These fulfill dependencies for glexec, specifically lcmaps-plugins-glexec-tracking
# so that people can use their own Condor install and still install osg-wn-client-glexec
Provides:       /usr/sbin/condor_procd
Provides:       /usr/sbin/gidd_alloc
Provides:       /usr/sbin/procd_ctl

%description

This pacakge is empty (it provides no files), but it claims to provide all of
Condor. This allows users to install Condor with a different mechanism 
(such as from a binary tarball or built from source), and fake out RPM so that it 
believes that Condor has been installed via RPM. 

%prep

%build

%install

%clean

%files

%doc

%changelog
* Tue Aug 28 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1-2
- Conflict with /usr/sbin/condor_master to avoid having this being installed
  alongside a real RPM Condor.

* Mon Aug 6 2012 Alain Roy <roy@cs.wisc.edu> - 1.1-1
- Added more provides clauses so this works with glexec-tracking plugin for lcmaps 

* Mon Jan 30 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-3
- Removing conflict with condor

* Mon Jan 30 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-2
- Adding conflict with RPM based Condor

* Thu Nov 17 2011 Alain Roy <roy@cs.wisc.edu> - 1.0-1
- Initial version
