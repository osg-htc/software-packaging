%global _hardened_build 1

%{!?_initddir: %global _initddir %{_initrddir}}
%{!?_unitdir:  %global _unitdir /usr/lib/systemd/system}
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%if %{?rhel}%{!?rhel:0} >= 7
%global use_systemd 1
%else
%global use_systemd 0
%endif

Name:		globus-gridftp-server
%global _name %(tr - _ <<< %{name})
Version:	13.9
Release:	1.1%{?dist}
Summary:	Grid Community Toolkit - Globus GridFTP Server

License:	ASL 2.0
URL:		https://github.com/gridcf/gct/
Source:		https://repo.gridcf.org/gct6/sources/%{_name}-%{version}.tar.gz
Source1:	%{name}.service
Source2:	globus-gridftp-sshftp.service
Source3:	%{name}
Source4:	globus-gridftp-sshftp
Source6:	globus-gridftp-server.sysconfig
Source7:	globus-gridftp-server.osg-sysconfig
Source8:	README
Source9:	globus-gridftp-server.logrotate
# SystemD helpers
Source11:       %{name}-start
Source13:       globus-gridftp-sshftp-reconfigure
Source14:       globus-gridftp-sshftp-start
Source15:       globus-gridftp-sshftp-stop
#               Add IPv6 enabled by default
#               SOFTWARE-2920
Source16:       ipv6.conf
#               Increase transfer timeout
#               SOFTWARE-3241
Source17:       timeout.conf

Patch101:       gridftp-conf-logging.patch

BuildRequires:	gcc
BuildRequires:	globus-common-devel >= 17
BuildRequires:	globus-xio-devel >= 5
BuildRequires:	globus-xio-gsi-driver-devel >= 2
BuildRequires:	globus-gfork-devel >= 3
BuildRequires:	globus-gridftp-server-control-devel >= 7
BuildRequires:	globus-ftp-control-devel >= 7
BuildRequires:	globus-authz-devel >= 2
BuildRequires:	globus-usage-devel >= 3
BuildRequires:	globus-gssapi-gsi-devel >= 10
BuildRequires:	globus-gss-assist-devel >= 9
BuildRequires:	globus-gsi-credential-devel >= 6
BuildRequires:	globus-gsi-sysconfig-devel >= 5
BuildRequires:	globus-io-devel >= 9
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	perl-generators
%if %{use_systemd}
BuildRequires:	systemd
%endif
#		Additional requirements for make check
BuildRequires:	openssl
BuildRequires:	fakeroot

Requires:	globus-xio-gsi-driver%{?_isa} >= 2
Requires:	globus-xio-udt-driver%{?_isa} >= 1
Requires:	globus-common%{?_isa} >= 17
Requires:	globus-xio%{?_isa} >= 5
Requires:	globus-gridftp-server-control%{?_isa} >= 7
Requires:	globus-ftp-control%{?_isa} >= 7

%package progs
Summary:	Grid Community Toolkit - Globus GridFTP Server Programs
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if %{use_systemd}
%{?systemd_requires}
%else
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
%endif

%package devel
Summary:	Grid Community Toolkit - Globus GridFTP Server Development Files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name} package contains:
Globus GridFTP Server

%description progs
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-progs package contains:
Globus GridFTP Server Programs

%description devel
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-devel package contains:
Globus GridFTP Server Development Files

%prep
%setup -q -n %{_name}-%{version}

%patch101 -p1

%build
# Reduce overlinking
#export LDFLAGS="-Wl,--as-needed -Wl,-z,defs %{?__global_ldflags} -lz"
export LDFLAGS="-Wl,--as-needed -Wl,-z,defs %{?__global_ldflags}"

export GRIDMAP=%{_sysconfdir}/grid-security/grid-mapfile
export GLOBUS_VERSION=6.2
%configure --disable-static \
	   --includedir=%{_includedir}/globus \
	   --libexecdir=%{_datadir}/globus \
	   --docdir=%{_pkgdocdir}

