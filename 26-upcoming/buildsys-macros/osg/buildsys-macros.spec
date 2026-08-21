%define osgver 26

%define dist .osg%{osgver}up.el%{rhel}

Name:           buildsys-macros
Summary:        Macros for the OSG Buildsystem
Version:        %{rhel}
Release:        1%{dist}
License:        GPL
BuildArch:      noarch
Requires:       redhat-release
Requires:       rpmdevtools

%description
Macros for the OSG Buildsystem

%prep

%build

%install
mkdir -p $RPM_BUILD_ROOT/etc/rpm/
echo "%%dist %{dist}"  >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
echo "%%osg 1"  >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
echo "%%_smp_ncpus_max 12"  >> $RPM_BUILD_ROOT/etc/rpm/macros.kojibuilder
echo "%%bcond_override_xrootd6 1"  >> $RPM_BUILD_ROOT/etc/rpm/macros.bcond
echo "%%_with_xrootd6 1"  >> $RPM_BUILD_ROOT/etc/rpm/macros.bcond


%files
/etc/rpm/macros.disttag
/etc/rpm/macros.kojibuilder
/etc/rpm/macros.bcond

%changelog
* Fri Aug 21 2026 Mátyás Selmeci <mselmeci@wisc.edu> - %{rhel}-1
- Use distro version as the version to satisfy dependencies of buildsys-build and buildsys-srpm-build
- Don't define %%rhel and %%el{8,9,10} - we get those from the OS

* Wed Aug 12 2026 Mátyás Selmeci <mselmeci@wisc.edu> - 26-1
- OSG 26 version

