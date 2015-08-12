Name:		voms-mysql-plugin
Version:	3.1.6
Release:	1.1%{?dist}
Summary:	VOMS server plugin for MySQL

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		https://wiki.italiangrid.it/twiki/bin/view/VOMS
#		This source tarball is created from a git checkout:
#		git clone git://github.com/italiangrid/voms-mysql-plugin.git
#		cd voms-mysql-plugin
#		git archive --format tar --prefix voms-mysql-plugin-3.1.6/ \
#		  3_1_6 | gzip - > ../voms-mysql-plugin-3.1.6.tar.gz
Source:		%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	voms-mysql = %{version}-%{release}
Obsoletes:	voms-mysql < 3.1.6
Requires:	voms-server%{?_isa}
BuildRequires:	libtool
BuildRequires:	mysql-devel%{?_isa}
BuildRequires:	openssl%{?_isa}

%description
The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for
authorization purposes.

This package offers the MySQL implementation for the VOMS server.

%prep
%setup -q
./autogen.sh

%build
%configure --libdir=%{_libdir}/voms --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/voms/libvomsmysql.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/voms/voms-mysql.data
%{_datadir}/voms/voms-mysql-compat.data
%dir %{_libdir}/voms
%{_libdir}/voms/libvomsmysql.so

%changelog
* Thu Aug 30 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.1.6-1.1.osg
- Release bump for koji

* Fri May 25 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.1.6-1
- Update to version 3.1.6 (EMI 2 version)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May 31 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.1.5.1-1
- Update to version 3.1.5.1

* Wed Mar 23 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.1.3.2-3
- Rebuild for mysql 5.5.10

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jun  6 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.1.3.2-1
- Update to version 3.1.3.2
- Drop all patches (accepted upstream)

* Thu Dec  3 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.1.3.1-1
- Update to version 3.1.3.1

* Sat Aug 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.1.1-1
- Update to version 3.1.1

* Tue Jun 30 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.1.0-1
- First build
