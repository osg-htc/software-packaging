# Instructions:
# Just define osg_version and dver here, use osg-build rpmbuild, then
# "osg-koji import" the resulting rpm and osg-koji tag-pkg the build into the
# appropriate osg-*-development tag
# This will require koji admin permissions.
%define osg_version 24
%define dver   10

%define osgver 24
%define dist .osg%{osgver}int.el%{dver}

Name:		buildsys-macros
Summary:	Macros for the OSG Buildsystem
Version:        %{dver}
Release:	16%{dist}
License:	GPL
BuildArch:      noarch
Requires:	rpmdevtools

%description
Macros for the OSG Buildsystem

%prep

%build

%install
mkdir -p $RPM_BUILD_ROOT/etc/rpm/
DVER=%{dver}
OSGVER=%{osgver}
DIST=%{dist}
printf %s%b "%" "rhel $DVER\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "dist $DIST\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "el$DVER 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "osg 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "__arch_install_post /usr/lib/rpm/check-buildroot\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.checkbuild
printf %s%b "%" "_smp_ncpus_max 12\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.kojibuilder


%files
/etc/rpm/macros.disttag
/etc/rpm/macros.checkbuild
/etc/rpm/macros.kojibuilder

%changelog
* Thu Jun 19 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 10-16
- OSG 24 EL10 version (SOFTWARE-6165)

* Fri Aug 30 2024 Matt Westphall <westphall@wisc.edu> - 8-16.osg24int.el8
- build for osg 23 internal

* Thu Jul 27 2024 Matt Westphall <westphall@wisc.edu> - 9-9.osg24.el9
- osg 24 el9 version

* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 9-8.osg36.el7
- Cap _smp_ncpus_max to 12 (SOFTWARE-4728)

* Mon Dec 12 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 9-3.osg36.el9
- Bump to rebuild

* Thu Dec 08 2022 Carl Edquist <edquist@cs.wisc.edu> - 9-1.osg36.el9
- 3.6 el9 version (SOFTWARE-5395)

* Wed Feb 03 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 8-7.osg36.el8
- 3.6 el8 version
