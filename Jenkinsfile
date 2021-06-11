pipeline {
	agent any
	parameters {
	    gitParameter branchFilter: 'origin/(.*)', defaultValue: 'SPM-Spring2021-2597-蓝嘉婕201831990605', name: 'BRANCH', type: 'PT_BRANCH'
	}
	stages {
        stage('MakeDatabasefile') {
	        steps {
	            sh 'touch ./app/static/wordfreqapp.db && rm -f ./app/static/wordfreqapp.db'
	            sh 'cat ./app/static/wordfreqapp.sql | sqlite3 ./app/static/wordfreqapp.db'
	        }
	    }
        stage('BuildIt') {
            steps {
                echo 'Building..'
                sh 'sudo docker build -t englishpal .'
                sh 'sudo docker stop $(docker ps -aq)'
                sh 'sudo docker run -d -p 91:80 -v /var/lib/jenkins/workspace/EnglishPal_Pipeline_master/app/static/frequency:/app/static/frequency -t englishpal'
            }
        }
        stage('TestIt') {
            steps {
                echo 'Testing..'
                sh 'sudo docker run -d -p 4444:4444 selenium/standalone-chrome'
                sh 'pip3 install pytest -U -q'
                sh 'pip3 install selenium -U -q'
                sh 'pytest -v -s html=EnglishPalTestReport.html ./app/test'
            }
        }
        stage('DeployIt') {
            steps {
                echo 'Under Construction....'
            }
        }
    }
}
