%define version 0.26.0.1
%define branch (echo %version|perl -pe 's/(\d+\.\d+)\..*/$1/g')
%define evo_version 2.26
%define eds_version 2.26
%define libmapi_version 0.8
%define intltool_version 0.35.5

%define __libtoolize /bin/true

%define evo_major 2.26
%define eds_major 1.2

%define strict_build_settings 1

Name: evolution-mapi
Version: %version
Release: %mkrel 1
Group: Networking/Mail
Summary: Evolution extension for MS Exchange 2007 servers
License: LGPLv2+
Epoch: 0
URL: http://www.gnome.org/projects/evolution-mapi/
Source: http://ftp.gnome.org/pub/gnome/sources/evolution-mapi/%{branch}/evolution-mapi-%{version}.tar.bz2
Requires: evolution >= %{evo_version}
Requires: evolution-data-server >= %{eds_version}

BuildRequires: evolution-data-server-devel >= %{eds_version}
BuildRequires: evolution-devel >= %{evo_version}
BuildRequires: gettext
BuildRequires: intltool >= %{intltool_version}
#BuildRequires: openchange-devel >= %{libmapi_version}
BuildRequires: lib64mapi-devel >= %{libmapi_version}
BuildRequires: gnome-pilot-devel

%description
This package allows Evolution to interact with MS Exchange 2007 servers.

%package devel
Summary: Development files for building against %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: evolution-data-server-devel >= %{eds_version}
Requires: evolution-devel >= %{evo_version}
Requires: openchange-devel >= %{libmapi_version}

%description devel
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

%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

find $RPM_BUILD_ROOT/%{_libdir} -name '*.la' -exec rm {} \;

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL README
%{_libdir}/libexchangemapi-1.0.so.*
%{_libdir}/evolution/%{evo_major}/plugins/*
%{_libdir}/evolution-data-server-%{eds_major}/camel-providers/libcamelmapi.so
%{_libdir}/evolution-data-server-%{eds_major}/camel-providers/libcamelmapi.urls
%{_libdir}/evolution-data-server-%{eds_major}/extensions/libebookbackendmapi.so
%{_libdir}/evolution-data-server-%{eds_major}/extensions/libecalbackendmapi.so
%{_datadir}/evolution-data-server-%{evo_major}/mapi

%files devel
%defattr(-,root,root,-)
%{_includedir}/evolution-data-server-%{evo_major}/mapi
%{_libdir}/libexchangemapi-1.0.so
%{_libdir}/pkgconfig/libexchangemapi-1.0.pc