import requests
from datetime import  datetime
date='%02d-%02d-%d'%(datetime.now().year,datetime.now().month,datetime.now().day)
mDict={}
uids=[]
def t_StoN(s):
    #возвращает n минут
    s=s.split(':')
    return int(s[0])*60+int(s[1])
def t_NtoS(n):
    h='%02d'%(n//60)
    m='%02d'%(n%60)
    return h+':'+m

def dictContent():
    #заполнение mDict
    global mDict
    for uid in uids:
        #thread
        r=requests.get('https://api.rasp.yandex.net/v3.0/thread'+
                '/?apikey=233d0d70-8861-4944-92ff-19b34348c0c9&format=json'+
                '&uid='+uid)
        r=r.json()
        #составляем словарь {остановка=[[время,поезд,ст. назн-ия]]}
        stops=r['stops']
        train=r['transport_subtype']['title']
        duration=r['title']
        for stop in stops:
            station=stop['station']['title']
            time=(stop['arrival'] or stop['departure'])[-8:-3]
            if not (station in mDict):
                mDict[station]=[[time,train,duration]]
                continue
            mDict[station].append([time,train,duration])
    #сортировка полученного словаря
    for key in mDict:
        mDict[key]=sorted(mDict[key])



def allUid():
    #заполнение uids
    def uExt(r):
        global uids
        for sch in r.json()['schedule']:
            uid=sch['thread']['uid']
            if uid in uids: continue
            uids.append(uid)

    #finl dep
    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9602497&transport_types=suburban&event=departure'+
    '&direction=Выборгское направление&date=%s'%(date))
    uExt(r)

    #finl arr
    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9602497&transport_types=suburban&event=arrival'+
    '&direction=Выборгское направление&date=%s'%(date))
    uExt(r)

    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9602497&transport_types=suburban&event=arrival'+
    '&direction=Выборгское направление&offset=100&date=%s'%(date))
    uExt(r)

    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9602497&transport_types=suburban&event=arrival'+
    '&direction=Выборгское направление&offset=200&date=%s'%(date))
    uExt(r)
    #zel dep
    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9602725&transport_types=suburban&event=departure&date=%s'%(date))
    uExt(r)
    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9602725&transport_types=suburban&event=departure&offset=100&date=%s'%(date))
    uExt(r)
    #zel arr
    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9602725&transport_types=suburban&event=arrival&date=%s'%(date))
    uExt(r)
    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9602725&transport_types=suburban&event=arrival&offset=100&date=%s'%(date))
    uExt(r)
    #vbg arr
    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9603175&transport_types=suburban&event=arrival'+
    '&date=%s'%(date))
    uExt(r)
    #vbg dep
    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9603175&transport_types=suburban&event=departure'+
    '&date=%s'%(date))
    uExt(r)

allUid()
dictContent()
#file=open('C:/save/saveDict','rb')
#mDict=pickle.loads(pickle.load(file))
#file.close()


stKeys=('Выборг','Лазоревка','Верхне-Черкасово','117 км','Лебедевка',
     'Гаврилово','Лейпясуо','Кирилловское','Заходское','Каннельярви',
     '73 км (Шевелёво)','Горьковское','63 км','Рощино','Ушково',
     'Зеленогорск','Комарово','Репино','Солнечное','Белоостров',
     'Дибуны','Песочная','Левашово','Парголово','Шувалово',
     'Озерки','Удельная','Ланская','Санкт-Петербург (Финляндский вокзал)',
     'Санкт-Петербург (Ладожский вокзал)')
