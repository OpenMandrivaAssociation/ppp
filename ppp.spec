%define	major	0
%define	libname	%mklibname radiusclient %{major}
%define	devname	%mklibname radiusclient -d

%bcond_without	inet6
%bcond_with	radiusclient
%bcond_without	uclibc

Summary:	The PPP daemon and documentation for Linux 1.3.xx and greater
Name:		ppp
Version:	2.4.6
Release:	1
License:	BSD-like
Url:		http://www.samba.org/ppp/
Group:		System/Servers
Source0:	ftp://ftp.samba.org/pub/ppp/%{name}-%{version}.tar.gz
Source1:	ppp-pam.conf
Source2:	ppp-logrotate.conf
Source3:	ppp-tmpfiles.conf
Source4:	ip-down
Source5:	ip-down.ipv6to4
Source6:	ip-up
Source7:	ip-up.ipv6to4
Source8:	ipv6-down
Source9:	ipv6-up
Source10:	ifup-ppp
Source11:	ifdown-ppp
Source12:	ppp-watch.tar.xz

Source100:	ppp-2.4.1-mppe-crypto.tar.bz2
Source101:	ppp-dhcpc.tar.bz2
Source102:	README.pppoatm

Patch101:	0001-build-sys-use-gcc-as-our-compiler-of-choice.patch
Patch102:	0002-build-sys-enable-PAM-support.patch
Patch103:	0003-build-sys-utilize-compiler-flags-handed-to-us-by-rpm.patch
Patch104:	0004-doc-add-configuration-samples.patch
Patch105:	0005-build-sys-don-t-hardcode-LIBDIR-but-set-it-according.patch
Patch106:	0006-scritps-use-change_resolv_conf-function.patch
Patch107:	0007-build-sys-don-t-strip-binaries-during-installation.patch
Patch108:	0008-build-sys-use-prefix-usr-instead-of-usr-local.patch
Patch109:	0009-pppd-introduce-ipv6-accept-remote.patch
Patch110:	0010-build-sys-enable-CBCP.patch
Patch111:	0011-build-sys-don-t-put-connect-errors-log-to-etc-ppp.patch
Patch112:	0012-pppd-we-don-t-want-to-accidentally-leak-fds.patch
Patch113:	0013-everywhere-O_CLOEXEC-harder.patch
Patch114:	0014-everywhere-use-SOCK_CLOEXEC-when-creating-socket.patch
Patch115:	0015-pppd-move-pppd-database-to-var-run-ppp.patch
Patch116:	0016-rp-pppoe-add-manpage-for-pppoe-discovery.patch
Patch117:	0017-pppd-rebase-EAP-TLS-patch-v0.994.patch
Patch118:	0018-scritps-fix-ip-up.local-sample.patch
Patch119:	0019-sys-linux-rework-get_first_ethernet.patch
# fixes a selinux issue, not relevant
#Patch120:	0020-pppd-put-lock-files-in-var-lock-ppp.patch
Patch121:	0021-build-sys-compile-pppol2tp-plugin-with-RPM_OPT_FLAGS.patch
Patch122:	0022-build-sys-compile-pppol2tp-with-multilink-support.patch
Patch123:	0023-build-sys-install-rp-pppoe-plugin-files-with-standar.patch
Patch124:	0024-build-sys-install-pppoatm-plugin-files-with-standard.patch
Patch125:	0025-pppd-install-pppd-binary-using-standard-perms-755.patch

Patch1001:	ppp-2.3.6-sample.patch
Patch1004:	ppp-options.patch
Patch1005:	ppp-2.4.6-pppdump-Makefile.patch
Patch1006:	ppp-2.4.6-noexttraffic.patch
# (blino) use external libatm for pppoatm plugin
Patch1007:	ppp-2.4.3-libatm.patch
Patch1008:	ppp-2.4.6-pie.patch
Patch1009:	ppp-2.4.4-multipledefrt.patch
# (blino) http://orakel.tznetz.com/dload/ppp-2.4.4-mppe-mppc-1.1.patch.gz
# original patch on http://mppe-mppc.alphacron.de/
# (tpg) disable this patch, because it need a rediff and also there are some legal issues
# Although the module's source code is completely free, MPPC itself is patented algorithm.
#Patent for *Microsoft* PPC is holded by the  Hifn Inc. This is obvious ;-).
#Furthermore, MPPE uses RC4[1] encryption algorithm which itself isn't patented,
#but RC4 is trademark of RSA Data Security Inc.
#To avoid legal problems, US citizens shouldn't use this module.
Patch1011:	ppp-2.4.6-mppe-mppc-1.1.patch
Patch1015:	ppp-2.4.3-pic.patch
Patch1016:	ppp-2.4.3-etcppp.patch
Patch1018:	ppp-2.4.5-includes-sha1.patch
Patch1019:	ppp-2.4.5-makeopt2.patch
Patch1022:	ppp-2.4.5-libtool-tag.patch
Patch1023:	ppp-2.4.6-use-gnu-for-O_CLOEXEC-with-uclibc.patch
Patch1024:	ppp-2.4.6-enable-dhcp-plugin.patch
Patch1025:	ppp-2.4.6-pppstats-Makefile.patch
Patch1026:	ppp-2.4.6-fix-radius-plugin-build.patch

