<#
.SYNOPSIS
    This is a script to export Azure Firewall rules

.DESCRIPTION
    This is a script to export Azure Firewall rules.

.PARAMETER FirewallName
    Specified the Azure firewall name.

.NOTES
    Name: Export-AzFirewallRule.ps1
    Author: imjoseangel
    Created: 06/05/2023
    Version: 1.0 //imjoseangel -- 06/05/2023
        Initial Build

.EXAMPLE
    .\Export-AzFirewallRule.ps1

Description
-----------
Export Firewall Rules.

.EXAMPLE
    .\Export-AzFirewallRule.ps1 FirewallName "myazfw"

Description
-----------
Export Firewall Rules.
#>
[cmdletbinding()]
Param (
    [parameter()]
    [datetime]$FirewallName = 'myazfw',
    [parameter()]
    [string]$ResourceGroup = 'myrsg',
    [parameter()]
    [string]$BackupFileName = 'myazfw-export.csv'
)

# Authenticate to Azure
Connect-AzAccount

# Get Firewall
$Firewall = Get-AzFirewall -Name $FirewallName -ResourceGroupName $ResourceGroup

# Backup Firewall Configuration

$RuleCollections = Get-AzFirewallNetworkRuleCollection -Firewall $Firewall
$NetworkRules = Get-AzFirewallNetworkRule -Firewall $Firewall
$AppRules = Get-AzFirewallApplicationRule -Firewall $Firewall

$FirewallConfig = @{
    Firewall         = $Firewall
    RuleCollections  = $RuleCollections
    NetworkRules     = $NetworkRules
    ApplicationRules = $AppRules
}

$BackupFilePath = Join-Path -Path . -ChildPath $BackupFileName $FirewallConfig | Export-Clixml -Path $BackupFilePath

Write-Host "Azure Firewall configuration backup saved to: $BackupFilePath"
