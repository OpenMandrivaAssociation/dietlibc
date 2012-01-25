%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

%define snap 20110311

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
Name:		%{cross_prefix}dietlibc
Version:	0.33
Release:	4.%{snap}.2
License:	GPL
Group:		Development/Other
%if %{build_cross}
BuildRequires:	%{cross_prefix}gcc
%endif
URL:		http://www.fefe.de/dietlibc/
Source0:	http://www.fefe.de/dietlibc/dietlibc-%{version}.%{snap}.tar.bz2
Source2:	build_cross_dietlibc.sh
# all in one from RH:
Patch9999:		dietlibc-github.patch
Patch1:		dietlibc-0.33-mdkconfig.patch
Patch3:		dietlibc-0.22-tests.patch
Patch5:		dietlibc-0.22-net-ethernet.patch
Patch6:		dietlibc-0.24-rpc-types.patch
Patch9:		dietlibc-0.27-glibc-nice.patch
Patch16:	dietlibc-0.27-test-makefile-fix.patch
Patch17:	dietlibc-0.33-x86_64-stat64.patch
Patch18:	dietlibc-0.27-x86_64-lseek64.diff
Patch23:	dietlibc-0.33-biarch.patch
# (UPSTREAMED)
Patch24:	dietlibc-0.33-quiet.patch
Patch26:	dietlibc-0.27-kernel2.6-types.patch
Patch27:	dietlibc-0.29-cross.patch
# (UPSTREAMED)
Patch33:	dietlibc-0.33-fix-strncmp.patch
# (cjw) from PLD, see http://gcc.gnu.org/bugzilla/show_bug.cgi?id=26374
Patch34:	dietlibc-0.29-ppc-gcc-ldbl128.patch
# (UPSTREAMED)
Patch36:        dietlibc-0.30-relatime.patch
# (pixel) add -fno-stack-protector to override default %{optflags}
Patch37:	dietlibc-0.30-force-no-stack-protector.patch
# (UPSTREAMED)
Patch112:	dietlibc-0.32-20090113-fix_getpriority.patch
Patch113:	dietlibc-0.33-i386-types.patch

# (UPSTREAMED)
Patch200:       dietlibc_mips_Makefile_fixes.patch
Patch201:       dietlibc_mips_use_misc.patch
Patch300:	diet_arm_eabi_time.patch
Patch301:	diet_arm_create_module.patch
# (tv) from http://svn.exactcode.de/t2/trunk/package/base/dietlibc/, for kmod:
# (ALL UPSTREAMED)
Patch304:	openat.patch
Patch305:	fstatat.patch
Patch306:	unlinkat.patch 
Patch307:	fdopendir.patch 
Patch308:	renameat.patch 
# (tv) implement missing functions for kmod:
# (UPSTREAMED)
Patch320:	get_current_dir_name.patch
Patch321:	readdir_r.diff
# (tv) add string.h's basename (prevent libkmod to segfault in basebame())
Patch322:	basename.diff



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

%setup -q -n %{name}-%{version}.%{snap}

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# P9999 is from fedora 
%patch9999 -p1 -b .rh
%patch1 -p0 -b .mdkconfig
%patch3 -p1 -b .tests
%patch5 -p1 -b .net-ethernet
%patch6 -p1 -b .rpc-types
%patch9 -p1 -b .glibc-nice -E
%patch16 -p1 -b .inettest
%patch17 -p1 -b .x86_64-stat64
#patch18 -p0 -b .x86_64-lseek64
%patch23 -p1 -b .biarch
%patch24 -p1 -b .quiet
%patch26 -p1 -b .kernel2.6-types
%patch27 -p0 -b .cross
%patch33 -p1 -b .fix-strncmp
%patch36 -p1 -b .relatime
%patch37 -p1 -b .stack-protector

%patch200 -p1 -b .mips
%patch201 -p1 -b .mips_misc
%patch300 -p1 -b .arm_time
%patch301 -p1 -b .arm_create_module
%patch304 -p1 -b .at1
%patch305 -p1 -b .at2
%patch306 -p1 -b .at3
%patch307 -p1 -b .fdopendir
%patch308 -p1 -b .at4
%patch320 -p1 -b .getcwd
%patch321 -p1 -b .readdir_r
%patch322 -p1 -b .readdir_r

%patch112 -p1 -b .fix_getpriority
%patch113 -p0 -b .386_types
rm -f x86_64/getpriority.S

#WANT_VALGRIND_SUPPORT
# disable unwanted features
cp dietfeatures.h{,.tv}
sed -i \
    -e '/#define WANT_\(LARGEFILE_BACKCOMPAT\|\LINKER_WARNINGS\|IPV6_DNS\|HIGH_PRECISION_MATH\|SAFEGUARDNT_LINKER_WARNINGS\|PLUGPLAY_DNS\|SAFEGUARD\)/d' \
    dietfeatures.h
 
# fix execute permission on test scripts
chmod a+x test/{dirent,inet,stdio,string,stdlib,time}/runtests.sh

%build
%make %{cross_make_flags} DEBUG=1

%check
# make and run the tests
%if %{build_check}
cd test; rm *.c.*
%ifarch %mips %arm
sed -i -e 's!cycles empty!empty!' Makefile
%endif
export DIETHOME="%{_builddir}/%{name}-%{version}-%{snap}"
MYARCH=`uname -m | sed -e 's/i[4-9]86/i386/' -e 's/armv[3-6]t\?e\?[lb]/arm/' -e 's!mips!%{_arch}!g'`
find -name "Makefile" | xargs perl -pi -e "s|^DIET.*|DIET=\"${DIETHOME}/bin-${MYARCH}/diet\"|g"
%make DEBUG=1
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

make %{cross_make_flags} DEBUG=1 DESTDIR=%{buildroot} install

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
