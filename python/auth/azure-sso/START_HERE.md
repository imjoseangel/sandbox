# 🚀 Getting Started - Choose Your Path

## 👨‍💻 I Want to...

### 🏃 Get Running Quickly (5 minutes)
→ **[QUICKSTART.md](QUICKSTART.md)** - Minimal setup to see it working

### 📖 Understand the Architecture
→ **[ARCHITECTURE.md](ARCHITECTURE.md)** - Deep dive into design decisions

### 🚢 Deploy to Production
→ **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment strategies

### 🎯 See What's Included
→ **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete feature overview

### 📚 Full Documentation
→ **[README.md](README.md)** - Comprehensive guide with all details

---

## ⚡ Super Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure (add your Azure AD credentials)
cp .env.example .env

# 3. Run
uvicorn src.main:app --reload

# 4. Open
# API Docs: http://localhost:8000/api/v1/docs
# Frontend: frontend/index.html
```

## 🎓 Key Concepts

### What is SSO?
Single Sign-On allows users to authenticate once with Microsoft (Azure AD) and access multiple applications without re-entering credentials.

### Why This Solution?
- ✅ **Production-Ready**: Used in enterprise environments
- ✅ **Secure**: Implements OAuth 2.0 best practices (PKCE, JWT validation)
- ✅ **Scalable**: Supports multiple instances with Redis
- ✅ **Flexible**: Multi-tenant, RBAC, customizable

### Common Use Cases
1. **Enterprise Applications**: Employee authentication via company Azure AD
2. **SaaS Products**: Allow customers to use their Microsoft accounts
3. **Internal Tools**: Secure access to admin panels, dashboards
4. **Multi-Tenant Apps**: Support multiple organizations
5. **Mobile/Web Apps**: Unified authentication across platforms

## 📞 Need Help?

### Common Questions

**Q: Do I need an Azure subscription?**
A: Yes, but the free tier is sufficient for development.

**Q: Can I use this with personal Microsoft accounts?**
A: Yes! Set `AZURE_AUTHORITY=common` in .env

**Q: How do I test without Azure AD?**
A: Use the included tests with mocked responses.

**Q: Can this work with other identity providers?**
A: This is specific to Azure AD, but the pattern can be adapted.

### Still Stuck?

1. Check the troubleshooting section in [README.md](README.md)
2. Review example in [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. Examine the test files for usage examples

---

**🎯 Ready? Start with [QUICKSTART.md](QUICKSTART.md)!**
