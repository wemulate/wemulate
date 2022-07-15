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
#
#   -i, --interface
#     Defines a default management interface
#
#   --api
#     Install api
#
#   --frontend
#     Install frontend
#
#   Example:
#     sh install.sh -i ens2 -y

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
  local sudo="$1"
  confirm "Install dependencies on system?"
  info "Install dependencies..."
  printf '\n'
  $sudo apt-get update
  $sudo apt-get install --yes python3 
  $sudo apt-get install --yes python3-pip 
  printf '\n'
  completed "Dependencies successful installed"
}

check_configuration_dir() {
  local configuration_dir="$1"
  local sudo="$2"

  if [ ! -d "$CONFIGURATION_DIR" ]; then
    warn "Configuration location $CONFIGURATION_DIR does not appear to be a directory"
    confirm "Do you want to create the directory"
    $sudo bash -c "mkdir "${CONFIGURATION_DIR}""
    completed "Directory $CONFIGURATION_DIR created"
  fi
}

create_default_configuration() {
  local sudo="$1"
  local path="$CONFIGURATION_DIR/wemulate.yml"
  $sudo bash -c "cat > "${path}"" << EOF
---
wemulate:
  db_location: /etc/wemulate/wemulate.db
EOF
  completed "Default configuration $path is generated"
}

configure_mgmt_interface() {
  local sudo="$1"
  $sudo wemulate config set -m $INTERFACE
  completed "Management interface $INTERFACE is configured"
}

