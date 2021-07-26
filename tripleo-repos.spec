%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{executable}/%{executable}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%package -n python3-%{executable}
Summary:    A tool for managing TripleO repos from places like dlrn and Ceph
%{?python_provide:%python_provide python3-%{executable}}
Obsoletes: python2-%{executable} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  git-core
BuildRequires:  python3-mock
BuildRequires:  python3-fixtures
# Required for unit tests
BuildRequires:  python3-requests
BuildRequires:  python3-oslotest
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-ddt
BuildRequires:  python3-pyyaml


Requires:       python3-requests
Requires:       python3-pyyaml

%description -n python3-%{executable}
%{common_desc}

%description
%{common_desc}


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{executable}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
%{py3_build}

%install
%{py3_install}

# TODO(mwhahaha): this needs to be fixed in tripleo-repos
if [ -d %{buildroot}/usr%{_sysconfdir}/tripleo_get_hash ]; then
  install -d -m 755 %{buildroot}/%{_sysconfdir}/tripleo_get_hash
  mv %{buildroot}/usr%{_sysconfdir}/tripleo_get_hash/* %{buildroot}%{_sysconfdir}/tripleo_get_hash/
fi

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{executable} %{buildroot}%{_bindir}/%{executable}-3

%check
%{__python3} setup.py test

%files -n python3-%{executable}
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/tripleo_get_hash
%{python3_sitelib}/tripleo_repos
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/tripleo_repos/tests
%{_bindir}/%{executable}
%{_bindir}/%{executable}-3
%{_bindir}/tripleo-get-hash
%{_bindir}/tripleo-yum-config
%config %{_sysconfdir}/tripleo_get_hash/config.yaml

%changelog
