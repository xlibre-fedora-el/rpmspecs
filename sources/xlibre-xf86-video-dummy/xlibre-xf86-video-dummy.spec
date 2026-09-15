%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/drivers
%global oldname xorg-x11-drv-dummy
%global reponame xf86-video-dummy
%define _disable_source_fetch 0

%undefine _hardened_build

Summary:   XLibre dummy X11 video driver
Name:      xlibre-xf86-video-dummy
Version:   25.0.0
Release:   2%{?dist}
URL:       https://github.com/X11Libre/%{reponame}
License:   MIT AND X11

Source0:   https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(xorg-server) >= 1.4.99.901

Provides:       %{oldname} = %{version}-%{release}
Provides:       %{oldname}%{?_isa} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
XLibre dummy X11 video driver.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -vif
%configure --disable-static --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install

find %{buildroot} -name "*.la" -delete

%files
%doc README.md
%{driverdir}/dummy_drv.so

%changelog
* Tue Sep 15 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.0-2
- Add arch-qualified Provides: %{oldname}%{?_isa} so packages requiring
  xorg-x11-drv-dummy(x86-64) (e.g. xpra) can be installed

* Wed Feb 18 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.0-1
- Upgrade XLibre dummy driver to version 25.0.0

* Wed Aug 13 2025 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.4.1.1-1
- Switch upstream to the X11Libre GitHub project
- Rename package from xorg-x11-drv-dummy to xlibre-xf86-video-dummy
- Requires: xlibre-xserver-Xorg instead of Xorg to ensure a compatible one

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 29 2024 Simone Caronni <negativo17@gmail.com> - 0.4.1-5
- Clean up SPEC file.
- Trim changelog.

* Fri Sep 27 2024 Sérgio Basto <sergio@serjux.com> - 0.4.1-4
- Rebuild for rebase of xorg-server to versions 21.1.x

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 05 2023 José Expósito <jexposit@redhat.com> - 0.4.1-1
- xorg-x11-drv-dummy 0.4.1

* Thu Sep 07 2023 José Expósito <jexposit@redhat.com> - 0.3.7-20
- SPDX Migration

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
