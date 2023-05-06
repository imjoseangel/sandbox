<#
.SYNOPSIS
    This is a script to find expiring credentials for Applications in Azure

.DESCRIPTION
    This is a script to find expiring credentials for Applications in Azure.

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

[CmdletBinding()]
param(
    [Parameter(HelpMessage = 'Will output credentials if withing this number of days, use 0 to report only expired and valid as of today')]
    $ExpiresInDays = 90
)

Write-Host 'Gathering necessary information...'
$applications = Get-AzADApplication

$appWithCredentials = @()
$appWithCredentials += $applications | Sort-Object -Property DisplayName | ForEach-Object {
    $application = $_
    Write-Verbose ('Fetching information for application {0}' -f $application.DisplayName)
    $application | Get-AzADAppCredential -ErrorAction SilentlyContinue | Select-Object -Property @{Name = 'DisplayName'; Expression = { $application.DisplayName } }, @{Name = 'ObjectId'; Expression = { $application.Id } }, @{Name = 'ApplicationId'; Expression = { $application.AppId } }, @{Name = 'KeyId'; Expression = { $application.PasswordCredentials.KeyId } }, @{Name = 'StartDate'; Expression = { $application.PasswordCredentials.startDateTime -as [datetime] } }, @{Name = 'EndDate'; Expression = { $application.PasswordCredentials.endDateTime -as [datetime] } }
}

Write-Host 'Validating expiration data...'
$today = (Get-Date).ToUniversalTime()
$limitDate = $today.AddDays($ExpiresInDays)
$appWithCredentials | Sort-Object EndDate | ForEach-Object {
    if ($_.EndDate -lt $today) {
        $_ | Add-Member -MemberType NoteProperty -Name 'Status' -Value 'Expired'
    }
    elseif ($_.EndDate -le $limitDate) {
        $_ | Add-Member -MemberType NoteProperty -Name 'Status' -Value 'ExpiringSoon'
    }
    else {
        $_ | Add-Member -MemberType NoteProperty -Name 'Status' -Value 'Valid'
    }
}

$appWithCredentials
Write-Host 'Done.'