# Reduce overlinking
sed 's!CC \(.*-shared\) !CC \\\${wl}--as-needed \1 !' -i libtool

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Remove libtool archives (.la files)
rm %{buildroot}%{_libdir}/*.la

mv %{buildroot}%{_sysconfdir}/gridftp.conf.default \
   %{buildroot}%{_sysconfdir}/gridftp.conf
mkdir -p %{buildroot}%{_sysconfdir}/xinetd.d
mv %{buildroot}%{_sysconfdir}/gridftp.xinetd.default \
   %{buildroot}%{_sysconfdir}/xinetd.d/gridftp
mv %{buildroot}%{_sysconfdir}/gridftp.gfork.default \
   %{buildroot}%{_sysconfdir}/gridftp.gfork
mkdir -p %{buildroot}%{_sysconfdir}/gridftp.d


# No need for environment in conf files
sed '/ env /d' -i %{buildroot}%{_sysconfdir}/gridftp.gfork
sed '/^env /d' -i %{buildroot}%{_sysconfdir}/xinetd.d/gridftp

# Remove start-up scripts
rm -rf %{buildroot}%{_sysconfdir}/init.d

# Install start-up scripts
%if %{use_systemd}
mkdir -p %{buildroot}%{_unitdir}
install -m 644 -p %{SOURCE1} %{SOURCE2} %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_libexecdir}
install -p -m 0755 %{SOURCE11} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{buildroot}%{_libexecdir}
%else
mkdir -p %{buildroot}%{_initddir}
install -p %{SOURCE3} %{SOURCE4} %{buildroot}%{_initddir}
%endif

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

mkdir -p $RPM_BUILD_ROOT/usr/share/osg/sysconfig
install -m 0644 %{SOURCE7} $RPM_BUILD_ROOT/usr/share/osg/sysconfig/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}.logrotate

install -m 0644 %{SOURCE16} %{SOURCE17} $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.d/

# Remove license file from pkgdocdir if licensedir is used
%{?_licensedir: rm %{buildroot}%{_pkgdocdir}/GLOBUS_LICENSE}

%check
make %{?_smp_mflags} check VERBOSE=1

%ldconfig_scriptlets

%if %{use_systemd}

%pre progs
# Remove old init config when systemd is used
/sbin/chkconfig --del %{name} > /dev/null 2>&1 || :
/sbin/chkconfig --del globus-gridftp-sshftp > /dev/null 2>&1 || :

%post progs
%systemd_post %{name}.service globus-gridftp-sshftp.service

%preun progs
%systemd_preun %{name}.service globus-gridftp-sshftp.service

%postun progs
%systemd_postun_with_restart %{name}.service globus-gridftp-sshftp.service

%else

%post progs
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
    /sbin/chkconfig --add globus-gridftp-sshftp
fi

%preun progs
if [ $1 -eq 0 ]; then
    /sbin/service %{name} stop > /dev/null 2>&1 || :
    /sbin/service globus-gridftp-sshftp stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
    /sbin/chkconfig --del globus-gridftp-sshftp
fi

%postun progs
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
    /sbin/service globus-gridftp-sshftp condrestart > /dev/null 2>&1 || :
fi

%endif

%files
%{_libdir}/libglobus_gridftp_server.so.*
%dir %{_sysconfdir}/gridftp.d
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%{!?_licensedir: %doc %{_pkgdocdir}/GLOBUS_LICENSE}
%{?_licensedir: %license GLOBUS_LICENSE}

%files progs
%{_sbindir}/gfs-dynbe-client
%{_sbindir}/gfs-gfork-master
%{_sbindir}/globus-gridftp-password
%{_sbindir}/globus-gridftp-server
%{_sbindir}/globus-gridftp-server-enable-sshftp
%{_sbindir}/globus-gridftp-server-setup-chroot
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}.logrotate
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/gridftp.conf
%config(noreplace) %{_sysconfdir}/gridftp.d/ipv6.conf
%config(noreplace) %{_sysconfdir}/gridftp.d/timeout.conf
%config(noreplace) %{_sysconfdir}/gridftp.gfork
%config(noreplace) %{_sysconfdir}/xinetd.d/gridftp
/usr/share/osg/sysconfig/%{name}
%if %{use_systemd}
%{_unitdir}/%{name}.service
%{_unitdir}/globus-gridftp-sshftp.service
%{_libexecdir}/%{name}-start
%{_libexecdir}/globus-gridftp-sshftp-reconfigure
%{_libexecdir}/globus-gridftp-sshftp-start
%{_libexecdir}/globus-gridftp-sshftp-stop
%else
%{_initddir}/%{name}
%{_initddir}/globus-gridftp-sshftp
%endif
%doc %{_mandir}/man8/globus-gridftp-password.8*
%doc %{_mandir}/man8/globus-gridftp-server.8*
%doc %{_mandir}/man8/globus-gridftp-server-setup-chroot.8*

%files devel
%{_includedir}/globus/*
%{_libdir}/libglobus_gridftp_server.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Feb 26 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 13.9-1.1.osg
- Merge OSG changes (SOFTWARE-3586)

* Fri Nov 16 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 13.9-1
- Fix data_node restrict path
- Bump GCT release version to 6.2

* Thu Sep 13 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 13.8-1
- Switch upstream to Grid Community Toolkit
- Grid Community Toolkit merged a number of outstanding pull requests (13.0)
  - Add option to send IPv6 address in EPSV response
  - Add function to get the command string
  - Be more selective in what config files we skip
  - Add unames for GNU/Hurd and kfreebsd to chroot setup script
- Merge GT6 update 12.5 into GCT (13.1)
- First Grid Community Toolkit release (13.2)
  - Disable usage statistics reporting by default
  - Add man page for globus-gridftp-password - contribution from IGE
- Use 2048 bit RSA key for tests (13.3)
- Merge GT6 update 12.6 into GCT (13.4)
- Merge GT6 update 12.7 into GCT (13.5)
- Merge GT6 update 12.8 into GCT (13.6)
- Merge GT6 update 12.9 into GCT (13.7)
- Merge GT6 update 12.12 into GCT (13.8)
- Drop patches globus-gridftp-server-unames.patch, -epsv-ip.patch,
  -cmd-string.patch and -config.patch (accepted upstream)
- Drop the man page for globus-gridftp-password from the source package
  (accepted upstream)

* Sat Sep 01 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 12.12-1
- GT6 update:
  - Use 2048 bit keys to support openssl 1.1.1 (12.10)
  - Log remote http connection address for legacy s3 transfers (12.11/12.12)

* Thu Aug 16 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 12.9-1
- GT6 update: Fix initscript status return codes

* Sat Jul 21 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 12.8-1
- GT6 update: Fix daemon config parsing not catching env vars

* Sun Jul 15 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 12.7-1
- GT6 update:
  - Force IPC encryption if server configuration requires
  - Fix old IPC bug making it hard to diagnose racy connection failures

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 12.6-1
- GT6 update: win: fix path restrictions on /

* Fri May 04 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 12.2-1.3.osg
- Increase transfer timeout to 2 hours (SOFTWARE-3241)

* Sat Apr 07 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 12.5-1
- GT6 update: win32 fix

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 12.4-1
- GT6 update
- Ignore backup & packaging files in config.d

* Mon Oct 16 2017 Edgar Fajardo <emfajard@ucsd.edu> - 12.2-1.2.osg
- Added IPv6 enabled by default

* Tue Sep 26 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 12.3-1
- GT6 update

* Tue Aug 22 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 12.2-1.1.osg
- Merge OSG changes

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 12.2-1
- GT6 update:
  - New error message format (12.0)
  - Configuration database (12.0)
  - Better delay for end of session ref check (12.1)
  - Fix tests when getgroups() does not return effective gid (12.2)

* Thu Jun 22 2017 Brian Lin <blin@cs.wisc.edu> - 11.8-1.3.osg
- Use the correct configuration file when using plugins (SOFTWARE-2645)

* Wed Jun 21 2017 Brian Lin <blin@cs.wisc.edu> - 11.8-1.2.osg
- Drop conflicts that are no longer necessary for OSG 3.3/3.4 (SOFTWARE-2713 related)

* Mon Apr 24 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 11.8-4
- Add patches from DPM developers:
  - Add an optional IPv6 address to EPSV response
  - Get command string

* Mon Mar 27 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 11.8-3
- EPEL 5 End-Of-Life specfile clean-up
  - Remove Group and BuildRoot tags
  - Remove _pkgdocdir and _initddir macro definitions
  - Drop redundant Requires corresponding to autogenerated pkgconfig Requires
  - Don't clear the buildroot in the install section
  - Remove the clean section
  - Drop the globus-gridftp-server-openssl098.patch

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Carl Edquist <edquist@cs.wisc.edu> - 11.8-1.1.osg
- Merge OSG changes (SOFTWARE-2436 related)

* Fri Nov 04 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 11.8-1
- GT6 update: Updated man pages, add adler32 checksum support

* Fri Oct 28 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 10.4-1.5.osg
- Use systemd service files on EL7 (SOFTWARE-2497)

* Wed Oct 19 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 10.4-1.4.osg
- Disable SSLv3 (SOFTWARE-2471)

* Wed Oct 19 2016 Brian Lin <blin@cs.wisc.edu> - 10.4-1.3.osg
- Fix exit code when determining service status (SOFTWARE-2470)

* Thu Oct 13 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 11.3-3
- Rebuild for openssl 1.1.0 (Fedora 26)

* Mon Sep 05 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 11.3-2
- Fix broken pre scriptlet

* Thu Sep 01 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 11.3-1
- GT6 update: Updates for OpenSSL 1.1.0

* Thu Sep 01 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 10.4-1.2.osg
- Do not ignore config.d files with a '.' in the name (SOFTWARE-2197)

* Sun Aug 14 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 11.1-2
- Convert to systemd unit files (Fedora 25+)

* Wed Aug 10 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 10.4-1.1.osg
- Merge OSG changes

* Wed Jul 27 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 11.1-1
- GT6 update
  - Fix forced order issues with restart (11.1)
  - Add forced ordering option (11.0)
  - Add Globus task id to transfer log (10.6)
  - Don't errantly kill a transfer due to timeout while client is still
    connected (10.5)

* Fri Jul 22 2016 Carl Edquist <edquist@cs.wisc.edu> - 7.20-1.3.osg
- Add TRANSFER to log_level (SOFTWARE-2397)

* Mon Jun 27 2016 Brian Bockelman <bbockelm@cse.unl.edu> - 7.20-1.2.osg
- Avoid deadlocking when the gridftp server closes its log file. SOFTWARE-2377
- Add support for adler32 checksums. SOFTWARE-2379

* Thu May 19 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.4-1
- GT6 update
  - Fix broken remote_node auth without sharing (10.4)
  - Fix configuration for ipc_interface (10.3)
  - Fix remote_node connection failing when ipc_subject isn't used (10.3)

* Fri May 06 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-1
- GT6 update
  - Spelling (10.2)
  - Don't overwrite LDFLAGS (10.1) - Fix for regressions in 9.8 ans 9.9
  - Updates for https support (10.0)

* Mon May 02 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.9-1
- GT6 update
  - Fix crash when storattr is used without modify (9.7)
  - Add SITE WHOAMI command to return currently authenticated user (9.6)
  - Update manpage for -encrypt-data (9.5)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.4-1
- GT6 update (fix mem error when sharing)

* Tue Nov 24 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.3-1
- GT6 update
  - Add configuration to require encrypted data channels (9.3)
  - More robust cmp function (9.2)

* Fri Nov 06 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.1-1
- GT6 update
  - fix for thread race crash between sequential transfers
  - fix for partial stat punting when passed a single entry
  - fix for double free on transfer failure race

* Tue Oct 27 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.0-2
- Missing ? in _isa macro

* Tue Oct 27 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.0-1
- GT6 update (add SITE STORATTR command and associated DSI api)

* Fri Oct 23 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.9-1
- GT6 update (Home directory fixes)

* Wed Aug 26 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.7-1
- GT6 update (Improvements to globus-gridftp-server-setup-chroot)
- Man page for globus-gridftp-server-setup-chroot now provided by
  upstream, remove the one from the source rpm
- Add build requires on openssl and fakeroot needed for new tests

* Thu Aug 06 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.1-1
- GT6 update (GT-622: GridFTP server crash with sharing group permissions)
- Enable checks

* Mon Jul 27 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.0-1
- GT6 update
- Add update_bytes api that sets byte counters and range markers separately

* Sat Jun 20 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.26-1
- GT6 update (man pages updates)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 08 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.25-1
- GT6 update (Fix order of drivers when using netmgr)

* Sat Mar 28 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.24-1
- GT6 update
- Fix netmanager crash (7.24)
- Allow netmanager calls when taskid isn't set (7.24)
- Fix threads commandline arg processing (7.23)
- Prevent parse error on pre-init envs from raising assertion (7.23)
- Restrict sharing based on username or group membership (7.21)
- Don't enable udt without threads (7.21)
- Environrment and threading config not loaded from config dir (7.21)
- Ignore config.d files with a '.' in name (7.21)
- Always install udt driver (7.21) - F20+, EPEL6+

* Mon Feb 16 2015 Matyas Selmeci <matyas@cs.wisc.edu> - 7.20-1.1.osg
- Merge OSG changes

* Fri Jan 23 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.20-1
- Implement updated license packaging guidelines
- GT6 update (-help fix)

* Wed Jan 07 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.18-1
- GT6 update (net mgr support)

* Fri Dec 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.17-1
- GT6 update

* Thu Nov 13 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.15-1
- GT6 update
- Drop patch globus-gridftp-server-ipv6log.patch (fixed upstream)

* Mon Oct 27 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.12-1
- GT6 update
- Drop patch globus-gridftp-server-deps.patch (fixed upstream)

* Tue Sep 30 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.11-2
- Fix logging of IPv6 addresses

* Fri Sep 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.11-1
- Update to Globus Toolkit 6.0
- Drop GPT build system and GPT packaging metadata
- Activate hardening flags

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Brent Baude <baude@us.ibm.com> - 6.38-2
- Replace arch def of ppc64 with power64 macro for ppc64le enablement

* Wed Apr 02 2014 Carl Edquist <edquist@cs.wisc.edu> - 6.38-1.3.osg
- Provide config dir /etc/gridftp.d/ (SOFTWARE-1412)

* Fri Jan 10 2014 Matyas Selmeci <matyas@cs.wisc.edu> 6.38-1.2.osg
- Fix init script chkconfig priorities to run after netfs and autofs (SOFTWARE-1250)

* Tue Dec 10 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 6.38-1.1.osg
- Merge OSG changes

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.38-1
- Update to Globus Toolkit 5.2.5
- Drop patch globus-gridftp-server-ac.patch (fixed upstream)

* Tue Sep 10 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 6.14-5.osg
- Use copytruncate for log rotation (SOFTWARE-1083)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.19-4
- Implement updated packaging guidelines

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 6.19-3
- Perl 5.18 rebuild

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.19-2
- Add aarch64 to the list of 64 bit platforms
- Don't use AM_CONFIG_HEADER (automake 1.13)

* Wed Feb 20 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.19-1
- Update to Globus Toolkit 5.2.4

* Wed Feb 20 2013 Dave Dykstra <dwd@fnal.gov> - 6.14-4.osg
- Add gridftp-conf-logging.patch to add back logging options in gridftp.conf
  that were (apparently) accidentally dropped in 6.14-1.osg

* Tue Feb 19 2013 Dave Dykstra <dwd@fnal.gov> - 6.14-3.osg
- Switch the default LCMAPS_POLICY_NAME to authorize_only, so it will
  work with the -with-chroot option; it also works without -with-chroot

* Mon Feb 18 2013 Dave Dykstra <dwd@fnal.gov> - 6.14-2.osg
- Move most of the OSG-specific code out of /etc/sysconfig/%{name}
  to /usr/share/osg/sysconfig/%{name} so it can be more easily replaced.
- Instead of sourcing /etc/sysconfig/gridftp.conf.d/* if they exist,
  source /usr/share/osg/sysconfig/%{name}-plugin.
- Add Conflicts statements on older gridftp-hdfs and xrootd-dsi packages
  because need new versions that understand the new sysconfig layout.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.16-1
- Update to Globus Toolkit 5.2.3

* Sun Jul 22 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.14-1
- Update to Globus Toolkit 5.2.2
- Drop patch globus-gridftp-server-pw195.patch (was backport)
- Drop patch globus-gridftp-server-format.patch (fixed upstream)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.10-2
- Backport security fix for JIRA ticket GT-195

* Thu May 17 2012 Alain Roy <roy@cs.wisc.edu> 6.5-1.7.osg
- Added patch for GT-195.

* Fri Apr 27 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.10-1
- Update to Globus Toolkit 5.2.1
- Drop patches globus-gridftp-server-deps.patch,
  globus-gridftp-server-funcgrp.patch, globus-gridftp-server-pathmax.patch
  and globus-gridftp-server-compat.patch (fixed upstream)
- Drop globus-gridftp-server man page from packaging since it is now included
  in upstream sources
- Add additional contributed man pages

* Mon Apr 23 2012 Dave Dykstra <dwd@fnal.gov> - 6.5-1.6.osg
- Remove variable in sysconfig for disabling voms certificate check;
  it is now the default

* Thu Mar 29 2012 Dave Dykstra <dwd@fnal.gov> - 6.5-1.5.osg
- Reduce default lcmaps syslog level from 3 to 2

* Sat Mar 10 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-4
- Restore enum and struct member order for improved backward compatibility

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> - 6.5-1.4.osg
- Rebuild after merging from branches/lcmaps-upgrade into trunk

* Mon Mar 05 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-3
- The last update broke backward compatibility and should have bumped
  the soname - so bump it now
- Add patch from upstream to reduce the chance of backward incompatible
  changes in the future

* Wed Jan 18 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-2
- Portability fixes
- Fix broken links in README file

* Fri Jan 6 2012 Dave Dykstra <dwd@fnal.gov> - 6.5-1.3
- Updated /etc/sysconfig/globus-gridftp-server for elimination of LCAS
  parameters and for new settings of lcas-lcmaps-gt4-interface parameters
  corresponding to the new upgrade of LCMAPS, including backward 
  compatibility with the old lcmaps.db where only the globus_gridftp_mapping
  policy worked.
- Eliminated need for separate sysconfig file for i386

* Tue Dec 27 2011 Doug Strain <dstrain@fnal.gov> - 6.5-1.2
- Changed LCMAPS_MOD_HOME to "lcmaps"
- For SOFTWARE-426 as per Dave Dykstra

* Mon Dec 19 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 6.5-1.1
- Merge OSG changes

* Wed Dec 14 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-1
- Update to Globus Toolkit 5.2.0
- Drop patches globus-gridftp-server-etc.patch,
  globus-gridftp-server-pathmax.patch and globus-gridftp-server-usr.patch
  (fixed upstream)

* Fri Nov 18 2011 Doug Strain <dstrain@fnal.gov> - 6.2-10
- Change sysconfig to add full file path

* Mon Nov 14 2011 Doug Strain <dstrain@fnal.gov> - 6.2-9
- Change sysconfig to source /var/lib/osg/globus-firewall

* Thu Nov 03 2011 Doug Strain <dstrain@fnal.gov> - 6.2-8
- Added logrotate for issue SOFTWARE-310
- Also fixed sysconfig issue for SOFTWARE-357

* Thu Nov 03 2011 Doug Strain <dstrain@fnal.gov> - 6.2-5
- Changed sysconfig to exclude sourcing files left behind by
- emacs, rpm, vi, etc

* Tue Oct 11 2011 Doug Strain <dstrain@fnal.gov> - 6.1-5
- Changes to sysconfig to 
-   1) get rid of a warning if nothing exists in gridftp.conf.d
-   2) Move the xrootd-dsi plugin stuff into the xrootd-dsi package.

* Sun Oct 02 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.33-2
- Update contributed manpage

* Fri Sep 30 2011 Jeff Dost <jdost@ucsd.edu> - 6.1-4
- Change sysconfig file to use correct globus_gridftp_mapping LCMAPS policy

* Tue Sep 27 2011 Doug Strain <dstrain@fnal.gov> - 6.1-3
- Re-Adding extra sysconfig directory and configurable conf file
- With new version of gridftp

* Fri Sep 23 2011 Joe Bester <bester@mcs.anl.gov> - 6.1-1
- GRIDFTP-184: Detect and workaround bug in start_daemon for LSB < 4

* Thu Sep 22 2011 Doug Strain <dstrain@fnal.gov> - 6.0-6
- Adding extra sysconfig directory and configurable conf file
- For different plugin supports

* Fri Sep 16 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 6.0-5
- Patched init script to work around an infinite loop caused by some versions of redhat-lsb

* Wed Sep 07 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 6.0-4
- Fix condition in post-script for progs

* Tue Aug 30 2011 Doug Strain <doug.strain@fnal.gov> - 5.4-4
- Updated to work on RHEL5
- Updated to patch conf to use log file options
- Updated to patch init script to source sysconfig
- Included sysconfig with lcas/lcmaps variables

* Sun Jun 05 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.33-1
- Update to Globus Toolkit 5.0.4

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.28-3
- Add README file
- Add missing dependencies

* Tue Apr 19 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.28-2
- Add start-up script and man page for globus-gridftp-server

* Fri Feb 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.28-1
- Update to Globus Toolkit 5.0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

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
