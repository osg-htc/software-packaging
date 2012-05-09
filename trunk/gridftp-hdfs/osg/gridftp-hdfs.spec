
# OSG packaging is a bit different from Globus
%if "0%{?dist}" == "0.osg"
%define _osg 1
%else
%define _osg 1
%endif


Name:           gridftp-hdfs
Version:        0.5.3
Release:        4%{?dist}
Summary:        HDFS DSI plugin for GridFTP
Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://twiki.grid.iu.edu/bin/view/Storage/HadoopInstallation
# TODO:  Check if this svn tag is the same as the source tarball available
# for download.  That might simplify this a bit.
# svn co svn://t2.unl.edu/brian/gridftp_hdfs
# cd gridftp_hdfs
# ./bootstrap
# ./configure
# make dist
Source0:        %{name}-%{version}.tar.gz
Patch0: lcmaps15.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# On SL6, build fails since java-devel pulls in java-1.5.0-gcj
#  which has libjvm in /usr/lib64/gcj-4.4.0 and gcc can't find it.
%if 0%{rhel} == 6
BuildRequires: jdk java-1.6.0-sun-compat
%else
BuildRequires: java-devel
%endif

BuildRequires: hadoop-0.20-libhdfs
BuildRequires: globus-gridftp-server-devel
BuildRequires: globus-common-devel

Requires: hadoop-0.20-libhdfs
Requires: globus-gridftp-server-progs
Requires: xinetd

Requires(pre): shadow-utils
Requires(preun): initscripts
Requires(preun): chkconfig
Requires(post): chkconfig
Requires(postun): initscripts
Requires(postun): xinetd

%description
HDFS DSI plugin for GridFTP 

%prep

%setup -q
%patch0 -p1

%build

%configure --with-java=/etc/alternatives/java_sdk

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Remove libtool turds
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# Remove the init script - in GT5.2, this gets bootstrapped appropriately
%if %_osg
rm $RPM_BUILD_ROOT%{_sysconfdir}/init.d/%{name}
%else
rm $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/gridftp.conf.d/%{name}-environment-bootstrap
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%if %_osg
/sbin/service globus-gridftp-server condrestart >/dev/null 2>&1 || :
%else
/sbin/chkconfig --add %{name}
%endif

%preun
if [ "$1" = "0" ] ; then
    /sbin/service xinetd condrestart >/dev/null 2>&1
%if %_osg
    /sbin/service globus-gridftp-server condrestart >/dev/null 2>&1 || :
%else
    /sbin/service %{name} stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
%endif
fi

%postun
/sbin/ldconfig
if [ "$1" -ge "1" ]; then
    /sbin/service xinetd condrestart >/dev/null 2>&1
%if %_osg
    /sbin/service globus-gridftp-server condrestart >/dev/null 2>&1 || :
%else
    /sbin/service gridftp-hdfs condrestart >/dev/null 2>&1 || :
%endif
fi

%files
%defattr(-,root,root,-)
%{_sbindir}/gridftp-hdfs-inetd
%{_bindir}/gridftp-hdfs-standalone
%{_libdir}/libglobus_gridftp_server_hdfs.so*
%{_datadir}/%{name}/%{name}-environment
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/gridftp-debug.conf
%config(noreplace) %{_sysconfdir}/%{name}/gridftp-inetd.conf
%config(noreplace) %{_sysconfdir}/%{name}/gridftp.conf
%config(noreplace) %{_sysconfdir}/%{name}/replica-map.conf
%config(noreplace) %{_sysconfdir}/sysconfig/gridftp.conf.d/%{name}
%if %_osg
%{_sysconfdir}/sysconfig/gridftp.conf.d/%{name}-environment-bootstrap
%else
%{_sysconfdir}/init.d/%{name}
%endif

%changelog
* Wed May 9 2012 Doug Strain <dstrain@fnal.gov> - 0.5.3-4
- Added new LCMAPs options to sysconfig

* Fri Apr 13 2012 Doug Strain <dstrain@fnal.gov> - 0.5.3-2
- Added dist tag
- Switched to using jdk for SL6

* Tue Dec 06 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.3-1
- Initial support for GlobusOnline.

