# Session Storage Bug Fix

## Problem

The OAuth2 callback was failing with "Invalid or expired state parameter" even though the state was valid and the session timeout hadn't expired.

### Root Cause

**Critical Bug**: Each `SessionManager` instance was creating its own `InMemorySessionStore()`, resulting in isolated storage:

```python
# BEFORE (BROKEN)
class InMemorySessionStore:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}  # Instance-level storage
```

**Why this failed:**

1. `/login` endpoint: Creates `SessionManager(settings)` → new `InMemorySessionStore` → stores session in instance A
2. `/callback` endpoint: Creates new `SessionManager(settings)` → new `InMemorySessionStore` → looks in instance B (empty!)
3. Session not found → "Invalid or expired state parameter" error

## Solution

Changed `InMemorySessionStore` to use **class-level shared storage**:

```python
# AFTER (FIXED)
class InMemorySessionStore:
    _shared_store: Dict[str, Dict[str, Any]] = {}  # Class-level shared storage

    async def set(self, key: str, value: Dict[str, Any], expire: int) -> None:
        InMemorySessionStore._shared_store[key] = value

    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        return InMemorySessionStore._shared_store.get(key)
```

Now all instances share the same storage dictionary, making sessions persist across requests.

## Changes Made

### 1. `/src/session.py`

- ✅ Fixed `InMemorySessionStore` to use class-level `_shared_store`
- ✅ Added logging to track session storage/retrieval
- ✅ Added info log showing which storage backend is active
- ✅ Fixed session timestamp (was `timedelta(seconds=0)`, now uses `time.time()`)

### 2. `/src/routes.py`

- ✅ Enhanced error message with actionable guidance
- ✅ Added logging for session creation and retrieval
- ✅ Added `await session_manager.close()` after login redirect
- ✅ Added debug endpoint `/auth/session/check`

## Verification

Run the test to verify the fix:

```bash
cd /Users/imjoseangel/playground/imjoseangel/sandbox/python/auth/azure-sso
python test_session_fix.py
```

Expected output:

```txt
✓ Created session with state: i0eNOW5yx0wAW84M...
✓ Successfully retrieved session from different SessionManager instance
  - code_verifier: test_verifier
  - nonce: test_nonce

✅ TEST PASSED: Sessions persist across instances!
```

## Testing the OAuth Flow

1. **Start your server**:

   ```bash
   uvicorn src.main:app --reload
   ```

2. **Initiate login**:

   ```txt
   http://localhost:8000/auth/login
   ```

3. **Complete Azure AD authentication**

4. **Callback should now work** - session will be found and tokens exchanged

## Monitoring

Check logs for session activity:

```log
INFO: Using in-memory session storage (not recommended for production)
INFO: Created login session with state: gPR52gl2...
DEBUG: Stored session session:gPR52gl2... in memory. Total sessions: 1
DEBUG: Retrieved session session:gPR52gl2...: Found. Total sessions: 1
INFO: Retrieved session for state: gPR52gl2...
```

## Production Recommendation

For production, **use Redis** instead of in-memory storage:

```bash
# .env
REDIS_ENABLED=true
REDIS_URL=redis://localhost:6379/0
```

This ensures:

- ✅ Sessions persist across server restarts
- ✅ Horizontal scaling support (multiple server instances)
- ✅ Proper expiration handling
- ✅ Better performance

## Additional Improvements

1. **Better error messages** - Users now see why the error occurred
2. **Debug endpoint** - `/auth/session/check?state=XXX` for troubleshooting
3. **Comprehensive logging** - Track session lifecycle
4. **Proper cleanup** - `await session_manager.close()` to close Redis connections

## Summary

The bug was a **singleton pattern violation** in the in-memory session store. Each request created a new store instance, making cross-request session retrieval impossible. The fix uses a class-level shared dictionary, allowing all instances to access the same storage.

**Status**: ✅ Fixed and tested
