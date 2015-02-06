%define version 0.2
%define release 9

Summary:		A mk712 touchscreen driver/calibration tool for X 
Name:			xtouch
Version:		%{version}
Release:		%{release}
License:		GPL
Group:			System/X11

Source:			xtouch-0.2_ML1.0.0-beta3-8.tar.bz2
Patch0:			xtouch-correct-device.patch
Patch1:			xtouch-conf-file.patch
Patch2:			xtouch-link.patch
URL:			http://unknown_originally_from_Transmeta's_Midori_Linux			
BuildRequires:		pkgconfig(x11)
BuildRequires:		pkgconfig(xtst)
BuildRequires:		pkgconfig(xt)
BuildRequires:		pkgconfig(xi)

%description
Xtouch enables the use of a mk712 touch screen as an input device for X.
If the configuration file is empty, a calibration routine is launched when
X starts.

%prep
%setup -q
patch -p2 < xtouch-bestfit.patch
%patch0 -p1 -b .dev
%patch1 -p1 -b .conf
%patch2 -p0 -b .link

%build
%setup_compile_flags
pushd src
%make
%make dump-mouse
popd

%install
install -d $RPM_BUILD_ROOT%{_usr}/X11R6/bin
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/devfs/conf.d
install src/%{name} $RPM_BUILD_ROOT%{_usr}/X11R6/bin
install src/dump-mouse $RPM_BUILD_ROOT%{_usr}/X11R6/bin
cat /dev/null >  $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

cat >> $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit.d/%{name} <<EOF
#!/bin/sh
# start the touchscreen handler, it will calibrate if there
# is no xtouch file in /etc or ~/.xtouch
XTOUCH_CALIBRATE=1 xtouch &
EOF
chmod +x $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit.d/%{name}
 
cat >> $RPM_BUILD_ROOT%{_sysconfdir}/devfs/conf.d/mk712.conf <<EOF
REGISTER        ^misc/mk712*        PERMISSIONS     root.root  0644
EOF

%files
%defattr (-,root,root)
%doc CONFIG
%{_usr}/X11R6/bin/%{name}
%{_usr}/X11R6/bin/dump-mouse
%config(noreplace) %{_sysconfdir}/%{name}
%{_sysconfdir}/X11/xinit.d/%{name}
%config(noreplace) %{_sysconfdir}/devfs/conf.d/mk712.conf

