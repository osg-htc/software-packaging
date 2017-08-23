# 
# Copyright (c) 2017, SingularityWare, LLC. All rights reserved.
#
# Copyright (c) 2015-2017, Gregory M. Kurtzer. All rights reserved.
# 
# Copyright (c) 2016, The Regents of the University of California, through
# Lawrence Berkeley National Laboratory (subject to receipt of any required
# approvals from the U.S. Dept. of Energy).  All rights reserved.
# 
# This software is licensed under a customized 3-clause BSD license.  Please
# consult LICENSE file distributed with the sources of this project regarding
# your rights to use or distribute this software.
# 
# NOTICE.  This Software was developed under funding from the U.S. Department of
# Energy and the U.S. Government consequently retains certain rights. As such,
# the U.S. Government has been granted for itself and others acting on its
# behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software
# to reproduce, distribute copies to the public, prepare derivative works, and
# perform publicly and display publicly, and to permit other to do so. 
# 
# 


%{!?_rel:%{expand:%%global _rel 0.1}}

# This allows us to pick up the default value from the configure
%define with_slurm no
%if "%{with_slurm}" == "yes"
%define slurm 1
%else
%define slurm 0
%endif

Summary: Application and environment virtualization
Name: singularity
Version: 2.3.1
Release: %{_rel}.3%{?dist}
# https://spdx.org/licenses/BSD-3-Clause-LBNL.html
License: BSD-3-Clause-LBNL
Group: System Environment/Base
URL: http://singularity.lbl.gov/
Source: %{name}-%{version}.tar.gz
ExclusiveOS: linux
BuildRoot: %{?_tmppath}%{!?_tmppath:/var/tmp}/%{name}-%{version}-%{release}-root

%if %slurm
# NOTE: doing a direct file dependency because experience has shown there are a few
# site-local RPMs that have random pieces missing.
BuildRequires: /usr/include/slurm/spank.h
%endif

Requires: %name-runtime = %{version}-%{release}

%description
Singularity provides functionality to make portable
containers that can be used across host environments.

%package devel
Summary: Development libraries for Singularity
Group: System Environment/Development

%description devel
Development files for Singularity

%if %slurm
%package slurm
Summary: Singularity plugin for SLURM
Group: System Environment/Libraries
Requires: %{name}-runtime = %{version}-%{release}

%description slurm
The Singularity plugin for SLURM allows jobs to be started within
a container.  This provides a simpler interface to the user (they
don't have to be aware of the singularity executable) and doesn't
require a setuid binary.
%endif

%package runtime
Summary: Support for running Singularity containers
# For debugging in containers.                                                                                                                                                                   
Requires: strace ncurses-base
Group: System Environment/Base

%description runtime
This package contains support for running containers created by %name,
e.g. "singularity exec ...".

%prep
%setup


%build
if [ ! -f configure ]; then
  ./autogen.sh
fi

%configure \
%if %slurm
  --with-slurm
%else
  --without-slurm
%endif

%{__make} %{?mflags}


%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT %{?mflags_install}
rm -f $RPM_BUILD_ROOT/%{_libdir}/singularity/lib*.la

%post runtime -p /sbin/ldconfig
%postun runtime -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc examples AUTHORS.md CONTRIBUTING.md COPYRIGHT.md INSTALL.md LICENSE-LBNL.md LICENSE.md README.md
%attr(0755, root, root) %dir %{_sysconfdir}/singularity
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/singularity/*


%{_libexecdir}/singularity/cli/bootstrap.*
%{_libexecdir}/singularity/cli/copy.*
%{_libexecdir}/singularity/cli/create.*
%{_libexecdir}/singularity/cli/expand.*
%{_libexecdir}/singularity/cli/export.*
%{_libexecdir}/singularity/cli/import.*
%{_libexecdir}/singularity/cli/inspect.*
%{_libexecdir}/singularity/cli/pull.*
%{_libexecdir}/singularity/cli/selftest.exec
%{_libexecdir}/singularity/helpers
%{_libexecdir}/singularity/image-handler.sh
%{_libexecdir}/singularity/python



# Binaries
%{_libexecdir}/singularity/bin/bootstrap
%{_libexecdir}/singularity/bin/copy
%{_libexecdir}/singularity/bin/cleanupd
%{_libexecdir}/singularity/bin/create
%{_libexecdir}/singularity/bin/expand
%{_libexecdir}/singularity/bin/export
%{_libexecdir}/singularity/bin/get-section
%{_libexecdir}/singularity/bin/import
%{_libexecdir}/singularity/bin/mount

# Directories
%{_libexecdir}/singularity/bootstrap-scripts

#SUID programs
%attr(4755, root, root) %{_libexecdir}/singularity/bin/create-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/expand-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/export-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/import-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/mount-suid

%files runtime
%dir %{_libexecdir}/singularity
%{_libexecdir}/singularity/functions
%{_bindir}/singularity
%{_bindir}/run-singularity
%dir %{_localstatedir}/singularity
%dir %{_localstatedir}/singularity/mnt
%dir %{_localstatedir}/singularity/mnt/session
%dir %{_localstatedir}/singularity/mnt/container
%dir %{_localstatedir}/singularity/mnt/overlay
%{_libexecdir}/singularity/cli/action_argparser.*
%{_libexecdir}/singularity/cli/exec.*
%{_libexecdir}/singularity/cli/run.*
%{_libexecdir}/singularity/cli/mount.*
%{_libexecdir}/singularity/cli/shell.*
%{_libexecdir}/singularity/cli/singularity.help
%{_libexecdir}/singularity/cli/test.*
%{_libexecdir}/singularity/bin/action
%{_libdir}/singularity/lib*.so.*
%dir %{_sysconfdir}/singularity
%config(noreplace) %{_sysconfdir}/singularity/*
%{_mandir}/man1/singularity.1*
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/singularity


#SUID programs
%attr(4755, root, root) %{_libexecdir}/singularity/bin/action-suid


%files devel
%defattr(-, root, root)
%{_libdir}/singularity/lib*.so
%{_libdir}/singularity/lib*.a
%{_includedir}/singularity/*.h


%if %slurm
%files slurm
%defattr(-, root, root)
%{_libdir}/slurm/singularity.so
%endif

%changelog
* Tue Aug 2 2017 Edgar Fajardo <emfajard@ucsd.edu> 2.3.1-0.1.3
- Split the package bit into the runtime and main (SOFTWARE-2755)
- Update to upstream's singularity-2.3.1-0.1 singularity.spec

* Thu Jun  1 2017 Dave Dykstra <dwd@fbak,giv> - 2.3-0.1
- Update to upstream's singularity-2.3-0.1 singularity.spec

* Tue Feb 14 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 2.2.1-1
- Packaging bug release version of Singularity 2.2.1

* Thu Nov 10 2016 Derek Weitzel <dweitzel@cse.unl.edu> - 2.2-1
- First packaging of Singularity 2.2 for OSG

