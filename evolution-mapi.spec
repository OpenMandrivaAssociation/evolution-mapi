%define version 3.4.3
%define evo_version 3.4.1
%define eds_version 3.4.1
%define libmapi_version 0.9
%define intltool_version 0.35.5

%define evo_major 3.4
%define eds_major 1.2

%define strict_build_settings 0

%define api 1.0
%define major 0
%define libname %mklibname exchangemapi %api %major
%define develname %mklibname -d exchangemapi

Name: evolution-mapi
Version: %version
Release: 1
Group: Networking/Mail
Summary: Evolution extension for MS Exchange 2007/2010 servers
License: LGPLv2+
URL: http://www.gnome.org/projects/evolution-mapi/
Source: http://ftp.gnome.org/pub/GNOME/sources/%name/%name-%{version}.tar.xz
Requires: evolution >= %{evo_version}
Requires: evolution-data-server >= %{eds_version}
Requires: %libname >= %version-%release
BuildRoot: {_tmppath}/%{name}-%{version}-root

BuildRequires: evolution-data-server-devel >= %{eds_version}
BuildRequires: evolution-devel >= %{evo_version}
BuildRequires: pkgconfig(libebackend-1.2)
BuildRequires: pkgconfig(libedata-cal-1.2)
BuildRequires: pkgconfig(libedata-book-1.2)
BuildRequires: gettext
BuildRequires: intltool >= %{intltool_version}
BuildRequires: gtk-doc
BuildRequires: libmapi-devel >= %{libmapi_version}
#gw another .la dep
BuildRequires: gnome-desktop-devel
BuildRequires: tdb-devel
BuildRequires: samba4-devel

%description
This package allows Evolution to interact with MS Exchange 2007/2010 servers.

%package -n %libname
Summary: Shared library of %name
Group: System/Libraries

%description -n %libname
This package allows Evolution to interact with MS Exchange 2007/2010 servers.


%package -n %develname
Summary: Development files for building against %{name}
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Requires: evolution-data-server-devel >= %{eds_version}
Requires: evolution-devel >= %{evo_version}
Provides: %name-devel = %version-%release
Obsoletes: %name-devel
Provides: lib%name-devel = %version-%release

%description -n %develname
Development files needed for building things which link against %{name}.

%prep
%setup -q

%build

# Add stricter build settings here as the source code gets cleaned up.
# We want to make sure things like compiler warnings and avoiding deprecated
# functions in the GNOME/GTK+ libraries stay fixed.
#
# Please file a bug report at bugzilla.gnome.org if these settings break
# compilation, and encourage the upstream developers to use them.

%if %{strict_build_settings}
CFLAGS="$CFLAGS \
	-DG_DISABLE_DEPRECATED=1 \
	-DPANGO_DISABLE_DEPRECATED=1 \
	-DGDK_PIXBUF_DISABLE_DEPRECATED=1 \
	-DGDK_DISABLE_DEPRECATED=1 \
	-DGTK_DISABLE_DEPRECATED=1 \
	-DEDS_DISABLE_DEPRECATED=1 \
	-Wdeclaration-after-statement \
	-Werror-implicit-function-declaration"
%endif

%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

find $RPM_BUILD_ROOT/%{_libdir}/evo* -name '*.la' -exec rm {} \;

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL README
%{_libdir}/evolution/%{evo_major}/plugins/*
%{_libdir}/evolution-data-server/camel-providers/libcamelmapi.so
%{_libdir}/evolution-data-server/camel-providers/libcamelmapi.urls
%{_libdir}/evolution-data-server/addressbook-backends/libebookbackendmapi.so
%{_libdir}/evolution-data-server/calendar-backends/libecalbackendmapi.so
%{_datadir}/evolution-data-server-%{evo_major}/mapi

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/libexchangemapi-%api.so.%{major}*

%files -n %develname
%defattr(-,root,root,-)
%{_includedir}/evolution-data-server-%{evo_major}/mapi
%{_libdir}/libexchangemapi-1.0.so
%{_libdir}/pkgconfig/libexchangemapi-1.0.pc
