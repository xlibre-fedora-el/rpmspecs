%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers
%global oldname xorg-x11-drv-nouveau
%global reponame xf86-video-nouveau

%define _disable_source_fetch 0

%undefine _hardened_build

Summary:   XLibre nouveau X11 video driver for NVIDIA graphics chipsets
Name:      xlibre-xf86-video-nouveau
Version:   25.0.0
Release:   2%{?dist}
URL:       https://github.com/X11Libre/%{reponame}
License:   MIT

Source0:   https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

ExcludeArch: s390 s390x

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig(xorg-server) >= 1.8
BuildRequires:  pkgconfig(libdrm) >= 2.4.60
BuildRequires:  pkgconfig(libdrm_nouveau) >= 2.4.25
BuildRequires:  pkgconfig(pciaccess) >= 0.10
BuildRequires:  pkgconfig(libudev)

Requires:   Xorg %(xserver-sdk-abi-requires ansic)
Requires:   Xorg %(xserver-sdk-abi-requires videodrv)
Requires:   libdrm >= 2.4.33-0.1

Provides:       %{oldname} = 1:%{version}-%{release}
Provides:       %{oldname}%{?_isa} = 1:%{version}-%{release}
Obsoletes:      %{oldname} < 1:%{version}-%{release}

%description 
XLibre nouveau X11 video driver.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -v --install --force
%configure --disable-static --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install
find %{buildroot} -name "*.la" -delete

%files
%{driverdir}/nouveau_drv.so
%{_mandir}/man4/nouveau.4*

%changelog
* Tue Sep 15 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.0-2
- Add arch-qualified Provides (%{?_isa}) for the renamed xorg-x11-drv-nouveau
  name so dependencies on xorg-x11-drv-nouveau(x86-64) resolve correctly

* Wed Feb 18 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.0-1
- Upgrade XLibre nouveau driver to version 25.0.0

* Thu Aug 14 2025 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.0.18.1-1
- Switch upstream to the X11Libre GitHub project
- Rename package from xorg-x11-drv-ati to xlibre-xf86-video-ati
- Drop Epoch because the package was renamed
- Drop all patches, all upstreamed
- Do not use %%autosetup

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.17-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 29 2024 Simone Caronni <negativo17@gmail.com> - 1:1.0.17-11
- Clean up SPEC file.
- Trim changelog.

* Fri Sep 27 2024 Sérgio Basto <sergio@serjux.com> - 1:1.0.17-10
- Rebuild for rebase of xorg-server to versions 21.1.x

* Sun Sep 22 2024 Sérgio Basto <sergio@serjux.com> - 1:1.0.17-9
- Add compability with X11-server-21.1.x

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild