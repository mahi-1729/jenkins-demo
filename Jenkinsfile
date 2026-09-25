pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checked out by Jenkins.'

                sh '''
                    echo "===== WORKSPACE ====="
                    pwd

                    echo "===== FILES ====="
                    find . -maxdepth 2 -type f | sort
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Building Python application...'

                sh '''
                    echo "===== BUILD ====="

                    rm -rf build
                    mkdir -p build

                    python3 -m py_compile app/main.py

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

        stage('Test') {
            steps {
                echo 'Running automated tests...'

                sh '''
                    echo "===== TEST ====="

                    pytest -v
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'build/jenkins-demo.tar.gz',
                             fingerprint: true
        }
    }
}
