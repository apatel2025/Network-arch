Import-Module ActiveDirectory
$users=Import-Csv -Path C:\scripts\users.csv

ForEach ($dude in $users) 
{

$username=$dude.FirstName+$dude.LastName
$domain='@aditya.local'
$upn=$username+$domain
$password=$dude.InitialPassword
$displayname=$dude.FirstName+" "+$dude.LastName

    $Parameters = @{
    'GivenName' = $dude.FirstName
    'Surname' = $dude.LastName
    'Name' = $displayname
    'SamAccountName' = $username
    'AccountPassword' = $password
    'UserPrincipalName' = $upn
    'Department'=$dude.Department
    'Description'=$dude.Notes
    
    }

New-ADUser @Parameters
Add-ADGroupMember -Identity "CN=Head Office Users, OU=Head Office, DC=Aditya, DC=local" -Members $username
}


