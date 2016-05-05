Name:      osg-version
Summary:   OSG Version
Version:   3.3.12
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
* Thu May 05 2016 Tim Theisen <tim@cs.wisc.edu> 3.3.12-1
- Updated to 3.3.12-1

* Tue Apr 05 2016 Tim Theisen <tim@cs.wisc.edu> 3.3.11-1
- Updated to 3.3.11-1

* Wed Feb 24 2016 Tim Theisen <tim@cs.wisc.edu> 3.3.10-1
- Updated to 3.3.10-1

* Wed Feb 03 2016 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.3.9-1
- Updated to 3.3.9-1

* Wed Jan 06 2016 Brian Lin <blin@cs.wisc.edu> 3.3.8-1
- Updated to 3.3.8-1

* Thu Dec 10 2015 Tim Theisen <tim@cs.wisc.edu> 3.3.7-1
- Updated to 3.3.7-1

* Wed Dec 01 2015 Tim Theisen <tim@cs.wisc.edu> 3.3.6-1
- Updated to 3.3.6-1

* Wed Nov 17 2015 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.3.5-1
- Updated to 3.3.5-1

* Wed Nov 04 2015 Brian Lin <blin@cs.wisc.edu> 3.3.4-1
- Updated to 3.3.4-1

* Fri Oct 30 2015 Tim Theisen <tim@cs.wisc.edu> 3.3.3-1
- Updated to 3.3.3-1

* Fri Oct 09 2015 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.3.2-1
- Updated to 3.3.2-1

* Wed Sep 02 2015 Tim Theisen <tim@cs.wisc.edu> 3.3.1-1
- Updated to 3.3.1-1

* Wed Jun 10 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3.0-1
- Updated to 3.3.0-1

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

