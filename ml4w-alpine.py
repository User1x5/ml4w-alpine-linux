# imports
import os
import sys
from pathlib import Path
from shutil import copy2, copytree, rmtree
from time import sleep

# First check
if os.getuid() != 0:
    print("Script not running as root.")
    sys.exit()

print("Checking repository files...")

communityenabled = False
testingenabled = False

try:
    with open("/etc/apk/repositories", "r") as f:
        lines = f.readlines()

    for line in lines:
        clean_line = line.strip()
        if not clean_line.startswith("#") and "community" in clean_line:
            communityenabled = True
            break

    for line in lines:
        clean_line = line.strip()
        if not clean_line.startswith("#") and "testing" in clean_line:
            testingenabled = True
            break

    if communityenabled == True and testingenabled == True:
        print("Community repo and testing repo are enabled, Continuing.")
        sleep(1)
        os.system("clear")

    else:
        print(
            "Community repo nor Testing repo is not enabled, Please enable it at /etc/apk/repositories"
        )
        sys.exit()

except FileNotFoundError:
    print("/etc/apk/repositories Not found, Are you sure you are in alpine linux?")
    sys.exit()

# Workspace setup
try:
    os.mkdir("/tmp/ml4w-alpine-installer")
    workspace = "ml4w-alpine-installer"

except FileExistsError:
    workspace = "ml4w-alpine-installer"

# ANSI Escape Codes
_GREEN = "\033[92m"
_YELLOW = "\033[93m"
_RED = "\033[91m"
_BLUE = "\033[94m"
_BOLD = "\033[1m"
_RESET = "\033[0m"


# Functions
def printsuccess(text):
    print(f"S: {_GREEN}{text}{_RESET}")


def printwarning(text):
    print(f"W: {_YELLOW}{text}{_RESET}")


def printerror(text):
    print(f"E: {_RED}{text}{_RESET}")


def printinfo(text):
    print(f"I: {_BLUE}{text}{_RESET}")


def printheader(text):
    print(f"{_BOLD}{text}{_RESET}")


def installapk(apk):
    exitcode = os.system(f"apk info -e {apk} > /dev/null 2>&1")
    if exitcode == 1:
        printinfo(f"{apk} Not installed, Installing now.")
        os.system(f"apk add -q {apk}")
        printinfo(f"{apk} Installed")
    else:
        printinfo(f"{apk} Already installed.")


# Other
packages = [
    "hyprland",
    "xdg-desktop-portal-hyprland",
    "xdg-desktop-portal-gtk",
    "kitty",
    "vim",
    "neovim",
    "hyprpaper",
    "rofi-wayland",
    "jq",
    "fastfetch",
    "brightnessctl",
    "networkmanager",
    "nm-applet",
    "thunar",
    "wireplumber",
    "gvfs",
    "curl",
    "wget",
    "qt5-wayland",
    "qt6-wayland",
    "font-awesome",
    "ttf-fira-sans",
    "ttf-fira-code",
    "font-nerd-symbols",
]

buildtools = [
    "nodejs",
    "npm",
    "rust",
    "cargo",
    "meson",
    "ninja",
    "build-base",
    "cmake",
    "samurai",
    "gtk+3.0-dev",
    "gtk-layer-shell-dev",
    "wayland-dev",
    "libxkbcommon-dev",
    "pixman-dev",
    "lcms2-dev",
    "gjs",
    "gjs-dev",
    "gobject-introspection-dev",
    "pulseaudio-dev",
    "json-glib-dev",
    "libhandy-dev",
    "libgtop-dev",
    "glib-dev",
    "vala",
]

