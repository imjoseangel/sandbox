import argparse
import asyncio
from fastmcp.server.auth.providers.jwt import JWTVerifier


# Configuration
# 1. Configure JWT verification for Azure Entra ID
# We need to handle both V1 and V2 tokens because Azure returns different versions depending on the client/scope.
async def main():
    parser = argparse.ArgumentParser(
        description="Verify a JWT token against Azure Entra ID"
    )
    parser.add_argument("--token", required=True, help="JWT token to verify")
    parser.add_argument(
        "--tenant-id",
        default="b6674be2-2860-4fc4-8ef9-451cb064dd70",
        help="Azure Entra ID tenant ID",
    )
    args = parser.parse_args()
    token_str = args.token
    tenant_id = args.tenant_id

    verifier_v2 = JWTVerifier(
        jwks_uri=f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys",
        issuer=f"https://login.microsoftonline.com/{tenant_id}/v2.0",
        audience=None,
    )
    verifier_v1 = JWTVerifier(
        jwks_uri=f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys",
        issuer=f"https://sts.windows.net/{tenant_id}/",
        audience=None,
    )

    print("Verifying token...")
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
            print("Type:   Application Service Principal")
            print(f"App ID: {claims.get('appid')}")
        elif id_type == "user":
            print("Type:   User")
            print(f"UPN:    {claims.get('upn') or claims.get('preferred_username')}")
            print(f"Name:   {claims.get('name')}")
        else:
            # Method B: Fallback heuristics
            if "upn" in claims or "unique_name" in claims:
                print("Type:   User (inferred)")
                print(f"UPN:    {claims.get('upn') or claims.get('unique_name')}")
            elif "appid" in claims:
                print("Type:   Application Service Principal (inferred)")
                print(f"App ID: {claims.get('appid')}")
            elif "roles" in claims and "scp" not in claims:
                # If it has app roles but no scopes, it's likely a service principal
                print("Type:   Application Service Principal (inferred from roles)")
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
