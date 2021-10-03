Remove-Alias -Name rm -Force

$Bash4PS_installDir="Bash4PowerShell"
Function Bash4PS_rm { python "$Bash4PS_installDir/rm.py" $PsBoundParameters.Values $args }

New-Alias -Name "rm" -Value Bash4PS_rm
