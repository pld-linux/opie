Summary:	OPIE suite of programs
Name:		opie
Version:	2.32
Release:	2
Copyright:	NRL/TIN
Group:		Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	%{name}-%{version}.tar.gz
Patch0:		opie-shared.patch
Patch1:		opie-install.patch
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

%package devel
Summary:	libraries and headers for developing OPIE enabled programs
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Libraries and headers for developing OPIE enabled programs.

%package static
Summary:	OPIE staic libraries
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
OPIE staic libraries.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
LDFLAGS="-s"; export LDFLAGS
%configure \
	--enable-access-file=%{_sysconfdir}/opie/access \
	--enable-user-locking=/var/lib/opie

%{__make} DEBUG="$RPM_OPT_FLAGS" KEY_FILE=%{_sysconfdir}/opie/keys

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/opie,%{_sbindir},%{_libdir},%{_includedir}/security,/var/lib}

%{__make} install KEY_FILE=%{_sysconfdir}/opie/keys DESTDIR=$RPM_BUILD_ROOT

install opie.h $RPM_BUILD_ROOT%{_includedir}/security

strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*

gzip -9nf $RPM_BUILD_ROOT/%{_mandir}/man{1,4,5,8}/* \
	BUG-REPORT README COPYRIGHT.NRL License.TIN

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {BUG-REPORT,README,COPYRIGHT.NRL,License.TIN}.gz
%attr(0755,root,root) %{_bindir}/opieinfo
%attr(0755,root,root) %{_bindir}/opiekey
%attr(0755,root,root) %{_bindir}/otp-*
%attr(4755,root,root) %{_bindir}/opiepasswd
%attr(4755,root,root) %{_sbindir}/opiesu
%attr(4755,root,root) %{_sbindir}/opielogin
%attr(0750,root,root) %{_sbindir}/opieftpd
%attr(0755,root,root) %{_libdir}/lib*.so.*.*
%dir %attr(700,root,root) /var/lib/opie
%dir %{_sysconfdir}/opie
%attr(444,root,root) %{_sysconfdir}/opie/keys
%{_mandir}/man1/*
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/security/opie.h
%attr(755,root,root) %{_libdir}/lib*.so

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/lib*.a
