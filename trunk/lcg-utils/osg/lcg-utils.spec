%if 0%{?rhel} <= 5
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%if 0%{?el5}
#python26 support for el5
%{!?python26_sitearch: %global python26_sitearch %(python26 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python26_support:  %global python26_support 1}
%global __os_install_post %{__multiple_python_os_install_post}
%endif


%{!?python_version: %global python_version %(%{__python} -c "import sys; print('%s.%s'%sys.version_info[:2])")}
%{!?python_version_nodot: %global python_version_nodot %(%{__python} -c "import sys; print('%s%s'%sys.version_info[:2])")}

## add filter setup
%{?filter_setup:
%filter_provides_in %{python_sitearch}.*\.so$
%filter_setup
}


Name:						lcg-utils
Version:					1.13.0
Release:					0%{?dist}
Summary:					Command line tools for wlcg storage system 
Group:						Applications/Internet
License:					ASL 2.0
URL:						https://svnweb.cern.ch/trac/lcgutil
# svn export http://svn.cern.ch/guest/lcgutil/lcg-util/trunk lcgutil
Source0:					http://grid-deployment.web.cern.ch/grid-deployment/dms/lcgutil/tar/%{name}/%{name}-%{version}.tar.gz 
BuildRoot:					%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
# exclude ppc architecture, compilation error internal to gcc on epel 5 for a dependency
# Bugzilla Ticket : 831264
ExcludeArch:				ppc 

BuildRequires:				CGSI-gSOAP-devel
BuildRequires:				gfal-devel
BuildRequires:				gridftp-ifce-devel
BuildRequires:				libtool
%if 0%{?el5}
BuildRequires:				e2fsprogs-devel
%else
BuildRequires:				libuuid-devel	
%endif
BuildRequires:				python-devel
%if 0%{?python26_support}
BuildRequires:				python26-devel
%endif
BuildRequires:				srm-ifce-devel
BuildRequires:				swig
BuildRequires:				voms-devel
BuildRequires:                          globus-common-progs


%description
The LCG Utilities package is the main end user command line tool \
for data management provided by LCG \
(applications will generally use the Grid File Access Library).

%package libs
Summary:					Shared library related to %{name} tools
Group:						Applications/Internet

%description libs
Shared libraries component for %{name}

%package devel
Summary:					Headers and development files for %{name} tools
Group:						Applications/Internet
Requires:					%{name}-libs%{?_isa} = %{version}-%{release} 

%description devel
This package contains development files for %{name} 

%package python
Summary:					Python bindings for %{name}
Group:						Applications/Internet
Provides:					%{name}-py%{python_version_nodot} = %{version}
Requires:					%{name}-libs%{?_isa} = %{version}-%{release} 

%description python
python bindings for %{name}

%if 0%{?python26_support}
%package python26
Summary:					Python 2.6 bindings for %{name}
Group:						System Environment/Libraries
Provides:					%{name}-py26 = %{version}
Obsoletes:					%{name}-py26 < %{version}
Requires:					%{name}-libs%{?_isa} = %{version}-%{release} 

%description python26
python 2.6 bindings for %{name}
%endif

%prep
%setup -q
%if 0%{?python26_support}
mkdir -p %{_builddir}/%{name}-py26-%{version};
cp -rf %{_builddir}/%{name}-%{version}/* %{_builddir}/%{name}-py26-%{version};
cd %{_builddir}/%{name}-%{version};
%endif

%build
mkdir -p src/autogen; 
aclocal -I m4-EPEL/; 
libtoolize --force; 
autoheader; 
automake --foreign --add-missing --copy; 
autoconf
%configure \
--with-version=%{version} \
--with-release=%{release} \
--with-gfal-location=/ \
--with-voms-location=/ \
--with-emi \
--with-pythonrelease=%{python_version} \
--disable-static \
--enable-epel
make %{?_smp_mflags}

%if 0%{?python26_support}
cd %{_builddir}/%{name}-py26-%{version};
mkdir -p src/autogen; 
aclocal -I m4-EPEL/; 
libtoolize --force; 
autoheader; 
automake --foreign --add-missing --copy; 
autoconf;
%{configure} \
--with-version=%{version} \
--with-release=%{release} \
--with-gfal-location=/ \
--with-voms-location=/ \
--with-emi \
--with-pythonrelease=2.6 \
--disable-static \
--disable-tests \
--enable-epel
make %{?_smp_mflags} 
cd %{_builddir}/%{name}-%{version};
%endif

%check
make check

%install
rm -rf %{buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} install;
# clear libtool files
rm -f %{buildroot}/%{_libdir}/liblcg_util.*a
rm -f %{buildroot}/%{python_sitearch}/_lcg_util.*a

%if 0%{?python26_support}
cd %{_builddir}/%{name}-py26-%{version};
make %{?_smp_mflags} DESTDIR=%{buildroot} install;
# clear libtool files
rm -f %{buildroot}/%{_libdir}/liblcg_util.*a
rm -f %{buildroot}/%{python26_sitearch}/_lcg_util.*a
cd %{_builddir}/%{name}-%{version};
%endif

#Fix doc dir names

mv $RPM_BUILD_ROOT%{_docdir}/lcg-util-1.13.0 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%defattr (-,root,root)
%{_libdir}/liblcg_util.so.*
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/README_LIBS
%{_docdir}/%{name}-%{version}/RELEASE-NOTES


%files devel
%defattr (-,root,root)
%{_includedir}/lcg_util.h
%{_mandir}/man3/*
%{_libdir}/liblcg_util.so

%files python
%defattr (-,root,root)
%{python_sitearch}/lcg_util.py*
%{python_sitearch}/_lcg_util.so
%{python_sitearch}/_lcg_util.so.*
%{_docdir}/%{name}-%{version}/README_PYTHON

%if 0%{?python26_support}
%files python26
%defattr (-,root,root)
%{python26_sitearch}/lcg_util.py*
%{python26_sitearch}/_lcg_util.so
%{python26_sitearch}/_lcg_util.so.*
%endif


%files
%defattr (-,root,root)
%{_docdir}/%{name}-%{version}/VERSION
%{_docdir}/%{name}-%{version}/LICENSE
%{_docdir}/%{name}-%{version}/README
%{_mandir}/man1/*
%{_bindir}/*



%changelog
* Fri Jul 20 2012 Adrien Devresse <adevress at cern.ch> - 1.13.0-0
 - gfal 1.0 32 bits problem correction (gfal)
 - stack smash correction
 - srm timeout management (srm-ifce)
 - gridftpv2 support (gridftp-ifce) 
 - first EPEL / EMI update synchronisation

* Tue Jun 12 2012 <adevress at cern.ch> - 1.12.0-6
 - First EPEL import
 
* Tue Jun 12 2012 <adevress at cern.ch> - 1.12.0-5.2012061214snap
 - First update from comments of the review

* Mon Apr 16 2012 <adevress at cern.ch> - 1.12.0-5.2012060109snap
 - add unit test execution
 - improve EPEL compliance.

* Mon Apr 16 2012 <adevress at cern.ch> - 1.12.0-4
 - fix python26 support

* Tue Mar 13 2012 <adevress at cern.ch> - 1.12.0-3
 - first corrections from the EPEL review

* Fri Mar 02 2012 <adevress at cern.ch> - 1.12.0-2
 - fix the compilation for the ppc architecture
 
* Tue Dec 13 2011 <adevress at cern.ch> - 1.12.0-1
 - Initial build 
