#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (not included in release tarball)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Sphinx extension to support coroutines in markup
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do obsługi korutyn w znacznikach
Name:		python-sphinxcontrib-asyncio
Version:	0.2.0
Release:	4
License:	Apache v2
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinxcontrib-asyncio/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinxcontrib-asyncio/sphinxcontrib-asyncio-%{version}.tar.gz
# Source0-md5:	ad3372cb3be157a98834c2f121674862
URL:		https://pypi.org/project/sphinxcontrib-asyncio/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
Requires:	python-sphinxcontrib
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sphinx extension for adding asyncio-specific markups.

%description -l pl.UTF-8
Rozszerzenie Sphinksa do dodawania oznaczeń specyficznych dla asyncio.

%package -n python3-sphinxcontrib-asyncio
Summary:	Sphinx extension to support coroutines in markup
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do obsługi korutyn w znacznikach
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3
Requires:	python3-sphinxcontrib

%description -n python3-sphinxcontrib-asyncio
Sphinx extension for adding asyncio-specific markups.

%description -n python3-sphinxcontrib-asyncio -l pl.UTF-8
Rozszerzenie Sphinksa do dodawania oznaczeń specyficznych dla asyncio.

%package apidocs
Summary:	API documentation for Python sphinxcontrib-asyncio module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sphinxcontrib-asyncio
Group:		Documentation

%description apidocs
API documentation for Python sphinxcontrib-asyncio module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sphinxcontrib-asyncio.

%prep
%setup -q -n sphinxcontrib-asyncio-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
# provides by python-sphinxcontrib in PLD
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/sphinxcontrib/__init__.py*
%endif

%if %{with python3}
%py3_install

# provides by python3-sphinxcontrib in PLD
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinxcontrib/__init__.py \
	$RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinxcontrib/__pycache__/__init__.*.py*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%{py_sitescriptdir}/sphinxcontrib/asyncio.py[co]
%{py_sitescriptdir}/sphinxcontrib_asyncio-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-sphinxcontrib-asyncio
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%{py3_sitescriptdir}/sphinxcontrib/asyncio.py
%{py3_sitescriptdir}/sphinxcontrib/__pycache__/asyncio.cpython-*.py[co]
%{py3_sitescriptdir}/sphinxcontrib_asyncio-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
