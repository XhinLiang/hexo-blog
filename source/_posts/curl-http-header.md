title: cURL 如何获取 HTTP Header
date: 2017-12-29 12:36:29
tags: [Linux,cURL,工具]
categories: 工具
toc: true
---

> cURL 是一个常用的 HTTP Client，利用它我们可以发起 HTTP 请求，并获取我们想要的信息

#### `curl -I`
`curl -I` 事实上是发起了 HEAD 请求，理论上 HEAD 请求已经能满足我们的需求了，但是有的时候并不是这样...

对于一个腾讯云 FTN 上的二进制资源，如果我们对他发起 HEAD 请求，返回的 Content-Length 居然是 0，而且它加上了一个 Size 的 HTTP Header，这个 Size 事实上就是真正的 Content-Length
``` bash
[webroot@QQ bin]$ curl "http://examplehost.com/xxx.mp4" -I     
HTTP/1.1 200 OK
Server: Gfp-Http-Api/1.0
Ip: 10.57.76.157
Connection: close
Content-Length: 0
Last-Modified: Thu, 28 Dec 2017 02:51:05 GMT
Size: 28649157
Etag: "c87ed909d7af5b8c710e4a7b58800d47-1"
x-cos-content-sha1: c87ed909d7af5b8c710e4a7b58800d47-1
x-cos-object-type: multipart
Content-Type: video/mp4
```

也就是说， `curl -I` 发起请求拿到的响应 Header，跟我们实际上 GET 发起的请求拿到的 Header 并不一致。
如果我们想拿到 HTTP GET 的时候拿到的 HTTP Header，怎么操作呢？

#### `curl -vvv`
很多 UNIX 的命令行工具，都提供一个叫 `-vvv` 的命令行参数，这个参数一般会把操作日志都打印出来，这个时候我们可以试用一下 `-vvv` 参数。
``` bash
-bash-4.1$ curl baidu.com -vvv
* About to connect() to baidu.com port 80 (#0)
*   Trying 220.181.57.217... connected
* Connected to baidu.com (220.181.57.217) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.13.1.0 zlib/1.2.3 libidn/1.18 libssh2/1.2.2
> Host: baidu.com
> Accept: */*
> 
< HTTP/1.1 200 OK
< Date: Fri, 29 Dec 2017 05:45:55 GMT
< Server: Apache
< Last-Modified: Tue, 12 Jan 2010 13:48:00 GMT
< ETag: "51-47cf7e6ee8400"
< Accept-Ranges: bytes
< Content-Length: 81
< Cache-Control: max-age=86400
< Expires: Sat, 30 Dec 2017 05:45:55 GMT
< Connection: Keep-Alive
< Content-Type: text/html
< 
<html>
<meta http-equiv="refresh" content="0;url=http://www.baidu.com/">
</html>
* Connection #0 to host baidu.com left intact
* Closing connection #0
```

