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

Name:		globus-gass-copy
%global _name %(tr - _ <<< %{name})
Version:	7.3
Release:	1%{?dist}
Summary:	Globus Toolkit - Globus Gass Copy

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.2/installers/src/gt5.0.2-all-source-installer.tar.bz2
#		tar -jxf gt5.0.2-all-source-installer.tar.bz2
#		mv gt5.0.2-all-source-installer/source-trees/gass/copy/source globus_gass_copy-5.7
#		cp -p gt5.0.2-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gass_copy-5.7
#		tar -zcf globus_gass_copy-5.7.tar.gz globus_gass_copy-5.7
Source:		%{_name}-%{version}.tar.gz
#		This is a workaround for the broken epstopdf script in RHEL5
#		See: https://bugzilla.redhat.com/show_bug.cgi?id=450388
Source9:	epstopdf-2.9.5gw
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-common
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-ftp-client-devel%{?_isa} >= 5
BuildRequires:	globus-common-devel%{?_isa} >= 6
BuildRequires:	globus-gssapi-gsi-devel%{?_isa} >= 4
BuildRequires:	globus-io-devel%{?_isa} >= 3
BuildRequires:	globus-gass-transfer-devel%{?_isa} >= 2
BuildRequires:	globus-ftp-control-devel%{?_isa} >= 1
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
Summary:	Globus Toolkit - Globus Gass Copy Programs
Group:		Applications/Internet
Requires:	%{name}%{?_isa} = %{version}-%{release}

%package devel
Summary:	Globus Toolkit - Globus Gass Copy Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-ftp-client-devel%{?_isa} >= 5
Requires:	globus-common-devel%{?_isa} >= 6
Requires:	globus-gssapi-gsi-devel%{?_isa} >= 4
Requires:	globus-io-devel%{?_isa} >= 3
Requires:	globus-gass-transfer-devel%{?_isa} >= 2
Requires:	globus-ftp-control-devel%{?_isa} >= 1
Requires:	globus-core%{?_isa} >= 4

%package doc
Summary:	Globus Toolkit - Globus Gass Copy Documentation Files
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
Globus Gass Copy

%description progs
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-progs package contains:
Globus Gass Copy Programs

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
Globus Gass Copy Development Files

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
Globus Gass Copy Documentation Files

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

# Remove unwanted documentation (needed for RHEL4)
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/*_%{_name}-%{version}_*.3
sed -e '/_%{_name}-%{version}_.*\.3/d' \
  -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
  | sed s!^!%{_prefix}! > package-progs.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  | sed s!^!%{_prefix}! > package-devel.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | grep -v GLOBUS_LICENSE \
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

%files -f package-doc.filelist doc
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}/html

%changelog
* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-1
- Update to Globus Toolkit 5.0.2

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.4-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.3-1
- Update to Globus Toolkit 5.0.0

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.14-4
- rebuilt with new openssl

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.14-3
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch

* Thu Jun 04 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.14-2
- Update to official Fedora Globus packaging guidelines

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.14-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages
- Put GLOBUS_LICENSE file in extracted source tarball

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.14-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.14-0.4
- Add s390x to the list of 64 bit platforms

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.14-0.3
- Adapt to updated GPT package

* Tue Oct 21 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.14-0.2
- Update to Globus Toolkit 4.2.1

* Tue Jul 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.10-0.1
- Autogenerated
