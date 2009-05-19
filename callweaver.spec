#
# Conditional build:
%bcond_with	simpledebug		# for safe_callweaver core dump storing
%bcond_with	zhone			# with zhone hack
%bcond_with	javascript		# with javascript support
#
%define	min_spandsp	1:0.0.6-0.pre12
Summary:	PBX in software
Summary(pl.UTF-8):	Programowy PBX
Name:		callweaver
Version:	1.2.1
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://devs.callweaver.org/release/callweaver-%{version}.tar.bz2
# Source0-md5:	54c2ba5852cbe43b802b4605584b5754
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
URL:		http://www.callweaver.org/
BuildRequires:	bluez-libs-devel
BuildRequires:	curl-devel
BuildRequires:	libcap-devel
BuildRequires:	libogg-devel
BuildRequires:	libpri-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libtiff-devel
BuildRequires:	libvorbis-devel
BuildRequires:	loudmouth-devel
BuildRequires:	mISDNuser-devel
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	spandsp-devel >= %{min_spandsp}
BuildRequires:	speex-devel
BuildRequires:	sqlite3-devel
BuildRequires:	unixODBC-devel
BuildRequires:	zaptel-devel >= 1.2
BuildRequires:	zlib-devel
Requires:	spandsp >= %{min_spandsp}
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open Source PBX and telephony toolkit. It is, in a sense, middleware
between Internet and telephony channels on the bottom, and Internet
and telephony applications at the top.

%description -l pl.UTF-8
PBX i zestaw narzędziowy do telefonii o otwartych źródłach. Jest to
middleware między kanałami internetowymi i telefonicznymi z dołu a
aplikacjami internetowymi i telefonicznymi z góry.

%package devel
Summary:	Header files for callweaver
Summary(pl.UTF-8):	Pliki nagłówkowe callweavera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for callweaver.

%description devel -l pl.UTF-8
Pliki nagłówkowe callweavera.

%if %{with simpledebug}
%define	no_install_post_strip	1
%endif

%prep
%setup -q

%{?with_zhone:sed -i -e 's|.*#define.*ZHONE_HACK.*|#define ZHONE_HACK 1|g' channels/chan_zap.c}

%build
%configure \
	--with-chan_misdn \
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

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d}
install -d $RPM_BUILD_ROOT%{_var}/spool/callweaver/voicemail

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 192 %{name}
%useradd -u 192 -d /var/lib/callweaver -s /bin/false -c "callweaver" -g %{name} %{name}

%post
/sbin/chkconfig --add %{name}
#%%service %%{name} restart


%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
        %userremove callweaver
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS CREDITS ChangeLog HARDWARE InstallGuide.txt README SECURITY sounds.txt
%doc doc
%dir %{_sysconfdir}/%{name}
%attr(640,root,callweaver) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so.*
%{_libdir}/%{name}/*.la
%dir %{_libdir}/%{name}/modules
%attr(755,root,root) %{_libdir}/%{name}/modules/*.so
%{_libdir}/%{name}/modules/*.la
%{_datadir}/%{name}
%{_mandir}/man*/*

%attr(750,callweaver,root) %dir %{_var}/lib/callweaver
%attr(750,callweaver,root) %dir %{_var}/lib/callweaver/core
%attr(750,callweaver,root) %dir %{_var}/log/callweaver
%attr(750,callweaver,root) %dir %{_var}/log/callweaver/*
%attr(750,callweaver,root) %dir %{_var}/run/callweaver
%attr(750,callweaver,root) %dir %{_var}/spool/callweaver
%attr(750,callweaver,root) %dir %{_var}/spool/callweaver/voicemail

%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
