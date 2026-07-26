#!/usr/bin/env bash
# =============================================================
# New-mir — Auto-installer for Linux (Debian/Ubuntu/CentOS/etc)
# Installs Docker + docker-compose, detects hardware (CPU/RAM/GPU)
# and generates docker-compose.override.yml with optimal settings.
# Usage:  bash install.sh
# =============================================================
set -euo pipefail

REPO_URL="https://github.com/mintfary-oss/New-mir.git"
INSTALL_DIR="${HOME}/new-mir"
PORT="${NEW_MIR_PORT:-8000}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

info()    { echo -e "${GREEN}[new-mir]${NC} $*"; }
warn()    { echo -e "${YELLOW}[warn]${NC} $*"; }
error()   { echo -e "${RED}[error]${NC} $*" >&2; }
section() { echo -e "\n${CYAN}══ $* ══${NC}"; }

# =============================================================
# 1. Require Docker
# =============================================================
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
    error "Unsupported package manager. Install Docker manually: https://docs.docker.com/engine/install/"
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

# =============================================================
# 2. Hardware detection
# =============================================================

# Detected values (filled by detect_hardware)
HW_CPU_CORES=1
HW_CPU_MODEL="Unknown"
HW_RAM_TOTAL_MB=0
HW_RAM_AVAIL_MB=0
HW_GPU=false
HW_GPU_NAME=""
HW_GPU_VRAM_MB=0
HW_GPU_COUNT=0
HW_NVIDIA_RUNTIME=false

# Computed limits (filled by compute_limits)
CPUS_LIMIT="1.0"
MEM_LIMIT="2g"
USE_GPU=false

detect_hardware() {
  section "Detecting hardware"

  # ── CPU ──────────────────────────────────────────────────────────
  HW_CPU_CORES=$(nproc 2>/dev/null || echo 1)
  HW_CPU_MODEL=$(grep -m1 "model name" /proc/cpuinfo 2>/dev/null \
                  | cut -d: -f2 | xargs || echo "Unknown")
  info "CPU: ${HW_CPU_CORES} cores — ${HW_CPU_MODEL}"

  # ── RAM ──────────────────────────────────────────────────────────
  if [[ -f /proc/meminfo ]]; then
    HW_RAM_TOTAL_MB=$(awk '/^MemTotal/{print int($2/1024)}' /proc/meminfo)
    HW_RAM_AVAIL_MB=$(awk '/^MemAvailable/{print int($2/1024)}' /proc/meminfo)
  fi
  info "RAM: ${HW_RAM_TOTAL_MB} MB total, ${HW_RAM_AVAIL_MB} MB available"

  # ── NVIDIA GPU ───────────────────────────────────────────────────
  if command -v nvidia-smi &>/dev/null; then
    if nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits \
         > /tmp/nvsmi_out.txt 2>/dev/null; then
      HW_GPU=true
      HW_GPU_COUNT=$(wc -l < /tmp/nvsmi_out.txt)
      HW_GPU_NAME=$(cut -d, -f1 /tmp/nvsmi_out.txt | head -1 | xargs)
      HW_GPU_VRAM_MB=$(cut -d, -f2 /tmp/nvsmi_out.txt | head -1 | xargs)
      info "GPU: ${HW_GPU_COUNT}× ${HW_GPU_NAME} (${HW_GPU_VRAM_MB} MB VRAM each)"
    fi
    rm -f /tmp/nvsmi_out.txt
  fi

  # ── AMD / Intel GPU (basic check via lspci) ──────────────────────
  if [[ "${HW_GPU}" == "false" ]] && command -v lspci &>/dev/null; then
    if lspci 2>/dev/null | grep -qiE "VGA|3D|Display" | grep -viE "Intel|VirtualBox|VMware"; then
      warn "Non-NVIDIA GPU detected. Only NVIDIA GPUs are currently supported for acceleration."
    fi
  fi

  # ── NVIDIA Container Runtime ─────────────────────────────────────
  if [[ "${HW_GPU}" == "true" ]]; then
    if docker info 2>/dev/null | grep -q "nvidia"; then
      HW_NVIDIA_RUNTIME=true
      info "NVIDIA Docker runtime: available ✓"
    else
      warn "NVIDIA GPU found but nvidia-container-toolkit not installed."
      warn "GPU will NOT be used. To enable GPU:"
      warn "  https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
    fi
  fi
}

