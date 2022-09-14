#!/usr/bin/env sh

# shellcheck disable=SC2039

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

help() {
   echo "Script to install WEmulate (a modern WAN Emulator)"
   echo
   echo "Syntax: install.sh [-h|f|i|v|a]"
   echo "options:"
   echo "-h               Print this Help."
   echo "-f               Force install."
   echo "-i <int1,int2>   Management interfaces to configure."
   echo "-v               Install frontend module."
   echo "-a               Install api module."
   echo
}

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

create_startup_configuration() {
  info "Creating startup configuration"
  local configuration_dir="/var/lib/wemulate"
  local path="$configuration_dir/startup.sh"
  local conf_folder=$configuration_dir/config
  local cron_config_file=/etc/crontab
  $sudo bash -c "cat > "${path}"" << EOF
#!/bin/bash
for directory in $conf_folder/*; do
    bash \$directory/bridge.conf
    bash \$directory/tc.conf
done
EOF
  sudo bash -c "cat >> "${cron_config_file}"" << EOF
@reboot root    bash $path >> $cron_config_file
EOF
  completed "Startup configuration created"
}

create_nginx_configuration() {
  info "Creating nginx configuration"
  local path="/etc/nginx/nginx.conf"
  sudo bash -c "cat > "${path}"" << EOF
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
            server 127.0.0.1:8080;
        }

        server {
            listen 80;

            location /api {
                proxy_pass         http://wemulateapi;
            }

            location / {
                root   /var/www/html;
                index  index.html;
                try_files \$uri \$uri/ /index.html; # escape variables because of EOF
            }
        }
}
EOF
  completed "Reverse proxy configured"
}

install_reverse_proxy() {
  info "Installing reverse proxy..."
  sudo apt update
  sudo apt -y install nginx
  create_nginx_configuration
  sudo rm -f /etc/nginx/sites-enabled/default
  sudo rm -f /etc/nginx/sites-available/default
  sudo rm -f /var/www/html/index.nginx-debian.html
  sudo systemctl restart nginx.service
  completed "Reverse proxy installed"
}

configure_mgmt_interfaces() {
  confirm "Do you want to configure the following mgmt intefaces: ${INTERFACES[@]}?"
  base_command=""
  for interface in "${INTERFACES[@]}"; do
    base_command+=" -m $interface"
  done
  sudo wemulate config set $base_command --force

  completed "Management interfaces (${INTERFACES[@]}) configured"
}

install_dependencies() {
  confirm "Do you want to install the dependencies?"
  printf '\n'
  sudo apt-get update
  sudo apt-get install --yes python3 
  sudo apt-get install --yes python3-pip 
  printf '\n'
  completed "Dependencies installed"
}

install_api() {
  if [ -z $(pip3 freeze | grep wemulate-api) ]; then
    confirm "Do you want to install the API module?"
    info "Installing API module"
    sudo pip3 install wemulate-api==${RELEASEAPI}
  else
    confirm "Do you want to update the API module?"
    info "Updating API module"
    sudo pip3 install wemulate-api==${RELEASEAPI} --upgrade
  fi
  local path="/etc/systemd/system/wemulateapi.service"
  sudo bash -c "cat > "${path}"" << EOF
[Unit]
Description=WEmulate API

[Service]
User=root
ExecStart=/usr/local/bin/wemulate-api
Restart=always

[Install]
WantedBy=multi-user.target
EOF
  sudo systemctl daemon-reload
  sudo systemctl enable wemulateapi.service
  sudo systemctl start wemulateapi.service
  completed "API module installed"
}

install_frontend() {
  if [ -f "/var/www/html/wemulate_logo_favicon.png" ]; then
    confirm "Do you want to update the Frontend module?"
    sudo rm -rf /var/www/html/*
  else
    confirm "Do you want to install the Frontend module"
  fi
  info "Installing Frontend module"
  install_reverse_proxy 
  sudo apt -y install unzip
  $(curl -s -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/wemulate/wemulate-frontend/releases \
  | grep "browser_download_url" \
  | grep ${RELEASEFRONTEND} \
  | cut -d : -f 2,3 \
  | tr -d \" \
  | sudo wget -O /var/www/html/release.zip -qi -)
  sudo unzip -o -q /var/www/html/release.zip -d /var/www/html/
  sudo rm -f /var/www/html/release.zip
  completed "Frontend module installed"
}

install_cli() {
  if [ -z $(pip3 freeze | grep wemulate) ]; then
    confirm "Do you want to install the CLI module?"
    sudo pip3 install wemulate==${RELEASECLI}
    completed "CLI module installed"
  else
    confirm "Do you want to update the CLI module?"
    sudo pip3 install wemulate==${RELEASECLI} --upgrade
    completed "CLI module updated"
  fi
}

install() {
  elevate_priv
  install_dependencies
  install_cli
  create_startup_configuration
  configure_mgmt_interfaces
  if [ -n "${API-}" ]; then
    install_api
  fi
  if [ -n "${FRONTEND-}" ]; then
    install_frontend
  fi
}

start_message() {
  printf '\n'
  info "Welcome to the WEmulate installer"
  printf '\n'
  info "The following releases will be installed:"
  info "${YELLOW}CLI Release:${NO_COLOR} ${RELEASECLI}"
  if [ -n "${API-}" ]; then
    info "${YELLOW}API Release:${NO_COLOR} ${RELEASEAPI}"
  fi
  if [ -n "${FRONTEND-}" ]; then
    info "${YELLOW}Frontend Release:${NO_COLOR} ${RELEASEFRONTEND}"
  fi
  printf '\n'
  info "The following mgmt interfaces will be configured:"
  info "${YELLOW}Mgmt Interfaces:${NO_COLOR} ${INTERFACES[@]}"
  printf '\n'
}

finish_message() {
  local url="https://wemulate.github.io/wemulate"

  printf '\n'
  info "Installation completed"
  info "Please follow the steps to use WEmulate on your machine:

    ${BOLD}${UNDERLINE}Change user${NO_COLOR}
    Execute the application with ${BOLD}sudo${NO_COLOR} e.g:

        sudo wemulate --help

    ${BOLD}${UNDERLINE}Documentation${NO_COLOR}
    To check out the documentation go to:

        ${UNDERLINE}${BLUE}${url}${NO_COLOR}
  "
}

# Set default argument variables
RELEASECLI=$(curl -s https://api.github.com/repos/wemulate/wemulate/releases/latest | jq -r '.tag_name' | sed 's/^v//')
RELEASEAPI=$(curl -s https://api.github.com/repos/wemulate/wemulate-api/releases/latest | jq -r '.tag_name' | sed 's/^v//')
RELEASEFRONTEND=$(curl -s https://api.github.com/repos/wemulate/wemulate-frontend/releases/latest | jq -r '.tag_name' | sed 's/^v//')
INTERFACES=("$(ip a | sed -n 's/.*\(eth[0-9]\+\|ens[0-9]\+\|enp[0-9]s[0-9]\+\|eno[0-9]\+\).*/\1/p' | head -n 1)")

# Parse arguments
while getopts "hfavi:" option; do
  case $option in
    h)
      help
      exit;;
    f)
      FORCE=1;;
    a)
      API=1;;
    v)
      FRONTEND=1;;
    i)
      if [ -n "${OPTARG}" ]; then
        IFS=',' read -r -a INTERFACES <<< $OPTARG;
      fi;;
    \?)
      echo "Invalid option: -$OPTARG"
      help
      exit;;
  esac
done

start_message
install
finish_message