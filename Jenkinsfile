pipeline {
    agent any

    environment {
        APP_DIR = "/opt/flask_app"
        SSH_CREDS = "root-ssh-key"
        CONTAINER_IP = "192.168.73.50"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/your-username/flask-app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Deploy to Container') {
            steps {
                sshagent(credentials: [SSH_CREDS]) {
                    sh """
                        ssh root@${CONTAINER_IP} '
                        systemctl restart flask_app
                        systemctl restart nginx
                        '
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://${CONTAINER_IP}", returnStdout: true).trim()
                    if (response != '200') {
                        error "Application is not responding with status 200!"
                    }
                }
            }
        }
    }
}
