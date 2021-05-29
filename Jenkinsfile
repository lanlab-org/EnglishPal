pipeline {
    agent any

    stages {

        stage('pull code') {
            steps {
                echo 'pull code'
                checkout([$class: 'GitSCM', branches: [[name: '*/SPM-Spring2021-2599-张小飞201831990641']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '15b0474b-b8eb-4574-9506-464f19a2b33e', url: 'https://github.com/lanlab-org/EnglishPal.git']]])
            }
	    }
	    stage('MakeDatabasefile') {
            steps {
                sh 'touch ./app/static/wordfreqapp.db && rm -f ./app/static/wordfreqapp.db'
                sh 'cat ./app/static/wordfreqapp.sql | sqlite3 ./app/static/wordfreqapp.db'
            }
        }
        stage('BuildIt') {
            steps {
                echo 'Building..'
                sh 'sudo docker build -t englishpalzhangxf .'
                sh 'sudo docker stop $(docker ps -aq)'
                sh 'sudo docker run -d -p 5000:80 -t englishpalzhangxf'
            }
        }
        stage('TestIt') {
            steps {
                echo 'Testing..'
                sh 'sudo docker run -d -p 4444:4444 selenium/standalone-chrome'
                sh 'pip3 install pytest -U -q'
                sh 'pip3 install selenium -U -q'
                sh 'python3 -m pytest -v -s ./code/test'
            }
        }
        stage('DeployIt') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
