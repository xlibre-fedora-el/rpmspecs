%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir	%{moduledir}/drivers
%global oldname xorg-x11-drv-ati
%global reponame xf86-video-ati

%undefine _hardened_build

Summary:   XLibre ati X11 video driver
Name:      xlibre-xf86-video-ati
Version:   25.0.1
Release:   1%{?dist}
URL:       https://github.com/X11Libre/%{reponame}
License:   MIT

Source0:   https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz

ExcludeArch: s390 s390x

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(pciaccess) >= 0.8.0
BuildRequires:  pkgconfig(gbm) >= 10.6
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libdrm) >= 2.4.89
BuildRequires:  pkgconfig(libdrm_radeon)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(xorg-server) >= 1.16

Requires: libdrm >= 2.4.89
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

Provides:       %{oldname} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

%description
XLibre ati X11 video driver.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -iv
%configure --disable-static --enable-glamor --with-xorg-module-dir="%{moduledir}"
%make_build

%install
%make_install
find %{buildroot} -name "*.la" -delete

%files
%{driverdir}/ati_drv.so
%{driverdir}/radeon_drv.so
%{_mandir}/man4/ati.4*
%{_mandir}/man4/radeon.4*
%{_datadir}/X11/xorg.conf.d/10-radeon.conf

%changelog
* Tue Apr 15 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.1-1
- Update to 25.0.1

* Fri Aug 22 2025 Kevin Kofler <Kevin@tigcc.ticalc.org> - 22.0.0.2-1
- Update to 22.0.0.2, now with a correctly named tag

* Thu Aug 14 2025 Kevin Kofler <Kevin@tigcc.ticalc.org> - 22.0.0.1-1
- Switch upstream to the X11Libre GitHub project
- Rename package from xorg-x11-drv-ati to xlibre-xf86-video-ati

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 22.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 22.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 29 2024 Simone Caronni <negativo17@gmail.com> - 22.0.0-3
- Clean up SPEC file.
- Adjust build requirement.
- Trim changelog.

* Fri Sep 27 2024 Sérgio Basto <sergio@serjux.com> - 22.0.0-2
- Rebuild for rebase of xorg-server to versions 21.1.x

* Tue Sep 10 2024 Sérgio Basto <sergio@serjux.com> - 22.0.0-1
- Update xorg-x11-drv-ati to 22.0.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 19.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 19.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 19.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 19.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 19.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 19.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
