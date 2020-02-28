# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global executable tripleo-repos

%global common_desc \
tripleo-repos is a tool to provide a single method for setting up the necessary \
yum repositories to do a TripleO deployment.

Name:       %{executable}
Version:    XXX
Release:    XXX
Summary:    A tool for managing TripleO repos from places like dlrn and Ceph.
License:    ASL 2.0
URL:        http://launchpad.net/tripleo/

Source0:    http://tarballs.openstack.org/%{executable}/%{executable}-%{upstream_version}.tar.gz

BuildArch:  noarch

%package -n python%{pyver}-%{executable}
Summary:    A tool for managing TripleO repos from places like dlrn and Ceph.
%{?python_provide:%python_provide python%{pyver}-%{executable}}
%if %{pyver} == 3
Obsoletes: python2-%{executable} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-fixtures
# Required for unit tests
BuildRequires:  python%{pyver}-requests
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-ddt


%if %{pyver} == 2
Requires:       python-requests
%else
Requires:       python%{pyver}-requests
%endif

%description -n python%{pyver}-%{executable}
%{common_desc}

%description
%{common_desc}


%prep
%autosetup -n %{executable}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{pyver_build}

%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{executable} %{buildroot}%{_bindir}/%{executable}-%{pyver}

%check
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{executable}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/tripleo_repos
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/tripleo_repos/tests
%{_bindir}/%{executable}
%{_bindir}/%{executable}-%{pyver}

%changelog
