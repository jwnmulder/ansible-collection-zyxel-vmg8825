FROM gitpod/workspace-full

# Install custom tools, runtime, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    direnv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# USER gitpod

# RUN echo 'eval "$(direnv hook bash)"' > $HOME/.bashrc.d/300-direnv.bashrc

# RUN if ! grep -q "export PIP_USER=no" "$HOME/.bashrc"; then printf '%s\n' "export PIP_USER=no" >> "$HOME/.bashrc"; fi

# USER root