compute_limits() {
  section "Computing resource limits"

  # CPU: use up to 90% of available cores (min 0.5, rounded to 1 decimal)
  CPUS_LIMIT=$(awk "BEGIN{v=${HW_CPU_CORES}*0.90; if(v<0.5)v=0.5; printf \"%.1f\", v}")
  info "CPU limit: ${CPUS_LIMIT} of ${HW_CPU_CORES} cores (90%)"

  # RAM: use 80% of total RAM (min 1g, expressed in MB then formatted)
  local ram_limit_mb
  ram_limit_mb=$(awk "BEGIN{v=int(${HW_RAM_TOTAL_MB}*0.80); if(v<1024)v=1024; print v}")
  MEM_LIMIT="${ram_limit_mb}m"
  info "Memory limit: ${MEM_LIMIT} of ${HW_RAM_TOTAL_MB} MB (80%)"

  # GPU: use only if NVIDIA runtime is available
  if [[ "${HW_GPU}" == "true" && "${HW_NVIDIA_RUNTIME}" == "true" ]]; then
    USE_GPU=true
    info "GPU acceleration: ENABLED (${HW_GPU_NAME})"
  else
    USE_GPU=false
    info "GPU acceleration: DISABLED (CPU only)"
  fi
}

# =============================================================
# 3. Write docker-compose.override.yml
# =============================================================
write_override() {
  section "Writing docker-compose.override.yml"
  local override="${INSTALL_DIR}/docker-compose.override.yml"

  # Base override — always written
  cat > "${override}" <<EOF
# AUTO-GENERATED by install.sh on $(date -u '+%Y-%m-%d %H:%M UTC')
# Hardware: ${HW_CPU_CORES} CPU cores | ${HW_RAM_TOTAL_MB} MB RAM | GPU: ${HW_GPU_NAME:-none}
# Re-run install.sh to regenerate after hardware changes.
#
# This file is picked up automatically by 'docker compose' alongside
# docker-compose.yml and overrides only the settings listed here.

services:
  new-mir:
    deploy:
      resources:
        limits:
          cpus: "${CPUS_LIMIT}"
          memory: "${MEM_LIMIT}"
        reservations:
          cpus: "0.25"
          memory: "512m"
EOF

  # Add NVIDIA GPU section if available and runtime is configured
  if [[ "${USE_GPU}" == "true" ]]; then
    cat >> "${override}" <<EOF
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    environment:
      # Tell PyTorch / transformers to use GPU
      CUDA_VISIBLE_DEVICES: "0"
EOF
  fi

  info "Written: ${override}"
  info "  CPUs limit : ${CPUS_LIMIT}"
  info "  Memory     : ${MEM_LIMIT}"
  info "  GPU        : ${USE_GPU}"
}

# =============================================================
# 4. Optionally install nvidia-container-toolkit
# =============================================================
maybe_install_nvidia_toolkit() {
  if [[ "${HW_GPU}" == "false" || "${HW_NVIDIA_RUNTIME}" == "true" ]]; then
    return
  fi
  warn "NVIDIA GPU detected but nvidia-container-toolkit is missing."
  if command -v apt-get &>/dev/null; then
    read -r -p "Install nvidia-container-toolkit for GPU support? [y/N] " ans
    if [[ "${ans,,}" == "y" ]]; then
      curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
        sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
      curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
      sudo apt-get update -qq
      sudo apt-get install -y nvidia-container-toolkit
      sudo nvidia-ctk runtime configure --runtime=docker
      sudo systemctl restart docker
      HW_NVIDIA_RUNTIME=true
      info "nvidia-container-toolkit installed. GPU will be used."
    fi
  else
    warn "Install nvidia-container-toolkit manually for GPU support."
  fi
}

# =============================================================
# 5. Build & start
# =============================================================
build_and_start() {
  section "Building and starting New-mir"
  cd "${INSTALL_DIR}"
  info "Building Docker image (this may take 2–5 min on first run) …"
  NEW_MIR_PORT="${PORT}" docker compose build --quiet
  info "Starting New-mir …"
  NEW_MIR_PORT="${PORT}" docker compose up -d
}

wait_for_health() {
  info "Waiting for service to become healthy …"
  local tries=0
  until curl -sf "http://localhost:${PORT}/api/health" > /dev/null 2>&1; do
    tries=$((tries + 1))
    if [[ $tries -ge 40 ]]; then
      warn "Service did not become healthy after 80s. Check logs:"
      echo "  docker compose -f ${INSTALL_DIR}/docker-compose.yml logs"
      return
    fi
    sleep 2
  done
  info "New-mir is running at http://localhost:${PORT}"
}

# =============================================================
# Main
# =============================================================
require_root
install_docker
clone_or_update
detect_hardware
maybe_install_nvidia_toolkit
compute_limits
write_override
build_and_start
wait_for_health

echo ""
section "Installation complete"
info "  Web UI        → http://localhost:${PORT}"
info "  API docs      → http://localhost:${PORT}/docs"
info "  Авто-обучение → http://localhost:${PORT}  (вкладка 🧠)"
info "  Logs          → docker compose -f ${INSTALL_DIR}/docker-compose.yml logs -f"
info "  Stop          → docker compose -f ${INSTALL_DIR}/docker-compose.yml down"
echo ""
info "Hardware summary:"
info "  CPU  : ${HW_CPU_CORES} cores (${HW_CPU_MODEL})"
info "  RAM  : ${HW_RAM_TOTAL_MB} MB"
info "  GPU  : ${HW_GPU_NAME:-none} — acceleration=${USE_GPU}"
