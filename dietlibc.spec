%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

%define snap %{nil}

%define name	%{cross_prefix}dietlibc

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
Version:	0.33
%if "%{snap}" != ""
Release:	5.%{snap}.1
Source0:	http://www.fefe.de/dietlibc/dietlibc-%{version}.%{snap}.tar.xz
%else
Release:	12
Source0:	http://www.fefe.de/dietlibc/dietlibc-%{version}.tar.bz2
%endif
License:	GPL
Group:		Development/Other
%if %{build_cross}
BuildRequires:	%{cross_prefix}gcc
%endif
URL:		http://www.fefe.de/dietlibc/
Source2:	build_cross_dietlibc.sh
# all in one from RH:
Patch9999:		dietlibc-github.patch
Patch1:		dietlibc-0.33-mdkconfig.patch
Patch5:		dietlibc-0.22-net-ethernet.patch
Patch6:		dietlibc-0.24-rpc-types.patch
Patch17:	dietlibc-0.33-x86_64-stat64.patch
Patch18:	dietlibc-0.27-x86_64-lseek64.diff
Patch23:	dietlibc-0.33-biarch.patch
Patch26:	dietlibc-0.27-kernel2.6-types.patch
Patch27:	dietlibc-0.29-cross.patch
# (UPSTREAMED differently)
Patch33:	dietlibc-0.33-fix-strncmp.patch
# (cjw) from PLD, see http://gcc.gnu.org/bugzilla/show_bug.cgi?id=26374
Patch34:	dietlibc-0.29-ppc-gcc-ldbl128.patch
# (pixel) add -fno-stack-protector to override default %{optflags}
Patch37:	dietlibc-0.30-force-no-stack-protector.patch
Patch113:	dietlibc-0.33-i386-types.patch

# (UPSTREAMED)
Patch200:       dietlibc_mips_Makefile_fixes.patch
Patch201:       dietlibc_mips_use_misc.patch
Patch300:	diet_arm_eabi_time.patch
Patch301:	diet_arm_create_module.patch
# (tv) from http://svn.exactcode.de/t2/trunk/package/base/dietlibc/, for kmod:
Patch305:	fstatat.patch
# (tv) add string.h's basename (prevent libkmod to segfault in basebame())
Patch322:	basename.diff

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
%if "%{snap}" != ""
%setup -q -n %{name}-%{version}.%{snap}
%else
%setup -q
%endif

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# P9999 is from fedora 
%patch9999 -p1 -b .rh
%patch1 -p0 -b .mdkconfig
%patch5 -p1 -b .net-ethernet
%patch6 -p1 -b .rpc-types
%patch17 -p1 -b .x86_64-stat64
#patch18 -p0 -b .x86_64-lseek64
%patch23 -p1 -b .biarch
%patch26 -p1 -b .kernel2.6-types
%patch27 -p0 -b .cross
%patch33 -p1 -b .fix-strncmp
%patch37 -p1 -b .stack-protector

%patch200 -p1 -b .mips
%patch201 -p1 -b .mips_misc
%patch300 -p1 -b .arm_time
%patch301 -p1 -b .arm_create_module
%patch305 -p1 -b .at2
%patch322 -p1 -b .readdir_r

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
# fix build in chroot:
%if "%{snap}" != ""
export DIETHOME="%{_builddir}/%{name}-%{version}.%{snap}"
%else
export DIETHOME="%{_builddir}/%{name}-%{version}"
%endif
MYARCH=`uname -m | sed -e 's/i[4-9]86/i386/' -e 's/armv[3-7]t\?e\?[lb]/arm/' -e 's!mips!%{_arch}!g'`
find -name "Makefile" | xargs perl -pi -e "s|^DIET.*|DIET=\"${DIETHOME}/bin-${MYARCH}/diet\"|g" 	 
# compile test suite:
%make all  DEBUG=1
%make -C inet all DEBUG=1

# run the tests
# getpass requires user input
perl -pi -e "s|^PASS.*|PASS=\"\"|g" runtests.sh
sh ./runtests.sh
cd ..
%endif

%install
make %{cross_make_flags} DEBUG=1 DESTDIR=%{buildroot} install

%files devel
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
