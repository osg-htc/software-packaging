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

Name:		globus-xio-popen-driver
%global _name %(tr - _ <<< %{name})
Version:	1.1
Release:	1%{?dist}
Summary:	Globus Toolkit - Globus XIO Pipe Open Driver

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.1/installers/src/gt5.0.1-all-source-installer.tar.bz2
#		tar -jxf gt5.0.1-all-source-installer.tar.bz2
#		mv gt5.0.1-all-source-installer/source-trees/xio/drivers/popen/source globus_xio_popen_driver-0.9
#		cp -p gt5.0.1-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_xio_popen_driver-0.9
#		tar -zcf globus_xio_popen_driver-0.9.tar.gz globus_xio_popen_driver-0.9
Source:		%{_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-common
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-xio-devel%{?_isa}

%package devel
Summary:	Globus Toolkit - Globus XIO Pipe Open Driver Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-xio-devel%{?_isa}

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus XIO Pipe Open Driver - allows a user to execute a program and treat it
as a transport driver by routing data through pipes

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
Globus XIO Pipe Open Driver Development Files

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

# This library is opened using lt_dlopenext, so the libtool archives
# (.la files) can not be removed - fix the libdir...
for lib in `find $RPM_BUILD_ROOT%{_libdir} -name 'lib*.la'` ; do
  sed "s!^libdir=.*!libdir=\'%{_libdir}\'!" -i $lib
done

# Move libtool archives (.la files) to rtl package
grep '\.la' $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist 
sed '/\.la$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  | sed s!^!%{_prefix}! > package-devel.filelist

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}

%files -f package-devel.filelist devel
%defattr(-,root,root,-)

%changelog
* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.9-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.7-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-4
- Add instruction set architecture (isa) tags

* Thu Jun 04 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-3
- Update to official Fedora Globus packaging guidelines

* Fri Apr 24 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-2
- Correct package description

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages
- Put GLOBUS_LICENSE file in extracted source tarball

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-0.4
- Add s390x to the list of 64 bit platforms

* Tue Dec 30 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-0.3
- Adapt to updated GPT package

* Mon Oct 20 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-0.2
- Update to Globus Toolkit 4.2.1

* Tue Jul 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.2-0.1
- Autogenerated
