%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input
%global oldname xorg-x11-drv-libinput
%global reponame xf86-input-libinput
%define _disable_source_fetch 0

Summary:    XLibre libinput X11 input driver
Name:       xlibre-xf86-input-libinput
Version:    25.0.1
Release:    2%{?dist}
URL :       https://github.com/X11Libre/%{reponame}
# SPDX
License:    MIT

Source0:    https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:    71-libinput-overrides-wacom.conf

# Fedora-only hack for hidpi screens
# https://bugzilla.redhat.com/show_bug.cgi?id=1413306
Patch01:    xlibre-xf86-input-libinput-1.5.0.1-Add-a-DPIScaleFactor-option-as-temporary-solution-to.patch

BuildRequires: make
BuildRequires: autoconf automake libtool
BuildRequires: xlibre-xserver-devel >= 1.14.0
BuildRequires: libudev-devel libevdev-devel libinput-devel >= 0.6.0-3
BuildRequires: xorg-x11-util-macros
BuildRequires: libinput-devel >= 0.6.0-3

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)
Requires: xkeyboard-config
Requires: libinput >= 0.21.0

Provides:  %{oldname} = %{version}-%{release}
Provides:  %{oldname}%{?_isa} = %{version}-%{release}
Obsoletes: %{oldname} < %{version}-%{release}

Provides: xorg-x11-drv-synaptics = 1.9.0-3
Provides: xorg-x11-drv-synaptics%{?_isa} = 1.9.0-3
Obsoletes: xorg-x11-drv-synaptics < 1.9.0-3

%description
A generic X11 input driver for the XLibre X server based on libinput,
supporting all devices.

%prep
%setup -q -n %{reponame}-%{name}-%{version}
%patch -P1 -p1 -b .DPIScaleFactor

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules --with-xorg-module-dir="%{moduledir}"
make %{?_smp_mflags}

%install
%make_install

find %{buildroot} -name "*.la" -delete

cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/

%files
%doc COPYING
%{driverdir}/libinput_drv.so
%{_datadir}/X11/xorg.conf.d/40-libinput.conf
%{_datadir}/X11/xorg.conf.d/71-libinput-overrides-wacom.conf
%{_mandir}/man4/libinput.4*

%package devel
Summary:        XLibre libinput X11 input driver development package.
Requires:       pkgconfig

Provides:       %{oldname}-devel = %{version}-%{release}
Provides:       %{oldname}-devel%{?_isa} = %{version}-%{release}
Obsoletes:      %{oldname}-devel < %{version}-%{release}

%description devel
XLibre libinput X11 input driver development files.

%files devel
%doc COPYING
%{_libdir}/pkgconfig/xorg-libinput.pc
%dir %{_includedir}/xorg/
%{_includedir}/xorg/libinput-properties.h


%changelog
* Tue Sep 15 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.1-2
- Add arch-qualified Provides (%{?_isa}) for the renamed xorg-x11-drv-*
  names so dependencies on e.g. xorg-x11-drv-libinput(x86-64) resolve correctly

* Wed Feb 18 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.1-1
- Upgrade XLibre libinput driver to version 25.0.1

* Mon Feb 02 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.0-1
- Upgrade XLibre libinput driver to version 25.0.0

* Thu Aug 14 2025 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.5.0.1-2
- Reenable DPIScaleFactor patch

* Thu Aug 14 2025 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.5.0.1-1
- Switch upstream to the X11Libre GitHub project
- Rename package from xorg-x11-drv-libinput to xlibre-xf86-input-libinput
- Rebase DPIScaleFactor patch (manpage conflicts only)
- Temporarily disable DPIScaleFactor patch (needs a small revert in xserver)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 15 2024 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.0-1
- xf86-input-libinput 1.5.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 05 2023 Peter Hutterer <peter.hutterer@redhat.com>
- SPDX migration: mark license as SPDX compatible

* Fri Aug 25 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-1
- xf86-input-libinput 1.4.0

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 04 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.0-1
- xf86-input-libinput 1.3.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jan 24 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.1-1
- xf86-input-libinput 1.2.1

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 20 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.0-1
- xf86-input-libinput 1.2.0

* Fri Sep 03 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.0-2
- Add support for high-resolution wheel scrolling

* Fri Sep 03 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.0-1
- xf86-input-libinput 1.1.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 29 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.0.1-2
- Use autosetup instead of manual patch handling

* Fri Apr 16 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.0.1-1
- xf86-input-libinput 1.0.1

* Tue Apr 06 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-1
- xf86-input-libinput 1.0.0

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov  5 10:09:04 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 0.30.0-4
- Add BuildRequires for make

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 19 2020 Peter Hutterer <peter.hutterer@redhat.com> 0.30.0-1
- xf86-input-libinput 0.30.0

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 12 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.29.0-1
- xf86-input-libinput 0.29.0

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.28.2-1
- xf86-input-libinput 0.28.2

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 15 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.28.1-1
- xf86-input-libinput 0.28.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.28.0-1
- xf86-input-libinput 0.28.0

