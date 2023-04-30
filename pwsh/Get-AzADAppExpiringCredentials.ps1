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
