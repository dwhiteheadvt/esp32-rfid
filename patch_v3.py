import os
Import("env")

# 1. Intercept the framework builder right before libraries are built
def patch_async_tcp(source, target, item):
    # Find the problematic header file path inside the local cache
    deps_dir = os.path.join(env.get("PROJECT_DIR"), ".pio", "libdeps", env.get("PIOENV"))
    target_header = os.path.join(deps_dir, "AsyncTCP-esphome", "src", "AsyncTCP.h")
    target_source = os.path.join(deps_dir, "AsyncTCP-esphome", "src", "AsyncTCP.cpp")

    # Automatically remove the missing IPv6 include line if the file exists
    if os.path.exists(target_header):
        with open(target_header, "r") as f:
            content = f.read()
        if '#include "IPv6Address.h"' in content:
            print(">>> [SCRIPT] Patching AsyncTCP-esphome for Arduino v3 compatibility...")
            content = content.replace('#include "IPv6Address.h"', '// #include "IPv6Address.h"')
            with open(target_header, "w") as f:
                f.write(content)

    # Automatically dummy out the source code calls that break without IPv6Address
    if os.path.exists(target_source):
        with open(target_source, "r") as f:
            lines = f.readlines()
        
        modified = False
        for i, line in enumerate(lines):
            if "bool AsyncClient::connect(IPv6Address" in line or "IPv6Address AsyncClient::" in line:
                # Comment out lines starting at the failing signatures to avoid parser drops
                lines[i] = "// " + line
                modified = True
                
        if modified:
            with open(target_source, "w") as f:
                f.writelines(lines)

# Bind the execution sequence to the framework pre-allocation process
env.AddPreAction("__pkg_config", patch_async_tcp)
