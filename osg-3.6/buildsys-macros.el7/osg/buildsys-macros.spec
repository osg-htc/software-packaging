# Instructions:
# Just define osg_version and dver here, use osg-build rpmbuild, then
# "osg-koji import" the resulting rpm and osg-koji tag-pkg the build into the
# appropriate osg-*-development tag
# This will require koji admin permissions.
%define osg_version 3.6
%define dver   7

%define osgver %(tr -d . <<< %{osg_version})
%define dist .osg%{osgver}.el%{dver}

Name:		buildsys-macros
Summary:	Macros for the OSG Buildsystem
Version:        %{dver}
Release:	8%{dist}
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
* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 7-8.osg36.el7
- Cap _smp_ncpus_max to 12 (SOFTWARE-4728)

* Wed Feb 03 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 7-7.osg36.el7
- 3.6 el7 version
