Summary:	OPIE suite of programs
Summary(pl):	Zestaw programów do OPIE
Name:		opie
Version:	2.4
Release:	1
Epoch:		1
License:	NRL/TIN
Group:		Libraries
Source0:	http://inner.net/pub/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-makefile.patch
#BuildRequires:	autoconf
#BuildRequires:	automake
BuildRequires:	bison
URL:		http://inner.net/opie
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

%package devel
Summary:	Libraries and headers for developing OPIE enabled programs
Summary(pl):	Biblioteki i nag³ówki konieczne do tworzenia programów z obs³ug± OPIE
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and headers for developing OPIE enabled programs.

%description -l pl devel
Biblioteki i nag³ówki konieczne do tworzenia programów z obs³ug± OPIE.

%package static
Summary:	OPIE static libraries
Summary(pl):	Statyczne biblioteki OPIE
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
OPIE staic libraries.

%description -l pl static
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

gzip -9nf BUG-REPORT README COPYRIGHT.NRL License.TIN

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(0755,root,root) %{_bindir}/opieinfo
%attr(0755,root,root) %{_bindir}/opiekey
%attr(0755,root,root) %{_bindir}/otp-*
%attr(4755,root,root) %{_bindir}/opiepasswd
%attr(4755,root,root) %{_sbindir}/opiesu
%attr(4755,root,root) %{_sbindir}/opielogin
%attr(0750,root,root) %{_sbindir}/opieftpd
%attr(0755,root,root) %{_libdir}/lib*.so.*.*
%attr(444,root,root) %{_sysconfdir}/opie/keys
%dir %attr(700,root,root) /var/lib/opie
%dir %{_sysconfdir}/opie
%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/security/opie.h
%attr(755,root,root) %{_libdir}/lib*.so

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/lib*.a
