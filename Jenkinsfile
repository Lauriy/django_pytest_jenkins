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
                            sh "mkdir -p ${reportDir} && chmod 777 ${reportDir}"
                            def database = docker.image("postgres")
                            def appRuntime = docker.build("laurielias/django_pytest_jenkins:latest", "-t laurielias/django_pytest_jenkins:latest --target common --ssh default .")
                            def appTest = docker.build("laurielias/django_pytest_jenkins:latest-test", "--target test-runner --ssh default .")
                            sh "docker network create --driver bridge postgres-net || true"
                            parallel(
                                testFirstApp: {
                                    database.withRun("--name django_pytest_jenkins_postgres_first -e 'POSTGRES_DB=django_pytest_jenkins_test_first' -e 'POSTGRES_USER=django_pytest_jenkins_test' -e 'POSTGRES_PASSWORD=django_pytest_jenkins_test' --network-alias postgres1 --net postgres-net") { c ->
                                        appTest.inside("--net postgres-net --entrypoint='' --user 0:0 -v ${reportDir}:/srv/django_pytest_jenkins/test-reports -e 'DB_HOST=postgres1'") {
                                            sh """
                                                cd /srv/django_pytest_jenkins
                                                python -m pytest django_pytest_jenkins_tests/test_first_app.py --cov-report=xml:/srv/django_pytest_jenkins/test-reports/coverage1.xml --junitxml=/srv/django_pytest_jenkins/test-reports/pytest-report1.xml
                                                ls -l /srv/django_pytest_jenkins/test-reports
                                            """
                                        }
                                    }
                                },
                                testSecondApp: {
                                    database.withRun("--name django_pytest_jenkins_postgres_second -e 'POSTGRES_DB=django_pytest_jenkins_test_second' -e 'POSTGRES_USER=django_pytest_jenkins_test' -e 'POSTGRES_PASSWORD=django_pytest_jenkins_test' --network-alias postgres2 --net postgres-net") { c ->
                                        appTest.inside("--net postgres-net --entrypoint='' --user 0:0 -v ${reportDir}:/srv/django_pytest_jenkins/test-reports -e 'DB_HOST=postgres2'") {
                                            sh """
                                                cd /srv/django_pytest_jenkins
                                                python -m pytest django_pytest_jenkins_tests/test_second_app.py --cov-report=xml:/srv/django_pytest_jenkins/test-reports/coverage2.xml --junitxml=/srv/django_pytest_jenkins/test-reports/pytest-report2.xml
                                                ls -l /srv/django_pytest_jenkins/test-reports
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
                        def reportDir = "${env.WORKSPACE}/test-reports"
                        sh "ls -l ${reportDir}"
                        junit "${reportDir}/pytest-report*.xml"
                        recordCoverage(tools: [[parser: 'COBERTURA', pattern: "${reportDir}/coverage*.xml", id: 'cobertura', name: 'Cobertura Coverage', sourceCodeRetention: 'EVERY_BUILD']])
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
