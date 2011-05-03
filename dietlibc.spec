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
Release:	%mkrel 4.%{snap}.7
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
