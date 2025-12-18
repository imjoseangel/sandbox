import asyncio
import os
from fastmcp.server.auth.providers.jwt import JWTVerifier

# Configuration
TENANT_ID = "b6674be2-2860-4fc4-8ef9-451cb064dd70"
# CLIENT_ID = "your-client-id"

# 1. Configure JWT verification for Azure Entra ID
# We need to handle both V1 and V2 tokens because Azure returns different versions depending on the client/scope.
ISSUER_V2 = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
ISSUER_V1 = f"https://sts.windows.net/{TENANT_ID}/"

verifier_v2 = JWTVerifier(
    jwks_uri=f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys",
    issuer=ISSUER_V2,
    audience=None
)

verifier_v1 = JWTVerifier(
    jwks_uri=f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys",
    issuer=ISSUER_V1,
    audience=None
)

async def main():
    # Paste your token here for testing
    token_str = "YOUR_JWT_TOKEN_HERE"

    if token_str == "YOUR_JWT_TOKEN_HERE":
        print("⚠️  Please replace 'YOUR_JWT_TOKEN_HERE' with a real token to test.")
        return

    print(f"Verifying token...")
    try:
        # 2. Verify the token directly using the verifier
        # Try V2 first
        access_token = await verifier_v2.verify_token(token_str)

        if not access_token:
            print("⚠️  V2 Verification failed, trying V1 issuer...")
            access_token = await verifier_v1.verify_token(token_str)

        if not access_token:
            print("❌ Verification failed: Invalid token (verify_token returned None)")
            return

        claims = access_token.claims
        print("\n✅ Token Verified Successfully!")

        # 3. Check claims to distinguish identity
        print("\n--- Identity Analysis ---")

        # Method A: Check 'idtyp' claim
        id_type = claims.get("idtyp")

        if id_type == "app":
            print(f"Type:   Application Service Principal")
            print(f"App ID: {claims.get('appid')}")
        elif id_type == "user":
            print(f"Type:   User")
            print(f"UPN:    {claims.get('upn') or claims.get('preferred_username')}")
            print(f"Name:   {claims.get('name')}")
        else:
            # Method B: Fallback heuristics
            if "upn" in claims or "unique_name" in claims:
                 print(f"Type:   User (inferred)")
                 print(f"UPN:    {claims.get('upn') or claims.get('unique_name')}")
            elif "appid" in claims:
                print(f"Type:   Application Service Principal (inferred)")
                print(f"App ID: {claims.get('appid')}")
            elif "roles" in claims and "scp" not in claims:
                 # If it has app roles but no scopes, it's likely a service principal
                 print(f"Type:   Application Service Principal (inferred from roles)")
                 print(f"App ID: {claims.get('azp') or claims.get('aud')}")
                 print(f"Roles:  {claims.get('roles')}")
            else:
                print("Type:   Unknown Identity Type")

        print("\n--- Full Claims ---")
        for k, v in claims.items():
            print(f"{k}: {v}")

    except Exception as e:
        print(f"❌ Error verifying identity: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
