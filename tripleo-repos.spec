%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


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

%package -n python2-%{executable}
Summary:    A tool for managing TripleO repos from places like dlrn and Ceph.
%{?python_provide:%python_provide python2-%{executable}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  python-mock
BuildRequires:  python-fixtures
# Required for unit tests
BuildRequires:  python-requests
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools


Requires:       python-requests

%description -n python2-%{executable}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{executable}
Summary:    tripleo-repos
%{?python_provide:%python_provide python3-%{executable}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-mock
BuildRequires:  python3-fixtures
# Required for unit tests
BuildRequires:  python3-requests
BuildRequires:  python3-oslotest
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools

Requires:       python3-requests

%description -n python3-%{executable}
%{common_desc}

%endif # with_python3


%description
%{common_desc}


%prep
%autosetup -n %{executable}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python3_version}
ln -s ./%{executable}-%{python3_version} %{buildroot}%{_bindir}/%{executable}-3
%endif
%py2_install
mv %{buildroot}%{_bindir}/%{executable} %{buildroot}%{_bindir}/%{executable}-%{python2_version}
ln -s %{_bindir}/%{executable}-%{python2_version} %{buildroot}%{_bindir}/%{executable}-2
ln -s %{_bindir}/%{executable}-2 %{buildroot}%{_bindir}/%{executable}

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{executable}
%license LICENSE
%doc README.rst
%{python2_sitelib}/tripleo_repos
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/tripleo_repos/tests
%{_bindir}/%{executable}
%{_bindir}/%{executable}-2
%{_bindir}/%{executable}-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{executable}
%license LICENSE
%doc README.rst
%{python3_sitelib}/tripleo_repos
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/tripleo_repos/tests
%{_bindir}/%{executable}-3
%{_bindir}/%{executable}-%{python3_version}
%endif

%changelog
