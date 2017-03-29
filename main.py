# e necessario far partire il programma dal terminale con i seguenti comandi:
# sudo python main.py
#cosi facendo si hanno i permessi di root

import sys
import os
import netifaces as ni

#########################################################################################################

#variabile statica globale presente all interno del file configured.txt che
# in base al valore capisco se non e configurato, e un host o e un gateway
file = open("configured.txt", "r")
configured = file.read()

#print 'Name wireless interface:'
wlan = "en1"  # <- - - - - - - - - - - - - - -  [MODIFICARE INTERFACCIA WIFI]

print '1) start'
print '2) reset'
start = raw_input()
if not start == '1':
    print '****************** reset configuration *************************'
    file = open("configured.txt", "w")
    file.write("null")
    sys.exit(0)

#il mio indirizzo IP
#prima configurazione oppure sono sia client,server o superclient
if str(configured) == "null" or str(configured) == "client" or str(configured) == "superclient" or str(configured) == "server":
    ni.ifaddresses(wlan)
    myIP = ni.ifaddresses(wlan)[2][0]['addr']
    print '- - - - - - - - - - '+myIP+' - - - - - - - - - - - \n'

    print os.system('iwconfig | grep '+wlan)
    print '- - - - - - - - - - - - - - - - - - - - - - - - - -'
#sono un gateway
else:
    ni.ifaddresses(wlan)
    myIP = ni.ifaddresses(wlan+':1')[2][0]['addr']
    print '- - - - - - - - - - ' + myIP + ' - - - - - - - - - - - \n'

    print os.system('iwconfig | grep ' + wlan)
    print '- - - - - - - - - - - - - - - - - - - - - - - - - - -'

#########################################################################################################

#non sono configurato
if str(configured) == "null":
    print '\nconfiguration:'

    print '0) gateway'
    print '1) super-client (network 1) 172.30.1.2'
    print '2) client (network 1) 172.30.1.3'
    print '3) client (network 1) 173.30.1.4'
    print '4) server (network 2) 172.30.2.2'

    print '\nchoose configuration:'
    option = raw_input()

    # prima configurazione

    # CONFIGURAZIONE GATEWAY
    if option == '0':
        option = None
        #impostazione indirizzi IP
        os.system('sudo ifconfig -v '+wlan+':1 172.30.1.1/24')
        os.system('sudo ifconfig -v '+wlan+':2 172.30.2.1/24')

        # cancella le route di default
        os.system('sudo route del default')

        # aggiunge route per vedere le reti
        os.system('sudo route add -net 172.30.1.0 netmask 255.255.255.0 gw 172.30.1.1 dev '+wlan+':1')
        os.system('sudo route add -net 172.30.2.0 netmask 255.255.255.0 gw 172.30.2.1 dev '+wlan+':2')

        # abilitare il forwarding dei pacchetti
        os.system('sudo sysctl -w net.ipv4.ip_forward=1')

        # disabilita ICMP redirect
        os.system('sudo sysctl -w net.ipv4.conf.all.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.all.send_redirects=0')

        # default
        os.system('sudo sysctl -w net.ipv4.conf.default.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.default.send_redirects=0')

        # dev wlan
        os.system('sudo sysctl -w net.ipv4.conf.'+wlan+'.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.'+wlan+'.send_redirects=0')

        # lo
        os.system('sudo sysctl -w net.ipv4.conf.lo.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.lo.send_redirects=0')

        print 'gateway configured!'
        file = open("configured.txt", "w")
        file.write("gateway")

    # CONFIGURAZIONE SUPER-CLIENT
    elif option == '1':
        os.system('ifconfig ' + wlan + ' 172.30.1.2/24')
        os.system('route del default')
        os.system('route add default gw 172.30.1.1')

        print 'super-client configured!'
        file = open("configured.txt", "w")
        file.write("superclient")

    # CONFIGURAZIONE ALTRI CLIENT
    elif option == '2':
        os.system('ifconfig '+wlan+' 172.30.1.3/24')
        os.system('route del default')
        os.system('route add default gw 172.30.1.1')

        print 'normal client configured!'
        file = open("configured.txt", "w")
        file.write("client")

    elif option == '3':
        os.system('ifconfig '+wlan+' 172.30.1.4/24')
        os.system('route del default')
        os.system('route add default gw 172.30.1.1')

        print 'normal client configured!'
        file = open("configured.txt", "w")
        file.write("client")

    # CONFIGURAZIONE SERVER
    elif option == '4':
        os.system('ifconfig '+wlan+' 172.30.2.2/24')
        os.system('route del default')
        os.system('route add default gw 172.30.2.1')
        
        print 'server configured!'
        file = open("configured.txt", "w")
        file.write("server")
    else:
        print '****************** reset configuration *************************'
        file = open("configured.txt", "w")
        file.write("null")
        sys.exit(0)

