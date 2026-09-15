%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/drivers
%global oldname xorg-x11-drv-amdgpu
%global reponame xf86-video-amdgpu
%define _disable_source_fetch 0

# XLibre cannot load hardened build
%undefine _hardened_build

Name:       xlibre-xf86-video-amdgpu
Version:    25.1.0
Release:    3%{?dist}

Summary:    XLibre amdgpu X11 video driver
License:    MIT

URL:        https://github.com/X11Libre/%{reponame}
Source0:    https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

ExcludeArch: s390 s390x

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  kernel-headers
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libdrm) >= 2.4.89
BuildRequires:  pkgconfig(libdrm_amdgpu) >= 2.4.76
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(xorg-server) >= 1.13
BuildRequires:  xorg-x11-util-macros

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
Requires: libdrm >= 2.4.89

Provides:       %{oldname} = %{version}-%{release}
Provides:       %{oldname}%{?_isa} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

%description
XLibre amdgpu X11 video driver.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -fiv
%configure --disable-static --enable-glamor --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%files
%{driverdir}/video/amdgpu_drv.so
%{_datadir}/X11/xorg.conf.d/10-amdgpu.conf
%{_mandir}/man4/amdgpu.4*

%changelog
* Tue Sep 15 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.1.0-3
- Add arch-qualified Provides (%{?_isa}) for the renamed xorg-x11-drv-amdgpu
  name so dependencies on xorg-x11-drv-amdgpu(x86-64) resolve correctly

* Tue Feb 10 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.1.2-1
- Upgrade XLibre amd-gpu driver to version 25.1.0

* Fri Aug 15 2025 Kevin Kofler <Kevin@tigcc.ticalc.org> - 23.0.0.4-1
- Switch upstream to the X11Libre GitHub project
- Rename package from xorg-x11-drv-amdgpu to xlibre-xf86-video-amdgpu
- Do not use %%autosetup

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 23.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 23.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 27 2024 Simone Caronni <negativo17@gmail.com> - 23.0.0-6
- Clean up SPEC file.
- Trim changelog.
- Do not disable debug stripping (caught by rpminspect) tests.

* Fri Sep 27 2024 Sérgio Basto <sergio@serjux.com> - 23.0.0-5
- Rebuild for rebase of xorg-server to versions 21.1.x

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 23 2023 Christopher Atherton <atherchris@gmail.com> - 23.0.0-1
- Update to 23.0.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 14 2022 Christopher Atherton <atherchris@gmail.com> - 22.0.0-1
- Update to 22.0.0

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
