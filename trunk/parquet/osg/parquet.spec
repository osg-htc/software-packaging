 
%define parquet_version 1.2.5 
%define parquet_patched_version 1.2.5-cdh4.7.1 
%define parquet_base_version 1.2.5 
%define parquet_release 1.cdh4.7.1.p0.9.1%{?dist}
%define cdh_customer_patch p0 
%define cdh_parcel_custom_version 1.2.5-1.cdh4.7.1.p0.9.1%{?dist}
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%define lib_parquet /usr/lib/parquet
%define hadoop_home /usr/lib/hadoop

# disable repacking jars
%define __os_install_post %{nil}

Name: parquet
Version: %{parquet_version}
Release: %{parquet_release}
Summary: A columnar storage format for Hadoop.
URL: http://parquet.io
Group: Development/Libraries
BuildArch: noarch
Buildroot: %(mktemp -ud %{_tmppath}/parquet-%{version}-%{release}-XXXXXX)
License: ASL 2.0 
Source0: parquet-%{parquet_patched_version}.tar.gz
Source1: do-component-build 
Source2: install_parquet.sh
Requires: hadoop, parquet-format

BuildRequires: java7-devel
BuildRequires: jpackage-utils
%if 0%{?rhel} >= 7
BuildRequires: maven >= 3.0.0
%else
BuildRequires: maven3
%endif

%description 
 Parquet-MR contains the java implementation of the Parquet format. Parquet is
 a columnar storage format for Hadoop; it provides efficient storage and
 encoding of data. Parquet uses the record shredding and assembly algorithm
 described in the Dremel paper to represent nested structures.

%prep
%setup -n parquet-%{parquet_patched_version}

%build
%if 0%{?rhel} < 7
export PATH=$PATH:/usr/share/apache-maven-3.0.4/bin
%endif
bash $RPM_SOURCE_DIR/do-component-build

%install
%__rm -rf $RPM_BUILD_ROOT
sh $RPM_SOURCE_DIR/install_parquet.sh \
          --build-dir=./ \
          --prefix=$RPM_BUILD_ROOT

#######################
#### FILES SECTION ####
#######################
%files 
%defattr(-,root,root,755)
%{lib_parquet}/*
%{hadoop_home}/*.jar

%changelog
* Tue Feb 23 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.2.5-1.cdh4.7.1.p0.9.1
- Add missing build dependencies (maven)

