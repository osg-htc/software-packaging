%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%if "%{?rhel}" == "5"
%global docdiroption "with-docdir"
%else
%global docdiroption "docdir"
%endif

Name:		globus-gsi-cert-utils
%global _name %(tr - _ <<< %{name})
Version:	7.2
Release:	2%{?dist}
Summary:	Globus Toolkit - Globus GSI Cert Utils Library

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.2/installers/src/gt5.0.2-all-source-installer.tar.bz2
#		tar -jxf gt5.0.2-all-source-installer.tar.bz2
#		mv gt5.0.2-all-source-installer/source-trees/gsi/cert_utils/source globus_gsi_cert_utils-6.6
#		cp -p gt5.0.2-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gsi_cert_utils-6.6
#		tar -zcf globus_gsi_cert_utils-6.6.tar.gz globus_gsi_cert_utils-6.6
Source:		%{_name}-%{version}.tar.gz
#		This is a workaround for the broken epstopdf script in RHEL5
#		See: https://bugzilla.redhat.com/show_bug.cgi?id=450388
Source9:	epstopdf-2.9.5gw
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	openssl%{?_isa}
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-common-devel%{?_isa} >= 3
BuildRequires:	globus-openssl-module-devel%{?_isa}
BuildRequires:	globus-gsi-openssl-error-devel%{?_isa}
BuildRequires:	openssl-devel%{?_isa}
BuildRequires:	globus-core%{?_isa} >= 4
BuildRequires:	doxygen
BuildRequires:	graphviz
%if "%{?rhel}" == "5"
BuildRequires:	graphviz-gd
%endif
BuildRequires:	ghostscript
%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:	tex(latex)
%else
BuildRequires:	tetex-latex
%endif

%package progs
Summary:	Globus Toolkit - Globus GSI Cert Utils Library Programs
Group:		Applications/Internet
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	openssl
Requires:	globus-common

%package devel
Summary:	Globus Toolkit - Globus GSI Cert Utils Library Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-common-devel%{?_isa} >= 3
Requires:	globus-openssl-module-devel%{?_isa}
Requires:	globus-gsi-openssl-error-devel%{?_isa}
Requires:	openssl-devel%{?_isa}
Requires:	globus-core%{?_isa} >= 4

%package doc
Summary:	Globus Toolkit - Globus GSI Cert Utils Library Documentation Files
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Requires:	%{name} = %{version}-%{release}

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus GSI Cert Utils Library

%description progs
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-progs package contains:
Globus GSI Cert Utils Library Programs

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
Globus GSI Cert Utils Library Development Files

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
Globus GSI Cert Utils Library Documentation Files

%prep
%setup -q -n %{_name}-%{version}

%if "%{rhel}" == "5"
mkdir bin
install %{SOURCE9} bin/epstopdf
%endif

%build
%if "%{rhel}" == "5"
export PATH=$PWD/bin:$PATH
%endif


# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache
unset GLOBUS_LOCATION
unset GPT_LOCATION

%{_datadir}/globus/globus-bootstrap.sh

%configure --with-flavor=%{flavor} --enable-doxygen \
    --%{docdiroption}=%{_docdir}/%{name}-%{version} \
    --disable-static

make %{?_smp_mflags}

%install
%if "%{rhel}" == "5"
export PATH=$PWD/bin:$PATH
%endif

rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Remove libtool archives (.la files)
find $RPM_BUILD_ROOT%{_libdir} -name 'lib*.la' -exec rm -v '{}' \;
sed '/lib.*\.la$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist

# Move client man pages to progs package
grep '.[18]$' $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist
sed '/.[18]$/d' -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Remove unwanted documentation (needed for RHEL4)
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/*_%{_name}-%{version}_*.3
sed -e '/_%{_name}-%{version}_.*\.3/d' \
  -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
  | sed -e s!^!%{_prefix}! -e 's!.*/man/.*!%doc &*!' > package-progs.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  | sed s!^!%{_prefix}! > package-devel.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' > package-doc.filelist

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/GLOBUS_LICENSE

%files -f package-progs.filelist progs
%defattr(-,root,root,-)

%files -f package-devel.filelist devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}.pc

%files -f package-doc.filelist doc
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}/html

%changelog
* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.6-1
- Update to Globus Toolkit 5.0.2
- Drop patch globus-gsi-cert-utils-oid.patch (fixed upstream)

* Mon May 31 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-2
- Fix OID registration pollution

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-1
- Update to Globus Toolkit 5.0.1

* Fri Jan 22 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.4-1
- Update to Globus Toolkit 5.0.0

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 5.5-4
- rebuilt with new openssl

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-3
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch

* Wed Jun 03 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-2
- Update to official Fedora Globus packaging guidelines

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-1
- Change defines to globals
- Remove explicit requires on library packages

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-0.4
- Add s390x to the list of 64 bit platforms
- Update to upstream update release 5.5
- Drop the environment elimination patch (accepted upstream)

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-0.3
- Adapt to updated GPT package

* Tue Oct 14 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-0.2
- Update to Globus Toolkit 4.2.1

* Mon Jul 14 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.1-0.1
- Autogenerated