km=[131,124.2,120,117,114,107.8,100,88,81,75,73,65.7,
63,60,54.6,50,43.4,40,34.4,32,25.3,23.8,19.5,16,11,10,7.5,5,0]
def trains():


    def trSt(stops,mdict):

        for stop in stops:
            title=stop['station']['title']
            ta=stop['arrival']
            if ta:ta=ta[-8:-3]
            td=stop['departure']
            if td:td=td[-8:-3]
            if title in stKeys:
                mdict[title]=(ta,td)

    notes=[]
    #расписание по VBG
    r=requests.get('https://api.rasp.yandex.net/v3.0/schedule/'+
    '?apikey=233d0d70-8861-4944-92ff-19b34348c0c9'+
    '&station=s9603175&transport_types=train'+
    '&date=%s'%(date))
    r=r.json()
    uids=[]
    sch=r['schedule']
    for note in sch:
        uids.append(note['thread']['uid'])
    uids=tuple(set(uids))
    for uid in uids:
        r=requests.get('https://api.rasp.yandex.net/v3.0/thread'+
        '/?apikey=233d0d70-8861-4944-92ff-19b34348c0c9&format=json'+
        '&uid='+uid)
        r=r.json()
        title=r['title']
        mdict={}
        trSt(r['stops'],mdict)
        note=(title,mdict)
        if note in notes:continue
        notes.append(note)

    #{Stantion:(time,trans_type,thread_title,st_dep)}
    def trainHand(note):
        title=note[0]
        sch=note[1]
        stDep='Выборг'
        lastSt='Санкт-Петербург (Финляндский вокзал)'
        s=km[0]

        def f(stDep,lastSt,fl=0):
            #fl = flag intermediate stantion
            depI=stKeys.index(stDep)
            lastI=stKeys.index(lastSt)
            step=1
            if depI>lastI:step=-1
            if lastSt=='Санкт-Петербург (Ладожский вокзал)':lastI=stKeys.index('Ланская')
            order=range(depI,lastI-fl,step)
            s=km[depI]-km[lastI]
            if lastSt=='Санкт-Петербург (Ладожский вокзал)': s+=12
            timeList=[]
            timeList.append(t_StoN(sch[stDep][1]))
            t=abs(t_StoN(sch[stDep][1])-t_StoN(sch[lastSt][0]))
            k=round(t/s,2)
            mDict[stDep].append((sch[stDep][1],'Поезд',title,stDep))
            for i in order:
                s1=km[i]-km[i+step]
                t1=abs(round(k*s1))
                timeList.append(timeList[-1]+t1)
                mDict[stKeys[i+step]].append((t_NtoS(timeList[-1]),'Поезд',title,stDep))

        #все order на 1 меньше для for: i+1
        if title=='Петрозаводск — Москва':
            #разные скорости от Зеленогорска
            mDict['Выборг'].append((sch['Выборг'][0],'Поезд',title,'Хийтола'))
            lastSt='Зеленогорск'
            f(stDep,lastSt,1)
            stDep=lastSt
            lastSt='Белоостров'
            f(stDep,lastSt,1)
            stDep=lastSt
            lastSt='Санкт-Петербург (Ладожский вокзал)'
            f(stDep,lastSt)

        if title=='Москва — Петрозаводск':
            mDict['Выборг'].append((sch['Выборг'][1],'Поезд',title,'Выборг'))
            stDep=lastSt
            lastSt='Выборг'
            f(stDep,lastSt)
        if title=='Сортавала — Санкт-Петербург':
            mDict['Выборг'].append((sch['Выборг'][0],'Поезд',title,'Хийтола'))
            #t1=t_StoN(sch['Удельная'][1])
            #t2=t_StoN(sch[lastSt][0])
            #t3=t_NtoS(t1+round((t2-t1)/2))
            #mDict['Ланская'].append((t3,'Поезд',title,'Выборг'))
            #mDict[lastSt].append((sch[lastSt][0],'Поезд',title,'Выборг'))
            lastSt='Удельная'
            f(stDep,lastSt,fl=1)
            stDep=lastSt
            lastSt='Санкт-Петербург (Финляндский вокзал)'
            f(stDep,lastSt)
        if title=='Санкт-Петербург — Сортавала':
            mDict['Выборг'].append((sch['Выборг'][1],'Поезд',title,'Выборг'))
            stDep=lastSt
            lastSt='Выборг'
            f(stDep,lastSt)


    for note in notes:
        trainHand(note)
trains()

mList=[]
def listContent():
    global mList
    stKeys=('Выборг','Лазоревка','Верхне-Черкасово','117 км','Лебедевка',
     'Гаврилово','Лейпясуо','Кирилловское','Заходское','Каннельярви',
     '73 км (Шевелёво)','Горьковское','63 км','Рощино','Ушково',
     'Зеленогорск','Комарово','Репино','Солнечное','Белоостров',
     'Дибуны','Песочная','Левашово','Парголово','Шувалово',
     'Озерки','Удельная','Ланская','Санкт-Петербург (Финляндский вокзал)')
    for k in stKeys:
        l=[]
        for note in mDict[k]:
            title=None
            time=note[0]
            #time=int(note[0].split(':')[0])*100+int(note[0].split(':')[1])
            train=note[1]
            if train=='Пригородный поезд':train=1
            if train=='состав 2-3 вагона':train=1
            if train=='«Ласточка»':train=2
            if train=='Поезд':
                train=3
                stDep=note[3].split(' ')[0]
                title=note[2]
            else:stDep=note[2].split(' ')[0]
            if stDep=='Санкт-Петербург':stDep='С-Пб'
            l.append([time,train,stDep,title]) if title else l.append([time,train,stDep])
        l=sorted(l)
        mList.append(l)
