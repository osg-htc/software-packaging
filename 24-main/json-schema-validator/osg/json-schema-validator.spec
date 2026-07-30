#############################################
# Package description and other info        #
#############################################
Name:           json-schema-validator
Version:        2.3.0
Release:        3%{?dist}
Summary:        JSON Schema Validator
License:        MIT
URL:            https://github.com/pboettch/json-schema-validator

Source0:        %{name}-%{version}.tar.gz

#############################################
# Build dependencies                        #
#############################################
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  cmake-rpm-macros
BuildRequires:  nlohmann-json-devel

%description
JSON Schema Validator is a library for validating JSON data against JSON Schema.

%package devel
Summary: Development files for JSON Schema Validator
Requires: %{name} = %{version}-%{release}

%description devel
Header, unversioned .so, and CMake files for JSON Schema Validator.

#############################################
# To suppress some of the debug outputs     #
#############################################
#%%global debug_package %{nil}

#############################################
# RHEL 9 will try to build out of source,   #
# so that needs to be overridden.           #
#############################################
%if 0%{?rhel} > 8
%global __cmake_in_source_build 1
%endif

#############################################
# Beginning of the build + make workflow    #
#############################################
%prep
%autosetup
#%%autosetup -n %{srcname}-%{version}

%build
mkdir -p build
cd build
%cmake ..
%make_build

%install
cd build
%make_install

#############################################
# Enumeration of the files we expect to be  #
# installed upon completion                 #
#############################################
%files
%doc README.md
%license LICENSE
%{_libdir}/libnlohmann_json_schema_validator.so.*
%{_bindir}/format-json-schema
%{_bindir}/readme-json-schema
%{_bindir}/json-schema-validate

%files devel
%{_includedir}/nlohmann/
%{_libdir}/cmake/nlohmann_json_schema_validator
%{_libdir}/libnlohmann_json_schema_validator.so

#############################################
# Changelog, where the version X.X.X-Y is   #
# referring to major, minor, patch and      #
# packaging revision.                       #
#############################################
%changelog
* Wed Jul 29 2026 Mátyás Selmeci <mselmeci@wisc.edu> - 2.3.0-3
- Split runtime package from devel package to conform to Fedora Packaging Guidelines (SOFTWARE-6382)

* Wed Sep 24 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 2.3.0-2
- Bump to rebuild for x86_64 on EL10

* Wed Sep 18 2024 Justin Hiemstra <jhiemstra@wisc.edu> - 2.3.0-1
- CMake/spec file updates to make project more flexible.

* Wed Sep 18 2024 Justin Hiemstra <jhiemstra@wisc.edu> - 2.2.0-2
- Bump release version for building against aarch64

* Mon Jun 26 2023 Justin Hiemstra <jhiemstra@morgridge.org> - 2.2.0-1
- Initial RPM release
