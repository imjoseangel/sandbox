pipeline {

    agent any

    options {
        timestamps()
    }

    environment {
        OMDB_API = credentials('65a37764-3a16-4034-8121-b187a71e2b2d')
        GITHUB_TOKEN = credentials('328cb8da-dc12-45ef-a25e-f809cee162ea')
    }

    stages {
        stage('Publish Artifact') {
            steps {
                script {
                    try {
                        sh '''
                            python3 -m venv $HOME/venv
                            . $HOME/venv/bin/activate
                            pip install -r requirements.txt
                            python python/omdb/omdb.py
                        '''
                    }
                    catch (exception) {
                        throw exception
                    }
                }
                archiveArtifacts artifacts: '*.json'
            }
        }
        stage ('Publish on GitHub') {
            steps {
                script {
                    try {
                        sh '''
                            export TAG=$(date +"%m.%d.%Y.%s")
                            release=$(curl -XPOST -H "Authorization:token $GITHUB_TOKEN" --data '{"tag_name": "'$TAG'", "target_commitish": "devel", "name": "'$TAG'", "body": "'$TAG'", "draft": false, "prerelease": false}' https://api.github.com/repos/imjoseangel/sandbox/releases)
                            id=$(echo "$release" | jq '.id')
                            curl -XPOST -H "Authorization:token $GITHUB_TOKEN" -H "Content-Type:application/octet-stream" --data-binary @movies.json https://uploads.github.com/repos/imjoseangel/sandbox/releases/$id/assets?name=movies.json
                        '''
                    }
                    catch (exception) {
                        throw exception
                    }
                }
            }
        }
    }
    post {
        always {
            sh 'rm -rf $HOME/venv'
        }
    }
}
