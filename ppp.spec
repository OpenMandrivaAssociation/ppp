%define	major 0
%define libname %mklibname radiusclient %{major}
%define develname %mklibname radiusclient -d

%define name	ppp
%define version	2.4.5
%define release	10

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
Patch21:	ppp-2.4.5-pppol2tpv3.patch
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
#%patch11 -p1 -b .mppe_mppc
%patch15 -p1 -b .pic
%patch16 -p1 -b .etcppp
%patch18 -p1 -b .incsha1
%patch19 -p1 -b .dhcp
%if %enable_debug
%patch20 -p1 -b .nostrip
%endif
%patch21 -p1 -b .pppol2tpv3

# lib64 fixes
perl -pi -e "s|^(LIBDIR.*)\\\$\(DESTDIR\)/lib|\1\\\$(INSTROOT)%{_libdir}|g" pppd/Makefile.linux pppd/plugins/Makefile.linux pppd/plugins/{pppoatm,radius,rp-pppoe,pppol2tp}/Makefile.linux
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
%makeinstall INSTROOT=%{buildroot} SUBDIRS="pppoatm rp-pppoe radius pppol2tp"

%multiarch_includes %{buildroot}%{_includedir}/pppd/pathnames.h

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
%{multiarch_includedir}/pppd/pathnames.h

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


%changelog
* Mon Jul 04 2011 Александр Казанцев <kazancas@mandriva.org> 2.4.5-6mdv2011.0
+ Revision: 688624
- fix spec due missing install openl2tp plugins

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.5-5
+ Revision: 661713
- multiarch fixes