可以看到，请求头，响应头都有了，完美。
但是，有的时候，HTTP Body 过大导致我们获取不到我们想要的信息。
例如 
``` bash
[webroot@QQ bin]$ curl http://xxxxx.mp4 -vvv
* About to connect() to skyuploadpublic-30038.sz.gfp.tencent-cloud.com port 80 (#0)
*   Trying 58.250.136.37... connected
* Connected to skyuploadpublic-30038.sz.gfp.tencent-cloud.com (58.250.136.37) port 80 (#0)
> GET /20171228/skynet_1018.mp4 HTTP/1.1
> User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.13.1.0 zlib/1.2.3 libidn/1.18 libssh2/1.2.2
> Host: skyuploadpublic-30038.sz.gfp.tencent-cloud.com
> Accept: */*
> 
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0< HTTP/1.1 200 OK
< Ip: 100.66.11.90
< x-cos-storage-class: STANDARD_IA
< Content-Type: video/mp4
< Content-Disposition: attachment; filename*="UTF-8''skynet_1018.mp4"
< Content-Language: zh-CN
< ETag: "c87ed909d7af5b8c710e4a7b58800d47-1"
< x-cos-object-type: normal
< Accept-Ranges: bytes
< Last-Modified: Thu, 28 Dec 2017 02:51:03 GMT
< x-cos-cache: true
< Content-Length: 28649157
< 
{ [data not shown]
 ftypisomisomiso2avc1mp4free²űmdat¼ÿÿ¸ۅ龦؈·,֠ף﮸264 - core 152 r19 ba24899 - H.264/MPEG-4 AVC codec - Copyleft 2003-2017 - http://www.videolan.org/x264.html - options: cabac=1 ref=3 deblock=1:0:0 analyse=0x3:0x113 me=hex subme=7 psy=1 psy_rd=1.00:0.00 mixed_ref=1 me_range=16 chroma_me=1 trellis=1 8x8dct=1 cqm=0 deadzone=21,11 fast_pskip=1 chroma_qp_offset=-2 threads=8 lookahead_threads=1 sliced_threads=0 nr=0 decimate=1 interlaced=0 bluray_compat=0 constrained_intra=0 bframes=3 b_pyramid=2 b_adapt=1 b_bias=0 direct=1 weightb=1 open_gop=0 Nx3@±¶ٳE@ÿvʮ񡉚h¿󛣍@V²M̼@md~gą%qeG¬zԄ5 scenecut=40 intra_refresh=0 rc_lookahead=40 rc=abr mbtree=1 bitrate=1500 ratetol=1.0 qcomp=0.60 qpmin=0 qpmax=69 qpstep=4 ip_ratio=1.40 aq=1:1.00i+eÿþ򨝂^aª䖅%ڏÿ«gp|灃羰rR|׳󿣀 
¨
 퇂񫶢*񥭏bSs¯ް<h!*脙!£
^1oSI§+CM|M¦kAZqa!ر*丠$º¾1YނԔ𦙠Mxu䍤'լ񶵠ƴþȦ񘼙3ｵþ] ! xEk׸⭐썕㋦񹖕j¬½b
;¹򓔚Qk¤e¬/QWþ·v²=ҡ1ÿR'8#W,ª                                                                        
```

好吧，grep 一下不就行了！

``` bash
[webroot@QQ bin]$ curl http://skyuploadpublic-30038.sz.gfp.tencent-cloud.com/20171228/skynet_1018.mp4 -vvv | grep '>'
* About to connect() to skyuploadpublic-30038.sz.gfp.tencent-cloud.com port 80 (#0)
*   Trying 58.251.82.174... connected
* Connected to skyuploadpublic-30038.sz.gfp.tencent-cloud.com (58.251.82.174) port 80 (#0)
> GET /20171228/skynet_1018.mp4 HTTP/1.1
> User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.13.1.0 zlib/1.2.3 libidn/1.18 libssh2/1.2.2
> Host: skyuploadpublic-30038.sz.gfp.tencent-cloud.com
> Accept: */*
> 
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0< HTTP/1.1 200 OK
< Ip: 100.107.28.154
< x-cos-storage-class: STANDARD_IA
< Content-Type: video/mp4
< Content-Disposition: attachment; filename*="UTF-8''skynet_1018.mp4"
< Content-Language: zh-CN
< ETag: "c87ed909d7af5b8c710e4a7b58800d47-1"
< x-cos-object-type: normal
< Accept-Ranges: bytes
< Last-Modified: Thu, 28 Dec 2017 02:51:03 GMT
< x-cos-cache: true
< Content-Length: 28649157
< 
{ [data not shown]
Binary file (standard input) matches
* Failed writing body (1592 != 4320)
  0 27.3M    0 10920    0     0  43975      0  0:10:51 --:--:--  0:10:51 61348* Closing connection #0

curl: (23) Failed writing body (1592 != 4320)

```

完美！
