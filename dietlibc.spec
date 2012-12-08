%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

%define snap 20090113

%define name	%{cross_prefix}dietlibc

# This is eventually a biarch package, so no %_lib for diethome
%define diethome %{_prefix}/lib/dietlibc

# Enable builds without testing (default shall always be testing)
%define build_check		0
%{expand: %{?_with_CHECK:	%%global build_check 1}}
%{expand: %{?_without_CHECK:	%%global build_check 0}}

# Enable cross compilation
%define build_cross		0
%{expand: %{?cross:		%%global build_cross 1}}
%if %{build_cross}
%define target_cpu		%{cross}
%define cross_prefix		cross-%{target_cpu}-
%define cross_make_flags	ARCH=%{target_cpu} CROSS=%{target_cpu}-linux-
%define build_check		0
%else
%define cross_prefix		%{nil}
%define cross_make_flags	%{nil}
%endif

Summary:	C library optimized for size
Name:		%{name}
Version:	0.32
Release:	%mkrel 4.%{snap}.8
License:	GPL
Group:		Development/Other
%if %{build_cross}
BuildRequires:	%{cross_prefix}gcc
%endif
URL:		http://www.fefe.de/dietlibc/
Source0:	http://www.fefe.de/dietlibc/dietlibc-%{version}-%{snap}.tar.gz
Source1:	build_cross_dietlibc.sh
Patch0:		dietlibc-0.29-features.patch
Patch1:		dietlibc-0.30-mdkconfig.patch
Patch3:		dietlibc-0.22-tests.patch
Patch5:		dietlibc-0.22-net-ethernet.patch
Patch6:		dietlibc-0.24-rpc-types.patch
Patch9:		dietlibc-0.27-glibc-nice.patch
Patch15:	dietlibc-0.27-ppc-rdtsc.patch
Patch16:	dietlibc-0.27-test-makefile-fix.patch
Patch17:	dietlibc-0.27-x86_64-stat64.patch
Patch18:	dietlibc-0.27-x86_64-lseek64.diff
Patch21:	dietlibc-0.24-ppc64-select.patch
Patch22:	dietlibc-0.27-ppc64-stat64.patch
Patch23:	dietlibc-0.29-biarch.patch
Patch24:	dietlibc-0.27-quiet.patch
Patch25:	dietlibc-0.27-ppc-select.patch
Patch26:	dietlibc-0.27-kernel2.6-types.patch
Patch27:	dietlibc-0.29-cross.patch
Patch29:	dietlibc-0.29-sparc-rdtsc-tick-noerror.patch
#Patch30:	dietlibc-0.29-sparc-disable-glob-test.patch
Patch31:	dietlibc-0.29-sparc-weak-asm.patch
Patch33:	dietlibc-0.29-fix-strncmp.patch
# (cjw) from PLD, see http://gcc.gnu.org/bugzilla/show_bug.cgi?id=26374
Patch34:	dietlibc-0.29-ppc-gcc-ldbl128.patch
Patch36:        dietlibc-0.30-relatime.patch
# (pixel) add -fno-stack-protector to override default %{optflags}
Patch37:	dietlibc-0.30-force-no-stack-protector.patch
Patch38:	dietlibc-0.32-fgetc.patch
Patch100:	dietlibc-0.28-setpriority.patch
Patch101:	dietlibc-0.29-scall.patch
Patch102:	dietlibc-0.31-defpath.patch
Patch103:	dietlibc-0.31-stacksmash.patch
Patch104:	dietlibc-0.31-stacksmash-dyn.patch
Patch105:	dietlibc-0.31.20080212-teststdout.patch
Patch106:	dietlibc-0.31-pagesize.patch
Patch107:	dietlibc-0.31-printFG.patch
Patch108:	dietlibc-0.31-testsuite.patch
Patch109:	dietlibc-0.31-lcctime.patch
Patch110:	dietlibc-0.31-implicitfunc.patch
Patch111:	dietlibc-0.31-noreturn.patch
Patch112:	dietlibc-0.32-20090113-fix_getpriority.patch
Patch113:	dietlibc-0.32-i386-types.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Small libc for building embedded applications.

