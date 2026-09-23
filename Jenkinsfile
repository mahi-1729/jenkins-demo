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

                    python3 -m py_compile app/main.py

                    echo "Build validation successful."
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
}
