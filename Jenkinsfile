pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {

                echo '========================================'
                echo '              CHECKOUT'
                echo '========================================'

                checkout scm

                sh '''
                    echo "===== CURRENT DIRECTORY ====="
                    pwd

                    echo "===== FILES ====="
                    ls -la

                    echo "===== GIT COMMIT ====="
                    git rev-parse HEAD

                    echo "===== GIT SHORT COMMIT ====="
                    git rev-parse --short=8 HEAD
                '''
            }
        }

        stage('Build') {
            steps {

                echo '========================================'
                echo '                BUILD'
                echo '========================================'

                sh '''
                    echo "===== PYTHON VERSION ====="
                    python3 --version

                    echo "===== PROJECT FILES ====="
                    find . -maxdepth 2 -type f | sort

                    echo "===== CREATING BUILD ARTIFACT ====="

                    mkdir -p build

                    tar \
                        --exclude='./build' \
                        --exclude='./.git' \
                        -czf build/jenkins-demo.tar.gz \
                        app \
                        tests \
                        Dockerfile \
                        requirements.txt

                    echo "===== BUILD ARTIFACT ====="

                    ls -lh build/
                '''
            }
        }

        stage('Test') {
            steps {

                echo '========================================'
                echo '                 TEST'
                echo '========================================'

                sh '''
                    echo "===== CREATE PYTHON VIRTUAL ENVIRONMENT ====="

                    python3 -m venv .venv

                    echo "===== INSTALL DEPENDENCIES ====="

                    .venv/bin/python -m pip install --upgrade pip

                    .venv/bin/python -m pip install \
                        -r requirements.txt

                    .venv/bin/python -m pip install pytest

                    echo "===== PYTHON VERSION ====="

                    .venv/bin/python --version

                    echo "===== PYTEST VERSION ====="

                    .venv/bin/python -m pytest --version

                    echo "===== RUNNING TESTS ====="

                    .venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {

                echo '========================================'
                echo '             DOCKER BUILD'
                echo '========================================'

                sh '''
                    echo "===== DOCKER VERSION ====="

                    docker --version

                    echo "===== JENKINS BUILD NUMBER ====="

                    echo "$BUILD_NUMBER"

                    echo "===== GIT COMMIT ====="

                    GIT_COMMIT_SHA=$(git rev-parse HEAD)

                    echo "$GIT_COMMIT_SHA"

                    echo "===== SHORT GIT COMMIT ====="

                    GIT_SHORT_SHA=$(git rev-parse --short=8 HEAD)

                    echo "$GIT_SHORT_SHA"

                    echo "===== BUILDING DOCKER IMAGE ====="

                    docker build \
                        -t jenkins-demo:$BUILD_NUMBER \
                        .

                    echo "===== TAGGING BUILD NUMBER ====="

                    docker tag \
                        jenkins-demo:$BUILD_NUMBER \
                        kubemahi/jenkins-demo:$BUILD_NUMBER

                    echo "===== TAGGING GIT COMMIT ====="

                    docker tag \
                        jenkins-demo:$BUILD_NUMBER \
                        kubemahi/jenkins-demo:$GIT_SHORT_SHA

                    echo "===== DOCKER IMAGES ====="

                    docker images | grep -E \
                        'jenkins-demo|REPOSITORY'

                    echo "===== IMAGE TAGS CREATED ====="

                    echo "Build Number Tag:"
                    echo "kubemahi/jenkins-demo:$BUILD_NUMBER"

                    echo "Git Commit Tag:"
                    echo "kubemahi/jenkins-demo:$GIT_SHORT_SHA"
                '''
            }
        }

        stage('Docker Push') {
            steps {

                echo '========================================'
                echo '              DOCKER PUSH'
                echo '========================================'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    sh '''
                        echo "===== DOCKER LOGIN ====="

                        echo "Docker Hub username: $DOCKER_USERNAME"

                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin

                        echo "Docker login successful."

                        echo "===== GET GIT COMMIT ====="

                        GIT_SHORT_SHA=$(git rev-parse --short=8 HEAD)

                        echo "Git commit tag: $GIT_SHORT_SHA"
                        echo "Build number tag: $BUILD_NUMBER"

                        echo "===== PUSH BUILD NUMBER TAG ====="

                        docker push \
                            kubemahi/jenkins-demo:$BUILD_NUMBER

                        echo "===== PUSH GIT COMMIT TAG ====="

                        docker push \
                            kubemahi/jenkins-demo:$GIT_SHORT_SHA

                        echo "===== DOCKER PUSH COMPLETED ====="

                        echo "===== DOCKER LOGOUT ====="

                        docker logout

                        echo "Docker logout completed."
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {

                echo '========================================'
                echo '                DEPLOY'
                echo '========================================'

                sshagent(credentials: ['rocky-deploy-key']) {

                    sh '''
                        echo "===== DEPLOYMENT INFORMATION ====="

                        echo "Target Server: 192.168.177.128"
                        echo "Container Name: jenkins-demo-web"
                        echo "Docker Image: kubemahi/jenkins-demo:$BUILD_NUMBER"

                        echo "===== VERIFY SSH CONNECTION ====="

                        ssh deploy@192.168.177.128 \
                            'echo "Connected to deployment server"; whoami; hostname'

                        echo "===== DEPLOY APPLICATION ====="

                        ssh deploy@192.168.177.128 "
                            set -e

                            echo '===== PULL NEW IMAGE ====='

                            docker pull \
                                kubemahi/jenkins-demo:$BUILD_NUMBER

                            echo '===== REMOVE OLD CONTAINER ====='

                            docker rm -f \
                                jenkins-demo-web \
                                2>/dev/null || true

                            echo '===== START NEW CONTAINER ====='

                            docker run -d \
                                --name jenkins-demo-web \
                                -p 5000:5000 \
                                kubemahi/jenkins-demo:$BUILD_NUMBER

                            echo '===== RUNNING CONTAINERS ====='

                            docker ps

                            echo '===== WAITING FOR APPLICATION ====='

                            for attempt in 1 2 3 4 5
                            do
                                echo \"Health check attempt: \$attempt\"

                                if curl -fsS \
                                    http://localhost:5000/health
                                then
                                    echo
                                    echo 'Application health check passed.'
                                    exit 0
                                fi

                                sleep 3
                            done

                            echo '===== HEALTH CHECK FAILED ====='

                            echo 'Container logs:'

                            docker logs \
                                jenkins-demo-web

                            exit 1
                        "
                    '''
                }
            }
        }
    }

    post {

        success {

            echo '========================================'
            echo '        PIPELINE SUCCESSFUL'
            echo '========================================'

            echo "Docker image:"
            echo "kubemahi/jenkins-demo:${BUILD_NUMBER}"

            archiveArtifacts \
                artifacts: 'build/jenkins-demo.tar.gz',
                fingerprint: true
        }

        failure {

            echo '========================================'
            echo '          PIPELINE FAILED'
            echo '========================================'

            echo 'Check the failed stage and console output.'
        }

        always {

            echo '========================================'
            echo '         PIPELINE FINISHED'
            echo '========================================'
        }
    }
}
