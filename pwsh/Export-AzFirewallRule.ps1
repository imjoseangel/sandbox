<#
.SYNOPSIS
    This is a script to export Azure Firewall rules

.DESCRIPTION
     This is a script to export Azure Firewall rules.

    Key Input Tips:
    r: Toggles the resize mode of the clock so you can adjust the size.
    o: Toggles whether the countdown remains on top of windows or not.
    +: Increases the opacity of the clock so it is less transparent.
    -: Decreases the opacity of the clock so it appears more transparent.

    Right-Click to close.
    Use left mouse button to drag clock.

.PARAMETER ExpiresInDays
    Specified time in days for the secret to expire.

.NOTES
    Name: Get-AzADAppExpiringCredentials.ps1
    Author: imjoseangel
    Created: 05/05/2023
    Version: 1.0 //imjoseangel -- 05/05/2023
        Initial Build

.EXAMPLE
    .\Get-AzADAppExpiringCredentials.ps1

Description
-----------
Review Azure Secrets for Applications

.EXAMPLE
    .\Get-AzADAppExpiringCredentials.ps1 ExpiresInDays 30

Description
-----------
Review secrets expiring in 30 days.
#>
