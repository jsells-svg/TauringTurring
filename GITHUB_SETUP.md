# GitHub Setup Instructions

Your local git repository is ready with all files committed! Follow these steps to push to GitHub.

## Step 1: Create a Repository on GitHub

1. Go to https://github.com/new
2. Enter repository name: `turing-interactive` (or your preferred name)
3. Add description: "Interactive executable for exploring Alan Turing's life and legacy"
4. Choose visibility: **Public** (to share easily) or **Private** (for personal use)
5. Click "Create repository"

## Step 2: Add Remote and Push (Copy-paste the commands)

After creating the repository, GitHub will show you commands to push an existing repository. They'll look similar to these (replace `YOUR_USERNAME` with your GitHub username):

### Option A: HTTPS (Easier if you don't have SSH set up)

```powershell
cd c:\ModelAMDRocM\tauringturring
& "C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/YOUR_USERNAME/turing-interactive.git
& "C:\Program Files\Git\cmd\git.exe" branch -M main
& "C:\Program Files\Git\cmd\git.exe" push -u origin main
```

You'll be prompted to enter your GitHub username and a **personal access token** (not your password):
- Go to https://github.com/settings/tokens
- Click "Generate new token" (Classic)
- Give it `repo` access
- Copy and paste it when prompted

### Option B: SSH (More secure, requires setup)

First, set up SSH keys (one-time setup):
```powershell
& "C:\Program Files\Git\cmd\git.exe" config --global user.name "YOUR_NAME"
& "C:\Program Files\Git\cmd\git.exe" config --global user.email "YOUR_EMAIL@example.com"
```

Then generate SSH key:
```powershell
ssh-keygen -t ed25519 -C "YOUR_EMAIL@example.com"
```

Add the public key to GitHub: https://github.com/settings/keys

Then push:
```powershell
cd c:\ModelAMDRocM\tauringturring
& "C:\Program Files\Git\cmd\git.exe" remote add origin git@github.com:YOUR_USERNAME/turing-interactive.git
& "C:\Program Files\Git\cmd\git.exe" branch -M main
& "C:\Program Files\Git\cmd\git.exe" push -u origin main
```

## Step 3: Verify

After pushing, verify on GitHub by visiting:
```
https://github.com/YOUR_USERNAME/turing-interactive
```

You should see all your files, commits, and documentation!

## Step 4: Share the Repository

Once on GitHub, you can:
- Share the link with others
- Enable GitHub Pages for documentation
- Set up continuous integration
- Invite collaborators

---

## Current Git Status

```
Repository: Initialized ✓
Branch: master
Commits: 1 (Initial commit)
Files: 27
Remote: Not yet configured
```

## Quick Reference: Common Git Commands

After setup, use these commands to keep the repository updated:

```powershell
# View status
& "C:\Program Files\Git\cmd\git.exe" status

# Add and commit changes
& "C:\Program Files\Git\cmd\git.exe" add .
& "C:\Program Files\Git\cmd\git.exe" commit -m "Your commit message"

# Push to GitHub
& "C:\Program Files\Git\cmd\git.exe" push

# View commits
& "C:\Program Files\Git\cmd\git.exe" log --oneline

# Create a new branch
& "C:\Program Files\Git\cmd\git.exe" checkout -b feature-name

# Switch branches
& "C:\Program Files\Git\cmd\git.exe" checkout main
```

---

**Ready to push? Follow the steps above!**
