# Instructions:
# Define osgver and dver here, use osg-build rpmbuild, then
# "osg-koji import" the resulting rpm and osg-koji tag-pkg the build into the
# appropriate osg-*-development tag
# This will require koji admin permissions.
%define osgver 26
%define dver    8

%define dist .osg%{osgver}.el%{dver}

Name:           buildsys-macros
Summary:        Macros for the OSG Buildsystem
Version:        %{osgver}
Release:        1%{dist}
License:        GPL
BuildArch:      noarch
Requires:       rpmdevtools

%description
Macros for the OSG Buildsystem

%prep

%build

%install
mkdir -p $RPM_BUILD_ROOT/etc/rpm/
DVER=%{dver}
DIST=%{dist}
echo "%%rhel $DVER"  >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
echo "%%dist $DIST"  >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
echo "%%el$DVER 1"  >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
echo "%%osg 1"  >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
echo "%%_smp_ncpus_max 12"  >> $RPM_BUILD_ROOT/etc/rpm/macros.kojibuilder
echo "%%bcond_override_xrootd6 1"  >> $RPM_BUILD_ROOT/etc/rpm/macros.bcond
echo "%%_with_xrootd6 1"  >> $RPM_BUILD_ROOT/etc/rpm/macros.bcond


%files
/etc/rpm/macros.disttag
/etc/rpm/macros.kojibuilder
/etc/rpm/macros.bcond

%changelog
* Wed Aug 12 2026 Mátyás Selmeci <mselmeci@wisc.edu> - 26-1
- OSG 26 version