listContent()
#############################################################################
####################HTML##########-=_JS_=-#################PYTHON############
#############################################################################


timeList=[]
for notes in mList:
    l=[note[0] for note in notes]
    l=[t_StoN(time) for time in l]
    timeList.append(l)
1

script='mList='+str(mList)+'\ntimeList='+str(timeList)
file=open(r'c:\Users\Iva\pit\lists.js','w');
file.write(script);
file.close()
scrDate='let footDate="'+date.replace('-','.')+'";'
script=scrDate+'''
let size=String(6*window.devicePixelRatio)+'mm';
document.querySelector('body').style.fontSize=size;
let date = new Date();
let time = date.getHours()*60+date.getMinutes();
let realTime=document.getElementById('realTime');
realTime.textContent=`${date.toTimeString()}`.slice(0,5);
let table=document.getElementById('table');
let selEl=document.getElementById('selEl');
selEl.addEventListener('change',gridTable);
let notifTime=8;
let selNum;
let i;
let l;
let trows;
let activeList;
function gridTable(){
    selNum=Number(selEl.value);
    table.innerHTML='';
    function tabCont(trainColor,stDep,stationTime,title){
        let tr=document.createElement('div');
        tr.className='tr '+trainColor;
        table.append(tr);
        let cell1=document.createElement('div');
        cell1.className='cell stDep ';
        cell1.textContent=stDep;
        let cell2=document.createElement('div');
        cell2.className='cell time ';
        cell2.textContent=stationTime;
        let cell3=document.createElement('div');
        cell3.className='cell title';
        cell3.textContent=title;
        let cell4=document.createElement('div');
        cell4.className='cell';
        tr.append(cell4,cell1,cell2,cell3);
        }
    for (n in mList[selNum]){
        let i=mList[selNum][n];

        let trainColor;
        switch(i[1]){
            case 1:
                trainColor='green';
                break;
            case 2:
                trainColor='red';
                break;
            case 3:
                trainColor='brown';
                break;
        }
        let stDep=i[2];
        let stationTime=i[0];
        let title='';
        if (i[1]==3){
            title=i[3];
        }
        tabCont(trainColor,stDep,stationTime,title);
    }
    let footer=document.createElement('div');
    footer.className='cell footer';
    footer.innerHTML=footDate+'<br>о найденных ошибках просьба писать на почту- naviantropos@gmail.com';
    table.append(footer);
    i;
    l=timeList[selNum];
    trows=document.getElementById('table').children;
    activeList=[];

    (()=>{
        for(i=0; i<l.length; i++){
                if(l[i]<time){
                    trows[i].classList.add('past');
                }else{
                    if(l[i]<=(time+notifTime)){
                            trows[i].classList.add('active');
                            activeList.push([l[i],i]);

                        }else if(activeList.length==0){
                            trows[i].classList.add('active');
                            activeList.push([l[i],i]);
                            i++
                            break;
                        }else{
                            break;
                        }
                }
            }
    })()
    if(i!=1){trows[i-2].children[0].textContent='через:';}
    if(i>3){
        trows[i-4].scrollIntoView();
    }
    (()=>{
    if(i>3){
    trows[i-4].scrollIntoView();
    }
    })();

}
gridTable();

function f(){
    date = new Date();
    time = date.getHours()*60+date.getMinutes();
//конец списка
    if(l[i+1]==undefined){
        console.log('конец списка');
        console.log(time);
        if(activeList[0][0]<time+soundTime){
           if (volumeFlag==true){
               audio.play();
           }
           }
        if (activeList[0][0]<time-2){
            trows[activeList[0][1]-1].children[0].textContent='';
            trows[activeList[0][1]].classList.remove('active');
            trows[activeList[0][1]].classList.add('past');
            trows[activeList[0][1]].children[0].textContent='через:';
            activeList.splice(0,1);
            if(activeList.length==0){
                clearTimeout(timerId);
                clearTimeout(timerId2);
                }
            }
        return;
    }
    if (activeList[0][0]<time-2){
        if(i>1){trows[activeList[0][1]-1].children[0].textContent='';}
        trows[activeList[0][1]].classList.remove('active');
        trows[activeList[0][1]].classList.add('past');
        trows[activeList[0][1]].children[0].textContent='через:';
        activeList.splice(0,1);
        if(activeList.length==0){
            activeList.push([l[i],i]);
            trows[i].classList.add('active');
            i++;
        }
    }
    if(l[i]<(time+notifTime)){
        activeList.push([l[i],i]);
        trows[i].classList.add('active');
        i++;
    }
}

f();


function timeRest(){
    let i=activeList[0][1];
    trows[i].children[0].innerHTML=
        timeDif(l[i],date.getHours(),date.getMinutes());
    if(i+1<=l.length){
       i++;
        trows[i].children[0].innerHTML=
            timeDif(l[i],date.getHours(),date.getMinutes());
        }
    if(i+2<=l.length){
       i++;
        trows[i].children[0].innerHTML=
            timeDif(l[i],date.getHours(),date.getMinutes());
        }
    }
timeRest()
function timeDif(h1m1,h2,m2){
    let sum1=h1m1
    let sum2=h2*60+m2;
    let h=Math.trunc((sum1-sum2)/60);
    let m=sum1-sum2-h*60;
    if(m<0){
        return " 0 мин"
    }
    if(h==0){
        if(m<10){
        m=`<b>0${m}</b>`;
        }
        return `<b>${m}</b>&nbspмин`
    }
    if(m<10){
        m=`<b>0${m}</b>`;
    }
    return `<b>${h}</b>ч <b>${m}</b>м`
}
function timeF(){
    date = new Date();
    realTime.textContent=`${date.toTimeString()}`.slice(0,5);
    timeRest();
}

let timerId=setInterval(timeF,1000);
let timerId2=setInterval(f,1000);
'''
stList=('Выборг','Лазоревка','Верхне-Черкасово','117км','Лебедевка',
 'Гаврилово','Лейпясуо','Кирилловское','Заходское','Каннельярви',
 '73км(Шевелёво)','Горьковское','63км','Рощино','Ушково','Зеленогорск',
 'Комарово','Репино','Солнечное','Белоостров','Дибуны','Песочная',
 'Левашово','Парголово','Шувалово','Озерки','Удельная','Ланская',
 'Финляндский вокзал')
