# Aws community day GT  Demo step by step Guide

## 1 Infrastructure Definition

### 1.1 Install Pulumi CLI  and install your choose Language runtime

    Follow the oficial documentation to install pulumi.  
    https://www.pulumi.com/docs/clouds/aws/get-started/begin/

### 1.2. Configure your backend state 
if you want to sue pulumi service as your backend state, then  create an free account and using the pulumi cli to login and set the pulumi token.

```bash
    pulumi login
```

### 1.3. Create your IAC Project
After login, create a new iac pulumi project (in this workshop we'll use Python as our iac language)

```bash
    # create the project directory
    mkdir aws-community-day-infra 

    cd aws-community-day-infra

    # start a new pulumi project with python
    pulumi new aws-python
```
you will be asked for a project name and project description. Hit ENTER to accept the default values or specify new values.

![pulumi-new-project-wizard](img/image.png)

Next, you will be asked for a stack name. Hit ENTER to accept the default value of dev.

Finally, you will be prompted for some configuration values for the stack. For AWS projects, you will be prompted for the AWS region. You can accept the default value or choose another value like us-east-1.

After the command completes, the project and stack will be ready.
Next, we’ll review the generated project files.

### 1.4 Define some Resources to be deployed

Edit the `main.py` file, this is the Pulumi program that defines your stack resources.