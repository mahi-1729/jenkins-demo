pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code....'

                sh '''
                    echo "===== Workspace ====="
                    pwd

                    echo "===== List of files ====="
                    ls -ltra
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Building the application....'

                sh '''
                    echo "===== Build ====="
                    echo "Building the application....."
                    echo "Build completed successfully....."
                '''
            }
        }

        stage('Test') {
            steps {
                echo "Running the test cases....."

                sh '''
                    echo "===== Test ====="

                    if grep -q "Hello from my Jenkins Git Project" app.txt; then
                        echo "Test cases passed successfully....."
                    else
                        echo "Test cases failed..... expected text not found in the file"
                        exit 1
                    fi
                '''
            }
        }
    }
}
