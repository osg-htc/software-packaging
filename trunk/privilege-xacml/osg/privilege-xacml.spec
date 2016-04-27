## Turn off meaningless jar repackaging
%define __jar_repack 0

%define local_maven /tmp/m2-repository
#%define mvn /usr/share/apache-maven-3.0.4/bin/mvn
%define _noarchlib %{_exec_prefix}/lib
%define jglobus_version 2.1.0

%define _jar_version 2.6.5

Name:		privilege-xacml
Version:	2.6.5
Release:	2%{?dist}
Summary:	Core bindings for XACML interoperability profile.

Group:		OSG/Libraries
License:	Apache 2.0
URL:		http://github.com/opensciencegrid/privilege-xacml

Source0:	%{name}-%{version}.tar.gz
Patch10:        update-2.6.5-requirements.patch
Patch11:        Remove-voms-api-java-requirement.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

#define slf4j_version 1.5.8

BuildRequires: jpackage-utils
BuildRequires: java7-devel
BuildRequires: joda-time
BuildRequires: emi-trustmanager
BuildRequires: emi-trustmanager-axis
BuildRequires: wsdl4j
BuildRequires: log4j
BuildRequires: axis
BuildRequires: jglobus >= %jglobus_version

%if 0%{?rhel} < 7
BuildRequires: maven22
%define mvn mvn22

%define commons_logging jakarta-commons-logging
%define commons_codec jakarta-commons-codec
%define commons_discovery jakarta-commons-discovery
%define commons_lang jakarta-commons-lang

%else

BuildRequires: maven >= 3.0.0
%define mvn mvn
%define commons_logging apache-commons-logging
%define commons_codec apache-commons-codec
%define commons_discovery apache-commons-discovery
%define commons_lang apache-commons-lang
BuildRequires: maven-clean-plugin
BuildRequires: maven-install-plugin

%endif
BuildRequires: %commons_logging
BuildRequires: %commons_codec
BuildRequires: %commons_discovery
BuildRequires: %commons_lang

Requires: log4j
Requires: jglobus >= %jglobus_version
Requires: joda-time
Requires: emi-trustmanager
Requires: emi-trustmanager-axis
Requires: wsdl4j
Requires: axis
Requires: %commons_lang
Requires: %commons_codec
Requires: %commons_discovery
Requires: %commons_logging
Requires: java7

%description
%{summary}

%prep
%setup -n %{name}-%{version}
%patch10 -p1
%patch11 -p1

%build
mkdir -p %{local_maven}
pushd %{local_maven} # don't read project's pom file while we're just installing deps
#log4j
%{mvn} install:install-file -B -DgroupId=log4j -DartifactId=log4j -Dversion=1.2.14 -Dpackaging=jar -Dfile=`build-classpath log4j` -Dmaven.repo.local=%{local_maven}
#emi-trustmanager-axis
%{mvn} install:install-file -B -DgroupId=emi -DartifactId=emi-trustmanager-axis -Dversion=1.0.1 -Dpackaging=jar -Dfile=`build-classpath trustmanager-axis` -Dmaven.repo.local=%{local_maven}
#trustmanager
%{mvn} install:install-file -B -DgroupId=emi -DartifactId=emi-trustmanager -Dversion=3.0.3 -Dpackaging=jar -Dfile=`build-classpath trustmanager` -Dmaven.repo.local=%{local_maven}
#axis
%{mvn} install:install-file -B  -DgroupId=axis -DartifactId=axis -Dversion=1.4 -Dpackaging=jar -Dfile=`build-classpath axis/axis.jar` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=org.apache.axis  -DartifactId=axis-jaxrpc -Dversion=1.4 -Dpackaging=jar -Dfile=`build-classpath axis/jaxrpc.jar` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=axis -DartifactId=axis-wsdl4j -Dversion=1.5.2 -Dpackaging=jar -Dfile=`build-classpath wsdl4j` -Dmaven.repo.local=%{local_maven}
#jakarta dependencies commons-codec
%{mvn} install:install-file -B -DgroupId=commons-codec -DartifactId=commons-codec -Dversion=1.3 -Dpackaging=jar -Dfile=`build-classpath %commons_codec` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=commons-discovery -DartifactId=commons-discovery -Dversion=0.4 -Dpackaging=jar -Dfile=`build-classpath %commons_discovery` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=commons-discovery -DartifactId=commons-discovery -Dversion=2.4 -Dpackaging=jar -Dfile=`build-classpath %commons_lang` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=commons-logging -DartifactId=commons-logging-api -Dversion=1.0.4 -Dpackaging=jar -Dfile=`build-classpath %commons_logging` -Dmaven.repo.local=%{local_maven}
#Added the jglobus required jars to replace the old cog-jglobus deps
%{mvn} install:install-file -B -DgroupId=globus -DartifactId=jglobus-ssl-proxies -Dversion=%{jglobus_version} -Dpackaging=jar -Dfile=`build-classpath jglobus/ssl-proxies-%{jglobus_version}.jar` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=globus -DartifactId=jglobus-gss -Dversion=%{jglobus_version} -Dpackaging=jar -Dfile=`build-classpath jglobus/gss-%{jglobus_version}.jar` -Dmaven.repo.local=%{local_maven}
#joda-time
%{mvn} install:install-file -B -DgroupId=joda-time -DartifactId=joda-time -Dversion=1.5.2 -Dpackaging=jar -Dfile=`build-classpath joda-time` -Dmaven.repo.local=%{local_maven}
popd