* Sat Nov 19 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.2-1
- Implement checksum support for gridftp-hdfs.

* Sat Oct 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.1-1
Migrate as much of the RPM as possible to the OSG-style of gridftp initialization while maintaining GT 52 compatibility.

* Sat Sep 24 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.0-1
- Redo gridftp to allow either xinetd or init startup; link with GT 5.2.

* Mon Jun 6 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.4.0-2
- Decrease logging verbosity.
- Make sure we always finish up the transfer.

* Mon Jun 6 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.4.0-1
- Rewrite of send/recv to clean up logic and error handling.
- Should improve multithreaded performance.

* Thu Jun 2 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.3.2-2
- Remove dependency on gratia probe.

* Thu May 26 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.3.2-1
- Attempt to fix the race issue for closing files.

* Tue Apr 26 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.3.1-1
- Fix listing of empty directories; error is now higher in the globus stack
- Fix listed modes in stat.
- Make everything friendly to dumping cores.
- On segfaults, inetd now spews Java mess back to the client.

* Mon Apr 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.3.0-1
- Re-organize code and tighten up visibility rules.

* Mon Apr 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.4-1
- Implement "ls" on directories.

* Mon Apr 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.3-8
- Fix generation of debuginfo RPM.

* Fri Apr 01 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.3-7
- Destroy HDFS handle only if it was initialized.  Fixes segfault on auth failure.

* Wed Mar 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.3-6
- Add explicit dep for globus-common
- Rebuild to trigger a 32-bit build in Koji.

* Mon Jan 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.3-4
- Purposefully leak file handle due to lifetime and synchronization issues.

* Fri Dec 17 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.3-2
- Protect against a double-free if only one block is read.

* Wed Dec 15 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.2-1
- Update the bootstrapping scripts for the correct HADOOP_HOME
  and exporting CLASSPATH

* Sun Oct 17 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.1-2
- Update the bootstrapping scripts to include the JVM paths.
- Fix library names for flavourless-Globus

* Fri Oct 15 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.0-3
- Rebuild to create new Koji build.

* Tue Sep 28 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.0-2
- Update configurations to use GT5 GridFTP server from Fedora
- Include environment variables for LCMAPS/LCAS support

* Mon May 17 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.0-1
- Adjust build to depend on hadoop-0.20 RPM layout.
- Commit patches to upstream source.

* Fri Apr 9 2010 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-16
- Add extra debugging lines for file buffer creation to help diagnose
  mmap() failures.  Clean up file buffer if mmap() fails.
- Use MAP_SHARED instead of MAP_PRIVATE to ensure that changes are
  written to disk and memory is not exhausted.

* Wed Feb 10 2010 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-15
- Fix library name on 32-bit arch

* Fri Aug 21 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-14
- Add logrotate configuration file

* Mon Aug 17 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-13
- Add Requires: for osg-ca-certs and fetch-crl
- New upstream source fixing a potential seg fault

* Mon Jul 27 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-12
- Additional debugging lines.
- Add dependency on gratia probes

* Thu Jul 23 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-11
- New upstream sources with syslog fixes

* Sat Jul 4 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-10
- Add GRIDFTP_REPLICA_MAP env var for setting per-file replicas

* Thu Jul 2 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-9
- Move config files to /etc
- Allow local env settings in /etc/gridftp-hdfs/gridftp-hdfs-local.conf

* Thu Jul 2 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-8
- Restart xinetd after installing, but only if xinetd was already running

* Thu Jun 25 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-7
- Add hadoop environment setup to xinetd scripts

* Thu Jun 25 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-6
- Update to latest tarball that contains fixes for the so name

* Thu Jun 25 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-5
- Fix bug in postun
- Add Requires: prima

* Wed Jun 24 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-4
- Add Requires: gpt-postinstall so we know where the globus libraries are
  located
- Update source tarball to pick up xinetd service name change.

* Wed Jun 24 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-3
- Fix paths in inetd scripts
- Add explicit dependency on hadoop

* Wed Jun 24 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-2
- spec file cleanup

* Thu Jun 18 2009 Brian Bockelman <bbockelm@cse.unl.edu> 0.1.0-1
- Creation of GridFTP/HDFS plugin

