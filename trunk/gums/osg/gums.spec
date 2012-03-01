
%define _noarchlib %{_exec_prefix}/lib
%define dirname gums
%define local_maven /tmp/m2-repository
# Don't want to repack jars
%define __os_install_post %{nil}

Name: gums
Summary: Grid User Management System.  Authz for grid sites
Version: 1.3.18.008
Release: 1%{?dist}
License: Unknown
Group: System Environment/Daemons
BuildRequires: maven2
BuildRequires: java-devel
Requires: java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

# Tarball can be generated by doing the following:
# svn export http://svn.usatlas.bnl.gov/svn/privilege/tags/gums-1.3.18.008 gums
# tar zcf gums-1.3.18.008.tar.gz gums/
Source0: %{name}-%{version}.tar.gz

Source3: gums-host-cron

Source4: gums-client-cron.cron
Source5: gums-client-cron.init

# Binary JARs not available from public maven repos.  To be eliminated, one-by-one.
Source6:  glite-security-trustmanager-2.5.5.jar
Source7:  glite-security-util-java-2.8.6.jar
Source8:  jta-1.0.1B.jar
Source9:  jacc-1.0.jar
#Source10: xml-apis-2.9.1.jar
#Source11: xercesImpl-2.9.1.jar
Source12: opensaml-2.2.2.jar
Source13: privilege-xacml-2.2.4.jar
Source14: privilege-1.0.1.3.jar
Source15: xmltooling-1.1.1.jar
Source16: xmltooling.pom 
Source17: maven-surefire-plugin-2.4.3.jar

Patch0: gums-build.patch
Patch1: gums-add-mysql-admin.patch
Patch2: gums-setup-mysql-database.patch
Patch3: gums-create-config.patch
Patch5: xml-maven2.patch

%description
%{summary}

%package client
Requires: %{name} = %{version}
Requires: osg-vo-map
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): chkconfig
Group: System Environment/Daemons
Summary: Clients for GUMS

%description client
%{summary}

%package service
Requires: %{name} = %{version}
Requires: /usr/share/java/xml-commons-apis.jar
Requires: tomcat5
Requires: emi-trustmanager-tomcat
Requires: mysql-server
Group: System Environment/Daemons
Summary: Tomcat5 service for GUMS

%description service
%{summary}

%prep

%setup -n %{name}
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch5 -p0

%build

# Binary JARs not available from public maven repos.
# gums-core
mvn install:install-file -B -DgroupId=org.glite -DartifactId=glite-security-trustmanager -Dversion=2.5.5 -Dpackaging=jar -Dfile=%{SOURCE6} -Dmaven.repo.local=%{local_maven}
mvn install:install-file -B -DgroupId=org.glite -DartifactId=glite-security-util-java -Dversion=2.8.6 -Dpackaging=jar -Dfile=%{SOURCE7} -Dmaven.repo.local=%{local_maven}
mvn install:install-file -B -DgroupId=javax.transaction -DartifactId=jta -Dversion=1.0.1B -Dpackaging=jar -Dfile=%{SOURCE8} -Dmaven.repo.local=%{local_maven}
mvn install:install-file -B -DgroupId=javax.security -DartifactId=jacc -Dversion=1.0 -Dpackaging=jar -Dfile=%{SOURCE9} -Dmaven.repo.local=%{local_maven}
# gums-client
mvn install:install-file -B -DgroupId=org.opensaml -DartifactId=xmltooling -Dversion=1.1.1 -Dpackaging=jar -DpomFile=%{SOURCE16} -Dfile=%{SOURCE15} -Dmaven.repo.local=%{local_maven}
#mvn install:install-file -B -DgroupId=org.opensaml -DartifactId=opensaml -Dversion=2.2.2 -Dpackaging=jar -Dfile=%{SOURCE12} -Dmaven.repo.local=%{local_maven}
mvn install:install-file -B -DgroupId=org.opensciencegrid -DartifactId=privilege -Dversion=1.0.1.3 -Dpackaging=jar -Dfile=%{SOURCE14} -Dmaven.repo.local=%{local_maven}
mvn install:install-file -B -DgroupId=org.opensciencegrid -DartifactId=privilege-xacml -Dversion=2.2.4 -Dpackaging=jar -Dfile=%{SOURCE13} -Dmaven.repo.local=%{local_maven}
#mvn install:install-file -B -DgroupId=org.apache.xerces -DartifactId=xercesImpl -Dversion=2.9.1 -Dpackaging=jar -Dfile=%{SOURCE11} -Dmaven.repo.local=%{local_maven}
#mvn install:install-file -B -DgroupId=org.apache.xerces -DartifactId=xml-apis -Dversion=2.9.1 -Dpackaging=jar -Dfile=%{SOURCE10} -Dmaven.repo.local=%{local_maven}

pushd gums-core
mvn -B -e -Dmaven.repo.local=/tmp/m2-repository -Dmaven.test.skip=true install
popd
pushd gums-client
mvn -B -Dmaven.repo.local=/tmp/m2-repository -Dmaven.test.skip=true install
popd
pushd gums-service
mvn -B -Dmaven.repo.local=/tmp/m2-repository -Dmaven.test.skip=true install
popd

%install

function replace_jar {
    if [[ -e $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/lib/$1 ]]; then
        rm -f $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/lib/$1
        ln -s %{_noarchlib}/%{dirname}/$1 $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/lib/$1
    fi
}
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

