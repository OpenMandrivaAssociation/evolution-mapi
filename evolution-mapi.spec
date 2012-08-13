%define evo_major 3.4
%define eds_major 1.2

%define strict_build_settings 0

%define api	1.0
%define major	0
%define libname	%mklibname exchangemapi %{api} %{major}
%define devname	%mklibname -d exchangemapi

Summary:	Evolution extension for MS Exchange 2007/2010 servers
Name:		evolution-mapi
Version:	3.4.4
Release:	1
Group:		Networking/Mail
License:	LGPLv2+
URL:		http://www.gnome.org/projects/evolution-mapi/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz

BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: evolution-data-server-devel
BuildRequires: pkgconfig(evolution-shell-3.0)
BuildRequires: pkgconfig(libebackend-1.2)
BuildRequires: pkgconfig(libedata-cal-1.2)
BuildRequires: pkgconfig(libedata-book-1.2)
BuildRequires: libmapi-devel
BuildRequires: gnome-desktop-devel
BuildRequires: tdb-devel
BuildRequires: samba4-devel

Requires:	evolution
Requires:	evolution-data-server

%description
This package allows Evolution to interact with MS Exchange 2007/2010 servers.

%package -n %{libname}
Summary: Shared library of %{name}
Group: System/Libraries

%description -n %{libname}
This package allows Evolution to interact with MS Exchange 2007/2010 servers.

%package -n %{devname}
Summary: Development files for building against %{name}
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %version-%release

%description -n %{devname}
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
%makeinstall_std

find $RPM_BUILD_ROOT/%{_libdir}/evo* -name '*.la' -exec rm {} \;

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING INSTALL README
%{_libdir}/evolution/%{evo_major}/plugins/*
%{_libdir}/evolution-data-server/camel-providers/libcamelmapi.so
%{_libdir}/evolution-data-server/camel-providers/libcamelmapi.urls
%{_libdir}/evolution-data-server/addressbook-backends/libebookbackendmapi.so
%{_libdir}/evolution-data-server/calendar-backends/libecalbackendmapi.so
%{_datadir}/evolution-data-server-%{evo_major}/mapi

%files -n %{libname}
%{_libdir}/libexchangemapi-%{api}.so.%{major}*

%files -n %{devname}
%{_includedir}/evolution-data-server-%{evo_major}/mapi
%{_libdir}/libexchangemapi-1.0.so
%{_libdir}/pkgconfig/libexchangemapi-1.0.pc
