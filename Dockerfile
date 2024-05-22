FROM python:3.12.3-slim AS common

LABEL maintainer='Lauri Elias <laurileet@gmail.com>'

RUN mkdir -p /srv/django_pytest_jenkins

WORKDIR /srv/django_pytest_jenkins

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=django_pytest_jenkins.settings

COPY requirements.txt manage.py ./

RUN --mount=target=/root/.cache/pip,type=cache pip install -r requirements.txt

COPY django_pytest_jenkins ./django_pytest_jenkins

COPY common_app ./common_app

COPY first_app ./first_app

COPY second_app ./second_app

RUN rm -rf /root/.cache/

ENTRYPOINT ["python", "manage.py", "runserver"]

FROM common AS test-runner

COPY django_pytest_jenkins_tests ./django_pytest_jenkins_tests

COPY requirements.test.txt conftest.py pytest.ini ./

RUN --mount=target=/root/.cache/pip,type=cache pip install -r requirements.test.txt

ENTRYPOINT ["python", "-m", "pytest", "-c", "/srv/django_pytest_jenkins/pytest.ini"]