* Mon Apr 18 2011 Eugeni Dodonov <eugeni@mandriva.com> 2.4.5-4
+ Revision: 655830
- Disable mppe-mppc patch as it breaks networkmanager (#16737)

* Sat Dec 04 2010 Funda Wang <fwang@mandriva.org> 2.4.5-3mdv2011.0
+ Revision: 608655
- patch to build with latest kernel

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Fri Jun 11 2010 Eugeni Dodonov <eugeni@mandriva.com> 2.4.5-2mdv2010.1
+ Revision: 547901
- Rediffed P11 (required for #16737).

* Thu Dec 31 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4.5-1mdv2010.1
+ Revision: 484614
- fix compiling on x86_64 by adding -fPIC flag
- update to new version 2.4.5
- merge makeopt patches into one patch 3
- diable patch 11
- rediff patch 18 and 19
- drop patches 12(fixed upstream), 21(unknown status) and 22(fixed upstream)
- update to new version 2.4.5

* Tue May 26 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.4.4-10mdv2010.0
+ Revision: 380029
- Fix build

* Wed Dec 17 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4.4-9mdv2009.1
+ Revision: 315253
- rediffed fuzzy patches

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4.4-8mdv2009.1
+ Revision: 298351
- rebuilt against libpcap-1.0.0

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 2.4.4-7mdv2009.0
+ Revision: 265533
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Jun 03 2008 Olivier Blin <oblin@mandriva.com> 2.4.4-6mdv2009.0
+ Revision: 214490
- rename new keepdefaultroute option as multipledefaultroutes

* Mon Jun 02 2008 Olivier Blin <oblin@mandriva.com> 2.4.4-5mdv2009.0
+ Revision: 214331
- delete route for current ppp interface only (when shutting down the connection)

* Mon Jun 02 2008 Olivier Blin <oblin@mandriva.com> 2.4.4-4mdv2009.0
+ Revision: 214300
- add keepdefaultroute option (to keep existing default routes)

* Fri Apr 04 2008 Olivier Blin <oblin@mandriva.com> 2.4.4-3mdv2008.1
+ Revision: 192326
- fix plugins path on x86_64 (#31794)

* Fri Feb 01 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4.4-2mdv2008.1
+ Revision: 160951
- new license policy
- spec file clean
- change buildrequires to libatm-devel

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Aug 20 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 2.4.4-1mdv2008.0
+ Revision: 68088
- rebuild


* Mon Nov 27 2006 Olivier Blin <oblin@mandriva.com> 2.4.4-1mdv2007.0
+ Revision: 87708
- use common make install for pppoatm plugin
- run lib64 fixes on plugin sub-makefiles as well
- adapt lib64 to latest ppp makefiles
- fix plugins installation
- really enable the dhcp plugin
- remove useless mkdir commands
- use updated mppe-mppc patch (from Michael Gschwandtner)
- drop cve-2006-2194 patch (merged upstream)
- drop passargv patch (merged upstream)
- rediff dontwriteetc patch
- use new INSTROOT variable for make install
- remove lcp_close patch (merged upstream, and our version looks incorrect BTW)
- 2.4.4
- drop merged patch13

* Thu Aug 10 2006 Olivier Blin <oblin@mandriva.com> 2.4.3-12mdv2007.0
+ Revision: 54763
- P23: security fix for CVE-2006-2194 (from Vincent Danen)
- import ppp-2.4.3-11mdv2007.0

* Tue Jul 11 2006 Olivier Blin <oblin@mandriva.com> 2.4.3-11mdv2007.0
- drop ppp-prompt package since it depends on gtk1
  (from Crispin Boylan, #23521)
- don't try to uncompress Source6, it's dropped
  (and duplicated official tarball parts...)
- drop Patch12, we don't want to build contrib stuff
- don't use pam_stack in pam.d config file

* Wed Jan 11 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.4.3-10mdk
- add BuildRequires: libtool

* Sun Aug 28 2005 Giuseppe Ghib� <ghibo@mandriva.com> 2.4.3-9mdk
- /etc/ppp/peers is not a file, removed from
  %%config(noreplace) list.
- Added missed CFLAGS to Patch3 (makeopt) and Patch19.
- Added Patch17 (make room for argv[4]).
- Added Patch18 (fix includes, merged from RH).
- Added Patch20 (don't let install scripts do strip of binaries).
- Added Patch21 (fix some function prototype and include, merged from RH). 
- Added Patch22 (add support for higher speeds according to bits/termios.h).

* Sat Aug 06 2005 Olivier Blin <oblin@mandriva.com> 2.4.3-8mdk
- do an lcp_close whenever the link terminates, not just if it
  terminates because of an error, this is needed for persist
  to work properly (Patch9 from CVS, possible fix for #16748)
- removes Requires on release

* Thu Jul 14 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4.3-7mdk
- rebuilt against new libpcap-0.9.1 (aka. a "play safe" rebuild)

* Fri Jun 03 2005 Pascal Terjan <pterjan@mandriva.org> 2.4.3-6mdk
- allow building with ipv6 support and enable it by default

* Sat Apr 23 2005 Olivier Blin <oblin@mandriva.com> 2.4.3-5mdk
- really use 2.4.3 tarball !
- rediff Patch0, Patch3, Patch5, Patch6, Patch10, Patch12, Patch15
- update man path in Patch12
- drop Patch9, Patch14 (merged upstream)
- use new internal pppoatm (drop Patch7)
- use external libatm for pppoatm (new Patch7)
- drop Patch16 since we use the real ppp-2.4.3 now ...
- drop radiusclient workaround
  (no more radiusclient subdir with configure stuff)
- fix install in MANDIR, INCDIR, RUNDIR and LOGDIR
- really install ppp files in etc (Patch16)
- ship pppoe-discovery in ppp-pppoe
- remove spurious man8 dir

* Wed Feb 02 2005 Olivier Blin <oblin@mandrakesoft.com> 2.4.3-4mdk
- do not mark symbolic links as config files (#13090)
- really ship README.pppoatm

* Tue Feb 01 2005 Olivier Blin <blino@mandrake.org> 2.4.3-3mdk
- multiarch support

* Tue Jan 18 2005 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 2.4.3-2mdk
- fix patchlevel (P16), pppd reported versions as 2.4.2 and not 2.4.3

* Mon Jan 17 2005 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 2.4.3-1mdk
- 2.4.3
- update mppe/mppc patch (P11)
- drop P13( merged upstream)
- pppgetpass has been silently dropped from upstream, ship it in own source (S6)
- fix summary-ended-with-dot
- fix cvs-internal-file

* Thu Oct 07 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.2-9mdk
- lib64 fixes

* Tue Sep 21 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.2-8mdk
- build DSO with PIC
- -pie & 64-bit fixes

* Wed Aug 25 2004 Olivier Blin <blino@mandrake.org> 2.4.2-7mdk
- fix infinite loop in pty program kill

* Sat Jun 19 2004 Florin <florin@mandrakesoft.com> 2.4.2-6mdk
- move the prompt program to ppp-prompt package (depends on gtk)
- add resolv.conf and connect-errors files
- the mppe syntax has changed (see the www.polbox.com/h/hs001/ page
for more info on this)

* Fri Jun 18 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.4.2-5mdk
- add BuildRequires: libgtk+-devel

* Thu Jun 17 2004 Florin <florin@mandrakesoft.com> 2.4.2-4mdk
- fix peers permissions

* Sun Jun 13 2004 Florin <florin@mandrakesoft.com> 2.4.2-3mdk
- enable the radius plugin/package
- strip the binary
- add the existing radiusclient files
- spec file cleaning
- add the dhcp plugin (source 5)
- build the password prompt (contrib patch)

* Wed Jun 02 2004 Florin <florin@mandrakesoft.com> 2.4.2-2mdk
- use a different pppoatm patch

* Tue May 25 2004 Florin <florin@mandrakesoft.com> 2.4.2-1mdk
- 2.4.2
- update the make, makeopt, wtmp patch
- remove the pam_session, zfree, mppe, includes, libdir, filter
- pppoe, disconnect, gcc, pcap, varargs obsolete patches
- add the includes files
- add the README.pppoatm FAQ PLUGINS files
- add the logrotate patch and file (rh)
- add the pie, dontwriteetc patches (rh)

* Fri Feb 27 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.4.1-13mdk
- Own dir (distlint)
- patch31 - fix build against pcap

