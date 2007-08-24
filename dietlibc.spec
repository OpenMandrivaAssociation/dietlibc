%define name	%{cross_prefix}dietlibc
%define version 0.30
%define release %mkrel 3

# This is eventually a biarch package, so no %_lib for diethome
%define diethome %{_prefix}/lib/dietlibc

# Enable builds without testing (default shall always be testing)
%define build_check		1
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
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
%if %{build_cross}
BuildRequires:	%{cross_prefix}gcc
%endif
URL:		http://www.fefe.de/dietlibc/
Source0:	http://www.fefe.de/dietlibc/dietlibc-%{version}.tar.bz2
Source1:	build_cross_dietlibc.sh
Patch0:		dietlibc-0.29-features.patch
Patch1:		dietlibc-0.30-mdkconfig.patch
Patch3:		dietlibc-0.22-tests.patch
Patch4:		dietlibc-0.27-fix-getpriority.patch
Patch5:		dietlibc-0.22-net-ethernet.patch
Patch6:		dietlibc-0.24-rpc-types.patch
Patch9:		dietlibc-0.27-glibc-nice.patch
Patch13:	dietlibc-0.27-x86_64-lseek64.patch
# (oe) http://synflood.at/patches/contrapolice/contrapolice-0.3.patch
#Patch14:	dietlibc-0.28-contrapolice.diff.bz2
Patch15:	dietlibc-0.27-ppc-rdtsc.patch
Patch16:	dietlibc-0.27-test-makefile-fix.patch
Patch17:	dietlibc-0.27-x86_64-stat64.patch
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
Patch32:	dietlibc-0.29-64bit-fixes-printf.patch
Patch33:	dietlibc-0.29-fix-strncmp.patch
# (cjw) from PLD, see http://gcc.gnu.org/bugzilla/show_bug.cgi?id=26374
Patch34:	dietlibc-0.29-ppc-gcc-ldbl128.patch
# (blino) from Alt Linux
Patch35:	dietlibc-0.30-alt-fstatfs64-typo.patch
Patch36:        dietlibc-0.30-relatime.patch
# (pixel) add -fno-stack-protector to override default %{optflags}
Patch37:	dietlibc-0.30-force-no-stack-protector.patch
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
%setup -q
%patch0 -p1 -b .features
%patch1 -p1 -b .mdkconfig
%patch3 -p1 -b .tests
%patch4 -p1 -b .fix-getpriority
%patch5 -p1 -b .net-ethernet
%patch6 -p1 -b .rpc-types
%patch9 -p1 -b .glibc-nice -E
%patch13 -p1 -b .x86_64-lseek64
# (oe) http://synflood.at/patches/contrapolice/contrapolice-0.3.patch
#%patch14 -p1 -b .contrapolice
%patch15 -p1 -b .ppc-rdtsc
%patch16 -p1 -b .inettest
%patch17 -p1 -b .x86_64-stat64
%patch21 -p1 -b .ppc64-select
#%patch22 -p1 -b .ppc64-stat64
%patch23 -p1 -b .biarch
%patch24 -p1 -b .quiet
%patch25 -p1 -b .ppc-select
%patch26 -p1 -b .kernel2.6-types
%patch27 -p1 -b .cross
%patch29 -p1 -b .sparc_rdtsc
#%patch30 -p1 -b .sparc_disable_glob_test
%patch31 -p1 -b .sparc_weak_asm
%patch32 -p1 -b .64bit-fixes-printf
%patch33 -p1 -b .fix-strncmp
%patch34 -p1 -b .gcc-ppc-ldbl-bug
%patch35 -p1 -b .fstatfs64
%patch36 -p1 -b .relatime

# fix execute permission on test scripts
chmod a+x test/{dirent,inet,stdio,string,stdlib,time}/runtests.sh

%build
%make %{cross_make_flags}

%check
# make and run the tests
%if %{build_check}
cd test; rm *.c.*
export DIETHOME="%{_builddir}/%{name}-%{version}"
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
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make %{cross_make_flags} DESTDIR=%{buildroot} install

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

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

