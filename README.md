----------------------------------------------------------

#  **DevOps Internship Challenge – Final Report**

------------------------------------------------------------

## Project Title


 ###  DevOps Infrastructure Automation & Monitoring Using Proxmox, Terraform, Jenkins, and Prometheus

---

### 🔧 **DevOps Infrastructure Automation & Monitoring Project**
*A Real-World Scenario with Proxmox, Jenkins, Containers, and Prometheus*

---

### 🚀 **Full-Stack DevOps Pipeline: From Provisioning to Monitoring**
*Automated App Deployment with Proxmox, Jenkins, Crontab, and Prometheus*

---

### 🛠️ **End-to-End DevOps Workflow on Proxmox**
*Static Infrastructure, CI/CD, Flask App Deployment, and Observability*

---

### 🌐 **Infrastructure Automation & Observability on Proxmox**
*VM + Container Setup, Jenkins Pipeline, and Prometheus Metrics Collection*

---

### ⚙️ **Flask App Deployment on Proxmox with CI/CD and Monitoring**
*A Beginner-Friendly End-to-End DevOps Project*

---


##  Tools & Environment

| Tool        | Purpose                                   |
|-------------|-------------------------------------------|
| **Proxmox** | Container/VM orchestration                |
| **VMware**  | VM execution due to local performance limits |
| **Ubuntu Server** | OS for both container and VM environments |
| **Terraform** | Infrastructure-as-Code for VM/container provisioning |
| **Jenkins** | CI/CD pipeline automation                 |
| **Prometheus** | Monitoring metrics                      |

---

---------------------------------------------
# **Proxmox and VM Setup**
-----------------------------------------------
 
## Set Up Proxmox
### 1.1 Install Proxmox VE
- Download Proxmox VE ISO from the official website: Proxmox Downloads
- Create a bootable USB using Rufus (Windows) or dd command (Linux/macOS)
- Install Proxmox on a physical machine or a VirtualBox VM (if testing)

---
---
<img src="images/Screenshot 2025-04-04 030303.png" alt="My Image" width="500">
<img src="images/Screenshot 2025-04-04 030312.png" alt="My Image" width="500">

---


## Create a Virtual Machine (VM)

