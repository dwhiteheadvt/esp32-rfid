import os
import shutil

Import("env")

# Locate the dependency tracking folder
libdeps_dir = os.path.join(env.get("PROJECT_DIR"), ".pio", "libdeps", env.get("PIOENV"))
target_conflict = os.path.join(libdeps_dir, "AsyncTCP-esphome")

# Wipe the directory so the compiler physically cannot see or process it
if os.path.exists(target_conflict):
    print(f"--- [REMOVING CONFLICT] Purging legacy library: {target_conflict} ---")
    shutil.rmtree(target_conflict)
