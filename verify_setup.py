import sys
import os
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_step(name, func):
    print(f"[*] Checking {name}...", end=" ")
    try:
        func()
        print("OK")
        return True
    except Exception as e:
        print(f"FAIL\n    Error: {e}")
        return False

def check_scapy_npcap():
    import scapy.all as scapy
    # Try to list interfaces. If Npcap is missing, this usually fails or returns empty/partial
    ifaces = scapy.get_if_list()
    if not ifaces:
        raise Exception("Scapy imported, but no interfaces found. Is Npcap installed?")
    print(f"(Found {len(ifaces)} interfaces)", end=" ")

def check_tensorflow():
    import tensorflow as tf
    print(f"(Version {tf.__version__})", end=" ")

def check_permissions():
    if not is_admin():
        raise Exception("Script is not running as Administrator. Sniffing requires Admin privileges.")

print("=== Project Alpha: Windows Environment Verifier ===\n")

steps = [
    ("Administrator Privileges", check_permissions),
    ("Python Dependencies", lambda: __import__('project_alpha.requirements')), # check if we can import our own ignores, actually just check libs directly
    ("Scapy (Packet Capture)", check_scapy_npcap),
    ("TensorFlow (Machine Learning)", check_tensorflow),
]

# We'll just define the lambda imports inside the loop or functions
passed = 0
total = 4

# 1. Admin
if check_step("Admin Privileges", check_permissions): passed += 1

# 2. Scapy Import & Npcap
if check_step("Scapy & Npcap", check_scapy_npcap): passed += 1
else:
    print("    -> ACTION: Please install Npcap from https://npcap.com/ (Select 'WinPcap API-compatible Mode')")

# 3. TensorFlow
if check_step("TensorFlow", check_tensorflow): passed += 1

# 4. Project Modules
def check_project():
    import project_alpha.src.sniffer
    import project_alpha.src.autoencoder
if check_step("Project Alpha Modules", check_project): passed += 1

print(f"\nResult: {passed}/{total} Checks Passed.")

if passed == total:
    print("\n[SUCCESS] Your environment is ready! You can run the project now.")
    print("Run: python -m project_alpha.main --train")
else:
    print("\n[WARNING] Please fix the errors above before running Project Alpha.")
