pipeline {
    agent any

    stages {
        stage('Cloning Github repo to Jenkins')
        {
            steps{
                script {
                    echo 'Cloning Github repo to Jenkins....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github_Token', url: 'https://github.com/Coderified/E-2-E-MLOPS-Project.git']])
                }
            }
        }
    }
}