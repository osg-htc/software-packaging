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

Name:		globus-gridftp-server
%global _name %(tr - _ <<< %{name})
Version:	6.1
Release:	3%{?dist}
Summary:	Globus Toolkit - Globus GridFTP Server

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.2/installers/src/gt5.0.2-all-source-installer.tar.bz2
#		tar -jxf gt5.0.2-all-source-installer.tar.bz2
#		mv gt5.0.2-all-source-installer/source-trees/gridftp/server/src globus_gridftp_server-3.23
#		cp -p gt5.0.2-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gridftp_server-3.23
#		tar -zcf globus_gridftp_server-3.23.tar.gz globus_gridftp_server-3.23
Source0:	%{_name}-%{version}.tar.gz
Source1:	globus-gridftp-server.sysconfig
Source2:	globus-gridftp-server.i386.sysconfig
Patch0:		osg-gridftp.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-xio-gsi-driver%{?_isa} >= 2
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-gridftp-server-control-devel%{?_isa} >= 2
BuildRequires:	globus-usage-devel%{?_isa} >= 3
BuildRequires:	globus-xio-gsi-driver-devel%{?_isa} >= 2
BuildRequires:	globus-xio-devel%{?_isa} >= 3
BuildRequires:	globus-authz-devel%{?_isa} >= 2
BuildRequires:	globus-gfork-devel%{?_isa} >= 3
BuildRequires:	globus-ftp-control-devel%{?_isa} >= 4

%package progs
Summary:	Globus Toolkit - Globus GridFTP Server Programs
Group:		Applications/Internet
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-xio-gsi-driver%{?_isa} >= 2

%package devel
Summary:	Globus Toolkit - Globus GridFTP Server Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-gridftp-server-control-devel%{?_isa} >= 2
Requires:	globus-usage-devel%{?_isa} >= 3
Requires:	globus-xio-gsi-driver-devel%{?_isa} >= 2
Requires:	globus-xio-devel%{?_isa} >= 3
Requires:	globus-authz-devel%{?_isa} >= 2
Requires:	globus-gfork-devel%{?_isa} >= 3
Requires:	globus-ftp-control-devel%{?_isa} >= 4

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus GridFTP Server

%description progs
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-progs package contains:
Globus GridFTP Server Programs

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
Globus GridFTP Server Development Files

%prep
%setup -q -n %{_name}-%{version}

%patch0 -p1
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

export GRIDMAP=/etc/grid-security/grid-mapfile
%configure --with-flavor=%{flavor} --sysconfdir=/etc/%{name} \
           --%{docdiroption}=%{_docdir}/%{name}-%{version} \
           --disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.conf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d
mv $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.xinetd.default $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/gridftp
mv $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.gfork.default $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.gfork

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/gridftp.conf.d
%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
%else
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
%endif

# Remove libtool archives (.la files)
find $RPM_BUILD_ROOT%{_libdir} -name 'lib*.la' -exec rm -v '{}' \;
sed '/lib.*\.la$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | grep -Ev '(gridftp.conf.default|gridftp.xinetd.default|gridftp.gfork.default)' \
  | sed -e s!^!%{_prefix}! | sed -e s!^/usr/etc!/etc! \
  > package-progs.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  | sed s!^!%{_prefix}! > package-devel.filelist

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post progs
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add globus-gridftp-server
    /sbin/chkconfig --add globus-gridftp-sshftp
fi

%preun progs
if [ $1 -eq 0 ]; then
    /sbin/chkconfig --del globus-gridftp-server
    /sbin/chkconfig --del globus-gridftp-sshftp
    /sbin/service globus-gridftp-server stop
    /sbin/service globus-gridftp-sshftp stop
fi

%postun progs
if [ $1 -ge 1 ]; then
    /sbin/service globus-gridftp-server condrestart > /dev/null 2>&1 || :
    /sbin/service globus-gridftp-sshftp condrestart > /dev/null 2>&1 || :
fi

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%dir %{_sysconfdir}/sysconfig/gridftp.conf.d

%files -f package-progs.filelist progs
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/gridftp.conf
%config(noreplace) %{_sysconfdir}/gridftp.gfork
%config(noreplace) %{_sysconfdir}/xinetd.d/gridftp

%files -f package-devel.filelist devel
%defattr(-,root,root,-)

%changelog
* Tue Sep 27 2011 Doug Strain <dstrain@fnal.gov> - 6.1-3
- Re-Adding extra sysconfig directory and configurable conf file
- With new version of gridftp

* Fri Sep 23 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 6.1-2
- Merged upstream 6.1-1:
    * Fri Sep 23 2011 Joe Bester <bester@mcs.anl.gov> - 6.1-1
    - GRIDFTP-184: Detect and workaround bug in start_daemon for LSB < 4

* Thu Sep 22 2011 Doug Strain <dstrain@fnal.gov> - 6.0-6
- Adding extra sysconfig directory and configurable conf file
- For different plugin supports

* Fri Sep 16 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 6.0-5
- Patched init script to work around an infinite loop caused by some versions of redhat-lsb

* Wed Sep 07 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 6.0-4
- Merge upstream 6.0-3:
    * Wed Aug 31 2011 Joseph Bester <bester@mcs.anl.gov> - 6.0-3
    - Add more config files for xinetd or gfork startup
    - Update to Globus Toolkit 5.1.2
- Fix condition in post-script for progs

* Tue Aug 30 2011 Doug Strain <doug.strain@fnal.gov> - 5.4-4
- Updated to work on RHEL5
- Updated to patch conf to use log file options
- Updated to patch init script to source sysconfig
- Included sysconfig with lcas/lcmaps variables

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.23-1
- Update to Globus Toolkit 5.0.2

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.21-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.19-1
- Update to Globus Toolkit 5.0.0

* Mon Oct 19 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.17-2
- Fix location of default config file

* Thu Jul 30 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.17-1
- Autogenerated
