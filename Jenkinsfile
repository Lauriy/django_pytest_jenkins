pipeline {
    agent any
    environment {
        DOCKER_BUILDKIT=1
    }
    stages {
        stage("Build Docker image and run tests") {
            steps {
                script {
                    sshagent(credentials: ['laurielias']) {
                        withEnv(["HOME=${env.WORKSPACE}"]) {
                            def reportDir = "${WORKSPACE}/test-reports"
                            sh "mkdir -p ${reportDir}"
                            def database = docker.image("postgres")
                            def appRuntime = docker.build("laurielias/django_pytest_jenkins:latest", "-t laurielias/django_pytest_jenkins:latest --target common --ssh default .")
                            def appTest = docker.build("laurielias/django_pytest_jenkins:latest-test", "--target test-runner --ssh default .")
                            sh "docker network create --driver bridge postgres-net || true"
                            parallel(
                                testFirstApp: {
                                    database.withRun("--name django_pytest_jenkins_postgres_first -e 'POSTGRES_DB=django_pytest_jenkins_test_first' -e 'POSTGRES_USER=django_pytest_jenkins_test' -e 'POSTGRES_PASSWORD=django_pytest_jenkins_test' --network-alias postgres1 --net postgres-net") { c ->
                                        appTest.inside("--net postgres-net --entrypoint='' --user 0:0 -e 'DB_HOST=postgres1'") {
                                            sh "cd /srv/django_pytest_jenkins; python -m pytest django_pytest_jenkins_tests/test_first_app.py --cov-report=xml:/srv/django_pytest_jenkins/test-reports/coverage.xml --junitxml=/srv/django_pytest_jenkins/test-reports/pytest-report.xml"
                                        }
                                    }
                                },
                                testSecondApp: {
                                    database.withRun("--name django_pytest_jenkins_postgres_second -e 'POSTGRES_DB=django_pytest_jenkins_test_second' -e 'POSTGRES_USER=django_pytest_jenkins_test' -e 'POSTGRES_PASSWORD=django_pytest_jenkins_test' --network-alias postgres2 --net postgres-net") { c ->
                                        appTest.inside("--net postgres-net --entrypoint='' --user 0:0 -e 'DB_HOST=postgres2'") {
                                            sh "cd /srv/django_pytest_jenkins; python -m pytest django_pytest_jenkins_tests/test_second_app.py --cov-report=xml:/srv/django_pytest_jenkins/test-reports/coverage.xml --junitxml=/srv/django_pytest_jenkins/test-reports/pytest-report.xml"
                                        }
                                    }
                                }
                            )
                        }
                    }
                }
            }
            post {
                always {
                    script {
                        sh "docker cp django_pytest_jenkins_postgres_first:/srv/django_pytest_jenkins/test-reports ${WORKSPACE}/test-reports-first-app"
                        sh "docker cp django_pytest_jenkins_postgres_second:/srv/django_pytest_jenkins/test-reports ${WORKSPACE}/test-reports-second-app"
                    }
                    junit '**/test-reports-first-app/pytest-report.xml'
                    junit '**/test-reports-second-app/pytest-report.xml'
                    recordCoverage(tools: [[parser: 'COBERTURA', pattern: '**/test-reports-first-app/coverage.xml']])
                    recordCoverage(tools: [[parser: 'COBERTURA', pattern: '**/test-reports-second-app/coverage.xml']])
                }
            }
        }
        stage('Push to Dockerhub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'laurielias-dockerhub', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
                    sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}"
                    sh "docker push laurielias/django_pytest_jenkins:latest"
                }
            }
        }
    }
}
