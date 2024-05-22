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
                            // sh "docker build --tag laurielias/django_pytest_jenkins:latest --target common ."
                            // sh "docker build --tag laurielias/django_pytest_jenkins:latest-test-runner --target test-runner ."
                            // sh "docker rm temp-container || true"
                            // sh "docker run --name temp-container laurielias/django_pytest_jenkins:latest-test-runner true"
                            // sh "docker rm temp-container"
                            database.withRun("--name django_pytest_jenkins_postgres -e 'POSTGRES_DB=django_pytest_jenkins_test' -e 'POSTGRES_USER=django_pytest_jenkins_test' -e 'POSTGRES_PASSWORD=django_pytest_jenkins_test' --network-alias postgres --net postgres--net") { c ->
                                appTest.inside("--net postgres-net --entrypoint=''") {
                                    sh "cd /srv/django_pytest_jenkins; python -m pytest ."
                                }
                            }
                        }
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