%package	devel
Group:          Development/C
Summary:        Development files for dietlibc
%if %{build_cross}
# Requires main dietlibc package for "diet" program (dispatcher)
# XXX: build %{target_cpu}-linux-diet wrapper too?
Requires:	dietlibc >= %{version}
Requires:	%{cross_prefix}gcc
%endif
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description	devel
Small libc for building embedded applications.

%prep

%setup -q -n %{name}-%{version}-%{snap}

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch0 -p1 -b .features
%patch1 -p0 -b .mdkconfig
%patch3 -p1 -b .tests
%patch5 -p1 -b .net-ethernet
%patch6 -p1 -b .rpc-types
%patch9 -p1 -b .glibc-nice -E
%patch15 -p1 -b .ppc-rdtsc
%patch16 -p1 -b .inettest
%patch17 -p1 -b .x86_64-stat64
%patch18 -p0 -b .x86_64-lseek64
%patch21 -p1 -b .ppc64-select
#%patch22 -p1 -b .ppc64-stat64
%patch23 -p1 -b .biarch
%patch24 -p1 -b .quiet
%patch25 -p1 -b .ppc-select
%patch26 -p1 -b .kernel2.6-types
%patch27 -p0 -b .cross
%patch29 -p1 -b .sparc_rdtsc
#%patch30 -p1 -b .sparc_disable_glob_test
%patch31 -p1 -b .sparc_weak_asm
%patch33 -p1 -b .fix-strncmp
%patch34 -p1 -b .gcc-ppc-ldbl-bug
%patch36 -p1 -b .relatime
%patch37 -p1 -b .stack-protector
%patch38 -p0 -b .fgetc

# P100 - P111 is from fedora 
%patch100 -p1 -b .setpriority
%patch101 -p1 -b .scall
%patch102 -p1 -b .defpath
%patch103 -p1 -b .stacksmash
%patch104 -p1 -b .stacksmash-dyn
%patch105 -p1 -b .teststdout
%patch106 -p1 -b .pagesize
%patch107 -p1 -b .printFG
%patch108 -p1 -b .testsuite
%patch109 -p1 -b .lcctime
%patch110 -p1 -b .implicitfunc
%patch111 -p1 -b .noreturn

%patch112 -p1 -b .fix_getpriority
%patch113 -p0 -b .386_types
rm -f x86_64/getpriority.S

# fix execute permission on test scripts
chmod a+x test/{dirent,inet,stdio,string,stdlib,time}/runtests.sh

%build
%make %{cross_make_flags}

%check
# make and run the tests
%if %{build_check}
cd test; rm *.c.*
export DIETHOME="%{_builddir}/%{name}-%{version}-%{snap}"
MYARCH=`uname -m | sed -e 's/i[4-9]86/i386/' -e 's/armv[3-6][lb]/arm/'`
find -name "Makefile" | xargs perl -pi -e "s|^DIET.*|DIET=\"${DIETHOME}/bin-${MYARCH}/diet\"|g"
%make
cd ..
%endif

# run the tests
%if %{build_check}
cd test
STANDARD_TESTPROGRAMS=`grep "^TESTPROGRAMS" runtests.sh | cut -d\" -f2`
# these fails: cp-test3 cp-test4 cp-test6 cp-test7 cp-test11 cp-test12 cp-test15
CP_TEST_PROGRAMS="cp-test1 cp-test2 cp-test5 cp-test8 cp-test9 cp-test10 cp-test13 cp-test14"
perl -pi -e "s|^TESTPROGRAMS.*|TESTPROGRAMS=\"${STANDARD_TESTPROGRAMS} ${CP_TEST_PROGRAMS}\"|g" runtests.sh
# getpass requires user input
perl -pi -e "s|^PASS.*|PASS=\"\"|g" runtests.sh
sh ./runtests.sh
cd ..
%endif

%install
rm -rf %{buildroot}

