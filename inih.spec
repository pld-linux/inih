#
# Conditional build:
%bcond_without	cxx		# C++ INIReader interface
%bcond_without	static_libs	# static library
#
Summary:	Simple .INI file parser written in C
Summary(pl.UTF-8):	Prosty parser plików .INI napisany w C
Name:		inih
Version:	58
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/benhoyt/inih/releases
Source0:	https://github.com/benhoyt/inih/archive/r%{version}/%{name}-r%{version}.tar.gz
# Source0-md5:	5c9725320ad2c79e0b1f76568bd0ff24
URL:		https://github.com/benhoyt/inih
%{?with_cxx:BuildRequires:	libstdc++-devel >= 6:4.7}
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
inih (INI Not Invented Here) is a simple .INI file parser written in
C. It's only a couple of pages of code, and it was designed to be
small and simple, so it's good for embedded systems. It's also more or
less compatible with Python's ConfigParser style of .INI files,
including RFC 822-style multi-line syntax and `name: value` entries.

%description -l pl.UTF-8
inih (INI Not Invented Here - INI nie wynalezione tutaj) to prosty
parser plików .INI, napisany w C. Jest to tylko kilka stron kodu,
zaprojektowane jako mała i prosta biblioteka, dobra do systemów
wbudowanych. Jest mniej więcej kompatybilna z plikami .INI w stylu
pythonowego ConfigParsera, włącznie ze składnią wielowierszową w
stylu RFC 822 oraz wpisami "nazwa: wartość".

%package devel
Summary:	Header file for inih library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki inih
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for inih library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki inih.

%package static
Summary:	Static inih library
Summary(pl.UTF-8):	Statyczna biblioteka inih
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static inih library.

%description static -l pl.UTF-8
Statyczna biblioteka inih.

%package c++
Summary:	INIReader - simple .INI file parser for C++
Summary(pl.UTF-8):	INIReader - prosty parser plików .INI dla C++
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
INIReader - simple .INI file parser for C++.

%description c++ -l pl.UTF-8
INIReader - prosty parser plików .INI dla C++.

%package c++-devel
Summary:	Header file for INIReader library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki INIReader
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description c++-devel
Header file for INIReader library.

%description c++-devel -l pl.UTF-8
Plik nagłówkowy biblioteki INIReader.

%package c++-static
Summary:	Static INIReader library
Summary(pl.UTF-8):	Statyczna biblioteka INIReader
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
Static INIReader library.

%description c++-static -l pl.UTF-8
Statyczna biblioteka INIReader.

%prep
%setup -q -n %{name}-r%{version}

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/sh,' examples/cpptest.sh

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	-Ddistro_install=true \
	%{?with_cxx:-Dwith_INIReader=true} \

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%if %{without cxx}
%{__rm} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/{INIReaderExample.cpp,cpptest.sh,cpptest.txt}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.md
%attr(755,root,root) %{_libdir}/libinih.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libinih.so
%{_includedir}/ini.h
%{_pkgconfigdir}/inih.pc
%dir %{_examplesdir}/%{name}-%{version}
%{_examplesdir}/%{name}-%{version}/*.c
%{_examplesdir}/%{name}-%{version}/config.def
%{_examplesdir}/%{name}-%{version}/test.ini

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libinih.a
%endif

%if %{with cxx}
%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libINIReader.so.0

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libINIReader.so
%{_includedir}/INIReader.h
%{_pkgconfigdir}/INIReader.pc
%{_examplesdir}/%{name}-%{version}/INIReaderExample.cpp
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/cpptest.sh
%{_examplesdir}/%{name}-%{version}/cpptest.txt

%if %{with static_libs}
%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libINIReader.a
%endif
%endif