#########################################################################################################

# gia configurato (configured = 1)
else:
    int_option = None

    print '* you are a '+str(configured)+' *\n'

    while int_option is None:

        #sono un client / superclient / server
        # hanno le medesime funzioni
        if str(configured) == "client" or str(configured) == "superclient" or str(configured) == "server":
            print "1) hping3"
            print "2) hping3 --fast"
            print "\nnetcat:"
            print "3) send"
            print "4) receive"
            print "5) file deletion"

            try:
                option1 = raw_input()
            except SyntaxError:
                option = None

            if option1 == '1':
                print "insert number of packet:"
                count = raw_input()
                print os.system('sudo hping3 -S 172.30.2.2 -p 80 -c '+count)

            elif option1 == '2':
                print "insert number of packet:"
                count = raw_input()
                print os.system('sudo hping3 -S 172.30.2.2 -p 80 -c ' + count+ ' --fast')

            elif option1 == '3':
                print "insert ip target:"
                ip=raw_input()
                os.system('sudo pv leone.jpg | nc -w 1 '+ip+' 3333')

            elif option1 == '4':
                print "waiting..."
                os.system('sudo nc -l -p 3333 | pv -rb > leone.jpg')

            elif option1 == '5':
                os.system('sudo rm -f leone.jpg')
                print "delete success!"

            else:
                print '****************** reset configuration *************************'
                file = open("configured.txt", "w")
                file.write("null")
                sys.exit(0)

            int_option = None

