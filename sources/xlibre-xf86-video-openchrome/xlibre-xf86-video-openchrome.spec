%define _disable_source_fetch 0

%global commit0 857d892b668b4737d41ef1b7f58fd45eac84d552
%global date 20230328
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

%define tarball xf86-video-openchrome
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers
%global oldname xorg-x11-drv-openchrome
%global reponame xf86-video-openchrome

%undefine _hardened_build

Summary:        X.Org X11 openchrome video driver rebuilt for XLibre
Name:           xlibre-xf86-video-openchrome
Version:        25.0.0%{!?tag:^%{date}git%{shortcommit0}}
Release:        2%{?dist}
URL:            http://www.freedesktop.org/wiki/Openchrome/
License:        MIT

%if 0%{?tag:1}
Source0:        https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz
%else
Source0:        %{tarball}-%{shortcommit0}.tar.bz2
%endif
Source1:        make-git-snapshot.sh

ExclusiveArch:  %{ix86} x86_64 x86_64_v2

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig(libdrm) >= 2.2
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pciaccess) >= 0.8.0
BuildRequires:  pkgconfig(xorg-server)

Requires:       Xorg %(xserver-sdk-abi-requires ansic)
Requires:       Xorg %(xserver-sdk-abi-requires videodrv)
Requires:       xorg-x11-server-wrapper

Obsoletes:      %{oldname}-devel < %{version}-%{release}
Provides:       %{oldname}-devel = %{version}-%{release}
Provides:       %{oldname}-devel%{?_isa} = %{version}-%{release}

Obsoletes:      %{oldname} < %{version}-%{release}
Provides:       %{oldname} = %{version}-%{release}
Provides:       %{oldname}%{?_isa} = %{version}-%{release}

%description
A build of the X.Org X11 openchrome video driver recompiled against the XLibre
X server.

%prep
%if 0%{?tag:1}
%setup -q -n %{reponame}-%{name}-%{version}
%else
%setup -q -n %{tarball}-%{commit0}
%endif

%build
autoreconf -vif
%configure --disable-static --enable-viaregtool --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install
find %{buildroot} -name "*.la" -delete

%files
%doc NEWS README
%license COPYING
%{driverdir}/openchrome_drv.so
%{_mandir}/man4/openchrome.4.gz
%{_sbindir}/via_regs_dump


%changelog
* Tue Sep 15 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.0-2
- Add arch-qualified Provides (%{?_isa}) for the renamed xorg-x11-drv-openchrome
  names so dependencies on e.g. xorg-x11-drv-openchrome(x86-64) resolve correctly

* Wed Feb 18 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.0-1
- Use XLibre openchrome driver version 25.0.0 instead of Xorg's version
- Remove patches which are now included upstream
- Remove XvMC

* Fri Aug 15 2025 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.6.604^20230328git857d892-4
- Rename package from xorg-x11-drv-openchrome to xlibre-xf86-video-openchrome
- Rebuild against XLibre
- Do not use %%autosetup
- Add hack to work around xf86ModeStatusToString removal from public headers
- Use xf86newOption instead of the removed xf86NewOption

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.604^20230328git857d892-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.604^20230328git857d892-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 30 2024 Simone Caronni <negativo17@gmail.com> - 0.6.604^20230328git857d892-1
- Update to latest snapshot.
- Clean up SPEC file.
- Trim changelog.
- Drop devel subpackage (no headers?).

* Fri Sep 27 2024 Sérgio Basto <sergio@serjux.com> - 0.6.400-9.20210215git5dbad06
- Rebuild for rebase of xorg-server to versions 21.1.x

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.400-8.20210215git5dbad06
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.400-7.20210215git5dbad06
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.400-6.20210215git5dbad06
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.400-5.20210215git5dbad06
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.400-4.20210215git5dbad06
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.400-3.20210215git5dbad06
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
