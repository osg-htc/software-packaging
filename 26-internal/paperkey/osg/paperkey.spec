Name:      paperkey
Version:   1.6
Release:   1.2%{?dist}
Summary:   An OpenPGP key archiver
Group:	   Applications/Archiving
License:   GPLv2+
URL:	   http://www.jabberwocky.com/software/paperkey/
Source0:   http://www.jabberwocky.com/software/%{name}/%{name}-%{version}.tar.gz
Source1:   http://www.jabberwocky.com/software/%{name}/%{name}-%{version}.tar.gz.sig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
A reasonable way to achieve a long term backup of OpenPGP (PGP, GnuPG,
etc) keys is to print them out on paper.  Paper and ink have amazingly
long retention qualities - far longer than the magnetic or optical
means that are generally used to back up computer data.  A paper
backup isn't a replacement for the usual machine readable (tape, CD-R,
DVD-R, etc) backups, but rather as an if-all-else-fails method of
restoring a key.

%prep
%setup -q

%build
# Paperkey does not build on x86_64_v2
%if 0%{?x86_64_v2}
%global _host x86_64-redhat-linux
%endif

%configure
make %{?_smp_mflags} check

%install
rm -rf "$RPM_BUILD_ROOT"
make install DESTDIR="$RPM_BUILD_ROOT"

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%{!?_licensedir:%global license %doc}
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README NEWS
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Mon Aug 31 2026 Matt Westphall <westphall@wisc.edu>
- Update %build to work-around x86_64_v2 build failures

* Mon Sep  5 2016 David Shaw <dshaw@jabberwocky.com>
- Use %license for the COPYING file and run the self checks during build.

* Fri Jan 16 2009 David Shaw <dshaw@jabberwocky.com>
- Borrow some RPM-fu from the Fedora RPM.
