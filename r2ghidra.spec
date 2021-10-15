%global r2ghidra_commit        f244bfa72677d10e5bd41183e0e51255b833b499
%global r2ghidra_shortcommit   %(c=%{r2ghidra_commit}; echo ${c:0:7})
%global r2ghidra_checkout_date 20211015
%global r2ghidra_snapshot      %{r2ghidra_checkout_date}git%{r2ghidra_shortcommit}

%global ghidra_commit          358132818b1055cd6bbfdb8c08819a79e1e9cde8
%global ghidra_shortcommit     %(c=%{ghidra_commit}; echo ${c:0:7})
%global ghidra_checkout_date   20211015
%global ghidra_snapshot        %{ghidra_checkout_date}git%{ghidra_shortcommit}

%global radare2_ver 5.4.2

Name:       r2ghidra
Version:    5.4.1
Release:    1.%{?r2ghidra_snapshot}%{?dist}
Summary:    Integration of the Ghidra decompiler for radare2

License:    LGPLv3+
URL:        https://github.com/radareorg/r2ghidra
%if 0%{?r2ghidra_checkout_date}
Source0:    https://github.com/radareorg/r2ghidra/archive/%{r2ghidra_commit}/%{name}-%{r2ghidra_snapshot}.tar.gz
%else
Source0:    https://github.com/radareorg/r2ghidra/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:    https://github.com/radareorg/ghidra-native/archive/%{ghidra_commit}/ghidra-native-%{ghidra_snapshot}.tar.gz

Patch0:     0001-Use-system-provided-pugixml.patch

BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  pugixml-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  radare2-devel = %{radare2_ver}

Requires: radare2 = %{radare2_ver}
Requires: %{name}-sleigh%{?_isa} = %{version}-%{release}


%description
r2ghidra is an integration of the Ghidra decompiler for radare2. It
is solely based on the decompiler part of Ghidra, which is written
entirely in C++, so Ghidra itself is not required at all and the plugin
can be built self-contained.


# TODO: Make SLEIGH package noarch.
%package sleigh
Summary:        SLEIGH files for r2ghidra


%description sleigh
SLEIGH files for r2ghidra. SLEIGH is a language for describing the
instruction sets of general purpose microprocessors, in order to
facilitate the reverse engineering of software written for them.


%prep
%if 0%{?r2ghidra_checkout_date}
%autosetup -p1 -b0 -n %{name}-%{r2ghidra_commit}
%autosetup -p1 -b1 -n %{name}-%{r2ghidra_commit}
%else
%autosetup -p1 -b0
%autosetup -p1 -b1
%endif

ln -s ../ghidra-native-%{ghidra_commit} ghidra-native


%build
make -C ghidra-native patch

%configure
make %{?_smp_mflags}


%install
%make_install
rm %{buildroot}%{_bindir}/sleighc


%files
%dir %{_libdir}/radare2
%dir %{_libdir}/radare2/%{radare2_ver}
%{_libdir}/radare2/%{radare2_ver}/anal_ghidra.so
%{_libdir}/radare2/%{radare2_ver}/asm_ghidra.so
%{_libdir}/radare2/%{radare2_ver}/core_ghidra.so


%files sleigh
%dir %{_libdir}/radare2
%dir %{_libdir}/radare2/%{radare2_ver}
%{_libdir}/radare2/%{radare2_ver}/r2ghidra_sleigh


%changelog
* Fri Oct 15 2021 Ivan Mironov <mironov.ivan@gmail.com> - 5.4.1-1
- Update to 5.4.1
- Drop iaito plugin

* Wed Mar 24 2021 Ivan Mironov <mironov.ivan@gmail.com> - 5.1.1-1
- Update to 5.1.1 plus git
- Migrate from cutter-re to r2cutter
- Separate subpackage for SLEIGH data

* Sat Nov 28 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.5.1-1
- Update to 4.5.1

* Fri Aug 07 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.5.0-1
- Update to 4.5.0

* Sat Apr 18 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.4.0-1
- Initial packaging
