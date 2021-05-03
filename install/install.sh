#!/usr/bin/env sh

# shellcheck disable=SC2039

# Options
#
#   -V, --verbose
#     Enable verbose output for the installer
#
#   -f, -y, --force, --yes
#     Skip the confirmation prompt during installation
#
#   -c, --configuration-dir
#     Override the bin installation directory
#
#   -r, --release
#     Override the release which should be installed

set -eu
printf '\n'

BOLD="$(tput bold 2>/dev/null || printf '')"
GREY="$(tput setaf 0 2>/dev/null || printf '')"
UNDERLINE="$(tput smul 2>/dev/null || printf '')"
RED="$(tput setaf 1 2>/dev/null || printf '')"
GREEN="$(tput setaf 2 2>/dev/null || printf '')"
YELLOW="$(tput setaf 3 2>/dev/null || printf '')"
BLUE="$(tput setaf 4 2>/dev/null || printf '')"
MAGENTA="$(tput setaf 5 2>/dev/null || printf '')"
NO_COLOR="$(tput sgr0 2>/dev/null || printf '')"

info() {
  printf '%s\n' "${BOLD}${GREY}>${NO_COLOR} $*"
}

warn() {
  printf '%s\n' "${YELLOW}! $*${NO_COLOR}"
}

error() {
  printf '%s\n' "${RED}x $*${NO_COLOR}" >&2
}

completed() {
  printf '%s\n' "${GREEN}✓${NO_COLOR} $*"
}

has() {
  command -v "$1" 1>/dev/null 2>&1
}

test_writeable() {
  local path
  path="${1:-}/test.txt"
  if touch "${path}" 2>/dev/null; then
    rm "${path}"
    return 0
  else
    return 1
  fi
}

elevate_priv() {
  if ! has sudo; then
    error 'Could not find the command "sudo", needed to get permissions for install.'
    info "Please run this script as root, or install sudo."
    exit 1
  fi
  if ! sudo -v; then
    error "Superuser not granted, aborting installation"
    exit 1
  fi
}

install_dependencies() {
    elevate_priv
    info "Install dependencies..."
    apt-get install --yes libpq-dev 
    apt-get install --yes python3-pip 
    apt-get install --yes ifupdown 
    apt-get install --yes bridge-utils 
    info "Dependencies successful installed"
}

create_user() {
    adduser wemulate --disabled-password
    echo "wemulate:wemulate" | chpasswd
    echo 'wemulate  ALL=(ALL:ALL) ALL' >> /etc/sudoers
}

install() {
  local msg
  local sudo

  if test_writeable "${CONFIGURATION_DIR}"; then
    sudo=""
    msg="Installing WEmulate, please wait…"
  else
    warn "Escalated permissions are required to write to ${CONFIGURATION_DIR}"
    elevate_priv
    sudo="sudo"
    msg="Installing WEmulate as root, please wait…"
  fi
  info "$msg"

  pip3 install wemulate

}


confirm() {
  if [ -z "${FORCE-}" ]; then
    printf "%s " "${MAGENTA}?${NO_COLOR} $* ${BOLD}[y/N]${NO_COLOR}"
    set +e
    read -r yn </dev/tty
    rc=$?
    set -e
    if [ $rc -ne 0 ]; then
      error "Error reading from prompt (please re-run with the '--yes' option)"
      exit 1
    fi
    if [ "$yn" != "y" ] && [ "$yn" != "yes" ]; then
      error 'Aborting (please answer "yes" to continue)'
      exit 1
    fi
  fi
}

check_configuration_dir() {
  local configuration_dir="$1"

  if [ ! -d "$CONFIGURATION_DIR" ]; then
    error "Configuration location $CONFIGURATION_DIR does not appear to be a directory"
    info "Make sure the location exists and is a directory, then try again."
    exit 1
  fi
}

if [ -z "${CONFIGURATION_DIR-}" ]; then
  CONFIGURATION_DIR=/etc/wemulate
fi

if [ -z "${RELEASE-}" ]; then
  RELEASE="latest"
fi

# parse argv variables
while [ "$#" -gt 0 ]; do
  case "$1" in
  -c | --configuration-dir)
    CONFIGURATION_DIR="$2"
    shift 2
    ;;
  -r | --release)
    RELEASE="$2"
    shift 2
    ;;

  -V | --verbose)
    VERBOSE=1
    shift 1
    ;;
  -f | -y | --force | --yes)
    FORCE=1
    shift 1
    ;;

  -c=* | --configuration-dir=*)
    CONFIGURATION_DIR="${1#*=}"
    shift 1
    ;;
  -r=* | --release=*)
    RELEASE="${1#*=}"
    shift 1
    ;;
  -V=* | --verbose=*)
    VERBOSE="${1#*=}"
    shift 1
    ;;
  -f=* | -y=* | --force=* | --yes=*)
    FORCE="${1#*=}"
    shift 1
    ;;

  *)
    error "Unknown option: $1"
    exit 1
    ;;
  esac
done

printf "  %s\n" "${UNDERLINE}Configuration${NO_COLOR}"
info "${BOLD}Configuration directory${NO_COLOR}: ${GREEN}${CONFIGURATION_DIR}${NO_COLOR}"
info "${BOLD}Release${NO_COLOR}:                 ${GREEN}${RELEASE}${NO_COLOR}"

# non-empty VERBOSE enables verbose untarring
if [ -n "${VERBOSE-}" ]; then
  VERBOSE=v
  info "${BOLD}Verbose${NO_COLOR}: yes"
else
  VERBOSE=
fi

printf '\n'

confirm "Install dependencies on system?"
install_dependencies

confirm "Create wemulate user on system?"
# create_user

confirm "Install WEmulate ${GREEN}${RELEASE}${NO_COLOR}?"
check_configuration_dir "${CONFIGURATION_DIR}"
install

completed "WEmulate installed"

URL="https://github.com/wemulate/wemulate"

printf '\n'
info "Please follow the steps to use WEmulate on your machine:

  ${BOLD}${UNDERLINE}Change user${NO_COLOR}
  Change to the user ${BOLD}wemulate${NO_COLOR} with the following command:

      su wemulate

  ${BOLD}${UNDERLINE}Create configuration${NO_COLOR}
  Create a configuration file ${BOLD}${CONFIGURATION_DIR}/wemulate.yml${NO_COLOR} take a look at the example below:

      ---
      wemulate:
        management_interfaces:
            - ens2
        db_location: /etc/wemulate/wemulate.db

  ${BOLD}${UNDERLINE}Documentation${NO_COLOR}
  To check out the documentation go to:

      ${UNDERLINE}${BLUE}${URL}${NO_COLOR}
"