#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (not included in sdist)

Summary:	Sphinx extension to support coroutines in markup
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do obsługi korutyn w znacznikach
Name:		python3-sphinxcontrib-asyncio
Version:	0.3.0
Release:	2
License:	Apache v2
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinxcontrib-asyncio/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinxcontrib-asyncio/sphinxcontrib-asyncio-%{version}.tar.gz
# Source0-md5:	5445823a927f3368dd81b9061bec0055
URL:		https://pypi.org/project/sphinxcontrib-asyncio/
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 3.0
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
# requires already installed package
BuildRequires:	python3-sphinxcontrib-asyncio
BuildRequires:	sphinx-pdg >= 3.0
%endif
Requires:	python3-modules >= 1:3.5
Requires:	python-sphinxcontrib
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sphinx extension for adding asyncio-specific markups.

%description -l pl.UTF-8
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
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

# provides by python3-sphinxcontrib in PLD
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinxcontrib/__init__.py \
	$RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinxcontrib/__pycache__/__init__.*.py*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%{py3_sitescriptdir}/sphinxcontrib/asyncio.py
%{py3_sitescriptdir}/sphinxcontrib/__pycache__/asyncio.cpython-*.py[co]
%{py3_sitescriptdir}/sphinxcontrib_asyncio-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
