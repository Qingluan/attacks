from qlib.net import to
from qlib.log import show, L
from qlib.asyn import Exe
from hashlib import sha1
from urllib.parse import urlencode
import demjson, os, json ,time
from qlib.data.sql import SqlEngine

ROOT = '/opt/attacks/cdn-test'
SQL_F = '%s/res_db' % ROOT

os.system('mkdir -p %s/cdn_cache' % ROOT)
os.system('mkdir -p %s/res_db' % ROOT)

def recv(url, resp):
    global STA
    content = resp.content
    sql_fi = '%s/res_db/%s.db' % (ROOT, url)
    db_init = SqlEngine(database=sql_fi)
    c = content.decode('utf8','ignore')
    o = demjson.decode(c)
    # path = ROOT+"/cdn_cache/" + url 
    # with open(path,'w') as fp:
    #     json.dump(o, fp)
    da=o['freshdata']
    if not da:
        STA[url] = 're-try'
        show("try - again")
        return
    for k in da:
        if not db_init.first('cdn', sid=k):
            db_init.insert('cdn', ['url','avgtime','srcip','srcname','isp','name','view'],
                url,
                da[k]['Avg'],
                da[k]['SrcIP']['srcip'],
                da[k]['SrcIP']['ipfrom'],
                da[k]['isp'],
                da[k]['name'],
                da[k]['view'],
            )


    STA[url] = False


def reqq(tar,req,url,data):
    return tar,req.post(url, data=data)

STA={
    
}

def bar():
    e = ['| ','\\','--','/ ']
    c = 0
    while 1:
        c+= 1
        yield e[c % 4]

def check(url):
    show(url, end='')
    global STA
    try:
        db_init = SqlEngine(database='%s/res_db/%s.db' % (ROOT, url))
        db_init.create('cdn',url=str, 
            sid=int,
            avgtime=str,
            srcip=str,
            srcname=str,
            isp=str,
            name=str,
            view=str,
            )
        
    except Exception as e:
        pass

    headers = {
        'origin':'https://www.17ce.com',
        'referer':'https://www.17ce.com/',
        'content-type':'application/x-www-form-urlencoded', 
    }
 
    req, res = to("www.17ce.com", cookie=True, agent=True)
    req.headers.update(headers)
    req.cookies.update({'allSites':url})
    verify = sha1(b'C^dLMi%r&JH7bkmdFCgGl8' + url.encode('utf8') + b"1TnvST&D9LJ").hexdigest()
    data = urlencode({
        'rt':'1',
        'nocache':'0',
        'url':url,
        'verify':verify,
        'host':'',
        'referer':'',
        'cookie':'',
        'agent':'',
        'speed':'',
        'postfield':'',
        'pingcount':'',
        'pingsize':'',
    })
    
    for i in range(4):
        data += '&' + urlencode({'area[]':i})

    for i in [0,1,2,4,6,7,8]:
        data +=  '&' +  urlencode({'isp[]':i})

    show(" init ", end='')
    res  = req.post("https://www.17ce.com/site/ping",data=data).content
    res = json.loads(res.decode('utf8','ignore'))
    L("  ok")
    time.sleep(1)
    # show(res)
    show("... from server getting data .. wait")
    e = Exe(3)
    d = urlencode({'tid':res['tid'],'num':0,'ajax_over':0})

    STA[url] = True
    e.done(reqq, recv, url,req,"https://www.17ce.com/site/ajaxfresh", d)
    b = bar()
    cc = 0
    while STA[url]:
        cc += 1
        time.sleep(1)
        show(next(b), end='\r')
        if STA[url] == 're-try':
            e.done(reqq, recv, url,req,"https://www.17ce.com/site/ajaxfresh", d)
            STA[url] = True


def shows(url, opt):
    show(url)
    if url+'.db' in os.listdir(SQL_F):
        ips = {}
        ip_g = {}
        s = SqlEngine(database=SQL_F + "/" + url + ".db")
        for r in s.select("cdn"):
            l = list(r[4:])
            l[0] = r[5]
            l[1] = r[4]
            if opt == 'd':
                L(*l,color='blue')
            if l[0] not in ips:
                ips[l[0]] = 1
            else:
                ips[l[0]] += 1
            if l[0] not in ip_g:
                ip_g[l[0]] = {l[2]}
            else:
                ip_g[l[0]].add(l[2])
        res = {i[1]:i[0] for i in ips.items()}
        L(res)
        for v in res.values():
            L(v,ip_g[v],color='green')


def list_ip(url):
    if not url+'.db' in os.listdir(SQL_F):
        return ''
    ips = {}
    ip_g = {}
    s = SqlEngine(database=SQL_F + "/" + url + ".db")
    for r in s.select("cdn"):
        l = list(r[4:])
        l[0] = r[5]
        l[1] = r[4]
        if l[0] not in ips:
            ips[l[0]] = 1
        else:
            ips[l[0]] += 1
        if l[0] not in ip_g:
            ip_g[l[0]] = {l[2]}
        else:
            ip_g[l[0]].add(l[2])

    if len(ip_g) > 4:
        show(url + '        ' + ' | '.join(list(ip_g)[:4])+ " ..." )
    else:
        show(url + '        ' + ' | '.join(list(ip_g)), tag=url)
