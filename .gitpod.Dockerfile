FROM gitpod/workspace-full

# Install custom tools, runtime, etc.
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    direnv \
    && sudo apt-get clean \
    && sudo rm -rf /var/lib/apt/lists/*

USER gitpod

ARG PYTHON_VERSION=3.10.4
RUN pyenv install ${PYTHON_VERSION} && pyenv global ${PYTHON_VERSION}

RUN echo 'eval "$(direnv hook bash)"' > /home/gitpod/.bashrc.d/300-direnv.bashrc
