# Quick Start Guide

## 🚀 Get Up and Running in 5 Minutes

### Step 1: Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

### Step 2: Configure Azure AD (2 min)

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Azure Active Directory → App registrations → New registration**
3. Fill in:
   - **Name**: My SSO App
   - **Redirect URI**: `http://localhost:8000/api/v1/auth/callback`
4. After creation:
   - Copy **Application (client) ID**
   - Copy **Directory (tenant) ID**
   - Go to **Certificates & secrets** → New client secret → Copy value

### Step 3: Configure Environment (1 min)

Create `.env` file:

```bash
cat > .env << EOF
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_ID=your-client-id-here
AZURE_CLIENT_SECRET=your-client-secret-here
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
SESSION_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
EOF
```

### Step 4: Run the Application (1 min)

```bash
uvicorn src.main:app --reload
```

### Step 5: Test It! (<1 min)

1. Open browser: `http://localhost:8000/api/v1/docs`
2. Click on `/auth/login` endpoint
3. Click "Try it out" → "Execute"
4. You'll be redirected to Microsoft login
5. After login, you'll receive your tokens!

## ✅ Verification Checklist

- [ ] API docs accessible at http://localhost:8000/api/v1/docs
- [ ] Health check returns: http://localhost:8000/api/v1/auth/health
- [ ] Login redirects to Microsoft
- [ ] After authentication, callback receives tokens
- [ ] Can access protected endpoint with token

## 🎉 Next Steps

1. **Test Frontend**: Open `frontend/index.html` in browser
2. **Try Protected Routes**: Use Swagger UI to test with Bearer token
3. **Customize**: Edit `src/config.py` to adjust settings
4. **Deploy**: Follow production deployment guide in README

## 🆘 Common Issues

**"Application not found"**
→ Check `AZURE_CLIENT_ID` is correct

**"Redirect URI mismatch"**
→ Ensure Azure AD has: `http://localhost:8000/api/v1/auth/callback`

**"Invalid client secret"**
→ Client secret expired or incorrect, create a new one

---

**🎯 You're now ready to build with Azure AD SSO!**
