Name:           koji-plugin-tag2distrepo
Version:        1.0.0
Release:        5%{?dist}
Summary:        Tag2distrepo plugin for koji-hub

Group:          Applications/System
License:        GPL 2.0
URL:            https://pagure.io/releng/tag2distrepo
Source:         %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  koji-hub
Requires:       koji-hub

Patch1: 0001-osg-build-opts.patch

%description
GPG signing plugin for koji-hub

%prep
%autosetup -p1

%build
exit 0


%install
mkdir -p $RPM_BUILD_ROOT
install -D tag2distrepo.py -m 0755 $RPM_BUILD_ROOT/usr/lib/koji-hub-plugins/tag2distrepo.py


%files
%attr(0755,root,root) /usr/lib/koji-hub-plugins/tag2distrepo.py*



%changelog
* Tue Jun 25 2024 Matt Westphall <westphall@wisc.edu> - 1.0.0-5
- Make 'latest' arg configurable (SOFTWARE-5911)

* Tue Jun 25 2024 Matt Westphall <westphall@wisc.edu> - 1.0.0-3
- Update args to distrepo to include 'src' as an arch (SOFTWARE-5911)

* Mon Jun 24 2024 Matt Westphall <westphall@wisc.edu> - 1.0.0-2
- Update args to distrepo in script (SOFTWARE-5911)

* Mon Jun 24 2024 Matt Westphall <westphall@wisc.edu> - 1.0.0-1
- Create initial release from upstream git repo (SOFTWARE-5911)