select=''
for n,st in enumerate(stList):
    select+='<option value="'+str(n)+'">'+st+'</option>\n'
1
##------------------CSS------------------------------
style='''
<style>
    body{
        margin: 0px;
    }
    .red{
        color:red;
    }
    .red .stDep{
        font-weight: bold;
    }
    .green{
        color:green;
    }
    .brown{
        color: #B8860B;
    }
    .past{
        color:gray;
    }
    .active.red{
        background-color: red;
        border:1px solid red;
        color: white;
    }
    .active.green{
        background-color: green;
        border:1px solid green;
        color: white;
    }
    .active.brown{
        background-color: #B8860B;
        border:1px solid #B8860B;
        color: white;
    }
    ::-webkit-scrollbar {
      width: 0;
    }
    #realTime{
        font-size: 1.5em;
        font-weight: normal;
    }
    .wrapper {
       display: grid;
       grid-template-columns: 1fr;
    }
    .tr{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
    }
    .cell{
        display: flex;
        justify-content: center;
        align-items: center;
        padding-top: 20px;
        padding-bottom: 20px;
    }
    .header {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        position: sticky;
        position: -webkit-sticky;
        background-color: white;
        top: 0;
        border-bottom: 1px solid black;

    }
    #realTime{
        font-size: 1.5em;
        font-weight: normal;
    }
    .stDep{
        border-right: 1px solid black;
    }
    #stantion{
        grid-column-start: 3;
        grid-column-end: 5;
        justify-content: flex-start;
        padding-left: 7%;
    }
    select{
        font-size: 1em;
        border: 2px solid lightgray;
        width: 50%;
        border-radius: 5px;
    }
    .footer{
        font-size: 0.8em;
        border-top: 1px solid black;
        text-align: center;
    }
</style>
    '''
##------------------HTML-----------------------------
mS=['<!DOCTYPE html>','<html>',
    '<head>',
    '<title>Уведомления</title>',
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">',
    style,
    '</head>',
    '<body>',
    '<div class="header">',
    '<div class="cell" id="realTime"></div>',
    '<div class="cell stDep">от ст.</div>',
    '<div class="cell" id="stantion">на ст.',
    '<select id="selEl">',
    select,
    '</select>',
    '</div>',
    '</div>',
    '<div class="wrapper" id="table">',
    '</div>',
    '</body>',
    '<script src="lists.js"></script>',
    '<script>',
    script,
    '</script>',
    '</html>']

file=open(r'c:\Users\Iva\pit\oldRzdPage.html','w',encoding='utf-8')
for i in mS:
    file.write(i+'\n')

file.close()
