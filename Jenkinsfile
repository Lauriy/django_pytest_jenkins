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
                            def database = docker.image("postgres")
                            sh "docker network create --driver bridge postgres-net || true"
                            sh "mkdir -p test-results && chmod 777 test-results && rm -rf test-results/*"
                            sh "docker build -t laurielias/django_pytest_jenkins:latest --ssh default --target common ."
                            sh "docker build -t laurielias/django_pytest_jenkins:latest-test --ssh default --target test-runner ."
                            parallel(
                                testFirstApp: {
                                    database.withRun("--name django_pytest_jenkins_postgres_first -e 'POSTGRES_DB=django_pytest_jenkins_test_first' -e 'POSTGRES_USER=django_pytest_jenkins_test' -e 'POSTGRES_PASSWORD=django_pytest_jenkins_test' --network-alias postgres1 --net postgres-net") { c ->
                                        sh "docker rm temp-container1 || true"
                                        sh "docker run --name temp-container1 --entrypoint='' --user 0:0 -e 'DB_HOST=postgres1' --net postgres-net -v ${env.WORKSPACE}/test-results:/srv/django_pytest_jenkins/test-results python -m pytest django_pytest_jenkins_tests/test_first_app.py --cov-report=xml:test-results/coverage1.xml --junitxml=test-results/pytest-report1.xml"
                                    }
                                },
                                testSecondApp: {
                                    database.withRun("--name django_pytest_jenkins_postgres_second -e 'POSTGRES_DB=django_pytest_jenkins_test_second' -e 'POSTGRES_USER=django_pytest_jenkins_test' -e 'POSTGRES_PASSWORD=django_pytest_jenkins_test' --network-alias postgres2 --net postgres-net") { c ->
                                        sh "docker rm temp-container2 || true"
                                        sh "docker run --name temp-container2 --entrypoint='' --user 0:0 -e 'DB_HOST=postgres2' --net postgres-net -v ${env.WORKSPACE}/test-results:/srv/django_pytest_jenkins/test-results python -m pytest django_pytest_jenkins_tests/test_second_app.py --cov-report=xml:test-results/coverage2.xml --junitxml=test-results/pytest-report2.xml"
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
                        junit "test-results/pytest-report*.xml"
                        recordCoverage(tools: [[parser: 'COBERTURA', pattern: "test-results/coverage*.xml"]])
                        sh "docker stop temp-container1 || true"
                        sh "docker stop temp-container2 || true"
                        sh "docker rm temp-container1 || true"
                        sh "docker rm temp-container2 || true"
                    }
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
