Summary:	OPIE suite of programs
Summary(pl):	Zestaw program�w do OPIE
Name:		opie
Version:	2.4
Release:	2
Epoch:		1
License:	NRL/TIN
Group:		Applications/System
Source0:	http://inner.net/pub/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-makefile.patch
URL:		http://inner.net/opie
#BuildRequires:	autoconf
#BuildRequires:	automake
BuildRequires:	bison
Requires:	%{name}-libs = %{version}
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
Zestaw program�w do OPIE.

OPIE jest implementacj� One-Time Password (OTP) System - systemu hase�
jednorazowych. Powinien on by� odporny na popularne w Internecie ataki
pasywne (zobacz RFC 1704). Jest on podatny na ataki s�ownikowe, kt�re
nie s� aktualnie szeroko rozpowszechnione.

%package libs
Summary:	OPIE shared libraries
Summary(pl):	Biblioteki wsp�dzielone OPIE
Group:		Libraries
Conflicts:	%{name} < 2.4-2

%description libs
OPIE (One-Time Password System) shared libraries.

%description libs -l pl
Biblioteki wsp�dzielone OPIE (systemu hase� jednorazowych).

%package devel
Summary:	Headers for developing OPIE enabled programs
Summary(pl):	Nag��wki do tworzenia program�w z obs�ug� OPIE
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}

%description devel
Headers for developing OPIE enabled programs.

%description devel -l pl
Pliki nag��wkowe potrzebne do tworzenia program�w z obs�ug� OPIE.

%package static
Summary:	OPIE static libraries
Summary(pl):	Statyczne biblioteki OPIE
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
OPIE staic libraries.

%description static -l pl
Statyczne biblioteki OPIE.

%prep
%setup -q
%patch0 -p1

%build
%configure2_13 \
	--enable-access-file=%{_sysconfdir}/opie/access \
	--enable-user-locking=/var/lib/opie

%{__make} DEBUG="%{rpmcflags}" \
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
%attr(0755,root,root) %{_bindir}/opieinfo
%attr(0755,root,root) %{_bindir}/opiekey
%attr(0755,root,root) %{_bindir}/otp-*
%attr(4755,root,root) %{_bindir}/opiepasswd
%attr(4755,root,root) %{_sbindir}/opiesu
%attr(4755,root,root) %{_sbindir}/opielogin
%attr(0750,root,root) %{_sbindir}/opieftpd
%dir %attr(700,root,root) /var/lib/opie
%{_mandir}/man*/*

%files libs
%defattr(644,root,root,755)
%doc BUG-REPORT README COPYRIGHT.NRL License.TIN
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_sysconfdir}/opie
%attr(444,root,root) %{_sysconfdir}/opie/keys

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/security/opie.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
