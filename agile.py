# ============================================================
# JENKINS CI/CD LAB - ISWE406L
# Interactive reference: pick a question number to view its
# full source code / script / procedure.
# ============================================================

topics = {

"1": r'''
============================================================
QUESTION 1 - PYTEST PIPELINE (Checkout / Install / Test)
============================================================

Create a Jenkins pipeline on a Windows agent with three stages:
Checkout, Install Dependencies, and Run Unit Tests with pytest.

------------------------------------------------------------
app.py
------------------------------------------------------------

def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


------------------------------------------------------------
test_app.py
------------------------------------------------------------

from app import multiply, divide


def test_multiply():
    assert multiply(4, 5) == 20


def test_divide():
    assert divide(20, 5) == 4


------------------------------------------------------------
requirements.txt
------------------------------------------------------------

pytest


------------------------------------------------------------
Jenkinsfile
------------------------------------------------------------

pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat 'python -m pytest'
            }
        }
    }

    post {
        success {
            echo 'BUILD SUCCESSFUL - All tests passed.'
        }

        failure {
            echo 'BUILD FAILED - Check the test results.'
        }
    }
}


------------------------------------------------------------
FAILURE DEMONSTRATION
------------------------------------------------------------

Change multiply() temporarily to:

def multiply(a, b):
    return a + b

Then push the change and rebuild.

The test:

assert multiply(4, 5) == 20

will fail because:

4 + 5 = 9

Therefore Jenkins enters the failure post block:

BUILD FAILED - Check the test results.
''',


"2": r'''
============================================================
QUESTION 2 - PARAMETRIZED PYTEST (Verbose)
============================================================

Pipeline stages:
Checkout
Install Dependencies
Run Unit Tests (verbose)

Use find_min() and count_odds().

------------------------------------------------------------
app.py
------------------------------------------------------------

def find_min(numbers):
    return min(numbers)


def count_odds(numbers):
    return sum(1 for number in numbers if number % 2 != 0)


------------------------------------------------------------
test_app.py
------------------------------------------------------------

import pytest
from app import find_min, count_odds


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([5, 2, 8, 1], 1),
        ([10, 20, 30], 10),
        ([-5, -2, -10], -10)
    ]
)
def test_find_min(numbers, expected):
    assert find_min(numbers) == expected


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([1, 2, 3, 4, 5], 3),
        ([2, 4, 6, 8], 0),
        ([1, 3, 5, 7], 4)
    ]
)
def test_count_odds(numbers, expected):
    assert count_odds(numbers) == expected


------------------------------------------------------------
requirements.txt
------------------------------------------------------------

pytest


------------------------------------------------------------
Jenkinsfile
------------------------------------------------------------

pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat 'python -m pytest -v'
            }
        }
    }
}


------------------------------------------------------------
EXPECTED TEST COUNT
------------------------------------------------------------

There are:

1 test function for find_min()
    x 3 parameter values
    = 3 tests

1 test function for count_odds()
    x 3 parameter values
    = 3 tests

Total = 6 tests

The number of tests is 6 even though there are only 2 test
functions because pytest executes each parameterized case
as a separate test.

------------------------------------------------------------
FAILURE DEMONSTRATION
------------------------------------------------------------

Add this wrong case:

([1, 2, 3], 10)

The actual minimum is 1, but the expected value is 10.

Only that parameterized case fails.
''',


"3": r'''
============================================================
QUESTION 3 - ENV VARIABLES + MANUAL APPROVAL (input step)
============================================================

Pipeline stages:
Checkout
Build
Deploy

APP_NAME and APP_VERSION must be custom environment variables.

Deploy must pause for approval.

------------------------------------------------------------
app.py
------------------------------------------------------------

def main():
    print("Application started successfully.")
    print("Application deployment completed.")


if __name__ == "__main__":
    main()


------------------------------------------------------------
Jenkinsfile
------------------------------------------------------------

pipeline {
    agent any

    environment {
        APP_NAME = 'JenkinsDemoApp'
        APP_VERSION = '1.0'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                bat 'python -m py_compile app.py'
            }
        }

        stage('Deploy') {
            steps {

                input(
                    message: "Approve deployment of ${APP_NAME} version ${APP_VERSION}?",
                    ok: "Release"
                )

                bat 'python app.py'
            }
        }
    }
}


------------------------------------------------------------
OUTCOME 1 - RELEASE
------------------------------------------------------------

If you click:

Release

the pipeline continues.

app.py executes and prints:

Application started successfully.
Application deployment completed.

The build finishes successfully.


------------------------------------------------------------
OUTCOME 2 - ABORT
------------------------------------------------------------

If you click:

Abort

the deployment is cancelled.

The command:

python app.py

is not executed.

The build is aborted rather than completing normally.
''',


"4": r'''
============================================================
QUESTION 4 - BUILD INFO + LINTER (flake8)
============================================================

Pipeline stages:
Checkout
Show Build Info
Run Linter

The pipeline displays:
BUILD_NUMBER
JOB_NAME
WORKSPACE

------------------------------------------------------------
app.py - INITIAL VERSION
------------------------------------------------------------

def greet(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("Jenkins"))


------------------------------------------------------------
requirements.txt
------------------------------------------------------------

flake8


------------------------------------------------------------
Jenkinsfile
------------------------------------------------------------

pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Show Build Info') {
            steps {
                bat 'echo BUILD_NUMBER=%BUILD_NUMBER%'
                bat 'echo JOB_NAME=%JOB_NAME%'
                bat 'echo WORKSPACE=%WORKSPACE%'
            }
        }

        stage('Run Linter') {
            steps {
                bat 'python -m pip install flake8'
                bat 'python -m flake8 app.py'
            }
        }
    }
}


------------------------------------------------------------
BUILD INFORMATION
------------------------------------------------------------

Build 1 might show:

BUILD_NUMBER=1
JOB_NAME=YourJobName
WORKSPACE=C:\Jenkins\workspace\YourJobName

Build 2 might show:

BUILD_NUMBER=2
JOB_NAME=YourJobName
WORKSPACE=C:\Jenkins\workspace\YourJobName


------------------------------------------------------------
COMPARISON
------------------------------------------------------------

BUILD_NUMBER changes:

1 -> 2

JOB_NAME normally stays the same.

WORKSPACE normally stays the same for the same Jenkins job.

The exact WORKSPACE path depends on the Jenkins installation
and job configuration.


------------------------------------------------------------
LINTER FAILURE DEMONSTRATION
------------------------------------------------------------

Add this unused import:

import os


def greet(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("Jenkins"))


flake8 will report the unused import.

The Run Linter stage therefore fails.
''',


"5": r'''
============================================================
QUESTION 5 - PARAMETERIZED PIPELINE (choice + boolean)
============================================================

Parameterized pipeline.

Choice parameter:

ENVIRONMENT

Options:

dev
staging
prod

Boolean parameter:

RUN_EXTRA_CHECK

------------------------------------------------------------
app.py
------------------------------------------------------------

def show_environment(environment):
    print("Selected environment:", environment)


if __name__ == "__main__":
    show_environment("dev")


------------------------------------------------------------
Jenkinsfile
------------------------------------------------------------

pipeline {
    agent any

    parameters {

        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'prod'],
            description: 'Select deployment environment'
        )

        booleanParam(
            name: 'RUN_EXTRA_CHECK',
            defaultValue: false,
            description: 'Run extra validation check'
        )
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Show Parameter') {
            steps {
                echo "Selected environment: ${params.ENVIRONMENT}"
            }
        }

        stage('Extra Check') {
            when {
                expression {
                    return params.RUN_EXTRA_CHECK
                }
            }

            steps {
                echo "Extra check is running..."
                bat 'python app.py'
            }
        }
    }
}


------------------------------------------------------------
FIRST BUILD
------------------------------------------------------------

The first time the Jenkins job is created, Jenkins may not
show "Build with Parameters" until the Jenkinsfile containing
the parameters has been loaded and the job configuration has
been processed.

After Jenkins recognizes the parameters, the job provides
the parameterized build option.


------------------------------------------------------------
CHECKBOX UNCHECKED
------------------------------------------------------------

RUN_EXTRA_CHECK = false

The Extra Check stage is skipped because:

when {
    expression {
        return params.RUN_EXTRA_CHECK
    }
}

evaluates to false.


------------------------------------------------------------
CHECKBOX CHECKED
------------------------------------------------------------

RUN_EXTRA_CHECK = true

The Extra Check stage executes.


------------------------------------------------------------
ENVIRONMENT EXAMPLES
------------------------------------------------------------

ENVIRONMENT = dev

Output:

Selected environment: dev


ENVIRONMENT = staging

Output:

Selected environment: staging


ENVIRONMENT = prod

Output:

Selected environment: prod
''',


"6": r'''
============================================================
QUESTION 6 - PARALLEL STAGES + ARCHIVE ARTIFACTS
============================================================

Pipeline stages:
Checkout
Parallel Checks
Archive Reports

frontend_check.py and backend_check.py must run in parallel.

------------------------------------------------------------
frontend_check.py
------------------------------------------------------------

import time

print("Starting frontend check...")

time.sleep(4)

with open("frontend_report.txt", "w") as file:
    file.write("Frontend check completed successfully.\n")

print("Frontend check completed.")


------------------------------------------------------------
backend_check.py
------------------------------------------------------------

import time

print("Starting backend check...")

time.sleep(4)

with open("backend_report.txt", "w") as file:
    file.write("Backend check completed successfully.\n")

print("Backend check completed.")


------------------------------------------------------------
Jenkinsfile
------------------------------------------------------------

pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Parallel Checks') {
            parallel {

                stage('Frontend Check') {
                    steps {
                        bat 'python frontend_check.py'
                    }
                }

                stage('Backend Check') {
                    steps {
                        bat 'python backend_check.py'
                    }
                }
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'frontend_report.txt,backend_report.txt', fingerprint: true
            }
        }
    }
}


------------------------------------------------------------
TIME COMPARISON
------------------------------------------------------------

Sequential execution:

Frontend = approximately 4 seconds
Backend  = approximately 4 seconds

Total = approximately 8 seconds


Parallel execution:

Frontend = approximately 4 seconds
Backend  = approximately 4 seconds

Both start at approximately the same time.

Total = approximately 4 seconds
        plus Jenkins overhead.


------------------------------------------------------------
ARCHIVED ARTIFACTS
------------------------------------------------------------

Build 1 creates:

frontend_report.txt
backend_report.txt

Jenkins archives both.

When Build 2 runs, Build 1's archived artifacts remain
available under Build 1.

The newer build does not automatically delete the older
build's archived artifacts unless build retention policies
remove them.
''',


"7": r'''
============================================================
QUESTION 7 - SLEEP + MILESTONE + NOTIFICATION
============================================================

Pipeline stages:
Checkout
Build
Send Notification

Build must:
1. Compile app.py
2. Wait 15 seconds
3. Execute milestone(1)

------------------------------------------------------------
app.py
------------------------------------------------------------

def main():
    print("Build completed successfully.")
    print("Application is ready.")


if __name__ == "__main__":
    main()


------------------------------------------------------------
Jenkinsfile
------------------------------------------------------------

pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                bat 'python -m py_compile app.py'

                sleep time: 15, unit: 'SECONDS'

                milestone(1)
            }
        }

        stage('Send Notification') {
            steps {

                echo "Sending build notification..."

                echo "Recipient: #email_id"

                echo "Subject: ${JOB_NAME} - Build ${BUILD_NUMBER}"

                echo "Build URL: ${BUILD_URL}"

                echo "Build notification sent."
            }
        }
    }
}


------------------------------------------------------------
WHY ECHO IS USED
------------------------------------------------------------

The assignment allows either:

mail step

or

echo workaround

when SMTP is not configured.

The above Jenkinsfile uses echo so it can be demonstrated
without configuring an SMTP server. Replace #email_id with
your actual recipient address, and replace the mail step
below with the real one if SMTP is configured:

mail to: '#email_id',
     subject: "${JOB_NAME} - Build ${BUILD_NUMBER}",
     body: "Build URL: ${BUILD_URL}"


------------------------------------------------------------
TWO QUICK BUILDS
------------------------------------------------------------

Start Build 1.

Before Build 1 reaches:

milestone(1)

start Build 2.

Jenkins uses milestone(1) to prevent an older build from
continuing past the milestone when a newer build has already
passed that milestone.

Therefore the older build may be stopped at the milestone.

If the older build is stopped before reaching
Send Notification, it does not execute that stage and does
not send the notification.


------------------------------------------------------------
SYNTAX ERROR DEMONSTRATION
------------------------------------------------------------

Temporarily change app.py to:

def main()
    print("Build completed successfully.")


The missing ':' causes:

python -m py_compile app.py

to fail.

Therefore the Build stage fails.

The pipeline never reaches:

Send Notification

Therefore no notification is sent.
''',


"8": r'''
============================================================
QUESTION 8 - MAVEN + JENKINS CI/CD PIPELINE (FULL SETUP)
============================================================

This follows the "Install Maven -> Configure Maven in Jenkins
-> GitHub repo -> Jenkins Pipeline" procedure exactly.

------------------------------------------------------------
STEP 1 - CHECK JAVA (CMD / PowerShell)
------------------------------------------------------------

java --version

Expected output looks like:

openjdk 21.0.5 2024-10-15 LTS
OpenJDK Runtime Environment Temurin-21.0.5+11 (build 21.0.5+11-LTS)
OpenJDK 64-Bit Server VM Temurin-21.0.5+11 (build 21.0.5+11-LTS, mixed mode, sharing)


------------------------------------------------------------
STEP 2 - INSTALL MAVEN
------------------------------------------------------------

1. Go to: #email_id   (Apache Maven download page)
2. Download apache-maven-bin.zip
3. Save it in the SAME folder as your JDK installation
   (e.g. C:\_tools\)
4. Extract all in that same folder
5. Copy the full path of the Maven "bin" directory, e.g.:

   C:\_tools\apache-maven-3.9.9\bin


------------------------------------------------------------
STEP 3 - SET ENVIRONMENT VARIABLES (Windows)
------------------------------------------------------------

Open: System Properties -> Advanced -> Environment Variables

A) Edit the "Path" variable:
   - Click New
   - Paste the Maven bin path:
     C:\_tools\apache-maven-3.9.9\bin
   - Click OK

B) Create MAVEN_HOME:
   - Click New under System Variables
   - Variable name:  MAVEN_HOME
   - Variable value: C:\_tools\apache-maven-3.9.9
     (same link as the bin path, with \bin removed)
   - Click OK

C) Create M2_HOME:
   - Click New under System Variables
   - Variable name:  M2_HOME
   - Variable value: C:\_tools\apache-maven-3.9.9
     (again, remove \bin from the value)
   - Click OK


------------------------------------------------------------
STEP 4 - VERIFY MAVEN INSTALLATION
------------------------------------------------------------

Open a new Command Prompt and run:

mvn --version

Expected output:

Apache Maven 3.9.9 (8e8579a9e76f7d015ee5ec7bfcdc97d260186937)
Maven home: C:\_tools\apache-maven-3.9.9
Java version: 21.0.5, vendor: Eclipse Adoptium, runtime: C:\_tools\jdk-21
Default locale: en_US, platform encoding: UTF-8
OS name: "windows 11", version: "10.0", arch: "amd64", family: "windows"

This confirms Maven is successfully installed.


------------------------------------------------------------
STEP 5 - CONFIGURE MAVEN IN JENKINS
------------------------------------------------------------

Path:
Manage Jenkins -> Tools -> Maven Installations

Configuration:
Name:              M3
MAVEN_HOME:        C:\Program Files\Apache\apache-maven-3.9.12
Install automatically: UNCHECKED

(Point this to wherever Maven is actually installed on the
Jenkins agent machine.)


------------------------------------------------------------
STEP 6 - CREATE THE GITHUB REPOSITORY
------------------------------------------------------------

1. Create a new repository, e.g.: simple-maven-app
2. Add a file: pom.xml


------------------------------------------------------------
pom.xml
------------------------------------------------------------

<project xmlns="http://maven.apache.org/POM/4.0.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
http://maven.apache.org/xsd/maven-4.0.0.xsd">
<modelVersion>4.0.0</modelVersion>
<groupId>com.example</groupId>
<artifactId>simple-maven-app</artifactId>
<version>1.0-SNAPSHOT</version>
<dependencies>
 <dependency>
 <groupId>junit</groupId>
 <artifactId>junit</artifactId>
 <version>4.13.2</version>
 <scope>test</scope>
 </dependency>
</dependencies>
</project>

Commit the changes.


------------------------------------------------------------
STEP 7 - CREATE THE FOLDER STRUCTURE
------------------------------------------------------------

src/
  main/java/com/example/App.java
  test/java/com/example/AppTest.java


------------------------------------------------------------
App.java
------------------------------------------------------------

package com.example;

public class App {
    public int add(int a, int b) {
        return a + b;
    }
}

Commit the changes.


------------------------------------------------------------
AppTest.java
------------------------------------------------------------

package com.example;

import org.junit.Test;
import static org.junit.Assert.*;

public class AppTest {

    @Test
    public void testAdd() {
        App app = new App();
        assertEquals(5, app.add(2, 3));
    }
}

Commit the changes.


------------------------------------------------------------
STEP 8 - LOCAL BUILD TEST (VS Code)
------------------------------------------------------------

1. Clone your Git repository in VS Code
2. In the integrated terminal, run:

   mvn clean test

Expected end of output:

[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS


------------------------------------------------------------
STEP 9 - CREATE THE JENKINS PIPELINE JOB
------------------------------------------------------------

1. New Item
2. Enter a name (e.g. "Maven Pipeline 2") and select "Pipeline"
3. Click OK


------------------------------------------------------------
Jenkinsfile (Pipeline script)
------------------------------------------------------------

pipeline {
    agent any

    tools {
        maven 'M3'
    }

    stages {

        stage('Checkout Git') {
            steps {
                git branch: 'main',
                    url: '#email_id'
            }
        }

        stage('Build and Test') {
            steps {
                bat 'mvn clean test'
            }
        }
    }
}

Replace #email_id above with your own GitHub repository URL,
e.g. https://github.com/#email_id/simple-maven-app.git

4. Click Apply and Save
5. Click "Build Now"


------------------------------------------------------------
EXPECTED CONSOLE OUTPUT
------------------------------------------------------------

[INFO] -------------------------------------------------------
[INFO] Running com.example.AppTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO]
[INFO] Results:
[INFO]
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO]
[INFO] -------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] -------------------------------------------------------
[Pipeline] }

A green checkmark on the build (#1, #2, #3 ...) under
"Builds" in Jenkins confirms the pipeline ran successfully,
and "Last successful build" updates on the Permalinks panel.
''',

}

