%define	major 0
%define libname %mklibname radiusclient %{major}
%define develname %mklibname radiusclient -d

%define name	ppp
%define version	2.4.5
%define release	%mkrel 1

%define enable_inet6 1
%{?_with_inet6: %{expand: %%global enable_inet6 1}}
%{?_without_inet6: %{expand: %%global enable_inet6 0}}

%define enable_debug	0
%{?_with_debug: %global enable_debug 1}
%{?_without_debug: %global use_debug 0}

%define enable_radiusclient 0
%{?_with_radiusclient: %{expand: %%global enable_radiusclient 1}}
%{?_without_radiusclient: %{expand: %%global enable_radiusclient 0}}

Summary:	The PPP daemon and documentation for Linux 1.3.xx and greater
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Url:		http://www.samba.org/ppp/
Group:		System/Servers
Source0:	ftp://ftp.samba.org/pub/ppp/%{name}-%{version}.tar.bz2
Source1:	ppp-2.4.3-pam.conf
Source2:	ppp-2.4.1-mppe-crypto.tar.bz2
Source3:	README.pppoatm
Source4:	ppp.logrotate
Source5:	ppp-dhcpc.tar.bz2
Patch0:		ppp-2.4.5-make.patch
Patch1:		ppp-2.3.6-sample.patch
Patch2:		ppp-2.4.2-wtmp.patch
Patch4:		ppp-options.patch
Patch5:		ppp-2.4.3-pppdump-Makefile.patch
Patch6:		ppp-2.4.3-noexttraffic.patch
# (blino) use external libatm for pppoatm plugin
Patch7:		ppp-2.4.3-libatm.patch
Patch8: 	ppp-2.4.2-pie.patch
Patch9: 	ppp-2.4.4-multipledefrt.patch
Patch10:	ppp-2.4.4-dontwriteetc.patch
# (blino) http://orakel.tznetz.com/dload/ppp-2.4.4-mppe-mppc-1.1.patch.gz
# original patch on http://mppe-mppc.alphacron.de/
# (tpg) disable this patch, because it need a rediff and also there are some legal issues
# Although the module's source code is completely free, MPPC itself is patented algorithm.
#Patent for *Microsoft* PPC is holded by the  Hifn Inc. This is obvious ;-).
#Furthermore, MPPE uses RC4[1]  encryption algorithm which itself isn't patented,
#but RC4 is trademark of RSA Data Security Inc.
#To avoid legal problems, US citizens shouldn't use this module.
Patch11:	ppp-2.4.4-mppe-mppc-1.1.patch
Patch15:	ppp-2.4.3-pic.patch
Patch16:	ppp-2.4.3-etcppp.patch
Patch18:	ppp-2.4.5-includes-sha1.patch
Patch19:	ppp-2.4.5-makeopt2.patch
Patch20:	ppp-2.4.3-nostrip.patch
BuildRequires:	libatm-devel
BuildRequires:	libpcap-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pam-devel
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	glibc >= 2.0.6

%description
The ppp package contains the PPP (Point-to-Point Protocol) daemon
and documentation for PPP support.  The PPP protocol provides a
method for transmitting datagrams over serial point-to-point links.

The ppp package should be installed if your machine need to support
the PPP protocol.


%package	devel
Summary:	PPP devel files
Group:		Development/C
Requires:	%{name} = %{version}

%description	devel
PPP over ATM plugin for %{name}.

%package	pppoatm
Summary:	PPP over ATM plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description	pppoatm
PPP over ATM plugin for %{name}.

%package	pppoe
Summary:	PPP over ethernet plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description	pppoe
PPP over ethernet plugin for %{name}.

%package	radius
Summary:	Radius plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}
Requires:	radiusclient-utils

%description	radius
Radius plugin for %{name}.

%package	dhcp
Summary:	DHCP plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description	dhcp
DHCP plugin for %{name}.

%if %enable_radiusclient
%package -n	radiusclient-utils
Summary:	Radiusclient library
Group:		System/Servers
Requires:	%{libname} = %{version}-%{release}
Conflicts:	radiusclient

%description -n	radiusclient-utils
Radiusclient is a /bin/login replacement which gets called by a getty
to log in a user and to setup the user's login environment. Normal
login programs just check the login name and password which the user
entered against the local password file (/etc/passwd, /etc/shadow). In
contrast to that Radiusclient also uses the RADIUS protocol to
authenticate the user.

