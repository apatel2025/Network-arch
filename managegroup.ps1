Import-Module ActiveDirectory
$Groups=Get-ADGroup -LDAPFilter "(ManagedBy=$((Get-ADUser -Identity $env:USERNAME).distinguishedname))"
$Groups

$groupname=Read-Host -Prompt "Select a group from the above list" 
$username=Read-host -prompt "Choose a User account that you want to add to this group"

$grp_object = Get-ADGroup -Identity "$groupname" -ErrorAction stop
$usr_object = Get-ADUser -Identity "$username" 

Add-ADGroupMember -Identity $grp_object -Members $usr_object
write-host "$username : Successfully added to $groupname" -ForegroundColor Green