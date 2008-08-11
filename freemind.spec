%define section         free
%define gcj_support     0

Name:           freemind
Version:        0.9.0
Release:        %mkrel 0.0.6
Epoch:          1
Summary:        Free mind mapping software
License:        GPL
URL:            http://freemind.sourceforge.net/
Group:          Development/Java
Source0:        http://downloads.sourceforge.net/sourceforge/freemind/freemind-src-0.9.0_Beta_19.tar.gz
Source1:        freemind.desktop
Source2:        freemind.sh
Source3:        freemind.xml
Source4:        freemind-bindings.patch
Patch0:         freemind-patch-bindings.patch
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:       firefox
Requires:       crimson
Requires:       simplyhtml
Requires:       jakarta-commons-lang
Requires:       jakarta-oro
Requires:       jgoodies-forms
Requires:       jibx
Requires:       echomine-muse
Requires:       javahelp2
Requires:       batik
Requires:       batik-squiggle
Requires:       fop
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  ant-trax
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  java-rpmbuild
BuildRequires:  crimson
BuildRequires:  simplyhtml
BuildRequires:  jakarta-commons-lang
BuildRequires:  jakarta-oro
BuildRequires:  jgoodies-forms
BuildRequires:  junit
BuildRequires:  jarbundler
BuildRequires:  jibx
BuildRequires:  echomine-muse
BuildRequires:  javahelp2
BuildRequires:  batik
BuildRequires:  batik-squiggle
BuildRequires:  fop
BuildRequires:  xsd2jibx
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%setup -q -c
find . -name '*.jar' | xargs -t %{__rm}
pushd freemind
%{__cp} -a %{SOURCE4} .
%patch0 -p1
%{__perl} -pi -e 's/^Class-Path:.*\n//' MANIFEST.MF
%{__perl} -pi -e 's/^properties_folder = freemind$/properties_folder = .freemind/;' \
              -e 's|\./|file://%{_datadir}/%{name}/|g;' \
              -e 's|mozilla|firefox|;' \
  freemind.properties

pushd lib/SimplyHTML
%{__ln_s} $(build-classpath simplyhtml) SimplyHTML.jar
%{__ln_s} $(build-classpath gnu-regexp) gnu-regexp-1.1.4.jar
popd

pushd lib
%{__ln_s} $(build-classpath commons-lang) commons-lang-2.0.jar
%{__ln_s} $(build-classpath jgoodies-forms) forms-1.0.5.jar
%{__ln_s} $(build-classpath junit) junit.jar
%{__ln_s} $(build-classpath jarbundler) jarbundler-1.8.1.jar
popd

pushd lib/jibx
%{__ln_s} $(build-classpath bcel) bcel.jar
%{__ln_s} $(build-classpath commons-logging) commons-logging-1.0.4.jar
%{__ln_s} $(build-classpath jaxme/ws-jaxmejs) jaxme-js-0.3.jar
%{__ln_s} $(build-classpath log4j) log4j-1.2.8.jar
%{__ln_s} $(build-classpath xpp3) xpp3.jar
%{__ln_s} $(build-classpath jibx/bind) jibx-bind.jar
%{__ln_s} $(build-classpath jibx/extras) jibx-extras.jar
%{__ln_s} $(build-classpath jibx/run) jibx-run.jar
%{__ln_s} $(build-classpath xsd2jibx) xsd2jibx.jar
popd

pushd plugins/collaboration/jabber
%{__ln_s} $(build-classpath commons-logging) commons-logging.jar
%{__ln_s} $(build-classpath crimson) crimson-1.1.3.jar
%{__ln_s} $(build-classpath oro) jakarta-oro.jar
%{__ln_s} $(build-classpath jaxp) jaxp-1.1.jar
%{__ln_s} $(build-classpath jdom) jdom.jar
%{__ln_s} $(build-classpath log4j) log4j.jar
%{__ln_s} $(build-classpath muse) muse.jar
popd

pushd plugins/help
%{__ln_s} $(build-classpath javahelp2) jhall.jar
popd

pushd plugins/latex
# FIXME: non-free HotEqn.jar
popd

pushd plugins/script
# FIXME: not in mdv (requires maven to build) groovy-all-1.5.6.jar
popd

pushd plugins/svg
%{__ln_s} $(build-classpath batik-all) batik-awt-util.jar
%{__ln_s} $(build-classpath batik-all) batik-bridge.jar
%{__ln_s} $(build-classpath batik-all) batik-css.jar
%{__ln_s} $(build-classpath batik-all) batik-dom.jar
%{__ln_s} $(build-classpath batik-all) batik-ext.jar
%{__ln_s} $(build-classpath batik-all) batik-extension.jar
%{__ln_s} $(build-classpath batik-all) batik-gui-util.jar
%{__ln_s} $(build-classpath batik-all) batik-gvt.jar
%{__ln_s} $(build-classpath batik-all) batik-parser.jar
%{__ln_s} $(build-classpath batik-all) batik-script.jar
%{__ln_s} $(build-classpath batik-squiggle) batik-squiggle.jar
%{__ln_s} $(build-classpath batik-all) batik-svg-dom.jar
%{__ln_s} $(build-classpath batik-all) batik-svggen.jar
%{__ln_s} $(build-classpath batik-all) batik-swing.jar
%{__ln_s} $(build-classpath batik-all) batik-transcoder.jar
%{__ln_s} $(build-classpath batik-all) batik-util.jar
%{__ln_s} $(build-classpath batik-all) batik-xml.jar
%{__ln_s} $(build-classpath rhino) js.jar
%{__ln_s} $(build-classpath pdf-transcoder) pdf-transcoder.jar
%{__ln_s} $(build-classpath xerces-j2) xerces_2_5_0.jar
%{__ln_s} $(build-classpath xml-commons-apis) xml-apis.jar
popd

