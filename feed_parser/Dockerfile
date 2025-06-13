FROM python:3.12-slim

ENV APP_PATH=/app

RUN \
  mkdir -p ${APP_PATH}/src && \
  # Add service user
  groupadd -g 11275 service && \
  useradd -g service -u 11275 service -s /bin/bash -d ${APP_PATH}/src && \
  # Create the virtual environment
  python -m venv ${APP_PATH}/service-venv && \
  chown -R service:service ${APP_PATH}/service-venv && \
  # Configure service user environment
  echo "#!/usr/bin/env bash" > ${APP_PATH}/src/.bashrc && \
  echo "" >> ${APP_PATH}/src/.bashrc && \
  echo ". ${APP_PATH}/service-venv/bin/activate" >> ${APP_PATH}/src/.bashrc && \
  echo ". ${APP_PATH}/src/.bashrc" >> ${APP_PATH}/src/.bash_profile && \
  chown -R service:service ${APP_PATH}/src && \
  chmod 750 ${APP_PATH}/src/.bashrc && \
  chmod 640 ${APP_PATH}/src/.bash_profile && \
  . ${APP_PATH}/service-venv/bin/activate && \
  # Set up virtual environment and install project packages
  (cd ${APP_PATH}/src; python -m pip install --upgrade pip setuptools)

COPY  --chown=service:service requirements.txt ${APP_PATH}/requirements.txt

RUN pip install -r ${APP_PATH}/requirements.txt

WORKDIR ${APP_PATH}/src

COPY  --chown=service:service /src .

ENTRYPOINT ["/bin/bash"]

CMD ["-c", ". ${APP_PATH}/service-venv/bin/activate; python3 app.py"]