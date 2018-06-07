import datetime
import requests
now = datetime.datetime.now()

print('Start Guild Zetas')

guildloop = 0
guildselect = "ERROR"
guildzeta = []

while guildloop < 2:
    #pull guild list from SWGOH.GG
    if guildloop == 0:
        zetareq = requests.get("https://swgoh.gg/g/12262/degeneration-x/zetas/")
        guildselect = "Degeneration X"
    elif guildloop == 1:
        zetareq = requests.get("https://swgoh.gg/g/8233/firmly-grasp-it/zetas/")
        guildselect = "Firmly Grasp It"

    zetaout = zetareq.text

    #Sven ruins your life here
    zetaout = zetaout.replace('ė', 'e')
    zetaout = zetaout.replace('ó', 'o')
    zetaout = zetaout.replace('Ξ', 'E')

    #export list to file
    a = open('swgohZeta.txt','w')

    a.write(zetaout)

    a.close()

    #reopen the thing you just closed because I have no clue how to do it otherwise
    b = open('swgohZeta.txt','r')

    zetafile = b.readlines()

    b.close()

    #strip guildfile of blank lines
    zetafile = [line for line in zetafile if line.strip() != '']

    baseline = 266 #261
    checkline = zetafile[baseline]

    #for v in range(60):
    while checkline.find('</div>') == -1:
        c = 0
        zetatotal = 0

        playerline = zetafile[baseline] #261
        playername = playerline[playerline.find('value="')+7:len(playerline)-3]

        checkline = playerline

        while checkline.find('a href=') == -1:
            if checkline.find('</div>') != -1:
                break;
            
            zeta = []

            #playername
            zeta.append(playername)
            zeta.append(guildselect)

            #character name
            charline = zetafile[baseline+11+(13*c)+zetatotal] #272
            charname = charline[charline.find('title="')+7:len(charline)-3]

            charname = charname.replace('&quot;','"')
            charname = charname.replace('&#39;',"'")

            zeta.append(charname)

            #zeta count for character
            zetaline = zetafile[baseline+18+(13*c)+zetatotal] #279
            zetacount = 0

            zeta.append('')

            while zetaline.find('guild-member-zeta-ability') != -1:

                zeta = []

                #append player name
                zeta.append(playername)
                zeta.append(guildselect)

                #append character name
                zeta.append(charname)

                #find and append zeta name
                zetacount = zetacount + 1
                
                zetaname = zetaline[zetaline.find('title="')+7:len(zetaline)-3]
                zetaname = zetaname.replace('&quot;','"')
                zetaname = zetaname.replace('&#39;',"'")
            
                zeta.append(zetaname)

                guildzeta.append(zeta)

                zetaline = zetafile[baseline+18+(13*c)+zetatotal+zetacount] #279

            #zeta.append(zetacount)

            zetatotal = zetatotal + zetacount

            #guildzeta.append(zeta)

            c = c + 1

            checkline = zetafile[baseline+11+(13*c) + zetatotal] #272
            #print(checkline)
        baseline = baseline+10+(13*c)+zetatotal

    guildloop = guildloop + 1

s = open('DXZetaList.csv','w')
s.write('Player,Guild,Character,Zeta,As Of\n')

for t in guildzeta:
    for u in range(4):
        s.write('{},'.format(t[u]))
    s.write('{}/{}/{}\n'.format(now.month,now.day,now.year))

s.close()

print('Guild Zetas Complete')