BuildRequires:	atm-devel
BuildRequires:	pcap-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pam-devel
BuildRequires:	libtool

%description
The ppp package contains the PPP (Point-to-Point Protocol) daemon
and documentation for PPP support.  The PPP protocol provides a
method for transmitting datagrams over serial point-to-point links.

The ppp package should be installed if your machine need to support
the PPP protocol.

%if %{with uclibc}
%package -n	uclibc-pppd
Summary:	uClibc-linked build of pppd
Group:		System/Servers
BuildRequires:	uClibc-devel >= 0.9.33.2-3

%description -n	uclibc-pppd
This package ships a build of pppd linked against uClibc.

It's primarily targetted for inclusion with the DrakX installer.
%endif

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

%if %{with radiusclient}
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

%package -n	%{devname}
Summary:	Header files and development documentation for radiusclient
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	radiusclient-devel = %{version}-%{release}
Provides:	libradiusclient-devel = %{version}-%{release}

%description -n	%{devname}
Header files and development documentation for radiusclient.

%package -n	%{staticname}
Summary:	Static libraries for radiusclient
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}

%description -n	%{staticname}
Radiusclient static library.
%endif

%prep
%setup -q -a 12 -a 100
pushd pppd/plugins
	tar -xjf %{SOURCE101}
popd
cp %{SOURCE102} .

%apply_patches

