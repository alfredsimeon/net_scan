# 🚀 Push NET_SCAN to GitHub

## Prerequisites

Before pushing to GitHub, you need to install Git:

### Option 1: Install Git for Windows (Recommended)
1. Download from: https://git-scm.com/download/win
2. Run the installer and follow the default options
3. Restart PowerShell/Command Prompt after installation

### Option 2: Install via Chocolatey (if installed)
```powershell
choco install git
```

### Option 3: Install via Windows Package Manager
```powershell
winget install Git.Git
```

---

## Steps to Push to GitHub

### Step 1: Configure Git (First Time Only)

After installing Git, open PowerShell and configure your identity:

```powershell
git config --global user.name "Fred"
git config --global user.email "your-email@example.com"
```

### Step 2: Initialize Repository

Navigate to project and initialize git:

```powershell
cd "c:\Users\Fred\Desktop\Cybersecurity Projects\net-scan"
git init
```

### Step 3: Add All Files

```powershell
git add .
```

### Step 4: Create Initial Commit

```powershell
git commit -m "Initial commit: NET_SCAN v1.0.0 - Production-grade web vulnerability scanner"
```

### Step 5: Add Remote Repository

```powershell
git remote add origin https://github.com/alfredsimeon/net_scan.git
```

### Step 6: Push to GitHub

```powershell
git branch -M main
git push -u origin main
```

---

## Complete Script (Copy & Paste)

Once Git is installed, run this entire block:

```powershell
# Navigate to project
cd "c:\Users\Fred\Desktop\Cybersecurity Projects\net-scan"

# Initialize git
git init

# Configure git (first time only)
git config user.name "Fred"
git config user.email "your-email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: NET_SCAN v1.0.0 - Production-grade web vulnerability scanner"

# Add remote (replace with your actual repo URL if different)
git remote add origin https://github.com/alfredsimeon/net_scan.git

# Rename branch to main and push
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### "fatal: not a git repository"
- Make sure you're in the correct directory
- Run `git init` first

### "fatal: remote origin already exists"
- The remote was already added
- Run: `git remote remove origin` then re-add it

### "fatal: could not read Username for github.com"
- Use GitHub Personal Access Token instead of password
- Or use SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Authentication Issues

**Option A: Personal Access Token (Recommended)**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select "repo" scope
4. Copy the token
5. When prompted for password, paste the token instead

**Option B: SSH Keys**
1. Generate SSH key: `ssh-keygen -t ed25519 -C "your-email@example.com"`
2. Add to GitHub: https://github.com/settings/keys
3. Use SSH URL: `git remote add origin git@github.com:alfredsimeon/net_scan.git`

---

## After Push

Once pushed to GitHub:

✅ Visit: https://github.com/alfredsimeon/net_scan  
✅ Verify all 30 files are there  
✅ Check that README.md displays correctly  
✅ Star the repository! ⭐  

---

## GitHub Repository Setup (Optional)

Once on GitHub, consider adding:

1. **Description**: "Production-grade web vulnerability scanner - identifies SQLi, XSS, CSRF, command injection, XXE, SSRF, and path traversal vulnerabilities"

2. **Topics**: `vulnerability-scanner`, `web-security`, `penetration-testing`, `python`, `cybersecurity`

3. **README**: Already included

4. **License**: MIT (already included)

---

## Next Steps

1. Install Git
2. Run the push commands above
3. Verify on GitHub
4. Share the link!

---

**Your project will be live on GitHub! 🎉**

For detailed Git help: https://git-scm.com/doc
