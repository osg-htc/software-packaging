%global srcname sqlite_orm

Name:           sqlite-orm-devel
Version:        1.8.2
Release:        1%{?dist}
Summary:        SQLite ORM library for modern C++

License:        AGPL-3.0 and MIT
URL:            https://github.com/fnc12/sqlite_orm

Source0:        %{srcname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  sqlite-devel

%description
%{summary}

Used as a dependency for lotman.


%global debug_package %{nil}

%if 0%{?rhel} > 8
%global __cmake_in_source_build 1
%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
mkdir -p build
cd build
%cmake -DBUILD_TESTING=OFF ..
%make_build

%install
cd build
%make_install

%files
%{_includedir}/sqlite_orm/
%{_libdir}/cmake/SqliteOrm/*.cmake

%changelog
* Tue Jul 28 2026 Mátyás Selmeci <mselmeci@wisc.edu> - 1.8.2-1.osg
- Initial RPM release (SOFTWARE-6381)
