import subprocess
import os
from colorama import init, Fore, Style

init(autoreset=True)

print(Fore.GREEN+Style.BRIGHT+'''
================================================================================
|                                            ______                            |
|                  \      /\      /    |    |           |                      |
|                   \    /  \    /     |    |______     |                      |
|                    \  /    \  /      |    |           |                      |
|                     \/      \/       |    |           |                      |
|                                                                              |
|                            C R A C K E R                                     |
|                             by:superxeon                                     |
|                            @copyright2024                                    |
================================================================================

''')

def get_wifi_profiles_windows():
    profiles = []
    result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if "All User Profile" in line:
            profile = line.split(":")[1].strip()
            profiles.append(profile)
    return profiles

def get_wifi_password_windows(profile):
    result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if "Key Content" in line:
            password = line.split(":")[1].strip()
            return password
    return None

def get_wifi_profiles_linux():
    profiles = []
    result = subprocess.run(['nmcli', '-t', '-f', 'NAME', 'connection', 'show'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if line:
            profiles.append(line.strip())
    return profiles

def get_wifi_password_linux(profile):
    result = subprocess.run(['sudo', 'grep', 'psk=', f'/etc/NetworkManager/system-connections/{profile}'], capture_output=True, text=True)
    if result.returncode == 0:
        password_line = result.stdout.strip().split('\n')[0]
        password = password_line.split('=')[1].strip()
        return password
    return None

def get_wifi_profiles_android():
    wifi_profiles = []
    wifi_conf_dir = "/data/misc/wifi"
    wifi_conf_file = "wpa_supplicant.conf"
    if os.path.exists(os.path.join(wifi_conf_dir, wifi_conf_file)):
        with open(os.path.join(wifi_conf_dir, wifi_conf_file), 'r') as file:
            lines = file.readlines()
            for line in lines:
                if 'ssid=' in line:
                    ssid = line.split('=')[1].strip().strip('"')
                    wifi_profiles.append(ssid)
    return wifi_profiles

def get_wifi_password_android(profile):
    wifi_conf_dir = "/data/misc/wifi"
    wifi_conf_file = "wpa_supplicant.conf"
    if os.path.exists(os.path.join(wifi_conf_dir, wifi_conf_file)):
        with open(os.path.join(wifi_conf_dir, wifi_conf_file), 'r') as file:
            lines = file.readlines()
            network_block = False
            for line in lines:
                if 'network={' in line:
                    network_block = True
                if network_block and f'ssid="{profile}"' in line:
                    for nline in lines[lines.index(line):]:
                        if 'psk=' in nline:
                            password = nline.split('=')[1].strip().strip('"')
                            return password
                        if '}' in nline:
                            network_block = False
                            break
    return None

def show_wifi_profiles(os_choice):
    if os_choice == 'windows':
        profiles = get_wifi_profiles_windows()
    elif os_choice == 'linux':
        profiles = get_wifi_profiles_linux()
    elif os_choice == 'android':
        if os.geteuid() != 0:
            print(Fore.RED + "Script ini memerlukan akses root pada Android.")
            return []
        profiles = get_wifi_profiles_android()
    else:
        print(Fore.RED + "Sistem operasi tidak didukung. Pilih 'windows', 'linux', atau 'android'.")
        return []

    if not profiles:
        print(Fore.RED + "WiFi tidak ditemukan.")
        return []

    print(Fore.GREEN + "WiFi profile yang tersedia:")
    for index, profile in enumerate(profiles):
        print(Fore.YELLOW + f"{index + 1}. {profile}")

    return profiles

def main():
    os_choice = input(Fore.CYAN + "Pilih sistem operasi Anda (windows/linux/android): ").strip().lower()
    profiles = show_wifi_profiles(os_choice)
    if not profiles:
        return

    while True:
        try:
            profile_choice = int(input(Fore.CYAN + "Ketik angka untuk melihat password WiFi: ")) - 1
            selected_profile = profiles[profile_choice]
        except (ValueError, IndexError):
            print(Fore.RED + "Pilihan tidak valid.")
            continue

        if os_choice == 'windows':
            password = get_wifi_password_windows(selected_profile)
        elif os_choice == 'linux':
            password = get_wifi_password_linux(selected_profile)
        elif os_choice == 'android':
            password = get_wifi_password_android(selected_profile)

        if password:
            print(Fore.GREEN + f"Password untuk WiFi {selected_profile}: {Fore.YELLOW + password}")
        else:
            print(Fore.RED + f"Password untuk WiFi {selected_profile} tidak ditemukan atau akses ditolak.")

        repeat = input(Fore.CYAN + "Ingin melihat password WiFi lain? (y/n): ").strip().lower()
        if repeat != 'y':
            break

if __name__ == "__main__":
    main()
