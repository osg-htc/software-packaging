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

Name:		globus-gatekeeper
%global _name %(tr - _ <<< %{name})
Version:	8.1
Release:	3%{?dist}
Summary:	Globus Toolkit - Globus Gatekeeper

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:         %{_name}-%{version}.tar.gz

# OSG customizations
Source1:        globus-gatekeeper.sysconfig
Patch0:         child_signals.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-common >= 13.4
Requires:	globus-gss-assist%{?_isa} >= 8
Requires:	globus-gssapi-gsi%{?_isa} >= 9

Requires:       lsb
Requires(post): globus-common-progs >= 13.4
Requires(preun):globus-common-progs >= 13.4
BuildRequires:  lsb
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-gss-assist-devel%{?_isa} >= 8
BuildRequires:	globus-gssapi-gsi-devel%{?_isa} >= 9
BuildRequires:	globus-core%{?_isa} >= 8

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus Gatekeeper
Globus Gatekeeper Setup

%prep
%setup -q -n %{_name}-%{version}

%patch0 -p0
# Note append here
cat %{SOURCE1} >> config/globus-gatekeeper.in

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

%{_datadir}/globus/globus-bootstrap.sh

%configure --with-flavor=%{flavor} \
           --%{docdiroption}=%{_docdir}/%{name}-%{version} \
           --disable-static \
           --with-lsb \
	   --with-initscript-config-path=/etc/sysconfig/globus-gatekeeper \
           --with-lockfile-path='${localstatedir}/lock/subsys/globus-gatekeeper'

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | grep -v '^/etc' \
  | sed -e s!^!%{_prefix}! -e 's!.*/man/.*!%doc &*!' > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | grep '^/etc' >> package.filelist
mkdir -p $RPM_BUILD_ROOT/etc/grid-services
mkdir -p $RPM_BUILD_ROOT/etc/grid-services/available

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/chkconfig --del %{name}
    /sbin/service %{name} stop > /dev/null 2>&1 || :
fi

%postun
if [ $1 -eq 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%dir /etc/grid-services
%dir /etc/grid-services/available
%config(noreplace) /etc/sysconfig/globus-gatekeeper

%changelog
* Thu Oct 27 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 8.1-3
- Merged upstream 8.1-2
    * Fri Oct 21 2011 Joseph Bester <bester@mcs.anl.gov> - 8.1-2
    - Fix %post* scripts to check for -eq 1
    - Add explicit dependencies on >= 5.2 libraries

* Fri Sep 23 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 8.1-2
- Removed my lsb patch, merged upstream 8.1-1:
    * Fri Sep 23 2011 Joe Bester <bester@mcs.anl.gov> - 8.1-1
    - GRAM-260: Detect and workaround bug in start_daemon for LSB < 4

* Fri Sep 16 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 8.0-4
- Patched init script to work around infinite loop caused by some versions of redhat-lsb

* Fri Sep 02 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 8.0-3
- Merged upstream 8.0-2:
    * Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 8.0-2
    - Update for 5.1.2 release

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 7.3-2
- Port OSG patches to released gatekeeper.

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-4
- Add README file

* Tue Apr 19 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-3
- Add start-up script and README.Fedora file

* Mon Feb 28 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-2
- Fix typos in the setup patch

* Thu Feb 24 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-1
- Update to Globus Toolkit 5.0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-2
- Simplify directory ownership

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.3-1
- Update to Globus Toolkit 5.0.0

* Wed Jul 29 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-1
- Autogenerated