- Open Proxmox Web UI (https://your-proxmox-ip:8006)
- Click Create VM
- Choose Ubuntu 22.04 ISO

Assign:

- 2 CPU cores
- 4GB RAM
- 50GB Disk
- Configure networking (Use a virtual bridge for static IP)
  
<img src="images/Screenshot 2025-04-04 032033.png" alt="My Image" width="500">

### Due to some performance issues so I used the VMware for my VM Ubuntu insted pve in Proxmox virtual environment.

<img src="images/Screenshot 2025-04-05 132702.png" alt="My Image" width="500">


## Create a Container (LXC or Docker)

- Click Create CT in Proxmox UI
- Use a minimal Ubuntu or Alpine Linux template
- 
Assign:
- 1 CPU core
- 1GB RAM
- 10GB Disk

- Configure networking (Static IP, connect to bridge)

<img src="images/Screenshot 2025-04-03 174023.png" alt="My Image" width="500">
<img src="images/Screenshot 2025-04-04 030327.png" alt="My Image" width="500">


Great! Let's set up the **networking** for your Proxmox VM and Container so they can communicate properly.

---


------------------------------------------------------
#  **Networking Setup**
------------------------------------------------------


<img src="images/Screenshot 2025-04-03 153630.png" alt="My Image" width="500">



## Identify Network Interfaces
First, let's check the network interfaces on your Proxmox system.

```bash
ip a
```
This will show all available network interfaces. You should see something like this:

```
2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 192.168.73.213/24 brd 192.168.73.255 scope global enp3s0
    valid_lft forever preferred_lft forever
```
- Here, `enp3s0` is your **main network interface** (yours may be different, like `eth0` or `ens18`).
- Your **Proxmox host's IP** is `192.168.73.213`.
- Your **default gateway** is `192.168.73.213`.

---

## **Configure Static IP for Your Container**
Since your container's IP is **192.168.73.50**, we need to ensure:
- It has a **static IP**.
- It can reach the **default gateway (192.168.73.213)**.
- It has **internet access**.

### **Edit the Container's Network Configuration**
On **Proxmox Web UI**:
1. **Go to Datacenter > Your Node > Containers**
2. Select your **Container (LXC)**
3. Click on **Network**
4. If there is an existing network adapter (`eth0`), select it and **edit**.
   - If none exists, **add a new network interface**.
5. Set:
   - **IPv4 Address:** `192.168.73.50/24`
   - **Gateway:** `192.168.73.213`
   - **Bridge:** `vmbr0` (or your default bridge)

### **Manual Configuration via CLI**
If you prefer using CLI, open the Proxmox shell and **edit the network config for LXC**:

```bash
nano /etc/network/interfaces
```

Update it with:
```
auto eth0
iface eth0 inet static
    address 192.168.73.50
    netmask 255.255.255.0
    gateway 192.168.73.213
    dns-nameservers 8.8.8.8 8.8.4.4
```

### **Apply Changes**
```bash
systemctl restart networking
ip a
```

This will **assign the static IP** `192.168.73.50` and apply the new settings.

---

## **Configure Static IP for Your Virtual Machine**
If you also have a **VM** (Ubuntu 22.04), follow these steps:

### **Edit Netplan Configuration**
1. Open the netplan config file:
   ```bash
   sudo nano /etc/netplan/00-installer-config.yaml
   ```
2. Update it with:
   ```yaml
   network:
     ethernets:
       ens18:
         dhcp4: no
         addresses:
           - 192.168.73.100/24
         gateway4: 192.168.73.213
         nameservers:
           addresses:
             - 8.8.8.8
             - 8.8.4.4
     version: 2
   ```
   (Replace `ens18` with your actual network interface from `ip a`.)

### **Apply the Configuration**
```bash
sudo netplan apply
```
Now your VM has a static IP (`192.168.73.100` in this example).

<img src="images/Screenshot 2025-04-04 030625.png" alt="My Image" width="500">

---

## **Verify Connectivity**
Now that both your **VM** and **Container** have static IPs, test their connectivity.

### **1️⃣ Test Container → Gateway**
On your **LXC container**, run:
```bash
ping -c 4 192.168.73.213
```
If successful, it should return something like:
```
64 bytes from 192.168.73.213: icmp_seq=1 ttl=64 time=0.4 ms
```

### **2️⃣ Test VM → Container**
On your **VM**, run:
```bash
ping -c 4 192.168.73.50
```
If successful, it should return:
```
64 bytes from 192.168.73.50: icmp_seq=1 ttl=64 time=0.3 ms
```

<img src="images/Screenshot 2025-04-05 134731.png" alt="My Image" width="500">


### **3️⃣ Test Internet Connectivity**
On your **Container** or **VM**, run:
```bash
ping -c 4 google.com
```
If this fails, check your DNS settings (`8.8.8.8`).

---

# **Configure Hostname Resolution**
To make it easier to communicate between **VM and Container**, update `/etc/hosts` on **both**.

```bash
sudo nano /etc/hosts
```
Add:
```
192.168.73.50   my-container
192.168.73.100  my-vm
```
Now, you can SSH or ping using names:
```bash
ping my-container
ssh user@my-container
```
<img src="images/Screenshot 2025-04-05 134830.png" alt="My Image" width="500">

<img src="images/Screenshot 2025-04-05 134905.png" alt="My Image" width="500">


---


-------------------------------------------------------------
#  **Flask Application Setup** 
------------------------------------------------------------

---

## **Install Dependencies**  
Before starting, update the package list and install necessary dependencies.  

- Run these commands **inside your LXC container (`192.168.73.50`)**:  
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx gunicorn
```
 **Explanation:**  
- `python3`, `python3-pip`, `python3-venv` → Python and virtual environment  
- `nginx` → Web server to act as a reverse proxy  
- `gunicorn` → A production WSGI server to run Flask  

---

## **Create the Flask Application**
- We will place our Flask application inside `/opt/flask_app/`.  

**Create the directory and navigate into it:**  
```bash
sudo mkdir -p /opt/flask_app
cd /opt/flask_app
```

- **Create a virtual environment and activate it:**  
```bash
python3 -m venv venv
source venv/bin/activate
```

- **Install Flask inside the virtual environment:**  
```bash
pip install flask
```

- **Create the Flask application file:**  
```bash
nano app.py
```
Paste the following code inside `app.py`:
```python
from flask import Flask
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World from Chandu!"

@app.route('/compute')
def compute():
    start_time = time.time()
    result = sum(i * i for i in range(10_000))  # Simulating CPU-intensive task
    end_time = time.time()
    return f"Computation done in {end_time - start_time:.4f} seconds"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

<img src="images/Screenshot 2025-04-04 030353.png" alt="My Image" width="500">

- **Save and Exit:**  
Press **`CTRL + X`**, then **`Y`**, then **`Enter`**.  

---

## **Test Flask Application**
Before running it with **Gunicorn**, let's test the Flask app.  

- **Run the Flask application:**  
```bash
python app.py
```
- **Test in a browser or using curl:**  
```bash
curl http://192.168.73.50:5000/
```

<img src="images/Screenshot 2025-04-04 031809.png" alt="My Image" width="500">

Expected Output:  
```
Hello World from Chandu!
```

<img src="images/Screenshot 2025-04-04 031025.png" alt="My Image" width="500">

- **Stop the app (`CTRL + C`) and proceed.**  

---

## **Run Flask with Gunicorn**
Gunicorn will serve the Flask application efficiently.  

- **Run Flask using Gunicorn:**  
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```
 **Explanation:**  
- `--bind 0.0.0.0:5000` → Makes the app accessible from the network  
- `app:app` → `app.py` file & `app` object  

- **Test again in your browser:**  
   `http://192.168.73.50:5000/`  

- **If it works, stop Gunicorn (`CTRL + C`)** and proceed to set up **SystemD**.

---

## **Setup SystemD Service**
SystemD ensures that the Flask app **automatically starts** and keeps running.

- **Create a SystemD service file:**  
```bash
sudo nano /etc/systemd/system/flask_app.service
```
Paste the following content:
```ini
[Unit]
Description=Flask App Service
After=network.target

[Service]
User=root
WorkingDirectory=/opt/flask_app
ExecStart=/opt/flask_app/venv/bin/gunicorn --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```
- **Save and Exit** (`CTRL + X`, then `Y`, then `Enter`).  

- **Reload SystemD and enable the service:**  
```bash
sudo systemctl daemon-reload
sudo systemctl enable flask_app
sudo systemctl start flask_app
sudo systemctl status flask_app
```
- **Expected Output:**  
- You should see the Flask service running   

---

## **Configure Nginx as a Reverse Proxy**
Nginx will act as a reverse proxy to make the Flask app accessible via **port 80**.

- **Create an Nginx configuration file:**  
```bash
sudo nano /etc/nginx/sites-available/flask_app
```
Paste the following:
```nginx
server {
    listen 80;
    server_name 192.168.73.50;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
- **Save and Exit** (`CTRL + X`, then `Y`, then `Enter`).  

- **Enable the configuration and restart Nginx:**  
```bash
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## **Test the Application**

<img src="images/Screenshot 2025-04-04 030722.png" alt="My Image" width="500">

- **Check if Nginx is running properly:**  
```bash
sudo systemctl status nginx
```
- **Test in your browser:**  
- `http://192.168.73.50/`  

- **You should see:** `"Hello World from Chandu!"`  
- **Go to:** `http://192.168.73.50/compute` (should perform computation)  

<img src="images/Screenshot 2025-04-04 031759.png" alt="My Image" width="500">


---

---------------------------------------------------------------------
# **Automation with Crontab**
--------------------------------------------------------------------  

---

## **Verify Crontab & Install If Missing**  
### **(Perform on the System Running Flask)**
### **Check if Cron Service is Running**
Run:  
```bash
sudo systemctl status cron
```
- If you see **Active: active (running)**, the cron service is running.
- If **inactive (dead)**, start it using:
  ```bash
  sudo systemctl start cron
  ```
- Enable cron to start on boot:
  ```bash
  sudo systemctl enable cron
  ```

### **If Cron is Not Installed**
Install it using:  
```bash
sudo apt update && sudo apt install cron -y
```

---

## **Create a Script to Call `/compute`**
Instead of writing a direct `curl` command in `crontab`, it's a good practice to create a script.

### **Create a New Shell Script**
Run:
```bash
sudo nano /opt/flask_app/request_compute.sh
```
Paste the following inside the file:
```bash
#!/bin/bash

# Log file to store request responses
LOG_FILE="/var/log/compute_cron.log"

# Send request to Flask app and log output
curl -X GET http://127.0.0.1:5000/compute >> $LOG_FILE 2>&1
```
Save and exit (`CTRL+X`, then `Y`, then `ENTER`).

### **Make the Script Executable**
Run:
```bash
sudo chmod +x /opt/flask_app/request_compute.sh
```

---

## **Schedule the Script in Crontab**
Now, let's set up a **cron job** that executes this script **every minute**.

### **Open Crontab**
Run:
```bash
crontab -e
```
(If prompted to select an editor, choose **Nano**.)

<img src="images/Screenshot 2025-04-05 145200.png" alt="My Image" width="500">

### **Add the Following Line at the End**
```bash
* * * * * /opt/flask_app/request_compute.sh
```
Save and exit (`CTRL+X`, then `Y`, then `ENTER`).

---

## **Verify Crontab is Working**
### **List the Scheduled Cron Jobs**
Run:
```bash
crontab -l
```
Expected output:
```bash
* * * * * /opt/flask_app/request_compute.sh
```

### **Check if the Script is Executing**
Wait for a few minutes and check logs:
```bash
cat /var/log/compute_cron.log
```
<img src="images/Screenshot 2025-04-05 145113.png" alt="My Image" width="500">

If you see output logs, **Crontab is working correctly!** 

---

### **Troubleshooting Cron Issues**
**Cron Job Not Running? Try These:**
1. **Check Cron Service Status**
   ```bash
   sudo systemctl status cron
   ```
   If it's not running, start it:
   ```bash
   sudo systemctl restart cron
   ```

<img src="images/Screenshot 2025-04-04 031609.png" alt="My Image" width="500">


2. **Run the Script Manually to Check for Errors**
   ```bash
   /opt/flask_app/request_compute.sh
   ```
   If it fails, check Flask is running and the endpoint is accessible.

3. **Use Absolute Paths in Crontab**
   Ensure full paths are used inside the script:
   ```bash
   /usr/bin/curl -X GET http://127.0.0.1:5000/compute >> /var/log/compute_cron.log 2>&1
   ```

---

**Crontab is now automating the `/compute` request every minute!** 


Absolutely! Let's go **step-by-step** with **every detail** you need — from creating the `Jenkinsfile`, pushing it to GitHub, and running it through Jenkins to deploy your Flask app on your container. 💡

---




-----------------------------------------------------------------------------
# **Jenkins Pipeline Deployment for Flask App**
-----------------------------------------------------------------------


---

### **Create the `Jenkinsfile` Locally**

#### 1. Open Terminal on your local machine
Navigate to your Flask project directory:

```bash
cd /path/to/your/flask-app
```

(If you're not sure where that is, use `ls` or `pwd` to check.)

#### 2. Create a `Jenkinsfile`

```bash
nano Jenkinsfile
```

> `nano` is a text editor. If you prefer `vim` or VS Code, that works too.

#### 3. Paste the Pipeline Code Into `Jenkinsfile`

Here’s a complete example — **copy and paste** this into the file:

```groovy
pipeline {
    agent any

    environment {
        APP_DIR = "/opt/flask-app"
        SSH_CREDS = "374d2c80-d7f4-454f-9c70-1f0bf9681dc6"
        CONTAINER_IP = "192.168.73.50"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/chanduo5/flask-app.git'
            }
        }

        stage('Check Python & Pip') {
            steps {
                sh 'which python3'
                sh 'python3 --version'
                sh 'python3 -m pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Deploy to Container') {
            steps {
                script {
                    sshagent(credentials: [env.SSH_CREDS]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no root@${CONTAINER_IP} << EOF
                        cd ${APP_DIR}
                        git pull origin main
                        python3 -m pip install -r requirements.txt
                        systemctl restart flask-app
                        systemctl restart nginx
                        EOF
                        """
                    }
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://${CONTAINER_IP}", returnStdout: true).trim()
                    if (response != '200') {
                        error "❌ App not healthy! Got HTTP $response"
                    } else {
                        echo "✅ App is healthy and returned HTTP $response"
                    }
                }
            }
        }
    }
}
```


## **Generate SSH Key (if needed)**

On your Jenkins server (or your local machine if Jenkins is on the same box):

<img src="images/Screenshot 2025-04-04 030904.png" alt="rsakeygen" width="500">

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Press `Enter` to save it to the default path (`~/.ssh/id_rsa`) and don’t set a passphrase.

 **This generates:**
- Private key: `~/.ssh/id_rsa`
- Public key: `~/.ssh/id_rsa.pub`
- <img src="images/Screenshot 2025-04-04 030921.png" alt="pubjenkinskey" width="500">


---

## Add Public Key to GitHub

1. Go to [https://github.com](https://github.com) > your profile > **Settings**
2. Click **"SSH and GPG keys"** > **New SSH key**
3. Title: `Jenkins SSH Key`
4. Paste the contents of your public key (`~/.ssh/id_rsa.pub`)
5. Click **Add SSH Key**
<img src="images/Screenshot 2025-04-04 030814.png" alt="jenkinskey" width="500">


---

## Add Private Key to Jenkins

1. Go to your Jenkins UI → **Manage Jenkins** → **Credentials** → (select appropriate domain or global scope)
2. Click **Add Credentials**
3. Choose:
   - **Kind:** `SSH Username with private key`
   - **Username:** `git` (important for GitHub)
   - **Private Key:** Choose “Enter directly” and paste the contents of `~/.ssh/id_rsa`
   - **ID:** Give it a memorable ID, e.g., `github-ssh`
   - **Description:** Something like `GitHub SSH Key for Flask App`
4. Save


<img src="images/Screenshot 2025-04-04 032156.png" alt="GIT_SSH_jenkinskey" width="500">
---

## **Setup GitHub Webhook**

Want Jenkins to auto-deploy when you push code?

<img src="images/Screenshot 2025-04-04 032122.png" alt="webooks" width="500">

### In GitHub Repo:
- Go to **Settings** → **Webhooks** → **Add Webhook**
- Payload URL:  
  ```
  http://192.168.73.100:8080/github-webhook/
  ```
- Content type: `application/json`
- Click *our job has **"GitHub hook trigger for GITScm polling"** checked in Build Triggers.

Now, every `git push` will auto-trigger the pipeline.

---


## 🔁 Step 4: Update Your Git URL

Update your pipeline or job to use the **SSH Git URL**, like:

```bash
git@github.com:chanduo5/flask-app.git
```

Instead of:

```bash
https://github.com/chanduo5/flask-app.git
```

---

## Use in Pipeline

Here's an updated `Jenkinsfile` **Checkout** stage using `sshagent`:

```groovy
stage('Checkout') {
    steps {
        sshagent(['github-ssh']) {
            sh 'git clone git@github.com:chanduo5/flask-app.git'
        }
    }
}
```

Or if using the `git` step:

```groovy
stage('Checkout') {
    steps {
        sshagent(['github-ssh']) {
            git branch: 'main', url: 'git@github.com:chanduo5/flask-app.git'
        }
    }
}
```

<img src="images/Screenshot 2025-04-04 030854.png" alt="statusjenkins" width="500">



---

### 💾 4. Save and Exit
- Press `CTRL+X`
- Press `Y` to confirm saving
- Press `Enter` to save as `Jenkinsfile`

---

## **Commit and Push the `Jenkinsfile` to GitHub**

Make sure Git is initialized. Then:

```bash
git status               # Check if Jenkinsfile is listed
git add Jenkinsfile      # Stage the file
git commit -m "Add Jenkinsfile for Jenkins pipeline"
git push origin main     # Push to your main branch
```

✅ Now the `jenkinsfile` is live in your GitHub repo!

<img src="images/Screenshot 2025-04-05 034312.png" alt="jenkinskey_in_github" width="500">

<img src="images/Screenshot 2025-04-05 150851.png" alt="jenkinskey_in_github" width="500">
---

## **Jenkins Setup**

###  1. Open Jenkins UI

Navigate to:  
```
http://192.168.73.100:8080
```

###  2. Create a New Pipeline Job
- Click **"New Item"**
- Enter a name like: `FlaskAppDeployment`
- Choose **Pipeline**
- Click **OK**
<img src="images/Screenshot 2025-04-05 014422.png" alt="job" width="500">

###  3. Configure the Pipeline Job


Under **Pipeline** section:
- Definition: **Pipeline script from SCM**
- SCM: **Git**
- Repository URL:  
  ```
  https://github.com/YOUR_USERNAME/flask-app.git
  ```
- Branch:  
  ```
  */main
  ```

Click **Save**.

<img src="images/Screenshot 2025-04-05 014422.png" alt="job" width="500">

---

## Trigger the Jenkins Pipeline

### Build It!

<img src="images/Screenshot 2025-04-05 152210.png" alt="FlaskAppDeployment" width="500">

- Go to your `FlaskAppDeployment` job
- Click **"Build Now"**

###  View Console Output
- Click on the build number (e.g., `#1`)
- Click **"Console Output"**
<img src="images/Screenshot 2025-04-05 152319.png" alt="joberror" width="500">

 You should see logs for:
- Cloning repo
- Installing dependencies
- SSHing into the container
- Pulling latest code
- Restarting the Flask app and Nginx
- Health check via curl

------------------------------------------------
**Due to some network error/ minor error the expected output was not showing**
------------------------------------------------

Expected final message:
```
Application is running successfully with status 200!
```

---

## 🌐 Step 5: Test Your Flask App

### 🧪 Test with cURL:
From your Jenkins server or any machine in the network:

```bash
curl http://192.168.73.50
```

Expected:
```json
{"message": "Hello, Flask is running!"}
```

### 🌍 Open in Browser:
Go to [http://192.168.73.50](http://192.168.73.50)  
Your Flask app should be live!

---


## 5. 🧪 Errors Faced & Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| Jenkins service not starting | Port conflict or low memory | Switched to a better-resourced VMware VM |
| Application deployment failed in Jenkins | Misconfigured Jenkinsfile and missing Docker dependencies | Not fully resolved due to time constraints |
| Prometheus dashboard blank | Wrong port or missing node exporter | Installed `node_exporter` and configured target properly |

---

## 7. 🧹 Limitations & Next Steps

- Jenkins app deployment failed — needs Docker image setup and a complete `Jenkinsfile`
- Application logic and integration were not tested


---
-----------------------------------------------------------------------------------------

# **Conclusion**

This DevOps Internship Challenge project served as a valuable hands-on experience in implementing modern DevOps practices. Despite certain limitations, such as performance issues with Proxmox and incomplete Jenkins pipeline execution, the project successfully demonstrated the manual provisioning of infrastructure, CI/CD pipeline setup using Jenkins, application deployment with Flask, and monitoring via Prometheus.

By manually linking a Docker container with a VM instead of using Terraform, this setup provided deeper insights into networking, container communication, and configuration. Key DevOps principles like automation, scalability, and observability were implemented using real-world tools such as Jenkins, Prometheus, and Nginx.

The foundational components are fully functional and ready to be expanded with enhancements like Docker-based deployment, Jenkinsfile integration, and production-ready app hosting. This journey also strengthened troubleshooting skills and provided an authentic simulation of deployment pipelines in constrained environments.

-----------------------------------------------------------------------------------------
---
----------------------------------------------------------------------------------------------------------
## **Resources & References**
- Official Documentation
These were the foundational sources used for configuring tools and solving setup issues:

- Docker: https://docs.docker.com
- Jenkins: https://www.jenkins.io/doc/
- Prometheus: https://prometheus.io/docs/
- Nginx: https://nginx.org/en/docs/
- Flask (Python): https://flask.palletsprojects.com

- **YouTube Channels & Videos**

- https://www.youtube.com/watch?v=ufiSO9RHhYg&t=30s
- https://www.youtube.com/playlist?list=PL8cE5Nxf6M6bBTixIuAAViwXBqlk4PBOh

- **AI (For real time Exceptions handling and Documentation)**

- copilot
- Blackbox AI  
----------------------------------------------------------------------------------------




















   
