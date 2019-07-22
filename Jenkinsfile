node{
       
    os = checkOs() 
    
    try {
    
        stage('Checkout'){
            checkout scm
        }

        stage('Run Script'){
            if (os == "Windows"){
            bat 'python src/system_inventory.py'
            }
            else{
            sh 'python3 src/system_inventory.py' 
            } 
               
        }

        stage('Archive'){
            archiveArtifacts 'Inventory_store/*/*.json'
        }

    } catch(err){
        notify("Error ${err}")
        currentBuild.result = 'Failure'
    }
}


def notify(status){
    emailext (
            to: "jbqjenkins@gmail.com",
            subject: "${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            body: """<p>${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
        <p>Check console output at <a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a></p>""",
    )
}

def checkOs(){
    if (isUnix()) {
        def uname = sh script: 'uname', returnStdout: true
        if (uname.startsWith("Darwin")) {
            return "Macos"
        }
          
        else {
            return "Linux"
        }
    }
    else {
        return "Windows"
    }
}
