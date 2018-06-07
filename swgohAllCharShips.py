import requests

print('Start All Characters and Ships')

##########CHARACTERS##########
#pull char list from SWGOH.GG
charreq = requests.get("https://swgoh.gg/")

charout = charreq.text

#export list to file
e = open('swgohCharList.txt','w')

e.write(charout)

e.close()

#reopen the thing you just closed because I have no clue how to do it otherwise
h = open('swgohCharList.txt','r')

charfile = h.readlines()

h.close()

#strip charfile of blank lines
charfile = [line for line in charfile if line.strip() != ''] 

#initialize chartable
chartable = []

a = 0

baseline = 0
endoffile = 0

while a < 1000:

    #if charfile[baseline+(17*a)].find('media list-group-item p-0 character') == -1:
    #    if charfile[baseline+(17*a)].find('media list-group-item ad-item visible') == -1:
    #        break
    #    else:
    #        baseline = baseline + 8

    lookup = 'media list-group-item p-0 character'
    foundflag = 0
    linemark = 1
    while foundflag == 0:
        if charfile[baseline + linemark].find(lookup) != -1:
            baseline = baseline + linemark
            foundflag = 1
            break
        elif charfile[baseline + linemark].find('</html>') != -1:
            endoffile = 1
            break
        linemark = linemark + 1

    if endoffile == 1:
        break

    char = []

    #Char Name
    charnameline = charfile[baseline+9]
    charname = charnameline[4:len(charnameline)-6]

    charname = charname.replace('&quot;','"')
    charname = charname.replace('&#39;',"'")

    char.append(charname)

    #Type
    chartype = 'Character'
    char.append(chartype)

    #Alignment
    alignline = charfile[(baseline+8)]

    alignlen = 1
    if alignline.find('Light') == -1:
            alignlen = 0
            
    align = alignline[alignline.find('hidden-xs">')+11:alignline.find('hidden-xs">')+20+alignlen]

    char.append(align)

    #Role
    roleline = charfile[baseline]

    role = ''

    if roleline.find('tank') == -1:
        if roleline.find('attacker') == -1:
            if roleline.find('healer') == -1:
                role = 'Support'
            else:
                role = 'Healer'
        else:
            role = 'Attacker'
    else:
        role = 'Tank'

    char.append(role)

    #Class
    classline = charfile[baseline]

    charclass = classline[classline.find('data-tags="')+len(role)+13:len(classline)-4]

    char.append(charclass)

    #append to chartable
    chartable.append(char)
    a = a + 1

##########SHIPS##########

#pull ship list from SWGOH.GG
shipreq = requests.get("https://swgoh.gg/ships")

shipout = shipreq.text

#export list to file
f = open('swgohShipList.txt','w')

f.write(shipout)

f.close()

#reopen the thing you just closed because I have no clue how to do it otherwise
k = open('swgohShipList.txt','r')

shipfile = k.readlines()

k.close()

#strip charfile of blank lines
shipfile = [line for line in shipfile if line.strip() != ''] 

#initialize chartable
shiptable = []

b = 0

baseline = 0
endoffile = 0

while b < 100:
    lookup = '<div title="'

    #find next ship line
    foundflag = 0
    linemark = 1
    while foundflag == 0:
        if shipfile[baseline + linemark].find(lookup) != -1:
            baseline = baseline + linemark
            foundflag = 1
            break
        elif shipfile[baseline + linemark].find('</html>') != -1:
            endoffile = 1
            break
        linemark = linemark + 1

    if endoffile == 1:
        break

    ship = []

    #Ship Name
    shipnameline = shipfile[baseline]
    shipname = shipnameline[12:len(shipnameline)-23]

    shipname = shipname.replace('&quot;','"')
    shipname = shipname.replace('&#39;',"'")

    ship.append(shipname)

    #Type
    shiptype = 'Ship'
    ship.append(shiptype)

    #Alignment
    shipcatline = shipfile[baseline-2]

    if shipcatline.find('dark side') != -1:
        shipalign = "Dark Side"
    elif shipcatline.find('light side') != -1:
        shipalign = "Light Side"
    else:
        shipalign = "Error"

    ship.append(shipalign)

    #Role
    if shipcatline.find('capital ship') != -1:
        shiprole = 'Capital Ship'
    elif shipcatline.find('tank') != -1:
        shiprole = 'Tank'
    elif shipcatline.find('attacker') != -1:
        shiprole = 'Attacker'
    elif shipcatline.find('support') != -1:
        shiprole = 'Support'
    elif shipcatline.find('healer') != -1:
        shiprole = 'Healer'
    else:
        shiprole = '###ERROR###'

    ship.append(shiprole)

    #Class
    shipclass = shipcatline[shipcatline.find('data-tags="')+len(shipalign)+len(shiprole)+13:len(shipcatline)-4]

    ship.append(shipclass)

    
    shiptable.append(ship)
    b = b + 1

#export to file
m = open('SWGOHcharlookup.csv','w')
m.write('Unit,Type,Alignment,Role,Classes\n')

for z in chartable:
    for y in range(5):
        m.write('{},'.format(z[y]))
    m.write('\n')

for x in shiptable:
    for w in range(5):
        m.write('{},'.format(x[w]))
    m.write('\n')
    
m.close()

print('All Characters and Ships Complete')
