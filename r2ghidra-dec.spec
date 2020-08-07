%global radare2_ver 4.5.0

%global ghidra_commit          6c10f36f06468f866188cccf960c019779fb9028
%global ghidra_shortcommit     %(c=%{ghidra_commit}; echo ${c:0:7})
%global ghidra_checkout_date   20200807
%global ghidra_snapshot        %{ghidra_checkout_date}git%{ghidra_shortcommit}

Name:       r2ghidra-dec
Version:    4.5.0
Release:    1%{?dist}
Summary:    Integration of the Ghidra decompiler for radare2

License:    LGPLv3+
URL:        https://github.com/radareorg/r2ghidra-dec
Source0:    https://github.com/radareorg/r2ghidra-dec/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:    https://github.com/thestr4ng3r/ghidra/archive/%{ghidra_commit}/ghidra-%{ghidra_snapshot}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  pugixml-devel
BuildRequires:  qt5-devel
BuildRequires:  radare2-devel = %{radare2_ver}
BuildRequires:  cutter-re-devel

Requires: radare2 = %{radare2_ver}


%description
r2ghidra-dec is an integration of the Ghidra decompiler for radare2. It
is solely based on the decompiler part of Ghidra, which is written
entirely in C++, so Ghidra itself is not required at all and the plugin
can be built self-contained.


%package cutter
Summary:        r2ghidra-dec plugin for Cutter
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cutter-re

%description cutter
Plugin to use r2ghidra-dec from Cutter UI.


%prep
%autosetup -b0
%autosetup -N -b1

cd ghidra/
rmdir ghidra
ln -s ../../ghidra-%{ghidra_commit} ghidra


%build
mkdir build
cd build
%cmake \
        -DRADARE2_INSTALL_PLUGDIR=%{_datadir}/%{name} \
        -DCUTTER_INSTALL_PLUGDIR=%{_libdir}/cutter/native \
        -DCUTTER_SOURCE_DIR=%{_includedir}/cutter \
        -DBUILD_CUTTER_PLUGIN=ON \
        -DUSE_SYSTEM_PUGIXML=ON \
        ..
%cmake_build


%install
cd build
%cmake_install

mkdir -p %{buildroot}%{_libdir}/radare2/%{radare2_ver}
mv \
        %{buildroot}%{_datadir}/%{name}/core_ghidra.so \
        %{buildroot}%{_libdir}/radare2/%{radare2_ver}/


%files
%{_libdir}/radare2/%{radare2_ver}/core_ghidra.so
%{_datadir}/%{name}/r2ghidra_sleigh


%files cutter
%{_libdir}/cutter/native/libr2ghidra_cutter.so


%changelog
* Fri Aug 07 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.5.0-1
- Update to 4.5.0

* Sat Apr 18 2020 Ivan Mironov <mironov.ivan@gmail.com> - 4.4.0-1
- Initial packaging
