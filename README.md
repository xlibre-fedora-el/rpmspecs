# XLibre for Fedora and Enterprise Linux

This repository contains both source code and instructions on how to install the XLibre third-party packages on [Fedora Linux](https://fedoraproject.org), [CentOS Stream](https://www.centos.org/download/), and Enterprise Linux distributions like [AlmaLinux](https://almalinux.org/), [Red Hat Enterprise Linux (RHEL)](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux), [Oracle Linux](https://www.oracle.com/linux), and [Rocky Linux](https://rockylinux.org).

## Installation Instructions

In the [XLibre Copr](https://copr.fedorainfracloud.org/coprs/g/xlibre/xlibre-xserver) repository, you will find the binary packages for the distributions listed above. The installation process differs per distribution as follows.

### Fedora Linux, CentOS Stream and Enterprise Linux 9

You can easily install the XLibre Xserver and the libinput driver using the [Copr plugin](https://dnf5.readthedocs.io/en/latest/dnf5_plugins/copr.8.html) of [`dnf`](https://dnf5.readthedocs.io/en/latest):

```shell
sudo dnf copr enable @xlibre/xlibre-xserver
sudo dnf install xlibre-xserver xlibre-xf86-input-libinput --allowerasing
```

### Enterprise Linux 10

> [!warning]
> Don't use the `dnf copr enable` command, as it will enable the [EPEL](https://docs.fedoraproject.org/en-US/epel) repository built for CentOS+EPEL. This can sometimes create incompatibilities on EL distributions due to newer package versions. 

Use the commands below to activate the RHEL+EPEL repository for Red Hat Enterprise Linux, Oracle Linux, and Rocky Linux. Then install the XLibre Xserver and the driver for libinput:

```shell
export XLIBRE_COPR='https://copr.fedorainfracloud.org/coprs/g/xlibre/xlibre-xserver'
sudo wget "$XLIBRE_COPR/repo/rhel+epel-10/group_xlibre-xlibre-xserver-rhel+epel-10.repo" \
    -O /etc/yum.repos.d/xlibre-xserver-rhel+epel-10.repo
sudo dnf install xlibre-xserver xlibre-xf86-input-libinput
```

### AlmaLinux 10 x86_64-v2

Download the repository description file and install the XLibre Xserver and the driver for libinput:

```shell
export XLIBRE_COPR='https://copr.fedorainfracloud.org/coprs/g/xlibre/xlibre-xserver'
sudo wget "$XLIBRE_COPR/repo/alma+epel-10/group_xlibre-xlibre-xserver-alma+epel-10.repo" \
    -O /etc/yum.repos.d/xlibre-xserver-alma+epel-10.repo
sudo dnf install xlibre-xserver xlibre-xf86-input-libinput
```
