Summary: Scitokens mapfile for OSG
Name: osg-scitokens-mapfile
Version: 4
Release: 1%{?dist}
License: ASL 2.0
Source0: https://github.com/opensciencegrid/topology/archive/data-%{version}.tar.gz
Source1: https://vdt.cs.wisc.edu/upstream/osg-scitokens-mapfile/pydeps/icalendar-4.0.7-py2.py3-none-any.whl
Source2: https://vdt.cs.wisc.edu/upstream/osg-scitokens-mapfile/pydeps/xmltodict-0.12.0-py2.py3-none-any.whl
BuildRequires: python3
BuildRequires: python3-pip
BuildRequires: python3-ldap3
%if 0%{?el7}
BuildRequires: python36-pytz
BuildRequires: python36-dateutil
BuildRequires: python36-PyYAML
BuildRequires: python36-six
%else
BuildRequires: python3-pytz
BuildRequires: python3-dateutil
BuildRequires: python3-pyyaml
BuildRequires: python3-six
%endif

%global debug_package %{nil}
%global __python /usr/bin/python3


%description
Contains file for mapping scitokens issuers to Unix users for OSG.


%prep
%setup -q -n topology-data-%{version}


%build
for whl in %{SOURCE1} %{SOURCE2}; do
    pip3 install --no-deps "$whl" --prefix $PWD
done
PYTHONPATH=$PYTHONPATH:$(echo "$PWD"/lib/python3*/site-packages)
export PYTHONPATH
./bin/get-scitokens-mapfile --regex --outfile osg-scitokens-mapfile.conf


%install
mkdir -p %{buildroot}/usr/share/condor-ce/mapfiles.d/
mv osg-scitokens-mapfile.conf %{buildroot}/usr/share/condor-ce/mapfiles.d/


%files
/usr/share/condor-ce/mapfiles.d/osg-scitokens-mapfile.conf


%changelog
* Thu Dec 16 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 4-1
- Update to data-4 tag (SOFTWARE-4854)
- Add ldap3 build requirement

* Wed Apr 28 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 3-1
- Update to data-3 tag (SOFTWARE-4572)

* Wed Apr 21 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 2-1
- Update to data-2 tag
- Use regex format and add .conf extension (SOFTWARE-4572)

* Thu Feb 11 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1-1
- First version (SOFTWARE-4453)