TOPIC_LABELS = {
    "1": "Pytest pipeline (Checkout / Install / Test)",
    "2": "Parametrized pytest (verbose)",
    "3": "Env variables + manual approval (input step)",
    "4": "Build info + linter (flake8)",
    "5": "Parameterized pipeline (choice + boolean)",
    "6": "Parallel stages + archive artifacts",
    "7": "Sleep + milestone + notification",
    "8": "Maven + Jenkins CI/CD pipeline (full setup)",
}


# ============================================================
# INTERACTIVE MENU
# ============================================================

def show_menu():
    print("\n" + "=" * 60)
    print("   JENKINS CI/CD LAB - ISWE406L")
    print("=" * 60)
    for key in sorted(topics, key=int):
        print(f"  {key}. {TOPIC_LABELS[key]}")
    print("  q. Quit")
    print("-" * 60)


def show_topic(choice):
    print(topics[choice])


def main():
    while True:
        show_menu()
        choice = input("Enter question number to view (or 'q' to quit): ").strip().lower()

        if choice == "q":
            print("Exiting. Goodbye!")
            break

        if choice in topics:
            show_topic(choice)
            input("\nPress Enter to return to the menu...")
        else:
            print(f"\nInvalid choice: '{choice}'. Please enter a number from 1 to {len(topics)}, or 'q'.\n")


if __name__ == "__main__":
    main()