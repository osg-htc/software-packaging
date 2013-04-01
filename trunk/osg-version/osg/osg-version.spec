Name:      osg-version
Summary:   OSG Version
Version:   3.1.16
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

# This is a OSG Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

Source0:   osg-version

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
%{summary}

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo %{version} > $RPM_BUILD_ROOT%{_sysconfdir}/osg-version
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/osg-version

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -pm 755 %{SOURCE0}  $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_sysconfdir}/osg-version
%{_bindir}/osg-version

%changelog
* Mon Apr 01 2013 Brian Lin <blin@cs.wisc.edu> - 3.1.16-1
- Updated to 3.1.16-1

* Mon Mar 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.1.15-1
- Updated to 3.1.15-1

* Mon Feb 11 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.1.14-1
- Updated to 3.1.14-1

* Mon Jan 28 2013 Tim Cartwright <cat@cs.wisc.edu> 3.1.13-1
- Updated to 3.1.13-1

* Mon Dec 10 2012 Doug Strain <dstrain@fnal.gov> 3.1.12-1
- Updated to 3.1.12-1

* Mon Nov 5 2012 Doug Strain <dstrain@fnal.gov> 3.1.11-1
- Updated to 3.1.11-1

* Mon Oct 8 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.1.10-1
- Updated to 3.1.10-1

* Tue Sep 24 2012 Tim Cartwright <cat@cs.wisc.edu> 3.1.9-1
- Updated to 3.1.9-1

* Tue Aug 14 2012 Matyas Selmeci <matyas@cs.wisc.edu> 3.1.8-1
- Updated to 3.1.8-1

* Mon Jul 30 2012 Alain Roy <roy@cs.wisc.edu> 3.1.7-1
- Updated to 3.1.7-1

* Mon Jul 09 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.1.6-1
- Updated to 3.1.6-1

* Mon Jun 11 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> -3.1.4-1
- Updated to 3.1.4-1

* Mon May 21 2012 Alain Roy <roy@cs.wisc.edu> - 3.1.3-1
- Updated to 3.1.3-1

* Tue May 15 2012 Alain Roy <roy@cs.wisc.edu> - 3.1.2-1
- Updated to 3.1.2-1

* Thu May 03 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.1.1-1
- Updated to 3.1.1-1

* Tue Apr 24 2012 Alain Roy <roy@cs.wisc.edu> - 3.1.0-1
- Updated to 3.1.0-1

* Tue Apr 10 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.10-1
- Updated to 3.0.10-1

* Tue Mar 27 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.9-1
- Updated to 3.0.9-1

* Tue Feb 28 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.8-1
- Updated to 3.0.8-1

* Mon Feb 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.7-1
- Updated to 3.0.7-1

* Mon Jan 30 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.6-1
- Updated to 3.0.6-1

* Mon Dec 12 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.5-1
- Updated to 3.0.5-1

* Mon Dec 05 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.4-1
- Updated to 3.0.4-1

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.3-1
- Updated version of 3.0.3
