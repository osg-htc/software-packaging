
Summary: CMS meta-RPM for Xrootd
Name: cms-xrootd
Version: 1.2
Release: 1%{?dist}
Group: System Environment/Daemons
License: Public Domain
URL: https://twiki.cern.ch/twiki/bin/view/Main/CmsXrootdArchitecture

# Note that we aren't shipping the T3 config until caching is better
# understood.
Source0:  xrootd.sample.t3.cfg.in
Source1:  xrootd.sample.posix.cfg.in
Source2:  Authfile
Source3:  xrootd.sample.dcache.cfg.in

Requires: xrootd-server >= 3.1.0
Conflicts: xrootd-server < 3.1.0

%ifarch %{ix86}
Requires: libXrdLcmaps.so.0
Requires: libXrdCmsTfc.so.0
%else
Requires: libXrdLcmaps.so.0()(64bit)
Requires: libXrdCmsTfc.so.0()(64bit)
%endif
Requires: fetch-crl
Requires: grid-certificates

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
%{summary}

%package hdfs
Summary: CMS meta-RPM for Xrootd over HDFS
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: xrootd-hdfs >= 1.5.0-2
%ifarch %{ix86}
Requires: libXrdHdfs.so.0
%else
Requires: libXrdHdfs.so.0()(64bit)
%endif

%description hdfs
%{summary}

%package dcache
Summary: CMS meta-RPM for Xrootd over dCache
Group: System Environment/Daemons
Requires: xrootd-server >= 3.1.0
Conflicts: xrootd-server < 3.1.0

%description dcache
%{summary}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xrootd

#sed -e "s#@LIBDIR@#%{_libdir}#" %{SOURCE0} > $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd.sample.t3.cfg
sed -e "s#@LIBDIR@#%{_libdir}#" %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd.sample.posix.cfg
sed -e "s#@LIBDIR@#%{_libdir}#" %{SOURCE3} > $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd.sample.dcache.cfg
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/Authfile

%clean
rm -rf $RPM_BUILD_ROOT

%files
#%{_sysconfdir}/xrootd/xrootd.sample.t3.cfg
%{_sysconfdir}/xrootd/xrootd.sample.posix.cfg
%{_sysconfdir}/xrootd/Authfile

%files hdfs

%files dcache
%{_sysconfdir}/xrootd/xrootd.sample.dcache.cfg

%changelog
* Mon Sep 17 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.2-1
- Tweaks for default configs, based on feedback from Estonia, Legnaro, and UCL.


