FROM gitpod/workspace-full

# Install custom tools, runtime, etc.
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    direnv \
    && sudo apt-get clean \
    && sudo rm -rf /var/lib/apt/lists/*