printheader("ML4W Alpine Setup script")
printheader("Continue?")
choice = input("Y/n: ")
if choice.lower() == "y":
    printinfo("Continuing.")
    printinfo("Installing build tools")
    for tool in buildtools:
        installapk(tool)

    printinfo("Build tools installed. installing other packages.")

    # SWWW Install
    printinfo("Compiling swww.")
    os.system(f"git clone https://github.com/LGFae/swww.git /tmp/{workspace}/swww")
    os.mkdir(f"/tmp/{workspace}/swww_build")
    os.system(
        f'CARGO_TARGET_DIR="/tmp/{workspace}/swww_build/" cargo build --manifest-path="/tmp/{workspace}/swww/Cargo.toml" --release'
    )
    printwarning("Deleting source.")
    rmtree(f"/tmp/{workspace}/swww")
    printinfo("Giving perms...")
    os.system(f"chmod +x /tmp/{workspace}/swww_build/release/swww")
    os.system(f"chmod +x /tmp/{workspace}/swww_build/release/swww-daemon")
    printinfo(
        "Copying binaries"
    )  # this is why i added a root check beside being lazy to detect doas or sudo
    copy2(f"/tmp/{workspace}/swww_build/release/swww", "/usr/bin/swww")
    copy2(f"/tmp/{workspace}/swww_build/release/swww-daemon", "/usr/bin/swww-daemon")
    printinfo("Cleaning up SWWW...")
    rmtree(f"/tmp/{workspace}/swww_build")
    printinfo("SWWW Installed!")
    sleep(1)

    # SwayNC install
    printinfo("Compiling swaync.")
    os.system(
        f"git clone https://github.com/ErikReider/SwayNotificationCenter.git /tmp/{workspace}/swaync"
    )
    os.mkdir(f"/tmp/{workspace}/swaync_build")
    os.system(
        f"meson setup --prefix=/usr /tmp/{workspace}/swaync_build /tmp/{workspace}/swaync"
    )
    printinfo("Compiling SwayNC...")
    os.system(f"meson compile -C /tmp/{workspace}/swaync_build")
    printinfo("Copying binaries...")
    os.system(f"meson install -C /tmp/{workspace}/swaync_build")
    printinfo("Giving perms...")
    os.chmod("/usr/bin/swaync", 0o755)
    os.chmod("/usr/bin/swaync-client", 0o755)
    printwarning("Cleaning up SwayNC...")
    rmtree(f"/tmp/{workspace}/swaync_build")
    rmtree(f"/tmp/{workspace}/swaync")
    printinfo("SwayNC Installed!")
    sleep(1)

    # Aylur's GTK Shell install
    printinfo("Compiling Aylur's GTK Shell...")
    os.system(f"git clone https://github.com/aylur/ags.git /tmp/{workspace}/ags")
    os.mkdir(f"/tmp/{workspace}/ags_build")
    printinfo("Installing js libraries...")
    os.system(f"npm install --prefix /tmp/{workspace}/ags")
    os.system(
        f"meson setup --prefix=/usr /tmp/{workspace}/ags_build /tmp/{workspace}/ags"
    )
    printinfo("Compiling Aylur's GTK Shell...")
    os.system(f"meson compile -C /tmp/{workspace}/ags_build")
    os.system(f"meson install -C /tmp/{workspace}/ags_build")
    printinfo("Giving perms...")
    os.chmod("/usr/bin/ags", 0o755)
    print("Cleaning up Aylur's GTK Shell...")
    rmtree(f"/tmp/{workspace}/ags_build")
    rmtree(f"/tmp/{workspace}/ags")
    printinfo("Aylur's GTK Shell Installed!")

    # Pre-install
    printinfo("Main compiling done.")
    printinfo("Installing other packages...")
    for package in packages:
        installapk(package)

    printinfo("Package installing done, moving on to dotfiles.")

    printwarning(
        "The script will try to get your original user, MAKE SURE YOUR RAN THE SCRIPT AS SUDO!"
    )
    originaluser = os.getenv("SUDO_USER")
    printinfo(
        f"The script detected {originaluser} as your original user. Is this right?"
    )
    choice = input("Y/n: ")
    if choice.lower() == "y":
        pass

    else:
        originaluser = input("Please enter your original user (HOME): ")

    printinfo("Generating hyprland config file...")
    if Path(f"/home/{originaluser}/.config").exists():
        if Path(f"/home/{originaluser}/.config/hypr").exists():
            printwarning(
                f"Hyprland config already exists at /home/{originaluser}/.config/hypr, skipping."
            )
        else:
            printwarning(
                f"Hyprland config does not exist at /home/{originaluser}/.config/hypr, creating it now."
            )
            os.mkdir(f"/home/{originaluser}/.config/hypr")

    else:
        printwarning(".config does not exist, creating it now.")
        os.mkdir(f"/home/{originaluser}/.config")
        os.mkdir(f"/home/{originaluser}/.config/hypr")

    printinfo("Cloning ML4W Dotfiles...")
    os.mkdir(f"/tmp/{workspace}/ml4w")
    os.system(
        f"git clone --depth=1 https://github.com/mylinuxforwork/dotfiles.git /tmp/{workspace}/ml4w/"
    )
    printinfo("Copying dotfiles to your home directory...")
    copytree(
        f"/tmp/{workspace}/ml4w/dotfiles", f"/home/{originaluser}/", dirs_exist_ok=True
    )
    printinfo("Cleaning up dotfiles...")
    rmtree(f"/tmp/{workspace}/ml4w")
    printinfo("All done! Please reboot your system to apply changes.")
    printinfo(
        "Reminder that this script was made in an arch linux machine, so some things may not work as intended. If you have any issues, please report them to the developer."
    )
    printwarning(
        "Make sure to run lbu commit to save your changes to the overlay before rebooting."
    )

else:
    printinfo("Exiting.")
    rmtree(f"/tmp/{workspace}")
    sys.exit()
