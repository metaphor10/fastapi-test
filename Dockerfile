FROM python:3
ENV AB_PRIVATE_TOKEN foo
ENV AB_GITLAB_URL bar
COPY . /ab-fastapi
WORKDIR /ab-fastapi


RUN pip install pipenv
RUN pipenv install --system --deploy

ENTRYPOINT ["bash", "start.sh"]  