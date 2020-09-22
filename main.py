
from scapy.all import *
import 	os

def Arp_Req(IP):  #returns the MAC address of a given IP address
    result = sr1(ARP(op=ARP.who_has, pdst=IP))
    return result[ARP].hwdst

def DNS_Req(URL): #Creates a DNS Query to 8.8.8.8 and returns the IP
    ans = sr1(IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=URL)),verbose=0)
    return ans[2].an.rdata


def update_hidtory(URL): #This function update the history table and file by adding the URL and time of visiting(current time)
    localtime = time.asctime( time.localtime(time.time()) )
    history  = open("history.txt", "a+")
    history.write("^"+URL+" "+localtime+"\n")
    history.close()

def Clear_History(): #This function removes all the data in the history table and file
    history  = open("history.txt", "w")
    history.close()

def Remove_From_History(URL): #This function remove all the records of the given URL from the History table and file
    newhistory=""
    history  = open("history.txt", "a+")
    data = history.read().replace('\n', '')
    arr = data.split("^")
    for line in arr:
        if(URL not in line and line != ''):
            newhistory = newhistory+"^"+line+"\n"
    history.close()
    history  = open("history.txt", "w")
    history.write(newhistory)
    history.close()



def Find_IP(URL): #The functions uses the functions "Ret_From_Cache" and "DNS_Req" to find the IP address of a given URL
    ans = "0"
    ans = get_cache(URL)
    if(ans=="0"):
        ans = DNS_Req(URL)
        cache = open("cache.txt", "a+")
        cache.write("^"+URL+"*"+ans+"\n")
        cache.close()
    return ans

def get_cache(URL): #returns the IP of the URL from the internal DNS table if exists else return 0
    ans = "0"
    cache = open("cache.txt", "a+")
    data = cache.read().replace('\n', '')
    arr = data.split("^")
    for line in arr:
        if(URL in line):
            linedata = line.split("*")
            ans = linedata[1]
    cache.close()	
    return ans

def Flush_DNS(): #This function delete all content of the DNS file and the content of the DNS table.
    cache  = open("cache.txt", "w")
    cache.close()

def Make_GET(URL) : 
    syn = IP(dst=URL) / TCP(dport=80, flags='S')
    syn_ack = sr1(syn)
    ack = IP(dst=URL) / TCP(dport=80, sport = syn_ack[TCP].dport, seq = syn_ack[TCP].ack, ack = syn_ack[TCP].seq + 1, flags='PA')
    send(ack)
    getStr = 'GET / HTTP/1.1\r\nHost: www.google.com\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: en-US,en;q=0.8\r\n\r\n'
    request = IP(dst=URL) / TCP(dport=80, sport=syn_ack[TCP].dport,seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
    reply = sr1(request)
    update_hidtory(URL)

def print_history():
    newhistory=""
    history  = open("history.txt", "a+")
    data = history.read()
    print data
    history.close()

def credits():
    print "------------------------------------------------------"
    print "Niv Shtibel - Always in motion"
    print "------------------------------------------------------"

def History_menu(): #this function will open a menu that contains the option
    os.system('color b')
    os.system('cls' if os.name == 'nt' else 'clear')
    exit_history = 0
    while (exit_history == 0):
        print "Choose one of these options \n"
        print "1.Show History" #print out all the history line by line
        print "2.Clear History" #clear the history using the function and print a "done" message
        print "3.Remove specific record" 
        print "4.Back to menu" 
        num = input("Enter a number : ")
        if (num == 1): 
            os.system('cls' if os.name == 'nt' else 'clear')
            print_history()
        elif (num == 2): 
            os.system('cls' if os.name == 'nt' else 'clear')
            Clear_History()
            print "Done!!\n\n"
        elif (num == 3):
            url = raw_input("Enter a url : ")
            Remove_From_History(url)
            os.system('cls' if os.name == 'nt' else 'clear')
            print "Done!!\n\n"
        elif (num==4):
	    os.system('cls' if os.name == 'nt' else 'clear')
            exit_history = 1


def menu():#This function will show the browser's menu who contains the options
    os.system('cls' if os.name == 'nt' else 'clear')
    exit_menu = 0
    while (exit_menu == 0):
        print "Choose one of these options: \n"
        print "1.History" #this choice will open the history's Menu
        print "2.Visit a site" #this choice will ask for URL address
        print "3.Credits" #this choice will show all the names that deserves some credits for building this browser
        print "4.Exit" # the choice will give the user the exit of the web page
        answer = input("Enter a number: ")
        if (answer == 1): 
            History_menu()
        elif (answer == 2): 
            url = raw_input("Enter the url: ")
            Make_GET(url)
        elif (answer == 3):
            credits()
        elif (answer == 4):
            exit_menu = 1


def main(): #the main function
    menu()

main()