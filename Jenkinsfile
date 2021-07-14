pipeline {
    agent any

    triggers {
    
        pollSCM('') // Enabling being build on Push

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
		sh 'sudo docker kill $(sudo docker ps -q)'
		sh 'sudo docker build -t englishpal .'
		sh 'sudo docker run -d -p 91:80 -v /var/lib/jenkins/workspace/EnglishPal_Pipeline_master/app/static/frequency:/app/static/frequency -t englishpal'
            }
        }
        stage('TestIt') {
            steps {
                echo 'Testing..'
		sh 'sudo docker run -d -p 4444:4444 selenium/standalone-firefox'
		sh 'pip3 install pytest -U -q'
		sh 'pip3 install pytest-html -U -q'		
		sh 'pip3 install selenium -U -q'
		sh 'pytest -v -s --html=EnglishPalTestReport.html ./app/test'
            }
        }
        stage('DeployIt') {
            steps {
                echo 'Deploying (TBD)'
            }
        }
    }
}