%package -n	%{libname}
Summary:	Radiusclient library
Group:		System/Libraries

%description -n	%{libname}
Libraries required for Radiusclient

%package -n	%{develname}
Summary:	Header files and development documentation for radiusclient
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	radiusclient-devel = %{version}-%{release}
Provides:	libradiusclient-devel = %{version}-%{release}

%description -n	%{develname}
Header files and development documentation for radiusclient.

%package -n	%{staticname}
Summary:	Static libraries for radiusclient
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}

%description -n	%{staticname}
Radiusclient static library.
%endif

%prep
%setup -q
find -type d -name CVS|xargs rm -rf
%patch0 -p1 -b .make
%patch1 -p1 -b .sample
%patch2 -p1 -b .wtmp
%patch4 -p1 -b .options
%patch5 -p1 -b .pppdump-Makefile

# (gg) add noext-traffic option
%patch6 -p1 -b .noext

%patch7 -p1 -b .libatm
%patch8 -p1 -b .pie
%patch9 -p1 -b .multipledefrt

tar -xjf %{SOURCE2}
pushd pppd/plugins
	tar -xjf %{SOURCE5}
popd

%patch10 -p1 -b .dontwriteetc
#%patch11 -p1 -b .mppe_mppc rediff?
%patch15 -p1 -b .pic
%patch16 -p1 -b .etcppp
%patch18 -p1 -b .incsha1
%patch19 -p1 -b .dhcp
%if %enable_debug
%patch20 -p1 -b .nostrip
%endif

# lib64 fixes
perl -pi -e "s|^(LIBDIR.*)\\\$\(DESTDIR\)/lib|\1\\\$(INSTROOT)%{_libdir}|g" pppd/Makefile.linux pppd/plugins/Makefile.linux pppd/plugins/{pppoatm,radius,rp-pppoe}/Makefile.linux
perl -pi -e "s|(--prefix=/usr)|\1 --libdir=%{_libdir}|g" pppd/plugins/radius/Makefile.linux
perl -pi -e "/_PATH_PLUGIN/ and s,(?:/usr/lib|DESTDIR (\")/lib),\$1%{_libdir},"  pppd/pathnames.h
# enable the dhcp plugin
perl -p -i -e "s|^(PLUGINS :=)|SUBDIRS += dhcp\n\$1|g" pppd/plugins/Makefile.linux

# fix /usr/local in scripts path
perl -pi -e "s|/usr/local/bin/pppd|%{_sbindir}/pppd|g;
	     s|/usr/local/bin/ssh|%{_bindir}/ssh|g;
	     s|/usr/local/bin/expect|%{_bindir}/expect|g" \
	scripts/ppp-on-rsh \
	scripts/ppp-on-ssh \
	scripts/secure-card

%if %enable_inet6
perl -pi -e "s/#HAVE_INET6/HAVE_INET6/" pppd/Makefile.linux
%endif

%build
# stpcpy() is a GNU extension
%if %enable_debug
OPT_FLAGS="%{optflags} -g -D_GNU_SOURCE"
%else
OPT_FLAGS="%{optflags} -D_GNU_SOURCE"
%endif
perl -pi -e "s/openssl/openssl -DOPENSSL_NO_SHA1/;" openssl/crypto/sha/Makefile

CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" %configure2_5x
# remove the following line when rebuilding against kernel 2.4 for multilink
#perl -pi -e "s|-DHAVE_MULTILINK||" pppd/Makefile
%make RPM_OPT_FLAGS="$OPT_FLAGS" LIBDIR=%{_libdir}
%make -C pppd/plugins -f Makefile.linux

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_sbindir},%{_bindir},/usr/X11R6/bin/,%{_mandir}/man8,%{_sysconfdir}/{ppp/peers,pam.d}}

%makeinstall LIBDIR=%{buildroot}%{_libdir}/pppd/%{version}/ INSTALL=install -C pppd/plugins/dhcp
%makeinstall INSTROOT=%{buildroot} SUBDIRS="pppoatm rp-pppoe radius"

%if %mdkversion >= 1020
%multiarch_includes %{buildroot}%{_includedir}/pppd/pathnames.h
%endif

