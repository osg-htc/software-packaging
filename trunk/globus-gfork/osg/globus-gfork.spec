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

Name:		globus-gfork
%global _name %(tr - _ <<< %{name})
Version:	2.0
Release:	4%{?dist}
Summary:	Globus Toolkit - GFork

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.0/installers/src/gt5.0.0-all-source-installer.tar.bz2
#		tar -jxf gt5.0.0-all-source-installer.tar.bz2
#		mv gt5.0.0-all-source-installer/source-trees/gridftp/gfork/source globus_gfork-0.2
#		cp -p gt5.0.0-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gfork-0.2
#		tar -zcf globus_gfork-0.2.tar.gz globus_gfork-0.2
Source:		%{_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-common
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-xio-devel%{?_isa} >= 2

%package progs
Summary:	Globus Toolkit - GFork Programs
Group:		Applications/Internet
Requires:	%{name}%{?_isa} = %{version}-%{release}

%package devel
Summary:	Globus Toolkit - GFork Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-xio-devel%{?_isa} >= 2

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
GFork Library

%description progs
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-progs package contains:
GFork Programs - GFork is user configurable super-server daemon very similar
to xinetd. It listens on a TCP port. When clients connect to a port it runs an
administrator defined program which services that client connection, just as
x/inetd do.

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
GFork Development Files

%prep
%setup -q -n %{_name}-%{version}

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

unset GLOBUS_LOCATION
unset GPT_LOCATION

%{_datadir}/globus/globus-bootstrap.sh

%configure --with-flavor=%{flavor} \
           --%{docdiroption}=%{_docdir}/%{name}-%{version} \
           --disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Remove libtool archives (.la files)
find $RPM_BUILD_ROOT%{_libdir} -name 'lib*.la' -exec rm -v '{}' \;
sed '/lib.*\.la$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist

# Add empty default configuration file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo "# This is the default gfork configuration file" > \
  $RPM_BUILD_ROOT%{_sysconfdir}/gfork.conf

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
  | sed s!^!%{_prefix}! > package.filelist

grep GLOBUS_LICENSE $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed s!^!%{_prefix}! >> package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | grep -v GLOBUS_LICENSE \
  | sed s!^!%{_prefix}! > package-progs.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  | sed s!^!%{_prefix}! > package-devel.filelist

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}

%files -f package-progs.filelist progs
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/gfork.conf
%doc %{_docdir}/%{name}-%{version}/README.txt

%files -f package-devel.filelist devel
%defattr(-,root,root,-)

%changelog
* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-4
- Update to Globus Toolkit 5.0.0

* Fri Oct 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-3
- Fix location of default config file
- Add empty default config file

* Wed Oct 07 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-2
- Include additional documentation

* Tue Jul 28 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-1
- Autogenerated
