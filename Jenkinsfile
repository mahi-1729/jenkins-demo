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

    stage('Docker Build') {
        steps {
            echo 'Building Docker image...'

            sh '''
                echo "===== DOCKER VERSION ====="
                docker --version

                echo "===== DOCKER BUILD ====="

                docker build -t jenkins-demo:1.0 .

                echo "===== DOCKER IMAGES ====="
                docker images
            '''
        }
    }

    stage('Docker Push'){
        steps{
            echo "Pushing Docker image to Docker Hub..."

            withCredentials([
                usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD'
                )
            ]){
                sh '''
                    echo "===== DOCKER LOGIN ====="
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin

                    echo "===== DOCKER PUSH ====="
                    #docker tag jenkins-demo:1.0 $DOCKER_USERNAME/jenkins-demo:1.0
                    #docker push kubemahi/jenkins-demo:1.0
                    docker push $DOCKER_USERNAME/jenkins-demo:1.0

                    echo "=======DOCKER LOGOUT======="
                    docker logout
                '''
            }
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

