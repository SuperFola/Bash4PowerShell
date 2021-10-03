# Bash4PowerShell

Trying to mimic standard Bash functionalities, for PowerShell.

# Dependencies

* Python >= 3.9
* PowerShell >= 5.1

# Installing

```shell
$folder="C:\Users\$env:username\Documents\WindowsPowerShell"
git clone https://github.com/SuperFola/Bash4PowerShell.git $folder\Bash4PowerShell

$uri="https://raw.githubusercontent.com/SuperFola/Bash4PowerShell/master/PowerShell_profile.ps1"
$content=(Invoke-webrequest -URI $uri).Content

if(!(Test-Path -Path $profile)) {
    New-Item -Path $profile -ItemType "file" -Force
}
Add-Content -Path $profile -Value $content
```
