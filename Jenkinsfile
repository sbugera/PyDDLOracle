pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    options {
        buildDiscarder(logRotator(
            numToKeepStr: '50',
            artifactNumToKeepStr: '5'
        ))
    }

    stages {
        stage('Setup Environment') {
            steps {
                sh '''
                    python3.13 -m venv ${VENV}
                    source ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install -r requirements-test.txt
                    cp config_con.template.yaml config_con.yaml || true
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source ${VENV}/bin/activate
                    mkdir -p test-results
                    pytest tests/unit \
                        --junitxml=test-results/junit.xml \
                        --html=test-results/report.html \
                        --self-contained-html \
                        --cov=. \
                        --cov-report=xml:test-results/coverage.xml \
                        --cov-report=html:test-results/coverage \
                        --cov-config=.coveragerc
                '''
            }
            post {
                always {
                    // Publish JUnit test results
                    junit 'test-results/junit.xml'
                    
                    // Publish HTML reports
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'test-results',
                        reportFiles: 'report.html',
                        reportName: 'Pytest Report'
                    ])
                    
                    // Publish Coverage Report
                    recordCoverage(
                        tools: [[parser: 'COBERTURA', pattern: 'test-results/coverage.xml']],
                        id: 'python-coverage',
                        name: 'Python Coverage',
                        sourceCodeRetention: 'EVERY_BUILD',
                        qualityGates: [
                            [threshold: 60.0, metric: 'LINE', baseline: 'PROJECT', unstable: true],
                            [threshold: 50.0, metric: 'LINE', baseline: 'PROJECT', fail: true]
                        ]
                    )
                    
                    // Archive the test reports
                    archiveArtifacts artifacts: 'test-results/**/*', fingerprint: true
                }
            }
        }

        stage('Code Quality') {
            parallel {
                stage('Pylint') {
                    steps {
                        sh '''
                            source ${VENV}/bin/activate
                            pylint main.py app/ --output-format=parseable --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > test-results/pylint-report.txt || true
                        '''
                    }
                    post {
                        always {
                            recordIssues(
                                tool: pyLint(pattern: 'test-results/pylint-report.txt'),
                                qualityGates: [[threshold: 10, type: 'TOTAL', unstable: true]],
                                healthy: 5,
                                unhealthy: 10
                            )
                        }
                    }
                }
                
                stage('Bandit Security Scan') {
                    steps {
                        sh '''
                            source ${VENV}/bin/activate
                            bandit -r main.py app/ -f html -o test-results/bandit-report.html || true
                        '''
                    }
                    post {
                        always {
                            publishHTML(target: [
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'test-results',
                                reportFiles: 'bandit-report.html',
                                reportName: 'Bandit Security Report'
                            ])
                        }
                    }
                }
                
                stage('Flake8') {
                    steps {
                        sh '''
                            source ${VENV}/bin/activate
                            flake8 main.py app/ --format=pylint > test-results/flake8-report.txt || true
                        '''
                    }
                    post {
                        always {
                            recordIssues(
                                tool: flake8(pattern: 'test-results/flake8-report.txt'),
                                qualityGates: [[threshold: 10, type: 'TOTAL', unstable: true]]
                            )
                        }
                    }
                }
            }
        }
    }
}
