Summary:	EVER UPS monitoring utilities
Summary(pl.UTF-8):	Narzędzia do monitorowania zasilaczy awaryjnych UPS firmy EVER
Name:		powersoft
Version:	1.1.1b
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://www.ever.com.pl/pliki/%{name}-%{version}.tar.gz
# Source0-md5:	3130716579a1af34620ebf0fe16f4134
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-nostrip.patch
Patch1:		%{name}-ppc.patch
Patch2:		%{name}-exit.patch
URL:		http://www.ever.com.pl/powersoft_prod.php
BuildRequires:	ncurses-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	SysVinit
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/powersoft
%define		_wwwdir		/home/services/httpd/powersoft
# statpage.htm refers to cgi-bin/psnet.cgi
%define		_cgidir		/home/services/httpd/posersoft/cgi-bin

%description
This package contains some utilities for EVER UPS monitoring.

%description -l pl.UTF-8
Ten zestaw programów służy do monitorowania pracy zasilaczy awaryjnych
UPS firmy EVER Sp. z o.o. o oznaczeniu DPC.

%package cgi
Summary:	CGI interface for EVER UPS monitoring service
Summary(pl.UTF-8):	Interfejs CGI do monitorowania zasilaczy awaryjnych UPS firmy EVER
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description cgi
CGI interface for EVER UPS monitoring service.

%description cgi -l pl.UTF-8
Interfejs CGI do monitorowania zasilaczy awaryjnych UPS firmy EVER.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} \
	CC="%{__cc}" \
	DEBUG="%{rpmcflags} -I/usr/include/ncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/var/run,%{_sysconfdir},/etc/{rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT{%{_wwwdir},%{_cgidir}}

install powersoft psstat $RPM_BUILD_ROOT%{_sbindir}
install powersoft.conf $RPM_BUILD_ROOT%{_sysconfdir}
install scripts/{pwrfail,pwrok,pshalt.msg,pshalt.sms,messages} $RPM_BUILD_ROOT%{_sysconfdir}

install psnet.cgi $RPM_BUILD_ROOT%{_cgidir}
install statpage.htm $RPM_BUILD_ROOT%{_wwwdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/powersoft
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/powersoft

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add powersoft
if [ -f /var/lock/subsys/powersoft ]; then
	/etc/rc.d/init.d/powersoft restart >&2
else
	echo "Run \"/etc/rc.d/init.d/powersoft start\" to start powersoft daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/powersoft ]; then
		/etc/rc.d/init.d/powersoft stop >&2
	fi
	/sbin/chkconfig --del powersoft
fi

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO LICENCJA
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/powersoft
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/powersoft
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/powersoft.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pshalt.msg
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pshalt.sms
%attr(750,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/messages
%attr(750,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pwrfail
%attr(750,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pwrok

%files cgi
%defattr(644,root,root,755)
%dir %{_wwwdir}
%{_wwwdir}/statpage.htm
%dir %{_cgidir}
%attr(755,root,root) %{_cgidir}/psnet.cgi
