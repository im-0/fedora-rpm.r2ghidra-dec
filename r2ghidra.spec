%global r2ghidra_commit        1fdcef615cddf4135aaeec97e129d4a376b1d934
%global r2ghidra_shortcommit   %(c=%{r2ghidra_commit}; echo ${c:0:7})
%global r2ghidra_checkout_date 20210324
%global r2ghidra_snapshot      %{r2ghidra_checkout_date}git%{r2ghidra_shortcommit}

%global ghidra_commit          44bacf3a13c52def99866ad2c9044044af393390
%global ghidra_shortcommit     %(c=%{ghidra_commit}; echo ${c:0:7})
%global ghidra_checkout_date   20210324
%global ghidra_snapshot        %{ghidra_checkout_date}git%{ghidra_shortcommit}

%global radare2_ver 5.1.1

Name:       r2ghidra
Version:    5.1.1
Release:    1.%{?r2ghidra_snapshot}%{?dist}
Summary:    Integration of the Ghidra decompiler for radare2

License:    LGPLv3+
URL:        https://github.com/radareorg/r2ghidra
%if 0%{?r2ghidra_checkout_date}
Source0:    https://github.com/radareorg/r2ghidra/archive/%{r2ghidra_commit}/%{name}-%{r2ghidra_snapshot}.tar.gz
%else
Source0:    https://github.com/radareorg/r2ghidra/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:    https://github.com/radareorg/ghidra/archive/%{ghidra_commit}/ghidra-%{ghidra_snapshot}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  pugixml-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  radare2-devel = %{radare2_ver}
BuildRequires:  r2cutter-devel

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


%package r2cutter
Summary:        r2ghidra plugin for r2cutter
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       r2cutter


%description r2cutter
Plugin to use r2ghidra from r2cutter UI.


%prep
%if 0%{?r2ghidra_checkout_date}
%autosetup -b0 -n %{name}-%{r2ghidra_commit}
%autosetup -N -b1 -n %{name}-%{r2ghidra_commit}
%else
%autosetup -b0
%autosetup -N -b1
%endif

cd ghidra/
rmdir ghidra
ln -s ../../ghidra-%{ghidra_commit} ghidra


%build
mkdir build
cd build
%cmake \
        -DRADARE2_INSTALL_PLUGDIR=%{_datadir}/%{name} \
        -DCUTTER_INSTALL_PLUGDIR=%{_libdir}/r2cutter/native \
        -DCUTTER_SOURCE_DIR=%{_includedir}/r2cutter \
        -DBUILD_CUTTER_PLUGIN=ON \
        -DUSE_SYSTEM_PUGIXML=ON \
        ..
%cmake_build


%install
cd build
%cmake_install

mkdir -p %{buildroot}%{_libdir}/radare2/%{radare2_ver}
mv \
        %{buildroot}%{_datadir}/%{name}/*.so \
        %{buildroot}%{_libdir}/radare2/%{radare2_ver}/


%files
%dir %{_libdir}/radare2
%dir %{_libdir}/radare2/%{radare2_ver}
%{_libdir}/radare2/%{radare2_ver}/anal_ghidra.so
%{_libdir}/radare2/%{radare2_ver}/asm_ghidra.so
%{_libdir}/radare2/%{radare2_ver}/core_ghidra.so


%files sleigh
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/r2ghidra_sleigh


%files r2cutter
%dir %{_libdir}/r2cutter
%dir %{_libdir}/r2cutter/native
%{_libdir}/r2cutter/native/libr2ghidra_cutter.so


%changelog
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