create_startup_configuration() {
  local sudo="$1"
  local path="$CONFIGURATION_DIR/startup.sh"
  local conf_folder=$CONFIGURATION_DIR/config
  local cron_config_file=/etc/crontab
  $sudo bash -c "cat > "${path}"" << EOF
#!/bin/bash
for directory in $conf_folder/*; do
    bash \$directory/bridge.conf
    bash \$directory/tc.conf
done
EOF
  completed "Startup configuration $path is generated"
  $sudo bash -c "cat >> "${cron_config_file}"" << EOF
@reboot root    bash $path >> $cron_config_file
EOF
  completed "Cron job configuration $cron_config_file was generated"
  }

read_management_interface() {
  local sudo="$1"
  if [ -z "${FORCE-}" ]; then
    printf "%s " "${MAGENTA}?${NO_COLOR} "Do you want to define a management interface" ${BOLD}[y/N]${NO_COLOR}"
    set +e
    read -r yn </dev/tty
    rc=$?
    set -e
    if [ $rc -ne 0 ]; then
      error "Error reading from prompt (please re-run with the 'yes or no' option)"
      exit 1
    fi
    if [ "$yn" != "y" ] && [ "$yn" != "yes" ]; then
      info "The default interface $INTERFACE has been added to the configuration"
    else
      printf "%s " "${MAGENTA}?${NO_COLOR} "Enter the desired name of the management interface" ${BOLD}[interface_name]${NO_COLOR}" 
      set +e
      read -r intname </dev/tty
      rc=$?
      set -e
      if [ $rc -ne 0 ]; then
        error "Error reading from prompt (please re-run with an interface name option)"
        exit 1
      fi
      if ! echo "$(ip a)" | grep -q $intname; then
        error "Interface is not available"
        exit 1
      fi
      INTERFACE="$intname"
    fi
  fi
  create_default_configuration $sudo
  create_startup_configuration $sudo
}

install_api () {
  local sudo="$1"
  info "Install API..."
  $sudo pip3 install wemulate-api
  local path="/etc/systemd/system/wemulateapi.service"
  $sudo bash -c "cat > "${path}"" << EOF
[Unit]
Description=WEmulate API

[Service]
User=root
ExecStart=/usr/local/bin/wemulate-api
Restart=always

[Install]
WantedBy=multi-user.target
EOF
  $sudo systemctl daemon-reload
  $sudo systemctl enable wemulateapi.service
  $sudo systemctl start wemulateapi.service
  completed "API installed successfully as service"
}

install_frontend () {
  local sudo="$1"
  info "Install frontend..."
  printf '\n'
  install_reverse_proxy $sudo
  $(curl -fsSL -o /var/www/html/release.zip https://github.com/wemulate/wemulate-frontend/releases/latest/download/release.zip)
  $sudo apt -y install unzip
  $sudo unzip -o -q /var/www/html/release.zip -d /var/www/html
  $sudo rm -f /var/www/html/release.zip
  printf '\n'
  completed "Frontend installed and started successfully"
}

install_reverse_proxy () {
  local sudo="$1"
  $sudo apt update
  $sudo apt -y install nginx
  create_nginx_configuration $sudo
  $sudo rm /etc/nginx/sites-enabled/default
  $sudo rm /etc/nginx/sites-available/default
  $sudo rm /var/www/html/index.nginx-debian.html
  $sudo systemctl restart nginx.service
}

create_nginx_configuration() {
  local sudo="$1"
  local path="/etc/nginx/nginx.conf"
  $sudo bash -c "cat > "${path}"" << EOF
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {}

http {
        sendfile on;
        tcp_nopush on;

        include /etc/nginx/mime.types;

        gzip on;

        upstream wemulateapi {
            server localhost:8080;
        }

        server {
            listen 80;

            location /api {
                proxy_pass         http://wemulateapi;
                proxy_redirect     off;
            }

            location / {
                root   /var/www/html;
                index  index.html;
                try_files \$uri \$uri/ /index.html; # escape variables because of EOF
            }
        }
}
EOF
  completed "Default configuration $path for nginx was created"
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
  check_configuration_dir "${CONFIGURATION_DIR}" $sudo
  install_dependencies $sudo
  read_management_interface $sudo
  completed "Install wemulate $RELEASE"
  printf '\n'
  $sudo pip3 install wemulate${RELEASE}
  configure_mgmt_interface $sudo

  if [ $ENABLE_FRONTEND = true ]; then
    install_frontend $sudo
  fi

  if [ $ENABLE_API = true ]; then
    install_api $sudo
  fi
}

if [ -z "${CONFIGURATION_DIR-}" ]; then
  CONFIGURATION_DIR=/etc/wemulate
fi

if [ -z "${RELEASE-}" ]; then
  RELEASE=""
fi

if [ -z "${INTERFACE-}" ]; then
  INTERFACE="ens2"
fi

if [ -z "${ENABLE_API-}"]; then
  ENABLE_API=false
fi

if [ -z "${ENABLE_FRONTEND-}"]; then
  ENABLE_FRONTEND=false
fi

# parse argv variables
while [ "$#" -gt 0 ]; do
  case "$1" in
  -c | --configuration-dir)
    CONFIGURATION_DIR="$2"
    shift 2
    ;;
  -r | --release)
    RELEASE="==$2"
    shift 2
    ;;

  -i | --interface)
    INTERFACE="$2"
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
  --api)
    ENABLE_API=true
    shift 1
    ;;
  --frontend)
    ENABLE_FRONTEND=true
    shift 1
    ;;

  -c=* | --configuration-dir=*)
    CONFIGURATION_DIR="${1#*=}"
    shift 1
    ;;
  -r=* | --release=*)
    RELEASE="==${1#*=}"
    shift 1
    ;;
  -i=* | --interace=*)
    INTERFACE="${1#*=}"
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

confirm "Install WEmulate ${GREEN}${RELEASE}${NO_COLOR}?"
install
printf '\n'
completed "WEmulate installed"

URL="https://github.com/wemulate/wemulate"

printf '\n'
info "Please follow the steps to use WEmulate on your machine:

  ${BOLD}${UNDERLINE}Change user${NO_COLOR}
  Execute the application with ${BOLD}sudo${NO_COLOR} e.g:

      sudo wemulate --help

  ${BOLD}${UNDERLINE}Create configuration${NO_COLOR}
  You can edit the configuration file ${BOLD}${CONFIGURATION_DIR}/wemulate.yml${NO_COLOR} default is:

      ---
      wemulate:
        db_location: $CONFIGURATION_DIR/wemulate.db

  ${BOLD}${UNDERLINE}Documentation${NO_COLOR}
  To check out the documentation go to:

      ${UNDERLINE}${BLUE}${URL}${NO_COLOR}
"
