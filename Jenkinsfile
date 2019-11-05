pipeline {
    agent any
    stages {

         stage('executing') {
            steps {

                bat 'python test_funct.py'
                publishHTML([allowMissing: false,
                             alwaysLinkToLastBuild: false, 
                             keepAll: false, 
                             reportDir: 'coverage', 
                             reportFiles: 'index.html',
                             reportName: 'HTML Report',
                             reportTitles: ''])

            }
        }




    }
}