# (gg) Allow stripping
chmod u+w %{buildroot}%{_sbindir}/*

%if !%enable_debug
# (florin) strip the binary
strip %{buildroot}%{_sbindir}/pppd
%endif

chmod go+r scripts/*
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/ppp
install -m 644 %{SOURCE3} %{_builddir}/%{name}-%{version}/

# (stew) fix permissions
chmod 0755 `find %{buildroot} -name "*\.so"`

# Provide pointers for people who expect stuff in old places
touch %{buildroot}/var/log/ppp/connect-errors
touch %{buildroot}/var/run/ppp/resolv.conf
ln -s ../../var/log/ppp/connect-errors %{buildroot}/etc/ppp/connect-errors
ln -s ../../var/run/ppp/resolv.conf %{buildroot}/etc/ppp/resolv.conf

# Logrotate script
mkdir -p %{buildroot}/etc/logrotate.d
install -m 644 %{SOURCE4} %{buildroot}/etc/logrotate.d/ppp

%if !%enable_radiusclient
rm -rf %{buildroot}%{_sbindir}/*rad*
rm -rf %{buildroot}%{_sysconfdir}/*rad*
rm -rf %{buildroot}%{_includedir}/*rad*
rm -rf %{buildroot}%{_libdir}/*rad*
%endif

%if %enable_debug
export DONT_STRIP=1
%endif

%if %enable_radiusclient
%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{develname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{develname} -p /sbin/ldconfig
%endif
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc FAQ PLUGINS README* scripts sample 
%{_sbindir}/chat
%{_sbindir}/pppdump
%attr(5755,root,root)	%{_sbindir}/pppd
%attr(0755,root,daemon)	%{_sbindir}/pppstats
%{_mandir}/man*/*
%exclude %{_mandir}/man8/*rad*
%dir %{_libdir}/pppd
%{_libdir}/pppd/%{version}
%exclude %{_libdir}/pppd/%{version}/pppoatm.so
%exclude %{_libdir}/pppd/%{version}/rp-pppoe.so
%exclude %{_libdir}/pppd/%{version}/rad*
%exclude %{_libdir}/pppd/%{version}/dhcpc.so
%dir %{_sysconfdir}/ppp
%dir /var/run/ppp 
/var/run/ppp/*
%attr(700, root, root) %dir /var/log/ppp
/var/log/ppp/*
%attr(0600,root,daemon)	%config(noreplace) %{_sysconfdir}/ppp/chap-secrets
%attr(0600,root,daemon)	%config(noreplace) %{_sysconfdir}/ppp/options
%attr(0600,root,daemon)	%config(noreplace) %{_sysconfdir}/ppp/pap-secrets
%attr(0600,root,daemon)	%{_sysconfdir}/ppp/connect-errors
%attr(0600,root,daemon)	%{_sysconfdir}/ppp/resolv.conf
%attr(755,root,daemon) %dir %{_sysconfdir}/ppp/peers
%config(noreplace) %{_sysconfdir}/pam.d/ppp
%config(noreplace) /etc/logrotate.d/ppp

%files devel
%defattr(-,root,root)
%doc README*
%{_includedir}/pppd/*
%if %mdkversion >= 1020
%multiarch %{multiarch_includedir}/pppd/pathnames.h
%endif

%files pppoatm
%defattr(-,root,root)
%doc README
%{_libdir}/pppd/%{version}/pppoatm.so

%files pppoe
%defattr(-,root,root)
%doc README
%{_libdir}/pppd/%{version}/rp-pppoe.so
%attr(755,root,root) %{_sbindir}/pppoe-discovery

%files radius
%defattr(-,root,root)
%doc README
%{_libdir}/pppd/%{version}/rad*.so
%{_mandir}/man8/*rad*

%files dhcp
%defattr(-,root,root)
%doc pppd/plugins/dhcp/README 
%doc pppd/plugins/dhcp/AUTHORS
%doc pppd/plugins/dhcp/COPYING
%{_libdir}/pppd/%{version}/dhcpc.so

%if %enable_radiusclient
%files -n radiusclient-utils
%defattr(644,root,root,755)
%doc pppd/plugins/radius/radiusclient/BUGS 
%doc pppd/plugins/radius/radiusclient/CHANGES 
%doc pppd/plugins/radius/radiusclient/README 
%doc pppd/plugins/radius/radiusclient/doc/*.html
%dir %{_sysconfdir}/radiusclient
%attr(644,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/radiusclient/*
%attr(755,root,root) %{_sbindir}/*rad*

%files -n %{libname}
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*rad*

%files -n %{staticname}
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
