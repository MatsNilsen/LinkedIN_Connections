pipeline {
    agent any
    options {
        ansiColor('xterm')
        timeout(time: 2, unit: 'HOURS')
    }
    parameters {
        choice(name: 'TEST_RUN_NAME', choices: ['regression', 'schedule_tab_api', 'link_coach', 'coach_creation_auth_deleting', 'coach_notes'], description: 'Test Run Name')
        choice(name: 'ENV', 
               choices: ['dev03', 'dev02', 'dev01', 
                         'dev04', 'dev05', 'dev06', 
                         'dev07', 'dev08', 'dev09', 
                         'dev10', 'uat01', 'uat02'], 
               description: 'dev03 is default')
    }

    stages {
        stage('Cleanup workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Clone sources') {
            steps {
                git(url: 'git@github.com:YouAble/able-api-tests.git',
                    credentialsId: 'github-jenkins-auth',
                    branch: "main")
            }
        }
        stage('Run tests') {
            steps {
                script {
                    currentBuild.displayName = "${TEST_RUN_NAME} on ${params.ENV}"
                    dir('build/reports') {
                        deleteDir()
                    }
                    docker.image('europe-north1-docker.pkg.dev/able-dev-15/able/api-testing:1.3').inside {
                        sh "pytest -v -m '${TEST_RUN_NAME}' --ENV=${params.ENV} --alluredir=${WORKSPACE}/allure-results"
                    }

                }
            }
        }
    }
    post {
        always {
            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, includes: '*/**', keepAll: false, reportDir: "${WORKSPACE}", reportFiles: 'vrt_result.html', reportName: 'HTML Report', reportTitles: ''])
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}