###########################################################################################################

        # sono un gateway
        else:
            print "1) setup iptables mangle"
            print "2) create root tree"
            print "3) packet loss"
            print "4) packet duplication"
            print "5) packet corruption"
            print "6) packet delay"

            try:
                option2 = raw_input()
            except SyntaxError:
                option = None

            # assegnare un mark per una specifica classe data nel punto 1
            if option2 == '1':
                os.system('iptables -A PREROUTING -t mangle -i ' + wlan + ' -s 172.30.1.2 -j MARK --set-mark 21')
                os.system('iptables -A PREROUTING -t mangle -i ' + wlan + ' -s 172.30.2.2 -j MARK --set-mark 30')
                os.system('iptables -A PREROUTING -t mangle -i ' + wlan + ' -p tcp -j MARK --set-mark 11')

                print ("172.30.1.2 is marked as superclient with MARK 21")
                print ("172.30.1.3 is marked as client with MARK 11")
                print ("172.30.1.4 is marked as client with MARK 11")
                print ("172.30.2.2 is marked as server with MARK 30\n")

                # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

            # creazione delle classi e dei limite della banda
            elif option2 == '2':
                # delete previous rules
                os.system('tc qdisc del dev ' + wlan + ' root')
                # create tree
                os.system('tc qdisc add dev ' + wlan + ' root handle 1: htb default 30')
                # root class
                os.system('tc class add dev ' + wlan + ' parent 1: classid 1:1 htb rate 2mbps ceil 3mbps burst 1mb')
                # gold user class
                os.system('tc class add dev ' + wlan + ' parent 1:1 classid 1:10 htb rate 400kbps ceil 600kbps burst 400kb')
                # normal user class
                os.system('tc class add dev ' + wlan + ' parent 1:1 classid 1:20 htb rate 150kbps ceil 180kbps burst 80kb')
                # server class
                os.system('tc class add dev ' + wlan + ' parent 1: classid 1:30 htb rate 1mbps ceil 1.5mbps burst 1mb')

                #TRAFFIC CONTROL RULES

                # super user
                os.system('tc class add dev ' + wlan + ' parent 1:20 classid 1:21 htb rate 100kbps ceil 150kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:21 handle 21: netem delay 1ms 20ms distribution normal loss 1% duplicate 0.1% corrupt 0.1% reorder 5% 15% gap 5')

                #server
                os.system('tc class add dev ' + wlan + ' parent 1:30 classid 1:31 htb rate 100kbps ceil 150kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:31 handle 30: netem delay 1ms 20ms distribution normal loss 1% duplicate 0.1% corrupt 0.5% reorder 5% 15% gap 5')

                # others
                os.system('tc class add dev ' + wlan + ' parent 1:10 classid 1:11 htb rate 300kbps ceil 450kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:11 handle 11: netem delay 1ms 1ms distribution normal loss 1% duplicate 0.1% corrupt 0.1% reorder 5% 15% gap 5')

                # filtri
                os.system('tc filter add dev ' + wlan + ' parent 1: prio 0 protocol ip handle 11 fw flowid 1:11')
                os.system('tc filter add dev ' + wlan + ' parent 1: prio 0 protocol ip handle 21 fw flowid 1:21')
                os.system('tc filter add dev ' + wlan + ' parent 1: prio 0 protocol ip handle 30 fw flowid 1:30')

            # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

            #packet loss, perdita di pacchetti tcp in base alle classi
            elif option2 == '3':
                print "insert % packet lost for handle 11:"
                param1= raw_input()
                # others
                os.system('tc qdisc add dev ' + wlan + ' parent 1:10 handle 1:11 htb rate 100kbps ceil 200kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:11 handle 11: netem delay 1ms 1ms distribution normal loss '+param1+'% '+'duplicate 0.1% corrupt 0.1% reorder 5% 15% gap 5')
                print "insert % packet lost for handle 21:"
                param2 = raw_input()
                # super user
                os.system('tc qdisc add dev ' + wlan + ' parent 1:20 handle 1:21 htb rate 100kbps ceil 200kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:21 handle 21: netem delay 1ms 20ms distribution normal loss '+param2+'% '+'duplicate 0.1% corrupt 0.1% reorder 5% 15% gap 5')

                print ("Done!\n")
            # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

            #dupplicazione dei pacchetti
            elif option2 == '4':
                print "insert % packet duplication for handle 11:"
                param1 = raw_input()
                # others
                os.system('tc qdisc add dev ' + wlan + ' parent 1:10 handle 1:11 htb rate 100kbps ceil 200kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:11 handle 11: netem delay 1ms 1ms distribution normal loss 1% duplicate '+param1+'% corrupt 0.1% reorder 5% 15% gap 5')
                print "insert % packet duplication for handle 21:"
                param2 = raw_input()
                # super user
                os.system('tc qdisc add dev ' + wlan + ' parent 1:20 handle 1:21 htb rate 100kbps ceil 200kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:21 handle 21: netem delay 1ms 20ms distribution normal loss 1% duplicate '+param2+'% corrupt 0.1% reorder 5% 15% gap 5')

                print ("Done!\n")
            # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

            # corruzione dei pacchetti
            elif option2 == '5':
                print "insert % packet corruption for handle 11:"
                param1 = raw_input()
                # others
                os.system('tc qdisc add dev ' + wlan + ' parent 1:10 handle 1:11 htb rate 100kbps ceil 200kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:11 handle 11: netem delay 1ms 1ms distribution normal loss 1% duplicate 1% corrupt '+param1+'% reorder 5% 15% gap 5')
                print "insert % packet corruption for handle 21:"
                param2 = raw_input()
                # super user
                os.system('tc qdisc add dev ' + wlan + ' parent 1:20 handle 1:21 htb rate 100kbps ceil 200kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:21 handle 21: netem delay 1ms 20ms distribution normal loss 1% duplicate 0.1% corrupt '+param2+'% reorder 5% 15% gap 5')

                print ("Done!\n")
            # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

            # ritardo dei pacchetti
            elif option2 == '6':
                print "insert % packet delay for handle 11:"
                param1 = raw_input()
                # others
                os.system('tc qdisc add dev ' + wlan + ' parent 1:10 handle 1:11 htb rate 100kbps ceil 200kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:11 handle 11: netem delay '+param1+'ms 1ms distribution normal loss 1% duplicate 1% corrupt 0.1% reorder 5% 15% gap 5')
                print "insert % packet delay for handle 21:"
                param2 = raw_input()
                # super user
                os.system('tc qdisc add dev ' + wlan + ' parent 1:20 handle 1:21 htb rate 100kbps ceil 200kbps')
                os.system('tc qdisc add dev ' + wlan + ' parent 1:21 handle 21: netem delay '+param2+'ms 20ms distribution normal loss 1% duplicate 0.1% corrupt 0.1% reorder 5% 15% gap 5')

                print ("Done!\n")
            # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

            else:
                print '****************** reset configuration *************************'
                file = open("configured.txt", "w")
                file.write("null")
                sys.exit(0)



