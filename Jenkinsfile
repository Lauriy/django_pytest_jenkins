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
                            def appRuntime = docker.build("laurielias/django_pytest_jenkins:latest", "-t laurielias/django_pytest_jenkins:latest --target common --ssh default .")
                            def appTest = docker.build("laurielias/django_pytest_jenkins:latest-test", "--target test-runner --ssh default .")
                            sh "docker network create --driver bridge postgres-net || true"
                            parallel(
                                testFirstApp: {
                                    database.withRun("--name django_pytest_jenkins_postgres_first -e 'POSTGRES_DB=django_pytest_jenkins_test_first' -e 'POSTGRES_USER=django_pytest_jenkins_test' -e 'POSTGRES_PASSWORD=django_pytest_jenkins_test' --network-alias postgres1 --net postgres-net") { c ->
                                        appTest.inside("--net postgres-net --entrypoint='' --user 0:0 -e 'DB_HOST=postgres1'") {
                                            sh """
                                                cd /srv/django_pytest_jenkins
                                                python -m pytest django_pytest_jenkins_tests/test_first_app.py --cov-report=xml:coverage1.xml --junitxml=pytest-report1.xml
                                            """
                                        }
                                    }
                                },
                                testSecondApp: {
                                    database.withRun("--name django_pytest_jenkins_postgres_second -e 'POSTGRES_DB=django_pytest_jenkins_test_second' -e 'POSTGRES_USER=django_pytest_jenkins_test' -e 'POSTGRES_PASSWORD=django_pytest_jenkins_test' --network-alias postgres2 --net postgres-net") { c ->
                                        appTest.inside("--net postgres-net --entrypoint='' --user 0:0 -e 'DB_HOST=postgres2'") {
                                            sh """
                                                cd /srv/django_pytest_jenkins
                                                python -m pytest django_pytest_jenkins_tests/test_second_app.py --cov-report=xml:coverage2.xml --junitxml=pytest-report2.xml
                                            """
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
                        // junit "pytest-report*.xml"
                        recordCoverage(tools: [[parser: 'COBERTURA', pattern: "coverage*.xml"]])
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
