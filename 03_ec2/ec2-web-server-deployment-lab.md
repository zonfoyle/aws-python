# EC2 Web Server Lab

## Goal
Launch an EC2 instance and host a public web server using Apache.

---

## Architecture

Internet
↓
Security Group (Ports 22, 80)
↓
EC2 Instance (Amazon Linux 2023)
↓
Apache Web Server
↓
Public Website

---

## Instance Configuration

AMI: Amazon Linux 2023  
Instance Type: t3.micro  
Public IP: Enabled  
Security Group:
- SSH (22)
- HTTP (80)

---

## Steps

### 1. Launch EC2 Instance

Create an EC2 instance using the AWS console.

Settings used:

- Amazon Linux 2023
- t3.micro
- Security group allowing:
  - SSH (22)
  - HTTP (80)
- Public IP enabled

---

### 2. Connect to Instance

From local machine:

```bash
ssh -i ec2-practice-key.pem ec2-user@PUBLIC_IP
```

---

### 3. Install Apache Web Server

```bash
sudo dnf update -y
sudo dnf install httpd -y
```

---

### 4. Start Apache

```bash
sudo systemctl start httpd
sudo systemctl enable httpd
```

---

### 5. Verify Server

Open browser:

```
http://PUBLIC_IP
```

You should see the Apache default page.

---

## Concepts Learned

- EC2 instance deployment
- SSH access to cloud servers
- Security groups as firewalls
- Linux package management
- Running a web server on AWS