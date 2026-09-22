pipeline {
    agent any

    stages {
        stage('Checkout Verification') {
            steps {
                sh '''
                    echo "===== PROJECT FILES ====="
                    ls -la

                    echo "===== APPLICATION FILE ====="
                    cat app.txt

                    echo "===== EXECUTION USER ====="
                    whoami
                '''
            }
        }
    }
}
