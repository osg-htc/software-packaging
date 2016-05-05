Name:      osg-version
Summary:   OSG Version
Version:   3.2.38
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
* Thu May 05 2016 Tim Theisen <tim@cs.wisc.edu> - 3.2.38-1
- Updated to 3.2.38-1

* Tue Apr 05 2016 Tim Theisen <tim@cs.wisc.edu> - 3.2.37-1
- Updated to 3.2.37-1

* Wed Feb 24 2016 Tim Theisen <tim@cs.wisc.edu> - 3.2.36-1
- Updated to 3.2.36-1

* Wed Feb 03 2016 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.35-1
- Updated to 3.2.35-1

* Thu Jan 06 2016 Brian Lin <blin@cs.wisc.edu> - 3.2.34-1
- Updated to 3.2.34-1

* Thu Dec 10 2015 Tim Theisen <tim@cs.wisc.edu> - 3.2.33-1
- Updated to 3.2.33-1

* Wed Dec 01 2015 Tim Theisen <tim@cs.wisc.edu> - 3.2.32-1
- Updated to 3.2.32-1

* Tue Nov 17 2015 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.2.31-1
- Updated to 3.2.31-1

* Wed Nov 04 2015 Brian Lin <blin@cs.wisc.edu> 3.2.30-1
- Updated to 3.2.30-1

* Fri Oct 30 2015 Tim Theisen <tim@cs.wisc.edu> - 3.2.29-1
- Updated to 3.2.29-1

* Fri Oct 09 2015 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.2.28-1
- Updated to 3.2.28-1

* Wed Sep 02 2015 Tim Theisen <tim@cs.wisc.edu> - 3.2.27-1
- Updated to 3.2.27-1

* Sun Aug 09 2015 Tim Theisen <tim@cs.wisc.edu> - 3.2.26-1
- Updated to 3.2.26-1

* Wed Jul 08 2015 Brian Lin <blin@cs.wisc.edu> - 3.2.25-1
- Updated to 3.2.25-1

* Fri Jun 05 2015 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.24-1
- Updated to 3.2.24-1

* Mon May 11 2015 Brian Lin <blin@cs.wisc.edu> - 3.2.23-1
- Updated to 3.2.23-1

* Wed Apr 08 2015 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.22-1
- Updated to 3.2.22-1

* Thu Mar 05 2015 Brian Lin <blin@cs.wisc.edu> - 3.2.21-1
- Updated to 3.2.21-1

* Fri Feb 06 2015 Tim Theisen <tim@cs.wisc.edu> - 3.2.20-1
- Updated to 3.2.20-1

* Tue Jan 09 2015 Brian Lin <blin@cs.wisc.edu> - 3.2.19-1
- Updated to 3.2.19-1

* Fri Dec 04 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.18-1
- Updated to 3.2.18-1

* Tue Nov 04 2014 Tim Theisen <tim@cs.wisc.edu> - 3.2.17-1
- Updated to 3.2.17-1

* Fri Oct 10 2014 Tim Theisen <tim@cs.wisc.edu> - 3.2.16-1
- Updated to 3.2.16-1

* Tue Aug 28 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.15-1
- Updated to 3.2.15-1

* Tue Aug 05 2014 Tim Theisen <tim@cs.wisc.edu> - 3.2.14-1
- Updated to 3.2.14-1

* Thu Jul 17 2014 Brian Lin <blin@cs.wisc.edu> - 3.2.13-1
- Updated to 3.2.13-1

* Thu Jul 03 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.12-1
- Updated to 3.2.12-1

* Wed Jun 04 2014 Brian Lin <blin@cs.wisc.edu> - 3.2.11-1
- Updated to 3.2.11-1

* Thu May 22 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.10-1
- Updated to 3.2.10-1

* Tue May 06 2014 Tim Theisen <tim@cs.wisc.edu> - 3.2.9-1
- Updated to 3.2.9-1

* Mon Mar 31 2014 Brian Lin <blin@cs.wisc.edu> 3.2.8-1
- Updated to 3.2.8-1

* Thu Mar 20 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2.7-1
- Updated to 3.2.7-1

* Tue Mar 4 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.6-1
- Updated to 3.2.6-1

* Tue Feb 25 2014 Brian Lin <blin@cs.wisc.edu> - 3.2.5-1
- Updated to 3.2.5-1

* Fri Feb 07 2014 Brian Lin <blin@cs.wisc.edu> - 3.2.4-1
- Updated to 3.2.4-1

* Fri Dec 13 2013 Tim Theisen <tim@cs.wisc.edu> - 3.2.2-1
- Updated to 3.2.2-1

* Thu Dec 05 2013 Tim Theisen <tim@cs.wisc.edu> - 3.2.1-1
- Updated to 3.2.1-1

* Tue Oct 29 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.2.0-1
- Updated to 3.2.0-1 -- forked from 3.1.25-1

