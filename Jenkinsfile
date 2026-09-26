pipeline {
    agent any

    stages {

        // =========================================================
        // 1. CHECKOUT
        // =========================================================
        stage('Checkout') {
            steps {
                echo '===== CHECKOUT ====='
                echo 'Source code checked out by Jenkins.'

                sh '''
                    echo "===== WORKSPACE ====="
                    pwd

                    echo "===== FILES ====="
                    find . -maxdepth 2 -type f | sort
                '''
            }
        }


        // =========================================================
        // 2. BUILD
        // =========================================================
        stage('Build') {
            steps {
                echo '===== BUILD ====='
                echo 'Building Python application...'

                sh '''
                    rm -rf build
                    mkdir -p build

                    echo "===== PYTHON CHECK ====="
                    python3 --version

                    echo "===== PYTHON COMPILE ====="
                    python3 -m py_compile app/main.py

                    echo "===== CREATING BUILD ARTIFACT ====="

                    tar --exclude='__pycache__' \
                        --exclude='*.pyc' \
                        -czf build/jenkins-demo.tar.gz app tests

                    echo "===== BUILD ARTIFACT ====="
                    ls -lh build/

                    echo "===== ARTIFACT CONTENTS ====="
                    tar -tzf build/jenkins-demo.tar.gz

                    echo "Build completed successfully."
                '''
            }
        }


        // =========================================================
        // 3. TEST
        // =========================================================
        stage('Test') {
            steps {
                echo '===== TEST ====='
                echo 'Running automated tests...'

                sh '''
                    echo "===== PYTEST VERSION ====="
                    pytest --version

                    echo "===== RUNNING TESTS ====="
                    pytest -v
                '''
            }
        }


        // =========================================================
        // 4. DOCKER BUILD
        // =========================================================
        stage('Docker Build') {
            steps {
                echo '===== DOCKER BUILD ====='
                echo 'Building Docker image...'

                sh '''
                    echo "===== DOCKER VERSION ====="
                    docker --version

                    echo "===== DOCKER INFO ====="
                    docker info | head -30

                    echo "===== BUILDING IMAGE ====="

                    docker build \
                        -t jenkins-demo:1.0 \
                        .

                    echo "===== TAGGING IMAGE ====="

                    docker tag \
                        jenkins-demo:1.0 \
                        kubemahi/jenkins-demo:1.0

                    echo "===== DOCKER IMAGES ====="

                    docker images | grep -E \
                        'jenkins-demo|REPOSITORY'
                '''
            }
        }


        // =========================================================
        // 5. DOCKER PUSH
        // =========================================================
        stage('Docker Push') {
            steps {
                echo '===== DOCKER PUSH ====='
                echo 'Logging into Docker Hub and pushing image...'

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

                        echo "===== DOCKER PUSH ====="

                        docker push kubemahi/jenkins-demo:1.0

                        echo "===== DOCKER PUSH COMPLETED ====="

                        echo "===== DOCKER LOGOUT ====="

                        docker logout

                        echo "Docker logout completed."
                    '''
                }
            }
        }
    }


    // =============================================================
    // POST ACTIONS
    // =============================================================
    post {

        success {
            echo '========================================'
            echo '        PIPELINE SUCCESSFUL'
            echo '========================================'

            echo 'Build artifact will be archived.'

            archiveArtifacts artifacts: 'build/jenkins-demo.tar.gz',
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
