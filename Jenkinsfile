
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

                    echo "===== GIT COMMIT ====="
                    git rev-parse HEAD
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


        // =========================================================
        // 5. DOCKER PUSH
        // =========================================================
        stage('Docker Push') {
            steps {
                echo '===== DOCKER PUSH ====='
                echo 'Logging into Docker Hub and pushing images...'

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
    }


    // =============================================================
    // POST ACTIONS
    // =============================================================
    post {

        success {
            echo '========================================'
            echo '        PIPELINE SUCCESSFUL'
            echo '========================================'

            echo "Docker image:"
            echo "kubemahi/jenkins-demo:${BUILD_NUMBER}"

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