# JARs
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/endorsed
install -m 0644 gums-client/target/lib/*.jar $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/
install -m 0644 gums-core/target/*.jar $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/
install -m 0644 gums-client/target/lib/endorsed/*.jar $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/endorsed/

# Service
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/
pushd $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/
jar xf $OLDPWD/gums-service/target/gums.war 
popd
rm $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/config/gums.config
ln -s %{_sysconfdir}/%{dirname}/gums.config $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/config

# Hack: we want slf4j-api-1.5.5 in core, but that's not what comes with
# it. Get it from the exploded WAR instead.
install -m 0644 $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/lib/slf4j-api-1.5.5.jar $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/

## Link the exploded WAR to gums-core JARs, instead of including a copy
for x in $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/*.jar; do
    replace_jar $(basename $x)
done

## gums-core and gums-service use different versions here...
rm -f $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/lib/slf4j-jdk14-1.5.2.jar


# Scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 gums-client/src/main/scripts/* $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/gums-host-cron
install -m 0755 gums-service/src/main/resources/scripts/gums-setup-mysql-database $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 gums-service/src/main/resources/scripts/gums-add-mysql-admin $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 gums-service/src/main/resources/scripts/gums-create-config $RPM_BUILD_ROOT%{_bindir}/

# Configuration files
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}
install -m 0644 gums-client/src/main/config/*  $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/
install -m 0600 gums-service/src/main/config/gums.config $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}

# Templates
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/sql
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/config
install -m 0644 gums-service/src/main/resources/sql/{addAdmin,setupDatabase}.mysql $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/sql/
install -m 0644 gums-service/src/main/resources/gums.config.template $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/config/

# Log directory
mkdir -p $RPM_BUILD_ROOT/var/log/%{dirname}

mkdir -p $RPM_BUILD_ROOT/var/lib/osg
cat > $RPM_BUILD_ROOT/var/lib/osg/user-vo-map << EOF
# This is an empty user-vo-map.
# Run gums-host-cron to generate a real one.
EOF

cat > $RPM_BUILD_ROOT/var/lib/osg/supported-vo-list << EOF
# This is an empty supported-vo-list.
# Run gums-host-cron to generate a real one.
EOF

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{init.d,cron.d}
mv %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/gums-client-cron
mv %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/gums-client-cron
chmod +x $RPM_BUILD_ROOT%{_sysconfdir}/init.d/gums-client-cron

%files
%defattr(-,root,root,-)
%dir %{_noarchlib}/%{dirname}
%dir %{_noarchlib}/%{dirname}/endorsed
%{_noarchlib}/%{dirname}/*.jar
%{_noarchlib}/%{dirname}/endorsed/*.jar

%files client
%defattr(-,root,root,-)
%{_bindir}/gums
%{_bindir}/gums-gridmapfile
%{_bindir}/gums-host
%{_bindir}/gums-host-cron
%{_bindir}/gums-nagios
%{_bindir}/gums-service
%{_bindir}/gums-vogridmapfile
%dir %{_sysconfdir}/%{dirname}
%config(noreplace) %{_sysconfdir}/%{dirname}/gums-client.properties
%config(noreplace) %{_sysconfdir}/%{dirname}/gums-nagios.conf
%config(noreplace) %{_sysconfdir}/%{dirname}/log4j.properties
%config(noreplace) /var/lib/osg/user-vo-map
%config(noreplace) /var/lib/osg/supported-vo-list
%dir /var/log/%{dirname}
%config(noreplace) %{_sysconfdir}/cron.d/gums-client-cron
%{_sysconfdir}/init.d/gums-client-cron

%post client
/sbin/chkconfig --add gums-client-cron

%preun client
if [ $1 -eq 0 ] ; then
    /sbin/service gums-client-cron stop >/dev/null 2>&1
    /sbin/chkconfig --del gums-client-cron
fi

%postun client
if [ "$1" -ge "1" ] ; then
    /sbin/service gums-client-cron condrestart >/dev/null 2>&1 || :
fi

%files service
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{dirname}
%attr(0600,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{dirname}/gums.config
%attr(0750,tomcat,tomcat) %dir %{_var}/lib/tomcat5/webapps/gums/WEB-INF/config
%{_var}/lib/tomcat5/webapps/gums
%{_noarchlib}/%{dirname}/sql
%{_noarchlib}/%{dirname}/config
%{_bindir}/gums-add-mysql-admin
%{_bindir}/gums-create-config
%{_bindir}/gums-setup-mysql-database

%changelog
* Wed Feb 29 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.008-1
- New version. Updated trustmanager.

* Mon Feb 20 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.006-2
- Fix for wrong version of slf4j-api in client

* Fri Feb 17 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.006-1
- New version.
- Build is now a multi-project

* Thu Feb 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.002-7
- Disabled jar repacking.
- Added /usr/share/java/xml-commons-apis.jar as a dependency to get around sun jdk falsely providing xml-commons-apis
- Cleaned up the way duplicate jar files are replaced with symlinks (replace_jar)

* Wed Nov 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.18.002-6
- Remove old copy of GUMS jar.  Remove ability to contact Archiva at BNL.

* Wed Nov 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.18.002-5
- Allow service to use the DNS hostname instead of DN for host mappings.  Allows glexec callouts without a hostcert for privileged user groups.
- Clean up some of the maven deps so this package can be built solely from the public maven repos; no BNL-private ones necessary.

* Sat Oct 08 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.18.002-4
- Add a minimal packaging of the service itself.

* Mon Aug 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.3.18.002-3
- Added init script for enabling/disabling gums-host-cron.

* Fri Jul 29 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.3.18.002-2
- Rewrite gums-host-cron to work with the RPM layout.

* Thu Jun 2 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.3.17-2
- Initial source RPM from GUMS website's binary tarball.

