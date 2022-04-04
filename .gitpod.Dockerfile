FROM gitpod/workspace-full

# Install custom tools, runtime, etc.
RUN sudo apt-get update \
    && sudo apt-get install -y \
        direnv \
    && sudo rm -rf /var/lib/apt/lists/*

RUN echo 'eval "$(direnv hook bash)"' > /home/gitpod/.bashrc.d/direnv.bashrc
