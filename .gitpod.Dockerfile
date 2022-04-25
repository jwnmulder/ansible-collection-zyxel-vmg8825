FROM gitpod/workspace-full

# Install custom tools, runtime, etc.
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    direnv \
    && sudo apt-get clean \
    && sudo rm -rf /var/lib/apt/lists/*

USER gitpod

RUN echo 'eval "$(direnv hook bash)"' > /home/gitpod/.bashrc/.bashrc.d/300-direnv.bashrc