* Thu Apr 12 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.27.1-2
- Build on s390x (#1565062)

* Tue Apr 10 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.27.1-1
- xorg-x11-drv-libinput 0.27.1

* Mon Apr 02 2018 Adam Jackson <ajax@redhat.com> - 0.27.0-3
- Rebuild for xserver 1.20

* Thu Mar 22 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.27.0-2
- Fix left-handed property missing on all but the first pointer device

* Tue Mar 20 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.27.0-1
- xorg-x11-drv-libinput 0.27.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 15 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.26.0-1
- xorg-x11-drv-libinput 0.26.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 18 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.25.1-2
- Add a new option to provide a workaround for the slow pointer movement on
  hidpi displays (#1413306) .
  That's a fedora-only patch for now, no idea what the permanent upstream
  solution will be here.

* Fri May 05 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.25.1-1
- xorg-x11-drv-libinput 0.25.1

* Thu Mar 09 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.25.0-1
- libinput 0.25.0

* Thu Feb 09 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.24.0-1
- libinput 0.24.0

* Wed Dec 21 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.23.0-2
- Ignore LED updates for disabled devices, avoids a null-pointer dereference
  when an AccessX timeout is set

* Mon Dec 12 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.23.0-1
- libnput 0.23.0

* Fri Nov 25 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.22.0-4
- Override touchpads assigned the wacom driver with libinput again
  (#1397477)

* Fri Nov 18 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.22.0-3
- Provide xorg-x11-drv-synaptics. The actual content is now provided by
  xorg-x11-drv-synaptics-legacy (#1394836). For details, see
  https://fedoraproject.org/wiki/Changes/RetireSynapticsDriver

* Tue Nov 01 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.22.0-2
- Match against tablets too

* Wed Oct 19 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.22.0-1
- xf86-input-libinput 0.22.0

* Tue Oct 18 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.20.0-1
- xf86-input-libinput 0.20.0

* Thu Sep 29 2016 Hans de Goede <hdegoede@redhat.com> 0.19.1-3.20160929
- Fix crash when the first detected input device gets removed (rhbz#1381840)

* Thu Sep 29 2016 Hans de Goede <hdegoede@redhat.com> 0.19.1-2.20160929
- Update to latest git master for use with xserver-1.19
- Rebuild against xserver-1.19

* Wed Sep 14 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.19.1-1
- xf86-input-libinput 0.19.1

* Tue Jul 19 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.19.0-2
- Bump to make F24 update path happy

* Thu Apr 28 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.19.0-1
- xf86-input-libinput 0.19.0

* Fri Feb 26 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-1
- xf86-input-libinput 0.17.0

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 23 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-1
- xf86-input-libinput 0.16.0

* Tue Oct 27 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-1
- xf86-input-libinput 0.15.0

* Wed Sep 16 2015 Dave Airlie <airlied@redhat.com> - 0.14.0-2
- 1.18 ABI rebuild

* Mon Aug 31 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.14.0-1
- xf86-input-libinput 0.14.0

* Mon Aug 17 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-2
- Add drag lock support (#1249309)

* Tue Aug 11 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-1
- xf86-input-libinput 0.13.0

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> 0.12.0-2
- bump for X server ABI

* Tue Jul 14 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.12.0-1
- xf86-input-libinput 0.12.0

* Mon Jul 13 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.11.0-3
- Restore unaccelerated valuator masks (#1208992)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.11.0-1
- xf86-input-libinput 0.11.0
- support buttons higher than BTN_BACK (1230945)

* Mon Jun 01 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-5
- Fix missing scroll button property

* Fri May 29 2015 Nils Philippsen <nils@redhat.com> 0.10.0-4
- fix URL

* Tue May 26 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-3
- Use the new unnaccelerated valuator masks, fixes nonmoving mouse in SDL
  (#1208992)

* Fri May 22 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-2
- Init mixed rel/abs devices as rel devices (#1223619)

* Thu May 21 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-1
- xf86-input-libinput 0.10.0

* Thu Apr 23 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.9.0-1
- xf86-input-libinput 0.9.0

* Tue Mar 10 2015 Peter Hutterer <peter.hutterer@redhat.com> - 0.8.0-2
- Rebuild for libinput soname bump

* Fri Mar 06 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.8.0-1
- xf86-input-libinput 0.8.0

* Thu Mar 05 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-5
- Fix two-finger scrolling speed (#1198467)

* Thu Feb 26 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-4
- Fix property setting patch, first version prevented re-enabling a device.

* Wed Feb 25 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-3
- Fix a crash when setting properties on a disabled device

* Wed Feb 25 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-2
- Fix stack smash on pointer init (#1195905)

* Tue Feb 24 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-1
- xorg-x11-drv-libinput 0.7.0

* Tue Jan 27 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.6.0-1
- xorg-x11-drv-libinput 0.6.0

* Fri Jan 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.5.0-1
- xorg-x11-drv-libinput 0.5.0

* Fri Dec 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.4.0-1
- xorg-x11-drv-libinput 0.4.0

* Mon Nov 24 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.3.0-1
- xorg-x11-drv-libinput 0.3.0

* Mon Nov 24 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.2.0-2
- Add explicit (Build)Requires for libinput 0.6.0-3, we rely on new symbols
  from the git snapshot

* Mon Nov 24 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.2.0-1
- Only match on specific device types, don't match on joysticks or tablets
- libinput 0.2.0
- switch to new fdo host

* Fri Sep 12 2014 Peter Hutterer <peter.hutterer@redhat.com> - 0.1.2-3
- Rebuild for libinput soname bump

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.1.2-1
- Update to 0.1.2, dropping the pkgconfig files

* Thu Jun 26 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.1.1-1
- Initial release (#1113392)

