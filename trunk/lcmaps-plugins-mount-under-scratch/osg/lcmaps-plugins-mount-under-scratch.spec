Summary: LCMAPS plugin for creating scratch directories for glexec
Name: lcmaps-plugins-mount-under-scratch
Version: 0.0.4
Release: 1%{?dist}
License: Public Domain
Group: System Environment/Libraries

# git clone https://github.com/lcmaps-plugins/lcmaps-plugins-mount-under-scratch.git
# cd lcmaps-plugins-mount-under-scratch
# ./bootstrap
# ./configure
# make dist
# cp lcmaps-plugins-mount-under-scratch-0.0.4.tar.gz ../
# cd .. ; rm -rf lcmaps-plugins-mount-under-scratch
Source0: %{name}-%{version}.tar.gz

BuildRequires: boost-devel
BuildRequires: lcmaps-interface

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This plugin creates temporary directories for the payload process,
giving it a unique /tmp and /var/tmp

%prep
%setup -q

%build

%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/lcmaps/liblcmaps_mount_under_scratch.la
rm $RPM_BUILD_ROOT%{_libdir}/lcmaps/liblcmaps_mount_under_scratch.a
mv $RPM_BUILD_ROOT%{_libdir}/lcmaps/liblcmaps_mount_under_scratch.so \
   $RPM_BUILD_ROOT%{_libdir}/lcmaps/lcmaps_mount_under_scratch.mod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/lcmaps/lcmaps_mount_under_scratch.mod

%changelog
* Fri Jan 27 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.3-1
Fix usage when run in Condor.

* Sun Jan 15 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.2-1
- Fix mounting of /var/tmp.

