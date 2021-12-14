#include "mbed.h"

Serial pc(USBTX, USBRX);
Serial esp(p28, p27); // tx, rx
Timer t;

int  counting,ended,timeout;
char buf[2024];
char snd[1024];

//char ssid[32] = "GTother";     // enter WiFi router ssid inside the quotes
//char pwd [32] = "GeorgeP@1927"; // enter WiFi router password inside the quotes
char ssid[32] = "cuatrocerberus";     // enter WiFi router ssid inside the quotes
char pwd [32] = "ligerzerojager1934"; // enter WiFi router password inside the quotes



void SendCMD(),getreply(),ESPconfig(),ESPsetbaudrate();


int main()
{
    pc.baud(9600);  // set what you want here depending on your terminal program speed
    esp.baud(9600);

    ESPconfig();        //******************  include Config to set the ESP8266 configuration  ***********************

    // continuosly get AP list and IP
    while(1) {
        pc.printf("\n---------- Listing Access Points ----------\r\n");
        strcpy(snd, "function listap(t)\r\n");
        wait(1);
        strcpy(snd, "for k,v in pairs(t) do\r\n");
        SendCMD();
        wait(1);
        strcpy(snd, "print(k..\" : \"..v)\r\n");
        SendCMD();
        wait(1);
        strcpy(snd, "end\r\n");
        SendCMD();
        wait(1);
        strcpy(snd, "end\r\n");
        SendCMD();
        wait(1);
        strcpy(snd, "wifi.sta.getap(listap)\r\n");
        SendCMD();
        wait(1);
        timeout=15;
        getreply();
        pc.printf(buf);
        wait(2);
        pc.printf("\n---------- Get IP and MAC ----------\r\n");
        strcpy(snd, "print(wifi.sta.getip())\r\n");
        SendCMD();
        timeout=10;
        getreply();
        pc.printf(buf);
        strcpy(snd, "print(wifi.sta.getmac())\r\n");
        SendCMD();
        timeout=10;
        getreply();
        pc.printf(buf);
        wait(2);
    }

}

//  +++++++++++++++++++++++++++++++++ This is for ESP8266 config only, run this once to set up the ESP8266 +++++++++++++++
void ESPconfig()
{
    wait(5);
    pc.printf("\f---------- Starting ESP Config ----------\r\n\n");
    pc.printf("---------- Reset & get Firmware ----------\r\n");
    strcpy(snd,"node.restart()\r\n");
    SendCMD();
    timeout=5;
    getreply();
    pc.printf(buf);

    wait(2);

    pc.printf("\n---------- Get Version ----------\r\n");
    strcpy(snd,"print(node.info())\r\n");
    SendCMD();
    timeout=4;
    getreply();
    pc.printf(buf);

    wait(3);

    // set CWMODE to 1=Station,2=AP,3=BOTH, default mode 1 (Station)
    pc.printf("\n---------- Setting Mode ----------\r\n");
    strcpy(snd, "wifi.setmode(wifi.STATION)\r\n");
    SendCMD();
    timeout=4;
    getreply();
    pc.printf(buf);

    wait(2);

    pc.printf("\n---------- Listing Access Points ----------\r\n");
    strcpy(snd, "function listap(t) \r\n");
    SendCMD();
    wait(1);
    strcpy(snd, "for k,v in pairs(t) do \r\n");
    SendCMD();
    wait(1);
    strcpy(snd, "print(k..\" : \"..v)\r\n");
    SendCMD();
    wait(1);
    strcpy(snd, "end\r\n");
    SendCMD();
    wait(1);
    strcpy(snd, "end\r\n");
    SendCMD();
    wait(1);
    strcpy(snd, "wifi.sta.getap(listap) \r\n");
    SendCMD();
    wait(1);
    timeout=15;
    getreply();
    pc.printf(buf);

    wait(2);

    pc.printf("\n---------- Connecting to AP ----------\r\n");
    pc.printf("ssid = %s   pwd = %s\r\n",ssid,pwd);
    
    //For Latest Version of firmware
    //strcpy(snd, "wifi.sta.config{ssid=\"");
    //strcat(snd, ssid);
    //strcat(snd, "\",pwd=\"");
    //strcat(snd, pwd);
    //strcat(snd, "\"}\r\n");
    
    //For older default firmware
    strcpy(snd, "wifi.sta.config(\"");
    strcat(snd, ssid);
    strcat(snd, "\",\"");
    strcat(snd, pwd);
    strcat(snd, "\")\r\n");
    
    SendCMD();
    timeout=10;
    getreply();
    pc.printf(buf);

    wait(10);

    pc.printf("\n---------- Get IP's ----------\r\n");
    strcpy(snd, "print(wifi.sta.getip())\r\n");
    SendCMD();
    timeout=3;
    getreply();
    pc.printf(buf);

    wait(1);

    pc.printf("\n---------- Get Connection Status ----------\r\n");
    strcpy(snd, "print(wifi.sta.status())\r\n");
    SendCMD();
    timeout=5;
    getreply();
    pc.printf(buf);

    pc.printf("\n\n\n  If you get a valid (non zero) IP, ESP8266 has been set up.\r\n");
    pc.printf("  Run this if you want to reconfig the ESP8266 at any time.\r\n");
    pc.printf("  It saves the SSID and password settings internally\r\n");
    wait(10);
}

void SendCMD()
{
    esp.printf("%s", snd);
}

void getreply()
{
    memset(buf, '\0', sizeof(buf));
    t.start();
    ended=0;
    counting=0;
    while(!ended) {
        if(esp.readable()) {
            buf[counting] = esp.getc();
            counting++;
        }
        if(t.read() > timeout) {
            ended = 1;
            t.stop();
            t.reset();
        }
    }
}