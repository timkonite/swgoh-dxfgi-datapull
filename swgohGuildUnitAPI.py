import requests
import datetime

print('Start Guild Units')

###CHARACTER LOOKUP###
d = requests.get('https://swgoh.gg/api/characters/')
charout = d.text

e = open('swgohCharAPI.txt','w')
e.write(charout)
e.close()

f = open('swgohCharAPI.txt','r')
charfile = str(f.readlines())
f.close()

charfilepos = 0
charmatrix = []
charfileend = 0

while charfileend == 0:
    char = []
    
    charstart = charfile.find('"name"',charfilepos) + 8
    charend = charfile.find('","base_id',charfilepos)
    charname = charfile[charstart:charend]
    charname = charname.replace('\\','')
    charname = charname.replace('u00ce','Î')
    

    charfilepos = charend

    charcodestart = charfile.find('"base_id"',charfilepos) + 11
    charcodeend = charfile.find('","pk',charfilepos)
    charcode = charfile[charcodestart:charcodeend]

    charfilepos = charcodeend

    char.append(charname)
    char.append(charcode)

    charmatrix.append(char)

    if charfile[charfile.find('combat_type',charfilepos)+14:charfile.find('combat_type',charfilepos)+16] == '}]':
        charfileend = 1


###SHIP LOOKUPS###
g = requests.get('https://swgoh.gg/api/ships/')
shipout = g.text

h = open('swgohShipAPI.txt','w')
h.write(shipout)
h.close()

k = open('swgohShipAPI.txt','r')
shipfile = str(k.readlines())
k.close()

shipfilepos = 0
shipmatrix = []
shipfileend = 0

while shipfileend == 0:
    ship = []
    
    shipstart = shipfile.find('"name"',shipfilepos) + 8
    shipend = shipfile.find('","base_id',shipfilepos)
    shipname = shipfile[shipstart:shipend]
    shipname = shipname.replace('\\','')
    shipname = shipname.replace('u00ce','Î')
    

    shipfilepos = shipend

    shipcodestart = shipfile.find('"base_id"',shipfilepos) + 11
    shipcodeend = shipfile.find('","url',shipfilepos)
    shipcode = shipfile[shipcodestart:shipcodeend]

    shipfilepos = shipcodeend

    ship.append(shipname)
    ship.append(shipcode)

    shipmatrix.append(ship)

    if shipfile[shipfile.find('combat_type',shipfilepos)+14:shipfile.find('combat_type',shipfilepos)+16] == '}]':
        shipfileend = 1



###UNIT DATA###
guildcycle = 0
guildmatrix = []
now = datetime.datetime.now()
currdate = '{}/{}/{}'.format(now.month,now.day,now.year)

