%define _disable_ld_no_undefined %nil
%global optflags %{optflags} -fPIC -Wall -fno-strict-aliasing
%global build_ldflags %{build_ldflags} -pie

Summary:	The PPP daemon and documentation
Name:		ppp
Version:	2.5.0
Release:	1
License:	BSD-like
Group:		System/Servers
Url:		http://www.samba.org/ppp/
Source0:	https://github.com/ppp-project/ppp/archive/refs/tags/ppp-%{version}.tar.gz
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

Patch0006:	0006-scritps-use-change_resolv_conf-function.patch
Patch0011:	0011-build-sys-don-t-put-connect-errors-log-to-etc-ppp.patch
Patch0012:	ppp-2.4.8-pppd-we-don-t-want-to-accidentally-leak-fds.patch
Patch0013:	ppp-2.4.9-everywhere-O_CLOEXEC-harder.patch
Patch0014:	0014-everywhere-use-SOCK_CLOEXEC-when-creating-socket.patch
Patch0018:	0018-scritps-fix-ip-up.local-sample.patch

BuildRequires:  slibtool
BuildRequires:	libtool
BuildRequires:	atm-devel
BuildRequires:	pkgconfig(libpcap)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pam-devel
Requires(post):	systemd
Requires:	glibc >= 2.0.6
Conflicts:	initscripts < 9.54-1
%rename %{name}-dhcp

BuildSystem:	autotools
BuildOption:	--enable-cbcp
BuildOption:	--with-pam

%description
The ppp package contains the PPP (Point-to-Point Protocol) daemon
and documentation for PPP support.  The PPP protocol provides a
method for transmitting datagrams over serial point-to-point links.

The ppp package should be installed if your machine need to support
the PPP protocol.

%files
%doc FAQ README README.cbcp README.linux README.MPPE README.MSCHAP80 README.MSCHAP81 README.pwfd README.pppoe scripts sample README.eap-tls
%{_sbindir}/chat
%{_sbindir}/pppd
%{_sbindir}/pppdump
%{_sbindir}/pppoe-discovery
%{_sbindir}/pppstats
%{_sbindir}/ppp-watch
%dir %{_sysconfdir}/ppp
%{_sysconfdir}/ppp/ip-up
%{_sysconfdir}/ppp/ip-down
%{_sysconfdir}/ppp/ip-up.ipv6to4
%{_sysconfdir}/ppp/ip-down.ipv6to4
%{_sysconfdir}/ppp/ipv6-up
%{_sysconfdir}/ppp/ipv6-down
%{_mandir}/man8/chat.8*
%{_mandir}/man8/pppd.8*
%{_mandir}/man8/pppdump.8*
%{_mandir}/man8/pppd-radattr.8*
%{_mandir}/man8/pppd-radius.8*
%{_mandir}/man8/pppstats.8*
%{_mandir}/man8/pppoe-discovery.8*
%{_mandir}/man8/ppp-watch.8*
%{_libdir}/pppd
%ghost %dir %{_rundir}/ppp
%ghost %dir %{_rundir}/lock/ppp
%dir %{_sysconfdir}/logrotate.d
%attr(700, root, root) %dir %{_localstatedir}/log/ppp
%config(noreplace) %{_sysconfdir}/ppp/eaptls-client
%config(noreplace) %{_sysconfdir}/ppp/eaptls-server
%config(noreplace) %{_sysconfdir}/ppp/chap-secrets
%config(noreplace) %{_sysconfdir}/ppp/options
%config(noreplace) %{_sysconfdir}/ppp/openssl.cnf
%config(noreplace) %{_sysconfdir}/ppp/pap-secrets
%config(noreplace) %{_sysconfdir}/pam.d/ppp
%config(noreplace) %{_sysconfdir}/logrotate.d/ppp
%{_tmpfilesdir}/ppp.conf

%post
%tmpfiles_create %{_tmpfilesdir}/%{name}.conf

#----------------------------------------------------------------------------

%package devel
Summary:	PPP devel files
Group:		Development/C
Requires:	%{name} = %{EVRD}

%description devel
PPP over ATM plugin for %{name}.

%files devel
%doc README*
%{_includedir}/pppd/*
%{_libdir}/pkgconfig/pppd.pc

#----------------------------------------------------------------------------

%package pppoatm
Summary:	PPP over ATM plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{EVRD}

%description pppoatm
PPP over ATM plugin for %{name}.

%files pppoatm
%doc README
%{_libdir}/pppd/%{version}/pppoatm.so

#----------------------------------------------------------------------------

%package pppoe
Summary:	PPP over ethernet plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{EVRD}

%description pppoe
PPP over ethernet plugin for %{name}.

%files pppoe
%doc README
%{_libdir}/pppd/%{version}/pppoe.so
%{_sbindir}/pppoe-discovery

#----------------------------------------------------------------------------

%package radius
Summary:	Radius plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{EVRD}
Requires:	radiusclient-utils

%description radius
Radius plugin for %{name}.

%files radius
%doc README
%{_libdir}/pppd/%{version}/rad*.so
%{_mandir}/man8/*rad*

#----------------------------------------------------------------------------
%package -n network-scripts-%{name}
Summary:	PPP legacy network service support

%description -n network-scripts-%{name}
This provides the ifup and ifdown scripts for use with the legacy network
service.

%files -n network-scripts-%{name}
%{_sysconfdir}/sysconfig/network-scripts/ifdown-ppp
%{_sysconfdir}/sysconfig/network-scripts/ifup-ppp

%prep -a
tar xf %{S:12}
sed -i -e 's,/usr/sbin,%{_sbindir},g' ppp-watch/Makefile

slibtoolize --force
aclocal
autoheader
automake -a
autoconf

%build -a
%make_build -C ppp-watch CC="%{__cc}" CXX="%{__cxx}" CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LDFLAGS="%{build_ldflags} -pie"

%install -a
#make INSTROOT=%{buildroot} install install-etcppp
find scripts -type f | xargs chmod a-x
make ROOT=%{buildroot} -C ppp-watch install
# create log files dir
install -d %{buildroot}%{_localstatedir}/log/ppp
# install pam config
install -d %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/ppp
# install logrotate script
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 -p %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/ppp
# install tmpfiles drop-in
install -d %{buildroot}%{_tmpfilesdir}
install -m 644 -p %{SOURCE3} %{buildroot}%{_tmpfilesdir}/ppp.conf
# install scripts (previously owned by initscripts package)
install -d %{buildroot}%{_sysconfdir}/ppp
install -p %{SOURCE4} %{buildroot}%{_sysconfdir}/ppp/ip-down
install -p %{SOURCE5} %{buildroot}%{_sysconfdir}/ppp/ip-down.ipv6to4
install -p %{SOURCE6} %{buildroot}%{_sysconfdir}/ppp/ip-up
install -p %{SOURCE7} %{buildroot}%{_sysconfdir}/ppp/ip-up.ipv6to4
install -p %{SOURCE8} %{buildroot}%{_sysconfdir}/ppp/ipv6-down
install -p %{SOURCE9} %{buildroot}%{_sysconfdir}/ppp/ipv6-up
install -d %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/
install -p %{SOURCE10} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ppp
install -p %{SOURCE11} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifdown-ppp
# ghosts
mkdir -p %{buildroot}%{_rundir}/ppp
mkdir -p %{buildroot}%{_rundir}/lock/ppp
