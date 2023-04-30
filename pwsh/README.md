# Azure AD Principal Expiration

## Context

There is 2 types of credentials that can be used for an Azure AD application: passwords (keys) and certificates. Both could (and should) have a realistic end date, and for the sake of good practices, they should not be configured to never end.

## Setup information

You'll need Azure Az PowerShell in order to use the script of this article.

Audit expiring soon Azure AD application credentials (keys/certificates) script from ScriptCenter

### Prepare for the audit

Open a PowerShell shell, log into Azure and position yourself on the desired subscription, here is an example on how to do so:

```powershell
Connect-AzAccount
```

### Perform a 120 days audit

```powershell
$audit = .\Get-AzADAppExpiringCredentials.ps1 -ExpiresInDays 120 -Verbose

Gathering necessary information...
VERBOSE: Fetching information for application ADAuditPlus Reporting
VERBOSE: Fetching information for application app registration
...
Validating expiration data...
Done.

#output the result as is
$audit

DisplayName   : ADAuditPlus Reporting
ObjectId      :
ApplicationId : 00000000-0000-0000-0000-000000000000
KeyId         : 00000000-0000-0000-0000-000000000000
Type          : Password
StartDate     : 4/9/2018 6:34:52 PM
EndDate       : 12/31/2299 5:00:00 AM
Status        : Valid

DisplayName   : ARM Test app
ObjectId      :
ApplicationId : 00000000-0000-0000-0000-000000000000
KeyId         : 00000000-0000-0000-0000-000000000000
Type          : Password
StartDate     : 2/12/2019 8:19:38 PM
EndDate       : 3/12/2019 8:19:38 PM
Status        : ExpiringSoon
```

### [Optional] Perform a grouped audit

```powershell
$audit | Group-Object -Property Status

# you'll end up with an output looking like this

Count Name                      Group
----- ----                      -----
   54 Expired                   {@{DisplayName=AutomationAccount_E+6heptOMzz8vX9ooTYFZq8DJYKweTDdIFrQmOo3BXs=; Objec...
   11 ExpiringSoon              {@{DisplayName=AutomationAccountQwerty_e1yHxjl45+GwXIxG/mwqMnARwn5i6C5zSMAAIxZyzw...
  173 Valid                     {@{DisplayName=ADAuditPlus Reporting; ObjectId=; ApplicationId=9db46068-49a0-45ae-b2...
```

### [Optional] Output the result as JSON and save it to disk for later use

```powershell
$audit | ConvertTo-Json -Depth 5 | Out-File .\audit.json

# you'll end up with a JSON file in this format

[
  {
    "DisplayName": "AutomationAccountQwerty_e1yHxjl45",
    "ObjectId": null,
    "ApplicationId": {
      "value": "00000000-0000-0000-0000-000000000000",
      "Guid": "00000000-0000-0000-0000-000000000000"
    },
    "KeyId": "00000000-0000-0000-0000-000000000000",
    "Type": "Password",
    "StartDate": {
      "value": "2016-05-11T14:55:30",
      "DateTime": "Wednesday, May 11, 2016 2:55:30 PM"
    },
    "EndDate": {
      "value": "2019-05-11T14:55:30",
      "DateTime": "Thursday, May 11, 2019 2:55:30 PM"
    },
    "Status": "ExpiringSoon"
  },
    ...
]
```

## Conclusion

If you want to be proactive and know in advance what application will have trouble because of expiring credentials, you now have another tool in your tool belt!
