Name:		im-ja
Summary:	Japanese input module for GTK2
Version:	1.5
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
URL:		http://im-ja.sourceforge.net/
Source:		http://im-ja.sourceforge.net/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Conflicts:	kinput2-wnn4 uim
BuildRequires:	gnome-panel-devel
BuildRequires:	canna-devel
BuildRequires:	anthy-devel
BuildRequires:	docbook-utils
BuildRequires:	perl-XML-Parser
Requires:	locales-ja
Requires(post,postun):	%_bindir/gtk-query-immodules-2.0
Requires(post,preun):	GConf2
Requires:	gtk+2.0 >= 2.4.4-2mdk

%description
im-ja aims to be a generic Japanese input module for GTK+2. Currently present
input modes are:
  * Direct input (romaji)
  * Hiragana
  * Katakana
  * Half-width katakana
  * Zenkaku
  * Kanji conversion using the following engines:
     o Canna
     o Anthy
     o Skk(server)
     o Kanji character recognition (based on Kanjipad)

Conversion hotkeys, status window, preedit text colors, etc. can be customized
through a GUI. An optional applet is also included for the gnome-panel which
can be used to display and change the input method.

im-ja also comes with a XIM server that can be used as a replacement for other
commonly used XIM servers such as kinput2 to enable Japanese input into
non-GTK2 applications.


%prep
%setup -q

%build
%configure2_5x --disable-schemas-install --disable-wnn
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# we don't care about the .la file...
rm -f %{buildroot}/%{_libdir}/gtk-2.0/*/immodules/*.la

%find_lang %{name}

# xdg menu entry
mkdir -p %buildroot%_datadir/applications
cat << EOF > %buildroot%_datadir/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=Im-Ja configurator
Comment=Configurator for the GTK+2 Japanese Input Module
Exec=/usr/bin/im-ja-conf
Icon=%{name}-conf.png
Type=Application
Categories=GTK;Settings;Languages;
EOF

%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
%{_bindir}/gtk-query-immodules-2.0 %_lib > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/im-ja.schemas > /dev/null
%update_menus

%preun
if [ "$1" = "0" ]; then
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/im-ja.schemas > /dev/null
fi

%postun
/sbin/ldconfig
%{_bindir}/gtk-query-immodules-2.0 %_lib > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib
%clean_menus

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING README TODO
%dir %{_libdir}/im-ja
%defattr(755,root,root,755)
%{_bindir}/*
%{_libdir}/gtk-2.0/*/immodules/*.so
%{_libdir}/im-ja/im-ja-applet
%{_libdir}/im-ja/im-ja-helper
%{_libdir}/im-ja/kpengine
%defattr(644,root,root,755)
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/bonobo/servers/*
%{_datadir}/%name
%{_datadir}/control-center-2.0/capplets/*
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_mandir}/man1/*
