%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input
%global oldname xorg-x11-drv-synaptics
%global reponame xf86-input-synaptics
%define _disable_source_fetch 0

Name:           xlibre-xf86-input-synaptics
Summary:        XLibre synaptics X11 input driver for Synaptics touchpads
Version:        25.0.0
Release:        1%{?dist}
URL :           https://github.com/X11Libre/%{reponame}
# SPDX
License:        MIT

Source0:        https://github.com/X11Libre/%{reponame}/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        70-synaptics.conf
Source2:        70-touchpad-quirks.rules

ExcludeArch:    s390 s390x

BuildRequires:  make
BuildRequires:  autoconf automake libtool pkgconfig
BuildRequires:  xorg-x11-server-devel >= 1.10.99.902
BuildRequires:  libX11-devel libXi-devel libXtst-devel
BuildRequires:  xorg-x11-util-macros >= 1.8.0
BuildRequires:  libevdev-devel
BuildRequires:  systemd

Requires:       Xorg %(xserver-sdk-abi-requires ansic)
Requires:       Xorg %(xserver-sdk-abi-requires xinput)
Requires:       libevdev
Requires:       libXi libXtst

Provides:       synaptics = %{version}-%{release}
Obsoletes:      synaptics < 0.15.0

Provides:       %{oldname} = %{version}-%{release}
Obsoletes:      %{oldname} < %{version}-%{release}

Provides:       %{oldname}-legacy = %{version}-%{release}
Obsoletes:      %{oldname}-legacy < %{version}-%{release}

%description
This is the Synaptics touchpad driver for the XLibre X server. The following
touchpad models are supported:
* Synaptics
* appletouch (Post February 2005 and October 2005 Apple Aluminium Powerbooks)
* Elantech (EeePC)
* bcm5974 (Macbook Air (Jan 2008), Macbook Pro Penryn (Feb 2008), iPhone
  (2007), iPod Touch (2008)

Note that support for appletouch, elantech and bcm5974 requires the respective
kernel module.
A touchpad by default operates in compatibility mode by emulating a standard
mouse. However, by using a dedicated driver, more advanced features of the
touchpad become available.

Features:

    * Movement with adjustable, non-linear acceleration and speed.
    * Button events through short touching of the touchpad ("tapping").
    * Double-Button events through double short touching of the touchpad.
    * Dragging through short touching and holding down the finger on the
      touchpad.
    * Middle and right button events on the upper and lower corner of the
      touchpad.
    * Vertical scrolling (button four and five events) through moving the
      finger on the right side of the touchpad.
    * The up/down button sends button four/five events.
    * Horizontal scrolling (button six and seven events) through moving the
      finger on the lower side of the touchpad.
    * The multi-buttons send button four/five events, and six/seven events for
      horizontal scrolling.
    * Adjustable finger detection.
      Multifinger taps: two finger for middle button and three finger for
      right button events. (Needs hardware support. Not all models implement
      this feature.)
    * Run-time configuration using shared memory. This means you can change
      parameter settings without restarting the X server.

%prep
%setup -q -n %{reponame}-%{name}-%{version}

%build
autoreconf -v --install --force || exit 1
%configure --disable-static --disable-silent-rules --with-xorg-module-dir="%{moduledir}"
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -name "*.la" -delete

# Remove upstream synaptics.conf as we've several special fixes in ours
rm $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/70-synaptics.conf

install -d $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/70-synaptics.conf

install -d $RPM_BUILD_ROOT%{_udevrulesdir}
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_udevrulesdir}/70-touchpad-quirks.rules

%post
udevadm control --reload-rules || :

%postun
udevadm control --reload-rules || :

%files
%doc README.md
%license COPYING
%{_datadir}/X11/xorg.conf.d/70-synaptics.conf
%{driverdir}/synaptics_drv.so
%{_bindir}/synclient
%{_bindir}/syndaemon
%{_mandir}/man4/synaptics.4*
%{_mandir}/man1/synclient.1*
%{_mandir}/man1/syndaemon.1*
%{_udevrulesdir}/70-touchpad-quirks.rules

%package devel
Summary:        XLibre synaptics X11 input driver development package
Requires:       pkgconfig

