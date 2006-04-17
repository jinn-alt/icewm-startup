Name: icewm-startup
Version: 0.0
Release: alt2

Summary: simple pluggable IceWM autostart manager

Summary(ru_RU.CP1251): менеджер автозапуска программ при старте IceWM
License: GPL
Group: Graphical desktop/Icewm
Url: http://www.imath.kiev.ua/~vlasenko/

Packager: Igor Vlasenko <viy@altlinux.ru>
#Source: %name-%version.tar.bz2

BuildArch: noarch
AutoReq: no
%define icewmconfdir %_sysconfdir/X11/icewm
#due to new icewmconfdir in xorg 7.0
Requires: icewm >= 1.2.25
#define icewmconfdir #_x11x11dir/icewm
#Requires: icewm

%description
Simple pluggable icewm autostart manager is a generic IceWM startup script
which allows one to configure IceWM autostart via installing corresponding
rpm plug-ins.

%description -l ru_RU.CP1251
менеджер автозапуска программ при старте IceWM позволяет просто настраивать 
рабочий стол IceWM путем установки rpm расширений.

%package gkrellm
Group: Graphical desktop/Icewm
Summary: gkrellm autostart at IceWM startup
Summary(ru_RU.CP1251): автозапуск gkrellm при старте IceWM
Requires: %name gkrellm xtoolwait
AutoReq: no

%description gkrellm
gkrellm plug-in for simple pluggable IceWM autostart manager.
%description -l ru_RU.CP1251 gkrellm
gkrellm plug-in для менеджера автозапуска программ при старте IceWM.

%package idesk
Group: Graphical desktop/Icewm
Summary: idesk autostart at IceWM startup
Summary(ru_RU.CP1251): автозапуск idesk при старте IceWM
Requires: %name idesk
Conflicts: %name-kdesktop
AutoReq: no

%description idesk
idesk plug-in for simple pluggable IceWM autostart manager.
%description -l ru_RU.CP1251 idesk
idesk plug-in для менеджера автозапуска программ при старте IceWM.

%package kdesktop
Group: Graphical desktop/Icewm
Summary: kdesktop autostart at IceWM startup
Summary(ru_RU.CP1251): автозапуск kdesktop при старте IceWM
Requires: %name kdebase-wm
Conflicts: %name-idesk
AutoReq: no

%description kdesktop
kdesktop plug-in for simple pluggable IceWM autostart manager.
%description -l ru_RU.CP1251 kdesktop
kdesktop plug-in для менеджера автозапуска программ при старте IceWM.

%package xxkb
Group: Graphical desktop/Icewm
Summary: xxkb autostart at IceWM startup
Summary(ru_RU.CP1251): автозапуск xxkb при старте IceWM
Requires: %name xxkb
AutoReq: no

%description xxkb
xxkb plug-in for simple pluggable IceWM autostart manager.
~/.xxkbrc or /etc/X11/app-defaults/XXkb is required.
%description -l ru_RU.CP1251 xxkb
xxkb plug-in для менеджера автозапуска программ при старте IceWM.
xxkb запускается только при наличии ~/.xxkbrc или /etc/X11/app-defaults/XXkb.

%prep
%setup -q -c -T

%build

%install
%__mkdir_p %buildroot/%icewmconfdir/startup.d
cat <<'EOF' > %buildroot/%icewmconfdir/startup
#!/bin/sh

# starting all system-wide icewm autostart programs
for file in %icewmconfdir/startup.d/*; do
  userfile=~/.icewm/startup.d/`echo $file | sed -e 's,%icewmconfdir/startup.d/,,'`
  # root can disable autostart removing 'execute' bits
  if [ -x $file ]; then 
    # User-supplied programs disable system-wide programs.
    # So user can disable system-wide program 
    # by touching file in ~/.icewm/startup.d/ with the same name
    # or even replace it with his own script.
    [ -e $userfile ] || . $file
  fi
done

# starting user-supplied icewm autostart programs
for file in ~/.icewm/startup.d/*; do
  # running user files 
  # user can disable autostart removing 'execute' bits
  [ -x $file ] && . $file
done
EOF

echo 'xtoolwait gkrellm'> %buildroot/%icewmconfdir/startup.d/gkrellm
echo 'kdesktop&'> %buildroot/%icewmconfdir/startup.d/kdesktop
cat <<EOF > %buildroot/%icewmconfdir/startup.d/idesk
#!/bin/sh
if [ -e ~/.ideskrc ]; then 
  idesk &
else # first run
  startidesk &
fi
EOF

cat <<EOF > %buildroot/%icewmconfdir/startup.d/xxkb
#!/bin/sh
# it is not wise to run non-configured xxkb, so we look 
# whether it is configured.
# if [ -e ~/.xxkbrc ] then user has configured xxkb properly
# if [ -e /etc/X11/app-defaults/XXkb ]
# then sysadmin has configured xxkb properly.

if [ -e ~/.xxkbrc ] || [ -e /etc/X11/app-defaults/XXkb ]; then
  xxkb&
fi
EOF

chmod 755 %buildroot/%icewmconfdir/startup.d/*
chmod 755 %buildroot/%icewmconfdir/startup

%files
#%doc README
%dir %icewmconfdir/startup.d
%config %icewmconfdir/startup
#%_man1dir/*

%files gkrellm
%config %icewmconfdir/startup.d/gkrellm

%files idesk
%config %icewmconfdir/startup.d/idesk

%files kdesktop
%config %icewmconfdir/startup.d/kdesktop

%files xxkb
%config %icewmconfdir/startup.d/xxkb

%changelog
* Mon Apr 17 2006 Igor Vlasenko <viy@altlinux.ru> 0.0-alt2
- added kdesktop support

* Wed Mar 22 2006 Igor Vlasenko <viy@altlinux.ru> 0.0-alt1
- build for Sisyphus

* Wed Mar 22 2006 Igor Vlasenko <viy@altlinux.ru> 0.0-alt0.M30.1
- backport for M30

* Wed Mar 22 2006 Igor Vlasenko <viy@altlinux.ru> 0.0-alt0
- initial build
