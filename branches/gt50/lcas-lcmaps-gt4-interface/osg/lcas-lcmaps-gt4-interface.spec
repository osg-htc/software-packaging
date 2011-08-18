Summary: Mapping interface between Globus Toolkit and LCAS/LCMAPS
Name: lcas-lcmaps-gt4-interface
Version: 0.1.4
Release: 2%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: Applications/System
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
Source1: gsi-authz.conf.in
Patch0: lcas_lcmaps_gt4_interface_nochangeuser.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: globus-core
BuildRequires: globus-common-devel
BuildRequires: globus-gridmap-callout-error-devel
BuildRequires: globus-gsi-callback-devel
BuildRequires: globus-gsi-credential-devel
BuildRequires: globus-gsi-proxy-core-devel
BuildRequires: globus-gssapi-error-devel
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: globus-gss-assist-devel
BuildRequires: lcas-devel, lcmaps-devel
BuildRequires: openssl-devel

# explicit requires as these are dlopen'd
Requires: lcas, lcmaps

%description

This interface extends the basic map-file based mapping capabilities of the
Globus Toolkit to use the full LCAS/LCMAPS pluggable framework, which includes
pool accounts and VOMS attribute based decisions and mappings.

%prep
%setup -q
%patch0 -p0

%build

CFLAGS="${CFLAGS:-%optflags} -I%{_libdir}/globus/include" ; export CFLAGS ;
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Install the mapping by default
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-security
sed -e "s#@LIBDIR@#%{_libdir}#" %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/gsi-authz.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc doc/README AUTHORS LICENSE 
%{_libdir}/liblcas_lcmaps_gt4_mapping.so
%{_libdir}/liblcas_lcmaps_gt4_mapping.so.0
%{_libdir}/liblcas_lcmaps_gt4_mapping.so.0.0.0
%{_sbindir}/gt4-interface-install.sh
%config(noreplace) %{_sysconfdir}/grid-security/gsi-authz.conf

%changelog
* Thu Jul 21 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.1.4-2
- Added default gsi-authz.conf

* Thu Jun 30 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.1.4-1
- Updated to version 0.1.4

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.1.2-1
- Fixed globus dependencies
- Added openssl dependency

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.1.1-3
- added ldconfig post(un) script
- disable static libraries

* Fri Feb 25 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


