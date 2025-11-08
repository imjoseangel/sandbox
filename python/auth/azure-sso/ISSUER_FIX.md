# Azure AD Issuer Validation Fix

## Problem

Getting "Invalid token issuer" error during OAuth2 callback, even though authentication was successful.

### Root Cause

**Authority vs Issuer Mismatch**

When using `AZURE_AUTHORITY=common` (multi-tenant mode), there's a mismatch between:

- **Authorization URL**: Uses `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`
- **Token Issuer**: Azure AD issues tokens with tenant-specific issuer like `https://login.microsoftonline.com/{tenant-id}/v2.0`

The JWT validation was expecting:
```
Expected: https://login.microsoftonline.com/common/v2.0
Actual:   https://login.microsoftonline.com/b6674be2-2860-4fc4-8ef9-451cb064dd70/v2.0
```

This is **expected Azure AD behavior** - even when using `/common` endpoint, tokens are issued with the tenant-specific issuer for security reasons.

## Solution

Modified token validation to accept **both** issuers when using "common" authority:

```python
# For multi-tenant apps using "common", accept the tenant-specific issuer
expected_issuers = [expected_issuer]
if self.settings.azure_authority == "common":
    # Also accept tenant-specific issuer
    tenant_specific_issuer = f"https://login.microsoftonline.com/{tenant_id}/v2.0"
    expected_issuers.append(tenant_specific_issuer)

# Validate issuer manually
if actual_issuer not in expected_issuers:
    raise jwt.InvalidIssuerError(f"Invalid issuer: {actual_issuer}")
```

## Changes Made

### `/src/auth.py`
- ✅ Added logging import
- ✅ Added debug logging for issuer comparison
- ✅ Implemented multi-issuer validation for "common" authority
- ✅ Enhanced error message with actual vs expected issuer
- ✅ Manual issuer validation before JWT decode

## Alternative Solutions

### Option 1: Use Tenant-Specific Authority (Single-Tenant Apps)

If your app only serves users from ONE tenant, use the tenant ID as authority:

```bash
# In .env file
AZURE_AUTHORITY=b6674be2-2860-4fc4-8ef9-451cb064dd70
```

**Pros:**
- Simpler validation
- More secure (restricts to specific tenant)
- No issuer mismatch

**Cons:**
- Only works for single-tenant scenarios
- Can't authenticate users from other tenants

### Option 2: Keep "common" Authority (Multi-Tenant Apps)

Use the implemented solution to accept both issuers.

**Pros:**
- Supports multi-tenant scenarios
- Users from any tenant can authenticate
- Flexible

**Cons:**
- Slightly more complex validation logic

## Configuration Examples

### Single-Tenant App
```env
AZURE_AUTHORITY=b6674be2-2860-4fc4-8ef9-451cb064dd70
```

### Multi-Tenant App (Any Organization)
```env
AZURE_AUTHORITY=common
# or
AZURE_AUTHORITY=organizations
```

### Consumer Accounts (Microsoft personal accounts)
```env
AZURE_AUTHORITY=consumers
```

## Understanding Azure AD Authorities

| Authority       | Accepts                          | Use Case                               |
|-----------------|----------------------------------|----------------------------------------|
| `common`        | Work/school + personal accounts  | Multi-tenant apps accepting both types |
| `organizations` | Work/school accounts only        | Multi-tenant B2B apps                  |
| `consumers`     | Personal Microsoft accounts only | Consumer apps                          |
| `{tenant-id}`   | Specific tenant only             | Single-tenant apps                     |

## Testing

After the fix, the OAuth flow should complete successfully:

1. **Login initiated**: User redirected to Azure AD
2. **User authenticates**: Azure AD login page
3. **Callback received**: Code exchanged for tokens
4. **Token validated**: ✅ Issuer validation passes
5. **User info extracted**: Success!

## Debug Logs

You'll see these logs during token validation:

```
DEBUG: Token validation - Expected issuer: https://login.microsoftonline.com/common/v2.0
DEBUG: Token validation - Actual issuer: https://login.microsoftonline.com/b6674be2-2860-4fc4-8ef9-451cb064dd70/v2.0
DEBUG: Multi-tenant mode - Also accepting: https://login.microsoftonline.com/b6674be2-2860-4fc4-8ef9-451cb064dd70/v2.0
```

## Related Documentation

- [Azure AD v2.0 endpoints](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-protocols)
- [Multi-tenant apps](https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-convert-app-to-be-multi-tenant)
- [Token validation](https://learn.microsoft.com/en-us/azure/active-directory/develop/access-tokens#validate-tokens)

## Summary

**Status**: ✅ Fixed

The issuer validation now properly handles Azure AD's multi-tenant behavior, accepting both the "common" issuer and tenant-specific issuers when using multi-tenant authority.