JARS=`%{_bindir}/find . ! -type l -name '*.jar'`
test -z "$JARS" || exit 1

# FIXME: non-free HotEqn.jar
%{__rm} -r plugins/latex
# FIXME: missing groovy-1.5.6
%{__rm} -r plugins/script
popd

%build
pushd freemind
export OPT_JAR_LIST="`%{__cat} %{_sysconfdir}/ant.d/nodeps` `%{__cat} %{_sysconfdir}/ant.d/trax`"
export CLASSPATH=$(build-classpath avalon-framework)
%{ant} all doc
popd

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a bin/dist/lib/freemind.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__cp} -a bin/dist/lib/bindings.jar %{buildroot}%{_javadir}/%{name}-bindings-%{version}.jar
%{__cp} -a bin/dist/browser/freemindbrowser.jar %{buildroot}%{_javadir}/%{name}browser-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a bin/dist/doc/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

# scripts
%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} -a %{SOURCE2} %{buildroot}%{_bindir}/%{name}

# data
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__cp} -a bin/dist/* %{buildroot}%{_datadir}/%{name}/

# freedesktop.org menu entry
%{_bindir}/desktop-file-install --vendor="" \
  --remove-category="Application" \
  --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

%{__mkdir_p} %{buildroot}%{_datadir}/pixmaps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps

pushd freemind
%{_bindir}/convert -scale 32 images/FreeMindWindowIcon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
%{_bindir}/convert -scale 16 images/FreeMindWindowIcon.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_bindir}/convert -scale 32 images/FreeMindWindowIcon.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_bindir}/convert -scale 48 images/FreeMindWindowIcon.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
popd

%{__mkdir_p} %{buildroot}%{_datadir}/mime/packages
%{__cp} -a %{SOURCE3} %{buildroot}%{_datadir}/mime/packages/

pushd %{buildroot}%{_datadir}/%{name}
%{__rm} freemind.bat
%{__rm} FreeMind.exe
%{__rm} freemind.sh
%{__rm} -r doc/javadoc
%{__ln_s}f %{_javadocdir}/%{name} doc/javadoc
%{__ln_s}f %{_javadir}/freemindbrowser.jar browser/freemindbrowser.jar
%{__ln_s}f %{_javadir}/freemind.jar lib/freemind.jar
%{__ln_s}f $(build-classpath jgoodies-forms) lib/forms-1.0.5.jar
%{__ln_s}f $(build-classpath simplyhtml) lib/SimplyHTML/SimplyHTML.jar
%{__ln_s}f $(build-classpath gnu-regexp) lib/SimplyHTML/gnu-regexp-1.1.4.jar
%{__ln_s}f %{_javadir}/freemind-bindings.jar lib/bindings.jar
%{__ln_s}f $(build-classpath xpp3) lib/jibx/xpp3.jar
%{__ln_s}f $(build-classpath jibx/run) lib/jibx/jibx-run.jar
%{__ln_s}f $(build-classpath commons-lang) lib/commons-lang-2.0.jar
%{__ln_s}f $(build-classpath javahelp2) plugins/help/jhall.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-awt-util.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-xml.jar
%{__ln_s}f $(build-classpath xml-commons-apis) plugins/svg/xml-apis.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-svg-dom.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-transcoder.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-bridge.jar
%{__ln_s}f $(build-classpath batik-squiggle) plugins/svg/batik-squiggle.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-dom.jar
%{__ln_s}f $(build-classpath xerces-j2) plugins/svg/xerces_2_5_0.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-util.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-swing.jar
%{__ln_s}f $(build-classpath rhino) plugins/svg/js.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-parser.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-css.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-extension.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-svggen.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-ext.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-gui-util.jar
%{__ln_s}f $(build-classpath pdf-transcoder) plugins/svg/pdf-transcoder.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-gvt.jar
%{__ln_s}f $(build-classpath batik-all) plugins/svg/batik-script.jar
JARS=`%{_bindir}/find . ! -type l -name '*.jar' -a ! -name '*_plugin.jar'`
test -z "$JARS" || exit 1
EXES=`%{_bindir}/find . -name '*.exe' -o -name '*.bat' -o -name '*.sh'`
test -z "$EXES" || exit 1
popd

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
%{update_mime_database}
%update_icon_cache hicolor

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif
%{clean_desktop_database}
%{clean_mime_database}
%clean_icon_cache hicolor

%files
%defattr(0644,root,root,0755)
%doc freemind/history.txt freemind/license freemind/readme.txt
%attr(0755,root,root) %{_bindir}/%{name}
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_javadir}/freemind.jar
%{_javadir}/freemind-%{version}.jar
%{_javadir}/freemind-bindings.jar
%{_javadir}/freemind-bindings-%{version}.jar
%{_javadir}/freemindbrowser.jar
%{_javadir}/freemindbrowser-%{version}.jar
%{_datadir}/%{name}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