Provides:       %{oldname}-devel = %{version}-%{release}
Obsoletes:      %{oldname}-devel < %{version}-%{release}

%description devel
Development files for the Synaptics TouchPad X11 input driver for XLibre.

%files devel
%license COPYING
%dir %{_includedir}/xorg
%{_includedir}/xorg/synaptics-properties.h

%changelog
* Mon Mar 02 2026 Anders da Silva Rytter Hansen <andersrh@users.noreply.github.com> - 25.0.0-1
- Upgrade XLibre synaptics driver to version 25.0.0

* Fri Aug 15 2025 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.10.0.1-1
- Switch upstream to the X11Libre GitHub project
- Rename package from xorg-x11-drv-synaptics to xlibre-xf86-input-synaptics
- Do not use git to apply patches (there are not any at this time anyway)
- Drop obsolete -legacy split, nothing Obsoletes xlibre-xf86-input-synaptics
- Do not require pkgconfig in the runtime package

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Peter Hutterer <peter.hutterer@redhat.com>
- Add SPDX marker to License

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 06 2025 Peter Hutterer <peter.hutterer@redhat.com> - 1.10.0-1
- xf86-input-synaptics 1.10.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 1.9.2-1
- Update to 1.9.2 (RHBZ #2105850)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov  5 10:14:22 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1.9.1-7
- Add BuildRequires for make
- We only need git-core to build, not full git

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 29 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-1
- synaptics 1.9.1

* Tue May 15 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.9.0-9
- Prevent infinite "Read Error" logspam

* Mon Apr 02 2018 Adam Jackson <ajax@redhat.com> - 1.9.0-8
- Rebuild for xserver 1.20

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.0-3
- Ship the synaptics file as 70-synaptics.conf to match upstream (and sort
  above libinput).

* Fri Nov 18 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.9.0-2
- Move actual driver to the -legacy package so we can obsolete the main
  package with xorg-x11-drv-libinput (#1394836)
  See https://fedoraproject.org/wiki/Changes/RetireSynapticsDriver

* Fri Nov 18 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.9.0-1
- synaptics 1.9.0

* Mon Oct 10 2016 Hans de Goede <hdegoede@redhat.com> 1.8.99.2-2
- Rebuild against xserver-1.19

* Sun Oct 09 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.8.99.2-1
- synaptics 1.9rc2

* Thu Sep 29 2016 Hans de Goede <hdegoede@redhat.com> 1.8.99.1-2.20160929git48632211
- Update to latest git master for use with xserver-1.19
- Rebuild against xserver-1.19

* Fri Apr 29 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.8.99.1-1
- synaptics 1.9rc1

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.8.3-1
- synaptics 1.8.3

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> - 1.8.2-4
- 1.15 ABI rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 01 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.8.2-2
- Drop the custom patch for the new X1 Carbon series. This was an early fix,
  the kernel now handles this correctly for us and we don't need userspace
  workarounds.

* Fri Mar 27 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.8.2-1
- synaptics 1.8.2

* Tue Mar 24 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.8.1-6
- Ignore MT devices without x/y (#1196975)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.8.1-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Feb 13 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.8.1-4
- Restore cursor jumping patch (#1149377)

* Thu Feb 05 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.8.1-3
- Fix missing bits and bobs for the X1 Carbon quirks (#1189329)

* Mon Feb 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.8.1-2
- Add support for the X1 Carbon 3rd quirks

* Thu Sep 18 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.8.1-1
- synaptics 1.8.1

* Thu Sep 18 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-9
- Discard jumps of more than 20mm (#1130656)

* Tue Sep 09 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-8
- Apply (and fix conflicts with) the clockdrift patch
- Use git to apply patches so I don't always forget to add them

* Fri Sep 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-7
- Fix click delays when realtime/monotonic clocks times drift apart

* Fri Aug 29 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-6
- Fix build errors with latest glibc

* Thu Aug 28 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-5
- Increase top software button area for easier clicks
- Prevent two-finger taps from being ignored

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Hans de Goede <hdegoede@redhat.com> - 1.8.0-2
- Set Option "HasSecondarySoftButtons" "on" in 50-synaptics.conf for devices
  with the touchpad_softbutton_top udev quirk, to keep topbuttons working on
  kernels which don't set INPUT_PROP_TOPBUTTONPAD
- Add W540 to 70-touchpad-quirks.rules as touchpad_softbutton_top (#1096436)

* Tue May 13 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-1
- synaptics 1.8

* Mon Apr 28 2014 Hans de Goede <hdegoede@redhat.com> - 1.7.99.1-8.20140318gitfd7099004
- xserver 1.15.99-20140428 git snapshot ABI rebuild

* Tue Apr 22 2014 Hans de Goede <hdegoede@redhat.com> 1.7.99.1-7.20140318gitfd7099004
- Add topbuttons quirk for Thinkpad Edge E341 (#1089689)

* Fri Apr 18 2014 Hans de Goede <hdegoede@redhat.com> 1.7.99.1-6.20140318gitfd7099004
- Add L540 to 70-touchpad-quirks.rules as touchpad_softbutton_top (#1088588)

* Mon Apr 14 2014 Hans de Goede <hdegoede@redhat.com> 1.7.99.1-5.20140318gitfd7099004
- Fix 3 finger clicking on clickpads (#1086218)
- Add T431 to 70-touchpad-quirks.rules as touchpad_softbutton_top (#1085582)
- Switch to using relative coordinates for the top softbutton area (#1085697)

* Wed Apr 09 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.1-4.20140318gitfd7099004
- Add L440 and X1 Carbon tags/config

* Wed Apr 02 2014 Peter Hutterer <peter.hutterer@redhat.com>
- Remove now superfluous xorg.conf.d snippet for left/right button split

* Fri Mar 21 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.1-3.20140318gitfd7099004
- Unset ClickPad for Cypress touchpads, they do everything in firmware, we
  can't compete with that. (fdo bug 76341 and 70819)

* Wed Mar 19 2014 Peter Hutterer <peter.hutterer@redhat.com> - 1.7.99.1-2.20140318gitfd7099004
- Update the various top softbutton ranges and use a udev quirk to tag them

* Mon Mar 17 2014 Peter Hutterer <peter.hutterer@redhat.com> - 1.7.99.1-1.20140318gitfd7099004
- 1.7.99.1 (from git)

* Wed Mar 12 2014 Peter Hutterer <peter.hutterer@redhat.com> - 1.7.99-3.20140312git2e5c0cf43
- New git snapshot, with improved T440, T540, X240 handling
- Drop mtdev, no longer used by synaptics

* Wed Feb 26 2014 Peter Hutterer <peter.hutterer@redhat.com>  1.7.99-2.20140226gitbbe4c56c4
- Require libevdev

* Wed Feb 26 2014 Peter Hutterer <peter.hutterer@redhat.com>  1.7.99-1.20140226gitbbe4c56c4
- Upstream git snapshot, includes better handling for the LEN0034 touchpads
  in the T440, T540, x240, etc. series.
- Update .conf file with a PnP match rule. Won't take effect just yet until
  we have the matching kernel and server patch in place though

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1.7.3-2
- 1.15 ABI rebuild

* Mon Jan 13 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.7.3-1
- synaptics 1.7.3

* Mon Jan 06 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.7.2-5
- Fix driver scaling for ABI 20

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1.7.2-4
- 1.15RC4 ABI rebuild

* Thu Dec 12 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.7.2-3
- Match for T440s and move the softbuttons to the top of the touchpad
  (#1035469)

* Mon Dec 09 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.7.2-2
- Drop the patch now merged upstream

* Mon Dec 09 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.7.2-1
- synaptics 1.7.2

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1.7.1-8
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1.7.1-7
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1.7.1-6
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.7.1-4
- Disable in-driver coordinate scaling on ABI 19.2, requires
  xorg-x11-server-1.14.2-7.fc19

* Fri Jul 12 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.7.1-3
- Quieten rpmlint (non-escaped percent sign, tab/spaces mix)

* Thu May 16 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.7.1-2
- add explicit BR for automake, autoconf
- Fix a few specfile complaints

* Mon May 13 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.7.1-1
- synaptics 1.7.1

* Tue Apr 02 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.7.0-1
- synaptics 1.7.0

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 1.6.99-8.20130214git4cdee4005
- Less RHEL customization

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.99-7.20130214git4cdee4005
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.99-6.20130214git4cdee4005
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.99-5.20130214git4cdee4005
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.99-4.20130214git4cdee4005
- ABI rebuild

* Thu Feb 14 2013 Peter Hutterer <peter.hutterer@redhat.com>  1.6.99-3.20130214git4cdee4005
- Today's git snapshot

* Thu Jan 10 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-2
- Add commitid file, got lost during a git reset

* Thu Jan 10 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-1
- Today's git snapshot

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 1.6.2-9
- ABI rebuild

* Fri Dec 21 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.2-8
- Allow right softbuttons in dead area (#888051)

* Wed Oct 31 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.6.2-7
- Fix {?dist} tag

* Fri Aug 31 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.2-6
- Fix memory corruption on resume. Triggered if fingers are still on the
  touchpad when the device is disabled.

* Fri Aug 10 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.2-5
- Use signal-safe logging

* Sun Aug 05 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.2-4
- Align git snapshot building with other drivers

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> - 1.6.2-2
- ABI rebuild

* Tue Jun 12 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.2-1
- synaptics 1.6.2

* Thu Jun 07 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.1-2
- Drop udev requires, install udev rules in /usr/lib

* Fri May 11 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.1-1
- synaptics 1.6.1 (#813668, #819348)

* Thu May 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-1
- synaptics 1.6.0

* Fri Apr 27 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.904-1
- synaptics 1.5.99.904

* Thu Apr 26 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.903-5.20120419git11d892964
- Force clickpad on for apple wireless trackpad

* Tue Apr 24 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.903-4.20120419git11d892964
- Reset touch state on DEVICE_OFF (#814972)

* Thu Apr 19 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.903-3.20120419git11d892964
- Update .conf file for softbuttons

* Thu Apr 19 2012 Peter Hutterer <peter.hutterer@redhat.com>  1.5.99.903-2.20120419git11d892964
- Git snapshot, fix for #813686

* Mon Apr 16 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.903-1
- synaptics 1.5.99.903

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 1.5.99.902-2
- RHEL arch exclude updates

* Fri Mar 23 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.902-1
- synaptics 1.5.99.902

* Wed Mar 14 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.901-2
- Require mtdev

* Wed Mar 14 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.901-1
- synaptics 1.5.99.901

* Thu Feb 23 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.99-8.20120223git0a2fd560a
- New git snapshot, with improved MT handling

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.99-7.20120207git141d9120b
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.99-6.20120207git141d9120b
- ABI rebuild

* Tue Feb 07 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99-5.20120207git141d9120b
- Update to today's git snapshot with MT support

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.5.99-4.20120104gitc861d4568
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99-3.20120104.gitc861d4568
- Update to today's git snapshot
- Switch define to global in spec file
- Append git version to NVR

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 1.5.99-2.20111110
- ABI rebuild

* Thu Nov 10 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99-1.20111110
- Update to today's git snapshot

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 1.5.0-3
- ABI rebuild

* Wed Oct 12 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.5.0-2
- Add libXtst dependency to enable syndaemon build with the RECORD
  extension (#745289)

* Fri Sep 02 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.5.0-1
- synaptics 1.5.0

* Fri Aug 19 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.4.99.1-1
- synaptics 1.4.99.1

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1.4.1-3
- Rebuild for xserver 1.11 ABI

* Mon Aug 01 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.4.1-2
- devel package requires pkgconfig

* Thu Jul 07 2011 Peter Hutterer <peter.hutterer@redhat.com>
- Disable silent rules on build

* Tue Jun 28 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.4.1-1
- synaptics 1.4.1

* Mon Apr 18 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0.901-1
- synaptics 1.4.1RC1

* Fri Mar 04 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-1
- synaptics 1.4

* Mon Feb 21 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.3.99.901-1
- synaptics 1.4 RC1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.99-3.20101125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.99-2.20101125
- Rebuild for server 1.10

* Thu Nov 25 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.3.99-1.20101125
- today's git snapshot

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 1.3.0-2
- Add ABI requires magic (#542742)

* Wed Sep 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-1
- synaptics 1.3.0

* Mon Aug 23 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.99.901-1.20100823
- synaptics 1.2.99.901 from git

* Thu Aug 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.99.1-4.20100819
- today's git snapshot
- synaptics-1.2.99.1-increase-accel-factor.patch: increase default accel
  factor to something more useful (#621591)
- drop unused patches

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 1.2.99.1-3
- Install COPYING

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.99.1-2.20100617
- rebuild for X Server 1.9

* Thu Jun 17 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.99.1-1.20100617
- synaptics 1.2.99.1 (from git)

* Tue Jun 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.99-1
- Update to today's git version. Includes the new pointer acceleration code.

* Tue May 18 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.2-6
- The rules file shouldn't end in .conf...

* Mon May 17 2010 Peter Hutterer <peter.hutterer@redhat.com>
- Add missing LABEL statement to 70-touchpad.rules

* Thu May 13 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.2-5
- Change ClickFinger defaults to 0 if there's more than one.
- Add ClickPad support, this requires a kernel patch as well (#590835)
- pop the udev rule into /lib/udev/rules.d instead of $sysconfigdir

* Mon May 10 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.2-4
- 70-touchpad-rules.conf: label Dell Mini touchpads as broken in udev,
  requiring special config.
- 50-synaptics.conf: add dell mini quirk for bottom edge. This is only
  partially useful for now, a real patch is coming soon.
  One half of the fix for #573463.

* Thu Apr 15 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.2-3
- Install config snippet in $datadir/X11/xorg.conf.d.
- Rename to 50-synaptics.conf to match upstream better.

* Wed Apr 14 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.2-2
- Only match /dev/input/event* in 10-synaptics.conf. (related #581573)

* Fri Mar 26 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.2-1
- synaptics 1.2.2

* Thu Mar 11 2010 Adam Jackson <ajax@redhat.com> 1.2.1-4
- synaptics-1.2.1-timer-fix.patch: Don't clobber the timer we just created.

* Tue Feb 16 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-3
- cvs add 10-synaptics.conf this time

* Tue Feb 16 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-2
- 10-synaptics.conf: new xorg.conf.d config file, replacing the fdi.
- 10-synaptics.fdi: drop, X server doesn't use HAL anymore.
- Drop HAL require

* Sat Feb 13 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-1
- synaptics 1.2.1

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.0-4
- Rebuild for server 1.8

* Wed Dec 09 2009 Adam Jackson <ajax@redhat.com> 1.2.0-3
- synaptics-1.2.0-timer-fix.patch: Don't free the timer in DeviceClose, since
  that gets called on VT switch. (#540248)

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.2.0-2
- BuildRequires xorg-x11-util-macros 1.3.0

* Fri Oct 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.2.0-1
- synaptics 1.2.0

* Mon Sep 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99-7.20090907
- This time with the tarball.

* Mon Sep 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99-6.20090907
- Update to today's git master (synaptics 1.1.99.1)

* Tue Jul 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99-5.20090728
- Update to today's git master.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.99-4.20090717
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99-3-20090717
- Update to today's git master.

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.1.99-2.20090710.1
- ABI bump

* Fri Jul 10 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99-2-20090710
- Update to today's git master.

* Mon Jun 22 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99.1-20090622
- Update to today's git master.

* Tue Apr 14 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.0-2
- synaptics-1.1.0-synclient-64.patch: fix 64-bit integer issues with
  synclient (#494766)

* Mon Mar 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.0-1
- synaptics 1.1

* Thu Mar 05 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.4-1
- synaptics 1.1, snapshot 4 (fix for 64 bit crashes)

* Wed Mar 04 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.3-1
- synaptics 1.1, snapshot 3

* Fri Feb 27 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.2-1
- Synaptics 1.1, snapshot 2
- Up Requires to 1.6.0-2 for XATOM_FLOAT defines.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-4
- Fix 10-synaptics.fdi, the warning added in the last commit was not
  well-formed xml.

* Mon Feb 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-3
- Revert last commit, this is against Fedora policy.
  https://fedoraproject.org/wiki/Packaging:Guidelines#Configuration_files

* Mon Feb 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-2
- mark the fdi file as %%config(noreplace)

* Mon Feb 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-1
- synaptics 1.0

* Mon Jan 05 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.99.3-3
- Require xorg-x11-server-devel 1.6 to build
- Update fdi file with comments on how to merge your own keys.

* Mon Dec 22 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.99.3-2
- Rebuild for server 1.6

* Mon Dec 15 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.99.3-1
- synaptics 1.0 RC 3

* Thu Dec 4 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.99.2-1
- synaptics 1.0 RC 2

* Thu Dec 4 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.99.1-2
- 10-synaptics.fdi: if something has capabilities input.touchpad match it.
  Don't bother about product names.

* Mon Nov 24 2008 Peter Hutterer <peter.hutterer@redhat.com>
- Fix up summary and description, provide list of supported models.

* Fri Nov 14 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.99.1-1
- synaptics 1.0 RC 1

* Tue Oct 14 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.99-0.2
- add the make-git-snapshot script.

* Tue Oct 14 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.99-0.1
- Today's git snapshot.
- Add devel subpackage.
- remove xf86-input-synaptics-0.15.2-maxtapmove.patch: driver autoscales now.

* Wed Sep 17 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.2-1
- update to 0.15.2
- remove patches merged upstream.
- xf86-input-synaptics-0.15.2-maxtapmove.patch: scale MaxTapMove parameter
  depending on touchpad height #462211

* Tue Sep 9 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.1-1
- update to 0.15.1
- remove xf86-input-synaptics-0.15.0-tap.patch: merged in upstream.
- update patches to apply against 0.15.1.
- xf86-input-synaptics-0.15.1-dont-crash-without-Device.patch: don't crash if
  neither Device nor Path is given.

* Mon Sep 8 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-6
- xf86-input-synaptics-0.15.0-edges.patch: updated to improve edge calculation
  and acceleration factors.
- xf86-input-synaptics-0.15.0-preprobe patch: pre-probe eventcomm devices for
  axis ranges if specifed with Device option.
- update fdi file to support "bcm5974" devices.

* Sun Sep 7 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-5
- update fdi file to support "appletouch" devices.

* Tue Sep 2 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-4
- xf86-input-synaptics-0.15.0-dont-lose-buttonup.patch: force a click if
  middle button emulation times out during ReadInput cycle. RH #233717.

* Thu Aug 28 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-3
- xf86-input-synaptics-0.15.0-edges.patch: reserve 5% on each side for edge
  detection.

* Mon Aug 25 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.15.0-2
- Enable tapping RH #439386

* Fri Aug 8 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-1
- Initial RPM release - this is the relicensed version of the old synaptics
  package.
- Includes Changelog from synaptics package.

* Wed Aug 6 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.14.6-10
- Update Release, really this time.

* Wed Aug 6 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.14.6-10
- Fix license tag and BuildRoot, reduce description line width.

* Tue Jun 17 2008 Adam Jackson <ajax@redhat.com> 0.14.6-9
- Fix %%fedora version comparison to be numeric not string.

* Thu Apr 10 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.14.6-8
- Build with $RPM_OPT_FLAGS, fix debuginfo (#249979).

* Fri Mar 28 2008 Rex Dieter <rdieter@fedoraproject.org> 0.14.6-7
- Synaptics default acceleration values are way slow for alps (#437039)

* Wed Mar 26 2008 Adam Jackson <ajax@redhat.com> 0.14.6-6
- synaptics-0.14.6-alps.patch: Fix the defaults on ALPS touchpads.  Values
  stolen from rhpxl.

* Tue Mar 18 2008 Matt Domsch <Matt_Domsch@dell.com> 0.14.6-5
- synaptics-0.14.6-poll-delay.patch: make poll interval user configurable
  http://www.bughost.org/pipermail/power/2008-January/001234.html
- synaptics-0.14.6-poll-200ms.patch: reduce default poll from 20ms to 200ms

* Sun Mar 09 2008 Adam Jackson <ajax@redhat.com> 0.14.6-4
- 10-synaptics.fdi: Get hal to report the X driver as synaptics for
  touchpads we support.
- synaptics-0.14.6-tap-to-click.patch: Disable tap to click by default in
  the name of accessibility.

* Wed Mar 05 2008 Dave Airlie <airlied@redhat.com> 0.14.6-3
- rebuild for ppc64

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.14.6-2
- Autorebuild for GCC 4.3

* Mon Jan 07 2008 Jarod Wilson <jwilson@redhat.com> 0.14.6-1
- Update to 0.14.6 w/permission from krh
- Adds two-finger scrolling capability on supported hardware

* Fri Nov 30 2007 Caolan McNamara <caolanm@redhat.com> 0.14.4-12
- Resolves: rhbz#396891 patch it to at least work

* Mon Oct 15 2007 Adam Jackson <ajax@redhat.com> 0.14.4-11
- Back to ExclusiveArch, buildsystem is a disaster.

* Wed Oct 03 2007 Adam Jackson <ajax@redhat.com> 0.14.4-10
- ExclusiveArch -> ExcludeArch.

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 0.14.4-9
- Rebuild for build id

* Wed Aug 16 2006 Jesse Keating <jkeating@redhat.com> - 0:0.14.4-8
- bump for missing ppc package
- remove 0 epoch
- add dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:0.14.4-7.1
- rebuild

* Tue May 16 2006 Kristian Høgsberg <krh@redhat.com> - 0:0.14.4-7
- Add missing build requires for libXext.

* Tue Apr 11 2006 Kristian Høgsberg <krh@redhat.com> 0:0.14.4-6
- Build as a shared object.

* Mon Apr 10 2006 Adam Jackson <ajackson@redhat.com 0:0.14.4-5
- Delibcwrap and rebuild for 7.1RC1 ABI.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:0.14.4-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:0.14.4-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 18 2005 Jeremy Katz <katzj@redhat.com> - 0:0.14.4-4
- fix install destination too

* Fri Nov 18 2005 Jeremy Katz <katzj@redhat.com> - 0:0.14.4-3
- patch for modular X include paths

* Fri Nov 18 2005 Kristian Høgsberg <krh@redhat.com> - 0:0.14.4-2
- Remove last bits of monolithic X paths.

* Mon Nov 07 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.4-1
- Modular X.org
- New upstream version

* Thu Aug 04 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.3-3
- Enable ppc builds as we have appletouch driver now

* Tue Jul 26 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.3-2
- Fix man page location (#164295)

* Fri Jul 22 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.3-1
- Update to 0.14.3

* Tue May 17 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.2-1
- Update to 0.14.2

* Mon May 16 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.1-1
- Update to 0.14.1

* Tue Mar 15 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.0-2
- Rebuild

* Thu Jan 06 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.0-1
- Update to 0.14.0
- Drop patch for 64bit as upstream now

* Wed Sep 01 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.5-5
- rebuild

* Wed Sep 01 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.5-4
- more ARCH fixes

* Wed Sep 01 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.5-3
- need to explicitely pass ARCH

* Wed Sep 01 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.5-2
- Add x86_64

* Mon Aug 09 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.5-1
- New version
- Override mandir/bindir rather than patching

* Wed Jul 28 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.4-3
- Fix typo
- Only i386 for the moment

* Wed Jul 28 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.4-2
- Add ExclusiveArch

* Wed Jul 28 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.4-1
- New version

* Fri Jul 09 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.3-1
- New version
- Update makefile patch

* Thu Apr 01 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.12.5-0.fdr.1
- New version
- Remove Imakefile

* Wed Feb 18 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.12.4-0.fdr.1
- New version

* Thu Feb 05 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.12.3-0.fdr.2
- Imakefile now builds synclient and syndaemon
- TODO manpages

* Mon Jan 19 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.12.3-0.fdr.1
- Revert to imakefile and XFree86-sdk
- Include missing sdk headers - push upstream
- don't build synclient and syndaemon for now

* Sat Nov 29 2003 Paul Nasrat <pauln@truemesh.com> - 0:0.12.1-0.fdr.1
- update to latest version
- Remove imake and XFree86-sdk magic

* Fri Oct 03 2003 Paul Nasrat <pauln@truemesh.com> - 0:0.11.7-0.fdr.1
- new version

* Tue Sep 16 2003 Paul Nasrat <pauln@truemesh.com> - 0:0.11.3-0.fdr.3.p11
- Build against latest XFree86-sdk

* Mon Sep 08 2003 Paul Nasrat <pauln@truemesh.com> - 0:0.11.3-0.fdr.2.p11
- Use XFree86 sdk

* Sun Aug 10 2003 Paul Nasrat <pauln@truemesh.com> - 0:0.11.3-0.fdr.1.p11
- Initial RPM release.
