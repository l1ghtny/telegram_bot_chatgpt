/**
* JetBrains Space Automation
* This Kotlin script file lets you automate build activities
* For more info, see https://www.jetbrains.com/help/space/automation.html
*/

job("Build and push Docker"){
    // parameters {
    //     // 'private-ssh-key' secret must be created in the project
    //     secret("OPENAI_API_KEY", "{{ project:OPENAI_API_KEY }}")
    //     secret("path", "{{ project:path }}")
    //     secret("token", "{{ project:token }}")
    // }
    host("Build and push a Docker image") {
        // fileInput {
        //     source = FileSource.Text("token:{{ project:token }} \n path:{{ project:path }} \n openai_api_key:{{ project:OPENAI_API_KEY }}")
        //     localPath = "/home/tg-bot-gpt/.env"
        // }
        // shellScript {
        //     content = """
        //         chmod +x /home/tg-bot-gpt/.env
        //         /home/tg-bot-gpt/.env .
        //     """
        // }
      	
        dockerBuildPush {
            // by default, the step runs not only 'docker build' but also 'docker push'
            // to disable pushing, add the following line:
            // push = false

            // path to Docker context (by default, context is working dir)
            // path to Dockerfile relative to the project root
            // if 'file' is not specified, Docker will look for it in 'context'/Dockerfile
            file = "Dockerfile"
            // build-time variables
            // args["HTTP_PROXY"] = "http://10.20.30.2:1234"
            // image labels
            //labels["vendor"] = "lightny"
            // to add a raw list of additional build arguments, use
            // extraArgsForBuildCommand = listOf("...")
            // to add a raw list of additional push arguments, use
            // extraArgsForPushCommand = listOf("...")
            // image tags
            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"lightny.registry.jetbrains.space/p/main/tg-gpt-bot/gpt-bot:1.0.${"$"}JB_SPACE_EXECUTION_NUMBER"
            }
        }
    }
}