while guildcycle < 2:
    if guildcycle == 0:
        guild = 'Degeneration X'
        guildid = 12262
        guildcode = 'DX'
    elif guildcycle == 1:
        guild = 'Firmly Grasp It'
        guildid = 8233
        guildcode = 'FGI'
    else:
        guild = 'ERROR'
        guildid = 0
        guildcode = 'ERR'
    
    a = requests.get('https://swgoh.gg/api/guilds/{}/units/'.format(guildid))
    unitout = a.text

    b = open('swgohGuildUnitAPI{}.txt'.format(guildcode),'w')
    b.write(unitout)
    b.close()

    c = open('swgohGuildUnitAPI{}.txt'.format(guildcode),'r')
    txtfile = str(c.readlines())
    c.close()

    startpos = 0
    unittype = 'ERR'

    while txtfile[startpos+1:startpos+4] != '}]}':

        if (startpos == 0) or (txtfile[startpos+1:startpos+3] == '}]'):
            index = txtfile.find('[{', startpos)-3
            unitstart = txtfile.rfind('"',0,index) + 1
            unitend = txtfile.find('":',index)
            unitcode = txtfile[unitstart:unitend]

            startpos = unitend

            if txtfile[unitend+5:unitend+15] == 'gear_level':
                unittype = 'Character'

                for charlookup in charmatrix:
                    if charlookup[1] == unitcode:
                        unitname = charlookup[0]
                        break;
            elif txtfile[unitend+5:unitend+11] == 'player':
                unittype = 'Ship'
                for shiplookup in shipmatrix:
                    if shiplookup[1] == unitcode:
                        unitname = shiplookup[0]
                        break;
            else:
                unittype = 'Error'
                unitname = unitcode

        if unittype == 'Character':
            gearstart = txtfile.find('gear_level',startpos) + 12
            gearend = txtfile.find(',"power',gearstart)
            gearnum = int(txtfile[gearstart:gearend])
            if gearnum == 1:
                gearlevel = 'I'
            elif gearnum == 2:
                gearlevel = 'II'
            elif gearnum == 3:
                gearlevel = 'III'
            elif gearnum == 4:
                gearlevel = 'IV'
            elif gearnum == 5:
                gearlevel = 'V'
            elif gearnum == 6:
                gearlevel = 'VI'
            elif gearnum == 7:
                gearlevel = 'VII'
            elif gearnum == 8:
                gearlevel = 'VIII'
            elif gearnum == 9:
                gearlevel = 'IX'
            elif gearnum == 10:
                gearlevel = 'X'
            elif gearnum == 11:
                gearlevel = 'XI'
            elif gearnum == 12:
                gearlevel = 'XII'
            else:
                gearlevel = ''

            startpos = gearend

            powstart = startpos + 9
            powend = txtfile.find(',"level',powstart)
            powlevel = int(txtfile[powstart:powend])

            startpos = powend

            levstart = startpos + 9
            levend = txtfile.find(',"url',levstart)
            lev = int(txtfile[levstart:levend])

            startpos = levend

            combstart = txtfile.find('"combat',startpos) + 14
            combend = txtfile.find(',"rarity',combstart)
            combattype = txtfile[combstart:combend]

            startpos = combend

            rarstart = startpos + 10
            rarend = txtfile.find(',"player',rarstart)
            raritylevel = int(txtfile[rarstart:rarend])

            startpos = rarend

            playstart = startpos + 11
            playend = txtfile.find('"}',playstart)
            playername = txtfile[playstart:playend]
            playername = playername.replace('u0117', 'e')
            playername = playername.replace('\\','')
            playername = playername.replace('u00f3', 'o')
            playername = playername.replace('u039e', 'E')

            startpos = playend

        elif unittype == 'Ship':
            playstart = startpos + 14
            playend = txtfile.find('","rarity',playstart)
            playername = txtfile[playstart:playend]
            playername = playername.replace('u0117', 'e')
            playername = playername.replace('\\','')
            playername = playername.replace('u00f3', 'o')
            playername = playername.replace('u039e', 'E')

            startpos = playend

            rarstart = startpos + 11
            rarend = txtfile.find(',"combat',rarstart)
            raritylevel = int(txtfile[rarstart:rarend])

            startpos = rarend

            combstart = startpos + 15
            combend = txtfile.find(',"power',combstart)
            combattype = txtfile[combstart:combend]

            startpos = combend

            powstart = startpos + 9
            powend = txtfile.find(',"level',powstart)
            powlevel = int(txtfile[powstart:powend])

            startpos = powend

            levstart = startpos + 9
            levend = txtfile.find('}',levstart)
            lev = int(txtfile[levstart:levend])

            startpos = levend - 1

            gearlevel = ''

        unitline = []
        unitline.append(playername)
        unitline.append(unittype)
        unitline.append(unitname)
        unitline.append(raritylevel)
        unitline.append(lev)
        unitline.append(gearlevel)
        unitline.append(powlevel)
        unitline.append(guild)
        unitline.append(currdate)

        guildmatrix.append(unitline)

    guildcycle = guildcycle + 1

guildlist = []

for v in guildmatrix:
    guildadd = 1
    guildmem = []
    for w in guildlist:
        if (v[0] == w[0]) and (v[7] == w[1]):
            guildadd = 0
    if guildadd == 1:
        guildmem.append(v[0])
        guildmem.append(v[7])
        guildlist.append(guildmem)

for x in charmatrix:
    for y in guildlist:
        charadd = 1
        for z in guildmatrix:
            if (x[0] == z[2]) and (y[0] == z[0]):
                charadd = 0
        if charadd == 1:
            unitline = []
            unitline.append(y[0])
            unitline.append("Character")
            unitline.append(x[0])
            unitline.append(0)
            unitline.append(0)
            unitline.append('0')
            unitline.append(0)
            unitline.append(y[1])
            unitline.append(currdate)

            guildmatrix.append(unitline)

for s in shipmatrix:
    for t in guildlist:
        charadd = 1
        for u in guildmatrix:
            if (s[0] == u[2]) and (t[0] == u[0]):
                charadd = 0
        if charadd == 1:
            unitline = []
            unitline.append(t[0])
            unitline.append("Ship")
            unitline.append(s[0])
            unitline.append(0)
            unitline.append(0)
            unitline.append('')
            unitline.append(0)
            unitline.append(t[1])
            unitline.append(currdate)

            guildmatrix.append(unitline)

#export to file
s = open('newDXcharlist.csv','w')
s.write('Player,Type,Unit,Rarity,Level,Gear,Power,Guild,As Of\n')

#export char
for t in guildmatrix:
    for u in range(8):
       s.write('{},'.format(t[u]))
    s.write('{}/{}/{}\n'.format(now.month,now.day,now.year))

s.close()

print('Guild Units Complete')
