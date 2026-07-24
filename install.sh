#!/usr/bin/env bash
# =============================================================
# New-mir — Auto-installer for Linux (Debian/Ubuntu/CentOS/etc)
# Installs Docker + docker-compose and starts the service.
# Usage:  bash install.sh
# =============================================================
set -euo pipefail

REPO_URL="https://github.com/mintfary-oss/New-mir.git"
INSTALL_DIR="${HOME}/new-mir"
SERVICE_NAME="new-mir"
PORT="${NEW_MIR_PORT:-8000}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

info()  { echo -e "${GREEN}[new-mir]${NC} $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC} $*"; }
error() { echo -e "${RED}[error]${NC} $*" >&2; }

require_root() {
  if [[ $EUID -ne 0 ]]; then
    warn "Not running as root — will use sudo where needed."
  fi
}

install_docker() {
  if command -v docker &>/dev/null; then
    info "Docker already installed: $(docker --version)"
    return
  fi
  info "Installing Docker …"
  if command -v apt-get &>/dev/null; then
    sudo apt-get update -qq
    sudo apt-get install -y --no-install-recommends \
      ca-certificates curl gnupg lsb-release
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
      sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
      https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update -qq
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
  elif command -v yum &>/dev/null; then
    sudo yum install -y yum-utils
    sudo yum-config-manager --add-repo \
      https://download.docker.com/linux/centos/docker-ce.repo
    sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo systemctl enable --now docker
  else
    error "Unsupported package manager.  Install Docker manually: https://docs.docker.com/engine/install/"
    exit 1
  fi
  sudo usermod -aG docker "${USER}" || true
  info "Docker installed."
}

clone_or_update() {
  if [[ -d "${INSTALL_DIR}/.git" ]]; then
    info "Updating existing installation at ${INSTALL_DIR} …"
    git -C "${INSTALL_DIR}" pull --ff-only
  else
    info "Cloning New-mir to ${INSTALL_DIR} …"
    git clone --depth 1 "${REPO_URL}" "${INSTALL_DIR}"
  fi
}

build_and_start() {
  info "Building Docker image (this may take 2–5 min on first run) …"
  cd "${INSTALL_DIR}"
  NEW_MIR_PORT="${PORT}" docker compose build --quiet
  info "Starting New-mir …"
  NEW_MIR_PORT="${PORT}" docker compose up -d
}

wait_for_health() {
  info "Waiting for service to become healthy …"
  local tries=0
  until curl -sf "http://localhost:${PORT}/api/health" > /dev/null 2>&1; do
    tries=$((tries + 1))
    if [[ $tries -ge 30 ]]; then
      warn "Service did not become healthy after 60s.  Check logs:"
      echo "  docker compose -f ${INSTALL_DIR}/docker-compose.yml logs"
      return
    fi
    sleep 2
  done
  info "New-mir is running at http://localhost:${PORT}"
}

# --- Main ---
require_root
install_docker
clone_or_update
build_and_start
wait_for_health

echo ""
info "Installation complete!"
info "  Web UI  → http://localhost:${PORT}"
info "  API docs → http://localhost:${PORT}/docs"
info "  Logs    → docker compose -f ${INSTALL_DIR}/docker-compose.yml logs -f"
info "  Stop    → docker compose -f ${INSTALL_DIR}/docker-compose.yml down"
