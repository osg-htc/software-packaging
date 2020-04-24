
Name: xrootd-multiuser
Version: 0.4.2
Release: 6%{?dist}
Summary: Multiuser filesystem writing plugin for xrootd

License: BSD
URL: https://github.com/bbockelm/xrootd-multiuser
# Generated from:
# git archive v%{version} --prefix=xrootd-multiuser-%{version}/ | gzip -7 > ~/rpmbuild/SOURCES/xrootd-multiuser-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz

%define xrootd_current 4.11
%define xrootd_next %(echo %xrootd_current | awk '{print $1,$2+1}' FS=. OFS=.)

BuildRequires: xrootd-server-libs >= 1:%{xrootd_current}.0-1
BuildRequires: xrootd-server-libs <  1:%{xrootd_next}.0-1
BuildRequires: xrootd-server-devel >= 1:%{xrootd_current}.0-1
BuildRequires: xrootd-server-devel <  1:%{xrootd_next}.0-1
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: libcap-devel
%{?systemd_requires}
# For %{_unitdir} macro
BuildRequires: systemd

Requires: xrootd-server >= 1:%{xrootd_current}.0-1
Requires: xrootd-server <  1:%{xrootd_next}.0-1

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
* Fri Apr 24 2020 Edgar Fajardo <emfajard@ucsd.edu> - 0.4.2-6
- Rebuild against xrootd 4.12; (SOFTWARE-4063)

* Wed Oct 23 2019 Carl Edquist <edquist@cs.wisc.edu> - 0.4.2-5
- Rebuild against xrootd 4.11; add version range dependency (SOFTWARE-3830)

* Thu Jul 18 2019 Carl Edquist <edquist@cs.wisc.edu> - 0.4.2-4
- Rebuild against xrootd 4.10.0 and update versioned dependency (SOFTWARE-3697)

* Wed Apr 10 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 0.4.2-3
- Rebuild against xrootd 4.9.1 and add versioned dependency (SOFTWARE-3485)

* Wed Feb 27 2019 Carl Edquist <edquist@cs.wisc.edu> - 0.4.2-2
- Rebuild against xrootd 4.9.0 (SOFTWARE-3485)

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

