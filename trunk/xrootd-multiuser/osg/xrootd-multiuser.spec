
Name: xrootd-multiuser
Version: 0.4.2
Release: 1%{?dist}
Summary: Multiuser filesystem writing plugin for xrootd

Group: System Environment/Daemons
License: BSD
URL: https://github.com/bbockelm/xrootd-multiuser
# Generated from:
# git archive v%{version} --prefix=xrootd-multiuser-%{version}/ | gzip -7 > ~/rpmbuild/SOURCES/xrootd-multiuser-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: xrootd-server-libs
BuildRequires: xrootd-server-devel
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: libcap-devel
%{?systemd_requires}
# For %{_unitdir} macro
BuildRequires: systemd

Requires: xrootd-server

%description
%{summary}

%prep
%setup -q

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo .
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post xrootd-privileged@.service

%preun
%systemd_preun xrootd-privileged@.service

%postun
%systemd_postun xrootd-privileged@.service

%files
%defattr(-,root,root,-)
%{_libdir}/libXrdMultiuser-4.so
%{_unitdir}/xrootd-privileged@.service

%changelog
* Wed Aug 08 2018 Brian Bockelman <bbockelm@cse.unl.edu> - 0.4.2-1
- Fix chaining of sendfile requests.
- Fix potentially misleading error message.

* Sun Aug 05 2018 Brian Bockelman <bbockelm@cse.unl.edu> - 0.4.1-1
- Fix errant message after GID switch.

* Mon Jul 30 2018 Brian Bockelman <bbockelm@cse.unl.edu> - 0.4.0-1
- Add support for POSIX-like umask.
- Make multiuser plugin compatible with Macaroons.
- Avoid a segfault if the plugin is improperly configured.

* Sat Jul 28 2018 Brian Bockelman <bbockelm@cse.unl.edu> - 0.3.1-1
- Propagate errors from underlying SFS object.

* Wed Sep 20 2017 Brian Bockelman <bbockelm@cse.unl.edu> - 0.3-1
- Fix effective capabilities on all transfer threads.

* Wed Sep 20 2017 Brian Bockelman <bbockelm@cse.unl.edu> - 0.2-1
- Initial packaging of the multiuser plugin.

