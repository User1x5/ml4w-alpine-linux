# imports
import os
import subprocess
import sys
from pathlib import Path
from shutil import copy2, copytree, rmtree
from time import sleep

manual = False

# First check
if os.getuid() != 0:
    print("Script not running as root.")
    sys.exit(1)

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
        sys.exit(1)

except FileNotFoundError:
    print("/etc/apk/repositories Not found, Are you sure you are in alpine linux?")
    sys.exit(1)

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
    print(f"{_GREEN}S:{_RESET} {text}")


def printwarning(text):
    print(f"{_YELLOW}W:{_RESET} {text}")


def printerror(text):
    print(f"E: {_RED}{text}{_RESET}")


def printinfo(text):
    print(f"{_BLUE}I:{_RESET} {text}")


def printheader(text):
    print(f"{_BOLD}{text}{_RESET}")


def installapk(apk):
    exitcode = subprocess.run(
        ["apk", "info", "-e", apk], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ).returncode
    if exitcode != 0:
        printwarning(f"{apk} Not installed, Installing now.")
        subprocess.run(
            ["apk", "add", apk], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        printsuccess(f"{apk} Installed")
    else:
        printinfo(f"{apk} Already installed.")


# Check if swww, ags, or swaync build files exist for some reason, I no likey "File exists" git errors.

if (
    Path("/tmp/ml4w-alpine-installer/swww").exists()
    or Path("/tmp/ml4w-alpine-installer/swaync").exists()
    or Path("/tmp/ml4w-alpine-installer/ags").exists()
):
    printerror(
        "SWWW build files already exist, please delete /tmp/ml4w-alpine-installer/ and its files and try again."  # Omitting the "File exists" since im a lazy dev and i do not want to check for each file individually. I will just check for the folder and if it exists, I will assume the files exist as well.
    )
    printinfo(
        "If the script ran earlier but failed and quitted delete /tmp/ml4w-alpine-installer"  # # 01001000 01100101 01101100 01110000
    )
    sys.exit(
        1
    )  # 01101000 01100101 01101100 01110000 00100000 01101101 01100101 00100000 01001001 00100000 01100011 01100001 01101110 00100000 01110100 01111001 01110000 01100101 00100000 01101001 01110100 00100000 01101001 01101110 00100000 01000010 01101001 01110100 00100000

# Other
packages = [  # 01001000 01100101 01101100 01110000 01101101 01100101 00100000 01001001 00100000 01100011 01100001 01101110 00100000 01110100 01111001 01110000 01100101 00100000 01101001 01110100 00100000 01101001 01101110 00100000 01000010 01101001 01110100
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
    "font-nerd-symbols",  # f**k you musl, why is alpine linux devving in arch linux so dang hard
]

buildtools = [
    "go",
    "nodejs",
    "npm",
    "meson",
    "ninja",
    "build-base",
    "cmake",
    "samurai",
    "gtk+3.0-dev",
    "gtk-layer-shell-dev",
    "gtk4-layer-shell-dev",
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
    "alpine-sdk",
    "wayland-protocols",
    "pkgconfig",
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
    print()
    # SWWW Install
    # There is no way i wrote all this to compile swww from source and just then discovered that its in the apk repositories

    printwarning(
        "Will download swww from apk, if you instead want to compile from source modify manual inside script to be True, In case that case be aware that it might have errors, Press enter to continue..."
    )
    input()
    print()
    if manual == True:
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
            "Copying biniaries"
        )  # this is why i added a root check beside being lazy to detect doas or sudo
        copy2(f"/tmp/{workspace}/swww_build/release/swww", "/usr/bin/swww")
        copy2(
            f"/tmp/{workspace}/swww_build/release/swww-daemon", "/usr/bin/swww-daemon"
        )
        printinfo("Cleaning up SWWW...")
        rmtree(f"/tmp/{workspace}/swww_build")
        printinfo("SWWW Installed!")
        sleep(1)

    else:
        installapk("swww")  # So dang simple.

    # SwayNC install
    # screw you compiling

    if manual == True:
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

    else:
        installapk("swaync")

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
    sys.exit(0)
