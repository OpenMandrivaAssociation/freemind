%define section         free
%define gcj_support     1

Name:           freemind
Version:        0.7.1
Release:        %mkrel 2
Epoch:          1
Summary:        Free mind mapping software
License:        GPL
URL:            http://freemind.sourceforge.net/
Group:          Development/Java
# cvs -z3 -d:pserver:anonymous@freemind.cvs.sourceforge.net:/cvsroot/freemind co -P -r FM-0-7-1 freemind
Source0:        freemind-%{version}.tar.bz2
Source1:        freemind.desktop
Source2:        freemind.sh
Patch0:         freemind-build.patch
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:       mozilla-firefox
BuildRequires:  ant
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  jpackage-utils
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
FreeMind is a premier free mind-mapping software written in Java. The 
recent development has hopefully turned it into high productivity tool. 
We are proud that the operation and navigation of FreeMind is faster 
than that of MindManager because of one-click "fold / unfold" and 
"follow link" operations.

So you want to write a completely new metaphysics? Why don't you use 
FreeMind? You have a tool at hand that remarkably resembles the tray 
slips of Robert Pirsig, described in his sequel to Zen and the Art of 
Motorcycle Maintenance called Lila. Do you want to refactor your essays 
in a similar way you would refactor software? Or do you want to keep 
personal knowledge base, which is easy to manage? Why don't you try 
FreeMind? Do you want to prioritize, know where you are, where you've 
been and where you are heading, as Stephen Covey would advise you? Have 
you tried FreeMind to keep track of all the things that are needed for 
that?

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{_bindir}/find -type d -name CVS | %{_bindir}/xargs -t %{__rm} -r
%patch0 -p1
%{__perl} -pi -e 's/^Class-Path:.*\n//' MANIFEST.MF
%{__perl} -pi -e 's/^properties_folder = freemind$/properties_folder = .freemind/;' \
              -e 's|\./|file://%{_datadir}/%{name}/|g;' \
              -e 's|mozilla|mozilla-firefox|;' \
  freemind.properties user.properties
%{__perl} -pi -e 's/<javadoc/<javadoc source="1.4"/g' build.xml

%build
%{ant} dist browser doc

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a bin/dist/lib/freemind.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__cp} -a bin/dist/browser/freemindbrowser.jar %{buildroot}%{_javadir}/%{name}browser-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a bin/dist/doc/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})
%{__rm} -rf doc/javadoc

# scripts
%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} -a %{SOURCE2} %{buildroot}%{_bindir}/%{name}

# data
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__cp} -a accessories/ doc/ html/ %{buildroot}%{_datadir}/%{name}

# freedesktop.org menu entry
%{_bindir}/desktop-file-install --vendor="mandriva" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Office-Presentations" \
  --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

%{__mkdir_p} %{buildroot}%{_datadir}/pixmaps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps

%{_bindir}/convert -scale 32 images/FreeMindWindowIcon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
%{_bindir}/convert -scale 16 images/FreeMindWindowIcon.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_bindir}/convert -scale 32 images/FreeMindWindowIcon.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_bindir}/convert -scale 48 images/FreeMindWindowIcon.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%post
%if %{gcj_support}
%{update_gcjdb}
%endif
%{update_desktop_database}
%update_icon_cache hicolor

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif
%{clean_desktop_database}
%clean_icon_cache hicolor

%post javadoc
%{__rm} -f %{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  %{__rm} -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc history.txt license
%attr(0755,root,root) %{_bindir}/%{name}
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_javadir}/freemind.jar
%{_javadir}/freemind-%{version}.jar
%{_javadir}/freemindbrowser.jar
%{_javadir}/freemindbrowser-%{version}.jar
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/accessories
%dir %{_datadir}/%{name}/doc
%dir %{_datadir}/%{name}/html
%{_datadir}/%{name}/accessories/mm2xbel.xsl
%{_datadir}/%{name}/accessories/xbel2mm.xsl
%{_datadir}/%{name}/doc/freemind.mm
%{_datadir}/%{name}/html/freemindbrowser.html
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%dir %{_javadocdir}/%{name}
