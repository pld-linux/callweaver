# TODO:
# - user/group
# - fix init scripts
%bcond_with	misdn
%bcond_with	javascript
#
%define	_rc	rc3
Summary:	PBX in software
Name:		callweaver
Version:	1.2
Release:	0.1
License:	GPL
Group:		Applications
# pending name change; for now use old-name tarballs
Source0:	http://www.openpbx.org/releases/openpbx.org-%{version}_%{_rc}.tar.gz
# Source0-md5:	e270c40626dfa2131cc39dd1352b46f9
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.callweaver.org/
BuildRequires:	bluez-libs-devel
BuildRequires:	curl-devel
BuildRequires:	libogg-devel
BuildRequires:	libtiff-devel
BuildRequires:	libvorbis-devel
BuildRequires:	loudmouth-devel
%{?with_misdn:BuildRequires:	mISDN-devel}
BuildRequires:	mysql-devel
BuildRequires:	popt-devel
BuildRequires:	postgresql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	spandsp-devel >= 1:0.0.3
BuildRequires:	speex-devel
BuildRequires:	sqlite3-devel
BuildRequires:	unixODBC-devel
BuildRequires:	zaptel-devel
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open Source PBX and telephony toolkit. It is, in a sense, middleware
between Internet and telephony channels on the bottom, and Internet
and telephony applications at the top.

%package devel
Summary:        Header files and develpment documentation for callweaver
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and develpment documentation for callweaver.

%prep
%setup -q -n openpbx.org-%{version}_%{_rc}

%build
%configure \
	%{?with_misdn:--with-chan_misdn} \
	--with-chan_fax \
	--with-chan_bluetooth \
	--enable-odbc \
	--with-cdr_odbc \
	--with-res_config_odbc \
	--with-res_odbc \
	--enable-mysql \
	--with-cdr_mysql \
	--with-res_config_mysql \
	--enable-postgresql \
	--with-cdr_pgsql \
	--with-res_config_pgsql \
	--with-res_config_curl \
	--enable-jabber \
	--with-res_jabber \
%if %{with javascript}
	--enable-javascript \
	--with-res_js \
%endif
	--with-res_sqlite \
	--with-directory-layout=lsb

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS CREDITS ChangeLog HARDWARE InstallGuide.txt README SECURITY sounds.txt
%doc doc
%dir /etc/openpbx.org
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/openpbx.org/*.*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/openpbx.org
%attr(755,root,root) %{_libdir}/openpbx.org/*.so.*
%{_libdir}/openpbx.org/*.la
%dir %{_libdir}/openpbx.org/modules
%attr(755,root,root) %{_libdir}/openpbx.org/modules/*.so
%{_libdir}/openpbx.org/modules/*.la
%{_datadir}/openpbx.org
%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/openpbx
