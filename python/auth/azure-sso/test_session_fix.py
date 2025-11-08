"""
Quick test to verify session storage persistence.
Run this to confirm the fix works.
"""

import asyncio
from src.session import SessionManager
from src.config import Settings


async def test_session_persistence():
    """Test that sessions persist across SessionManager instances."""

    # Create settings (will use in-memory storage)
    settings = Settings(
        azure_client_id="test",
        azure_client_secret="test",
        azure_tenant_id="test",
        redis_enabled=False,
    )

    # Create first SessionManager and store a session
    manager1 = SessionManager(settings)
    state1 = manager1.generate_state()
    await manager1.create_session(
        state=state1,
        code_verifier="test_verifier",
        nonce="test_nonce",
    )
    print(f"✓ Created session with state: {state1[:16]}...")
    await manager1.close()

    # Create second SessionManager and try to retrieve the session
    manager2 = SessionManager(settings)
    session_data = await manager2.get_session(state1)
    await manager2.close()

    if session_data:
        print(f"✓ Successfully retrieved session from different SessionManager instance")
        print(f"  - code_verifier: {session_data.get('code_verifier')}")
        print(f"  - nonce: {session_data.get('nonce')}")
        print("\n✅ TEST PASSED: Sessions persist across instances!")
        return True
    else:
        print("❌ TEST FAILED: Session not found in second instance")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_session_persistence())
    exit(0 if result else 1)