chmod go+r scripts/*
find scripts -type f | xargs chmod a-x
rm scripts/*~

%build
%if %mdvver >= 201200
%serverbuild_hardened
%else
%serverbuild
%endif

%configure2_5x
%make RPM_OPT_FLAGS="%{optflags}" CC=%{__cc}
%make CFLAGS="%{optflags}" -C ppp-watch

%if %{with uclibc}
pushd pppd
%{uclibc_cc} -I../include -I. -o pppd-uclibc main.c magic.c fsm.c lcp.c ipcp.c upap.c chap-new.c chap-md5.c md5.c ccp.c auth.c options.c demand.c utils.c sys-linux.c ipxcp.c tdb.c tty.c session.c ecp.c spinlock.c eap.c -lcrypt -lutil -Wall -Wno-deprecated-declarations %{uclibc_cflags} -Os -fwhole-program %{ldflags} -flto -Wl,-O2 %{ldflags} -Wl,--no-warn-common
popd
%endif

%install
install -d %{buildroot}%{_sysconfdir}/ppp/peers

make INSTROOT=%{buildroot} SUBDIRS="pppoatm rp-pppoe radius pppol2tp dhcp" ETCDIR=%{buildroot}%{_sysconfdir}/ppp RUNDIR=%{buildroot}%{_varrun}/ppp LOGDIR=%{buildroot}%{_logdir}/ppp install install-etcppp
make ROOT=%{buildroot} -C ppp-watch install


%if %{with uclibc}
install -m755 pppd/pppd-uclibc -D %{buildroot}%{uclibc_root}/sbin/pppd
%endif

# (gg) Allow stripping
chmod u+w %{buildroot}%{_sbindir}/*


# (stew) fix permissions
chmod 0755 `find %{buildroot} -name "*\.so"`

# Provide pointers for people who expect stuff in old places
touch %{buildroot}/var/log/ppp/connect-errors
touch %{buildroot}/var/run/ppp/resolv.conf

%if !%{with radiusclient}
rm -rf %{buildroot}%{_sbindir}/*rad*
rm -rf %{buildroot}%{_sysconfdir}/*rad*
rm -rf %{buildroot}%{_includedir}/*rad*
rm -rf %{buildroot}%{_libdir}/*rad*
%endif

# install pam config
install -p -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/pam.d/ppp

# install logrotate script
install -p -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/logrotate.d/ppp

# install tmpfiles drop-in
# not yet...
#install -p -m644 %{SOURCE3} -D %{buildroot}%{_tmpfilesdir}/ppp.conf

# install scripts (previously owned by initscripts package)
install -p -m755 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/ppp/ip-down
install -p -m755 %{SOURCE5} -D %{buildroot}%{_sysconfdir}/ppp/ip-down.ipv6to4
install -p -m755 %{SOURCE6} -D %{buildroot}%{_sysconfdir}/ppp/ip-up
install -p -m755 %{SOURCE7} -D %{buildroot}%{_sysconfdir}/ppp/ip-up.ipv6to4
install -p -m755 %{SOURCE8} -D %{buildroot}%{_sysconfdir}/ppp/ipv6-down
install -p -m755 %{SOURCE9} -D %{buildroot}%{_sysconfdir}/ppp/ipv6-up

install -p -m755 %{SOURCE10} -D %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ppp
install -p -m755 %{SOURCE11} -D %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifdown-ppp

%files
%doc FAQ PLUGINS README* scripts sample 
%{_sbindir}/chat
%{_sbindir}/pppdump
%attr(5755,root,root)	%{_sbindir}/pppd
%attr(0755,root,daemon)	%{_sbindir}/pppstats
%{_sbindir}/ppp-watch
%dir %{_sysconfdir}/ppp
%{_sysconfdir}/ppp/ip-up
%{_sysconfdir}/ppp/ip-down
%{_sysconfdir}/ppp/ip-up.ipv6to4
%{_sysconfdir}/ppp/ip-down.ipv6to4
%{_sysconfdir}/ppp/ipv6-up
%{_sysconfdir}/ppp/ipv6-down
%{_sysconfdir}/sysconfig/network-scripts/ifdown-ppp
%{_sysconfdir}/sysconfig/network-scripts/ifup-ppp
%{_mandir}/man8/chat.8*
%{_mandir}/man8/pppd.8*
%{_mandir}/man8/pppdump.8*
%{_mandir}/man8/pppstats.8*
%{_mandir}/man8/ppp-watch.8*
%dir %{_libdir}/pppd
%dir %{_libdir}/pppd/%{version}
%{_libdir}/pppd/%{version}/minconn.so
%{_libdir}/pppd/%{version}/openl2tp.so
%{_libdir}/pppd/%{version}/passprompt.so
%{_libdir}/pppd/%{version}/passwordfd.so
%{_libdir}/pppd/%{version}/pppol2tp.so
%{_libdir}/pppd/%{version}/winbind.so
%dir %{_varrun}/ppp 
%ghost %{_varrun}/ppp/resolv.conf
%attr(700, root, root) %dir %{_logdir}/ppp
%ghost %{_logdir}/ppp/connect-errors
%attr(0600,root,daemon) %config(noreplace) %{_sysconfdir}/ppp/eaptls-client
%attr(0600,root,daemon) %config(noreplace) %{_sysconfdir}/ppp/eaptls-server
%attr(0600,root,daemon)	%config(noreplace) %{_sysconfdir}/ppp/chap-secrets
%attr(0600,root,daemon)	%config(noreplace) %{_sysconfdir}/ppp/options
%attr(0600,root,daemon)	%config(noreplace) %{_sysconfdir}/ppp/pap-secrets
%attr(755,root,daemon) %dir %{_sysconfdir}/ppp/peers
%config(noreplace) %{_sysconfdir}/pam.d/ppp
%config(noreplace) %{_sysconfdir}/logrotate.d/ppp

%if %{with uclibc}
%files -n uclibc-pppd
%{uclibc_root}/sbin/pppd
%endif

%files devel
%doc README*
%dir %{_includedir}/pppd
%{_includedir}/pppd/*

%files pppoatm
%doc README
%{_libdir}/pppd/%{version}/pppoatm.so

%files pppoe
%doc README
%{_libdir}/pppd/%{version}/rp-pppoe.so
%attr(755,root,root) %{_sbindir}/pppoe-discovery
%{_mandir}/man8/pppoe-discovery.8*

%files radius
%doc README
%{_libdir}/pppd/%{version}/radattr.so
%{_libdir}/pppd/%{version}/radius.so
%{_libdir}/pppd/%{version}/radrealms.so
%{_mandir}/man8/pppd-radattr.8*
%{_mandir}/man8/pppd-radius.8*

%files dhcp
%doc pppd/plugins/dhcp/README 
%doc pppd/plugins/dhcp/AUTHORS
%doc pppd/plugins/dhcp/COPYING
%{_libdir}/pppd/%{version}/dhcpc.so

%if %{with radiusclient}
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
%attr(755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{devname}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*rad*

%files -n %{staticname}
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