make %{cross_make_flags} DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files devel
%defattr(-,root,root)
%doc AUTHOR BUGS CAVEAT CHANGES README THANKS TODO FAQ
%if ! %{build_cross}
%{_bindir}/diet
%{_mandir}/man*/*
%dir %{diethome}
%dir %{diethome}/include
%{diethome}/include/*
%endif
%dir %{diethome}/lib-*
%{diethome}/lib-*/*


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.32-4.20090113.7mdv2011.0
+ Revision: 663773
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.32-4.20090113.6mdv2011.0
+ Revision: 604789
- rebuild

* Fri May 21 2010 Pascal Terjan <pterjan@mandriva.org> 0.32-4.20090113.5mdv2010.1
+ Revision: 545621
- Fix dev_t (and others) size on ix86, stat would need to be fixed too

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 0.32-4.20090113.4mdv2010.1
+ Revision: 520080
- rebuilt for 2010.1

* Fri Oct 09 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.32-4.20090113.3mdv2010.0
+ Revision: 456249
- Fix broken getpriority (#53430).

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0.32-4.20090113.2mdv2010.0
+ Revision: 413354
- rebuild

* Fri Feb 13 2009 Pascal Terjan <pterjan@mandriva.org> 0.32-4.20090113.1mdv2009.1
+ Revision: 339959
- Add upstream fix on fgetc, fixes stage 1 looking ugly

* Wed Jan 28 2009 Oden Eriksson <oeriksson@mandriva.com> 0.32-3.20090113.1mdv2009.1
+ Revision: 335015
- new cvs snap (20090113)
- rediff patches

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0.32-3.20080509.2mdv2009.0
+ Revision: 264403
- rebuild early 2009.0 package (before pixel changes)

* Tue Jun 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.32-0.20080509.2mdv2009.0
+ Revision: 217518
- rebuild
- drop the fix-getpriority patch (fixes #41386)

* Sun Jun 08 2008 Oden Eriksson <oeriksson@mandriva.com> 0.32-0.20080509.1mdv2009.0
+ Revision: 216900
- 0.32 (actually a cvs snap 20080509)
- rediffed the mdv patches (P1,P23,P27,P33)
- added fedora patches (P100 - P111)

* Mon Dec 31 2007 Pascal Terjan <pterjan@mandriva.org> 0.31-5mdv2008.1
+ Revision: 139897
- Commit the correct stat64 fix

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.31-4mdv2008.1
+ Revision: 136466
- revert commit 102905 (which removed __NO_STAT64), it breaks stage1 build and does not fix dash
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Nov 17 2007 Funda Wang <fwang@mandriva.org> 0.31-3mdv2008.1
+ Revision: 109297
- rebuild for new lzma

* Mon Nov 05 2007 Pascal Terjan <pterjan@mandriva.org> 0.31-2mdv2008.1
+ Revision: 106080
- Add back x86_64-lseek64 patch

* Sun Oct 28 2007 Pascal Terjan <pterjan@mandriva.org> 0.31-1mdv2008.1
+ Revision: 102905
- Try again to fix stat64
- 0.31

* Sun Oct 28 2007 Pascal Terjan <pterjan@mandriva.org> 0.30-4mdv2008.1
+ Revision: 102886
- Put back patch17 not that it is fixed
- Synchronize stat and stat64
- Disable P17, it breaks dash on x86_64

* Fri Aug 24 2007 Pixel <pixel@mandriva.com> 0.30-3mdv2008.0
+ Revision: 70836
- add -fno-stack-protector to override default %%{optflags}

* Sat Aug 11 2007 Andrey Borzenkov <arvidjaar@mandriva.org> 0.30-2mdv2008.0
+ Revision: 61994
- add MS_RELATIME definition

* Tue Jul 17 2007 Olivier Blin <oblin@mandriva.com> 0.30-1mdv2008.0
+ Revision: 53058
- 0.30
- rediff mdk patch
- drop 64bit-size_t patch (merged upstream)
- fix build of fstatfs64 (from Alt Linux)

* Sun May 06 2007 Christiaan Welvaart <spturtle@mandriva.org> 0.29-7mdv2008.0
+ Revision: 23754
- patch34: fix build on ppc

* Fri May 04 2007 Gwenole Beauchesne <gbeauchesne@mandriva.org> 0.29-6mdv2008.0
+ Revision: 22461
- fix strncmp() (nano)
- fix *printf("%%u") for 64-bit platforms (dmraid)


* Thu Oct 12 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-11 11:46:17 (63424)
- bunzip patches

* Thu Oct 12 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-11 11:43:34 (63423)
Import dietlibc

* Sat Jul 22 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.29-4mdv2007.0
- srpm got lost, might as well rebuild for new release tag too..

* Thu May 04 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.29-3mdk
- fix typo in P23 to fix build on x86_64
- fix rdtsc sparc hack (P29) for sparcv9

* Fri Apr 21 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.29-2mdk
- add missing sparc .weak asm (P31 from ROCK Linux)
- reenable glob test for sparc again as we no now have asm inst (drops P30)

* Fri Apr 21 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.29-1mdk
- 0.29
- update P0 to disable zeroconf
- regenerate P23 & P27
- drop broken contrapolice (P14)
- reenable test on sparc as things should be working again now :)
- disable P22 (fixed upstream? someone please verify!)
- versioned provides
- move checks to %%check
- hack rdtsc for sparc testsuite
- disable glob test for sparc testsuite

* Thu Dec 15 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.28-3mdk
- remove merged patches that 0.28-1mdk uploader forgot about

* Wed Aug 31 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.28-2mdk
- fix <asm/types.h> size_t definition for 64-bit platforms

* Sat May 07 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.28-1mdk
- New version 0.28
- Remove patches 7, 8, 10, 11, 12, 19, 20
- Adapt patch 14

* Sat Apr 23 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.27-14mdk
- don't do check on sparc

* Wed Mar 30 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.27-13mdk
- always prototype lseek64(), aka fix mdassemble though they should
  not use *64() functions directly

* Tue Mar 08 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.27-12mdk
- cross compilation support

* Sat Jan 29 2005 Luca Berra <bluca@vodka.it> 0.27-11mdk 
- added pgoff_t to kernel 2.6.10 types definitions

* Wed Jan 26 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.27-10mdk
- provide some kernel 2.6.10 types definitions

* Tue Jan 18 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.27-9mdk
- fix getpriority() as the return value from the syscall is biased
- add nice() implementation from glibc, make it use the fixed getpriority()

* Wed Dec 15 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.27-8mdk
- fix ppc select()
- quiet test bsearch

* Tue Dec 14 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.27-7mdk
- biarch builds on x86_64 and ppc64

* Tue Dec 14 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.27-6mdk
- ppc64 fixes: umount, setjmp, __WORDSIZE, select, stat64, rdtsc

* Wed Dec 08 2004 Luca Berra <bluca@vodka.it> 0.27-5mdk 
- added struct stat64 as struct stat and fstat64() as fstat()
  on x86_64, so test suite builds

* Fri Nov 26 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.27-4mdk
- add RDTSC in testsuite for ppc
- remove patch9 - fixed upstream
- fix permissions on test scripts in subdirs
- Patch16: build inet tests

* Tue Nov 09 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.27-3mdk
- added the contrapolice patch (P14)
- make and run the test suite

* Wed Oct 27 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.27-2mdk
- implement lseek64() as lseek() on x86_64

* Fri Aug 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.27-1mdk
- 0.27
- deactivated P9 as it won't apply

* Fri Jul 23 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.26-4mdk
- fix rdtsc in testsuite for amd64
- fix tzfile() for 64-bit architectures, aka. fix mktime()

* Fri Jul 23 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.26-3mdk
- Patch10: ISO C defines LC_ macros (7.11 [#3])

* Sat Jul 10 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.26-2mdk
- Patch9: fix ppc build

* Tue Jun 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.26-1mdk
- 0.26
- merge P2 and P4 into P1 (ppc64asppc and lib64 fixes are now in P1)

* Fri May 07 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.25-1mdk
- 0.25
- drop the sprinf() patch, it's included

* Wed Apr 07 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.24-2mdk
- sprinf() fixes from CVS

* Mon Feb 09 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.24-1mdk
- 0.24
- Patch8: Fix strtol() + testcase on 64-bit platforms

* Wed Oct 29 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.22-7mdk
- Patch18: Enable inb() and friends in <sys/io.h> on AMD64 too

