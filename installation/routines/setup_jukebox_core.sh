#!/usr/bin/env bash

JUKEBOX_SERVICE_NAME="${SYSTEMD_USR_PATH}/jukebox-daemon.service"

# RPi.GPIO uses direct /sys/class/gpio/ access, removed since kernel 6.6 (Trixie / Bookworm).
# Superseded by rpi-lgpio (see pyproject.toml). See also
# - https://github.com/MiczFlor/RPi-Jukebox-RFID/pull/2470
# - https://github.com/MiczFlor/RPi-Jukebox-RFID/discussions/2295
JUKEBOX_CORE_EXCLUDED_PIP_MODULE="RPi.GPIO"

_jukebox_core_ensure_uv() {
  if command -v uv >/dev/null 2>&1; then
    return
  fi
  print_lc "  Install uv (Python package manager)"
  curl -LsSf https://astral.sh/uv/install.sh | sh || exit_on_error "ERROR: Failed to install uv"
  # The installer places uv in ~/.local/bin by default; make sure this shell session finds it.
  export PATH="${HOME}/.local/bin:${PATH}"
  command -v uv >/dev/null 2>&1 || exit_on_error "ERROR: uv installed but not found on PATH"
}

_jukebox_core_install_python_requirements() {
  print_lc "  Install Python requirements"

  _jukebox_core_ensure_uv
  cd "${INSTALLATION_PATH}" || exit_on_error

  if [[ -d "${VIRTUAL_ENV}" ]]; then
    python3 -m venv --upgrade --system-site-packages "${VIRTUAL_ENV}"
  else
    python3 -m venv --system-site-packages "${VIRTUAL_ENV}"
  fi
  source "$VIRTUAL_ENV/bin/activate"

  # Remove excluded libs, if installed (see JUKEBOX_CORE_EXCLUDED_PIP_MODULE above).
  # A no-op (exit 0, just a warning) if it wasn't installed.
  uv pip uninstall "${JUKEBOX_CORE_EXCLUDED_PIP_MODULE}"

  # Older installations may still have a leftover PyZMQ in the venv from when the Jukebox used
  # ZeroMQ (removed, see documentation/developers/roadmap-core-architecture.md). Harmless to
  # leave, but nothing installs or needs it anymore, so clean it up if present.
  uv pip uninstall pyzmq

  uv sync --no-dev
}

_jukebox_core_install_settings() {
  print_lc "  Register Jukebox settings"
  cp -f "${INSTALLATION_PATH}/resources/default-settings/jukebox.default.yaml" "${SETTINGS_PATH}/jukebox.yaml"
  cp -f "${INSTALLATION_PATH}/resources/default-settings/logger.default.yaml" "${SETTINGS_PATH}/logger.yaml"
}

_jukebox_core_register_as_service() {
  print_lc "  Register Jukebox Core user service"

  sudo cp -f "${INSTALLATION_PATH}/resources/default-services/jukebox-daemon.service" "${JUKEBOX_SERVICE_NAME}"
  sudo sed -i "s|%%INSTALLATION_PATH%%|${INSTALLATION_PATH}|g" "${JUKEBOX_SERVICE_NAME}"
  sudo chmod 644 "${JUKEBOX_SERVICE_NAME}"

  systemctl --user daemon-reload
  systemctl --user enable jukebox-daemon.service
}

_jukebox_core_check() {
    print_verify_installation

    local apt_packages=$(get_args_from_file "${INSTALLATION_PATH}/packages-core.txt")
    verify_apt_packages $apt_packages

    verify_dirs_exists "${VIRTUAL_ENV}"

    local pip_modules=$(python3 -c "
import re
import tomllib
with open('${INSTALLATION_PATH}/packages/jukebox/pyproject.toml', 'rb') as f:
    deps = tomllib.load(f)['project']['dependencies']
print(' '.join(re.split(r'[<>=!; ]', dep, 1)[0] for dep in deps))
")
    verify_pip_modules $pip_modules

    verify_pip_modules_not "${JUKEBOX_CORE_EXCLUDED_PIP_MODULE}"

    verify_files_chown "${CURRENT_USER}" "${CURRENT_USER_GROUP}" "${SETTINGS_PATH}/jukebox.yaml"
    verify_files_chown "${CURRENT_USER}" "${CURRENT_USER_GROUP}" "${SETTINGS_PATH}/logger.yaml"

    verify_files_chown root root "${SYSTEMD_USR_PATH}/jukebox-daemon.service"

    verify_file_contains_string "${INSTALLATION_PATH}" "${JUKEBOX_SERVICE_NAME}"

    verify_service_enablement jukebox-daemon.service enabled --user
}

_run_setup_jukebox_core() {
    _jukebox_core_install_python_requirements
    _jukebox_core_install_settings
    _jukebox_core_register_as_service
    _jukebox_core_check
}

setup_jukebox_core() {
    run_with_log_frame _run_setup_jukebox_core "Install Jukebox Core"
}
