Summary:	OPIE suite of programs
Summary(pl):	Zestaw programów do OPIE
Name:		opie
Version:	2.4
Release:	10
Epoch:		1
License:	NRL/TIN
Group:		Applications/System
Source0:	http://inner.net/pub/opie/%{name}-%{version}.tar.gz
# Source0-md5:	d46e0ff8cc721a287892192dc4e7b7e1
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-ttyname.patch
Patch2:		%{name}-bison.patch
Patch3:		%{name}-acfix.patch
Patch4:		%{name}-errno.patch
Patch5:		%{name}-suse.patch
Patch6:		%{name}-uint4.patch
URL:		http://inner.net/opie
BuildRequires:	autoconf >= 2.52
BuildRequires:	bison
Requires:	%{name}-libs = %{epoch}:%{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OPIE suite of programs.

OPIE is an implementation of the One-Time Password (OTP) System that
is being considered for the Internet standards-track. OPIE provides a
one-time password system. The system should be secure against the
passive attacks now commonplace on the Internet (see RFC 1704 for more
details). The system is vulnerable to active dictionary attacks,
though these are not widespread at present and can be detected through
proper use of system audit software.

%description -l pl
Zestaw programów do OPIE.

OPIE jest implementacj± One-Time Password (OTP) System - systemu hase³
jednorazowych. Powinien on byæ odporny na popularne w Internecie ataki
pasywne (zobacz RFC 1704). Jest on podatny na ataki s³ownikowe, które
nie s± aktualnie szeroko rozpowszechnione.

%package libs
Summary:	OPIE shared libraries
Summary(pl):	Biblioteki wspó³dzielone OPIE
Group:		Libraries
Conflicts:	%{name} < 2.4-2

%description libs
OPIE (One-Time Password System) shared libraries.

%description libs -l pl
Biblioteki wspó³dzielone OPIE (systemu hase³ jednorazowych).

%package devel
Summary:	Headers for developing OPIE enabled programs
Summary(pl):	Nag³ówki do tworzenia programów z obs³ug± OPIE
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}
Requires:	FHS >= 2.2-9

%description devel
Headers for developing OPIE enabled programs.

%description devel -l pl
Pliki nag³ówkowe potrzebne do tworzenia programów z obs³ug± OPIE.

%package static
Summary:	OPIE static libraries
Summary(pl):	Statyczne biblioteki OPIE
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}

%description static
OPIE staic libraries.

%description static -l pl
Statyczne biblioteki OPIE.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p0

%build
%{__autoconf}
%configure \
	--enable-access-file=%{_sysconfdir}/opie/access \
	--enable-user-locking=/var/lib/opie \
	--enable-insecure-override

%{__make} DEBUG="%{rpmcflags} " \
	KEY_FILE=%{_sysconfdir}/opie/keys

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/opie,%{_sbindir},%{_libdir},%{_includedir}/security,/var/lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	KEY_FILE=%{_sysconfdir}/opie/keys

install opie.h $RPM_BUILD_ROOT%{_includedir}/security

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/opieinfo
%attr(755,root,root) %{_bindir}/opiekey
%attr(755,root,root) %{_bindir}/otp-*
%attr(4755,root,root) %{_bindir}/opiepasswd
%attr(4755,root,root) %{_sbindir}/opiesu
%attr(4755,root,root) %{_sbindir}/opielogin
%attr(750,root,root) %{_sbindir}/opieftpd
%dir %attr(700,root,root) /var/lib/opie
%{_mandir}/man*/*

%files libs
%defattr(644,root,root,755)
%doc BUG-REPORT README COPYRIGHT.NRL License.TIN
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_sysconfdir}/opie
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/opie/keys

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/security/opie.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
