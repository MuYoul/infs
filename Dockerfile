FROM python:3

RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get -y install git \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

#ENV
ENV BASE_PATH /app
ENV SSH_DIR /app/.ssh
ENV APP_PATH ${BASE_PATH}/infs

#mkdir
RUN mkdir -p $SSH_DIR

#code clone
WORKDIR ${BASE_PATH}
RUN git clone https://github.com/ccassistant/Ants-Auto-Trading-Bot.git

#bot copy
WORKDIR ${APP_PATH}
RUN python3 -m venv venv_ants

#add PYTHONPATH
ENV PYTHONPATH ""

#pip install
RUN . ${APP_PATH}/venv_ants/bin/activate \ 
    && pip install -r requirements.txt

#export port
EXPOSE 5000

#run bot
CMD bash entrypoint.sh