%{mvn} -B -ff package -Dmaven.repo.local=%{local_maven}

%install
%define _otherlibs %{buildroot}%{_noarchlib}/%{name}
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_javadir}
install -m 755 target/%{name}-%{_jar_version}.jar %{buildroot}%{_javadir}/%{name}.jar
install -d -m 755 %{buildroot}/usr/share/maven3/poms
install -pm 644 pom.xml %{buildroot}/usr/share/maven3/poms/%{name}.pom
install -d  %{buildroot}%{_libexecdir}/%{name}
install -m 700 src/test/XACMLClientTest.sh %{buildroot}%{_libexecdir}/%{name}/XACMLClientTest.sh


install -d -m 755 %{_otherlibs}
build-jar-repository %{_otherlibs} jglobus trustmanager-axis trustmanager wsdl4j %commons_lang %commons_codec %commons_discovery %commons_logging joda-time axis/axis.jar axis/jaxrpc.jar log4j wsdl4j
install -pm 744 %{local_maven}/org/opensaml/opensaml/2.4.1/opensaml-2.4.1.jar %{_otherlibs}/opensaml-2.4.1.jar
install -pm 744 %{local_maven}/org/opensaml/xmltooling/*/*.jar  %{_otherlibs}/
install -pm 744 %{local_maven}/org/apache/santuario/xmlsec/1.4.1/xmlsec-1.4.1.jar %{_otherlibs}/xmlsec-1.4.1.jar
install -pm 744 %{local_maven}/velocity/velocity/1.5/velocity-1.5.jar %{_otherlibs}/velocity-1.5.jar
install -pm 744 %{local_maven}/xerces/xercesImpl/2.9.1/xercesImpl-2.9.1.jar %{_otherlibs}/xercesImpl-2.9.1.jar
install -pm 744	%{local_maven}/xerces/xmlParserAPIs/2.6.2/xmlParserAPIs-2.6.2.jar %{_otherlibs}/xmlParserAPIs-2.6.2.jar
install -pm 744 %{local_maven}/xalan/xalan/2.7.1/xalan-2.7.1.jar %{_otherlibs}/xalan-2.7.1.jar
install -pm 744 %{local_maven}/commons-collections/commons-collections/3.1/commons-collections-3.1.jar %{_otherlibs}/commons-collections-3.1.jar
install -pm 744 %{local_maven}/org/opensaml/openws/1.4.1/openws-1.4.1.jar %{_otherlibs}/openws-1.4.1.jar
install -pm 744 %{local_maven}/org/slf4j/slf4j-api/*/*.jar  %{_otherlibs}/
install -pm 744 %{local_maven}/org/slf4j/slf4j-simple/*/*.jar  %{_otherlibs}/



%clean
rm -rf %{buildroot}
rm -rf %{local_maven}
%files
%defattr(-,root,root,-)
%{_javadir}/%{name}.jar
/usr/share/maven3/poms/%{name}.pom
%{_noarchlib}/%{name}/*.jar
%{_libexecdir}/%{name}/XACMLClientTest.sh

%changelog
* Wed Apr 27 2016 Matyas Selmeci <matyas@cs.wisc.edu> 2.6.5-2
- Remove voms-api-java requirement (not used in production code) (SOFTWARE-2308)

* Tue Sep 15 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 2.6.5-1.osg
- Add changes for el7 build
- Update to 2.6.5
- Remove bouncycastle requirement
- Don't require system slf4j (it's not the version that gets used anyway)

* Mon Aug 17 2015 Carl Edquist <edquist@cs.wisc.edu> - 2.6.4-2
- Improved logging for mapping errors (SOFTWARE-1990)

* Fri Nov 21 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.6.4-1
- Final 2.6.4 release

* Wed Oct 29 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.6.4-0.1.rc1
- Updated to 2.6.4.rc1

* Tue Sep 16 2014 Edgar Fajardo <emfajard@ucsd.edu> - 2.6.3.1-2
- Added build requires maven22

* Tue Sep 16 2014 Brian Bockelman <bbockelm@cse.unl.edu> - 2.6.3.1-1
- Final 2.6.3 release.
- 2.6.3.1 fixes a release branching issue; 2.6.3 base should be ignored.

* Fri Jun 6 2014 Edgar Fajardo <emfajard@ucsd.edu> 2.6.3-0.1.rc1
- Updated to new tag 2.6.3.rc1

* Mon Jun 2 2014 Edgar Fajardo <emfajard@ucsd.edu> 2.6.2-1
- The WSDL code generator is now working.

* Wed May 7 2014 Edgar Fajardo <emfajard@ucsd.edu> 2.6.1-3
- The XACMLClientTest was moved from /usr/bin to /usr/libexec

* Tue May 6 2014 Edgar Fajardo <emfajard@ucsd.edu> 2.6.1-2
- Changed the non needed specific version on log4j

* Thu Mar 27 2014 Edgar Fajardo <emfajard@ucsd.edu> 2.6.1-1
- Initial packaging of privilege-xacml
