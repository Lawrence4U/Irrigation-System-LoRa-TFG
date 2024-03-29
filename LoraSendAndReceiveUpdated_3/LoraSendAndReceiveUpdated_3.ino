#include <MKRWAN.h>
#include <RTCZero.h>
#include "arduino_secrets.h"

RTCZero rtc;
LoRaModem modem(Serial1);

struct Time{
  byte hour;
  byte minute;
  byte second;
};

struct PeripherialAction{
  Time hora;
  byte gap;
  byte id_periferico;
  bool on_off;
  int nextDay; //este campo servirá para ordenar las acciones correctamente habiendo pasado un dia
};

struct PeripherialAction acciones[10];
int indice_acc=0;
int accion_sel=0;

#define TEROS 0
#define SEED_STUDIO 1
typedef struct{
  const int pin_sensor; // Pin analógico al que se ha conectado el sensor
  const int pin_enable; // Pin digital para habilitar la alimentación del sensor
  const int tipo;       // Tipo de sensor (Teros o Seed Studio)
}sensor_t;
// Se supone que los sensores capacitivos de Seed Studio se han conectado a las entradas 1 a 3 y el Teros a la 4 (la de la derecha)
sensor_t sensores[]={{A1, 1, SEED_STUDIO},{A2, 2, SEED_STUDIO}, {A3, 3, SEED_STUDIO}, {A4, 7, SEED_STUDIO}};

bool con_horario = false;
long timer_start = 0;
const long OFFSET = 42000;//420000;//7minutos en milisegundos

const int valvula0[2] = {4,5}; //pines de cada valvula
const int valvula1[2] = {7,7};
const int valvula2[2] = {7,7};
const int valvula3[2] = {7,7};
int valvulas[8] = {valvula0[0],valvula0[1],valvula1[0],valvula1[1],valvula2[0],valvula2[1],valvula3[0],valvula3[1]};
int enableValvula[4] = {6,7,7,7};

String appEui = SECRET_APP_EUI;
String appKey = SECRET_APP_KEY;

void setup(){
  int n;
  
  Serial.begin(115200);
  while (!Serial);
  if (!modem.begin(EU868)) {
    Serial.println("Failed to start module");
    while (1) {}
  };
  Serial.print("Your module version is: ");
  Serial.println(modem.version());
  Serial.print("Your device EUI is: ");
  Serial.println(modem.deviceEUI());

  int connected = modem.joinOTAA(appEui, appKey);
  if (!connected) {
    Serial.println("Something went wrong; are you indoor? Move near a window and retry");
    while (1) {}
  }
  analogReadResolution(12);//el Teros 10 envia datos de 12bits
  modem.minPollInterval(60);

  pinMode(valvula0[0], OUTPUT);
  pinMode(valvula1[0], OUTPUT);
  pinMode(valvula2[0], OUTPUT);
  pinMode(valvula3[0], OUTPUT);
  pinMode(valvula0[1], OUTPUT);
  pinMode(valvula1[1], OUTPUT);
  pinMode(valvula2[1], OUTPUT);
  pinMode(valvula3[1], OUTPUT);
  pinMode(enableValvula[0], OUTPUT);
  pinMode(enableValvula[1], OUTPUT);
  pinMode(enableValvula[2], OUTPUT);
  pinMode(enableValvula[2], OUTPUT);

  for(n=0; n<4; n++){
    pinMode(sensores[n].pin_sensor, INPUT);    // entrada analógica (creo que esto sobra)
    pinMode(sensores[n].pin_enable, OUTPUT);   // Habilita la alimentación del sensor
    digitalWrite(sensores[n].pin_enable, LOW); // Sensor sin alimentar por ahora.
  }

  digitalWrite(enableValvula[0], LOW);
  digitalWrite(enableValvula[1], LOW);
  digitalWrite(enableValvula[2], LOW);
  digitalWrite(enableValvula[3], LOW);
  
  rtc.begin();
  Serial.println("Setup complete");
  /*char mensaje[7] = "AABBCC";
  sendMessage(mensaje, 6);*/
}

void loop() {
  int n; // índice para los bucles
  static int humedad[4]; // Los cuatro valores de humedad medidos
  char mensaje[30]="Init";
  if(!con_horario){
    //mandar mensaje
    Serial.println("Checking for messages...");
   
    sendMessage(mensaje, 4);
    delay(1000);//damos tiempo para recibir el mensaje de vuelta
    if(!modem.available()){
      Serial.println("Sin mensajes");
      delay(20000);//2 minutos para reenviar paquete
      return;
    }else{
      Serial.println("received, now checking...");
      con_horario = 1;
      char rcv[64];
      //rcv[54] = 63;//pongo un valor aleatorio para luego comprobar que el paquete tiene la longitud necesaria
      int i = 0; //i tendra la longitud de la cadena recibida
      while (modem.available()) {
        rcv[i++] = (char)modem.read();
      }
      /*if(rcv[54] == 63){
      char msg[6] = "ERROR";//error de recepcion
      sendMessage(msg, 5);
      con_horario = 0;
      return;
      }*/
      Serial.print("Received: ");
      for (int j = 0; j < i; j++) {
        Serial.print(rcv[j] >> 4, HEX);
        Serial.print(rcv[j] & 0xF, HEX);
        Serial.print(" ");
      }
      Serial.println();
      indice_acc = 0; 
      manageSchedule(rcv);
      timer_start = millis();
      //poner alarmas etc
      if(indice_acc!=0){
        Serial.println("Poniendo alarmas...");
        //ponemos la primera alarma en funcionamiento
        rtc.setAlarmTime(acciones[0].hora.hour,acciones[0].hora.minute,acciones[0].hora.second);
        rtc.enableAlarm(rtc.MATCH_HHMMSS);
        rtc.attachInterrupt(alarma);
        Serial.println("Setup completo");
      }
    }
  }
  if(!modem.available()){
    if(millis() - timer_start >= OFFSET){
      timer_start = millis();
      // Leemos los cuatro sensores
      for(n=0; n<4; n++){
        double humedad_sensor, valorSensor;
        digitalWrite(sensores[n].pin_enable, HIGH);
        delay(20);
        Serial.print("Midiendo sensor ");Serial.println(sensores[n].pin_sensor);
        valorSensor = analogRead(sensores[n].pin_sensor);
        Serial.print("Valor sensor ");Serial.println(valorSensor);
        digitalWrite(sensores[n].pin_enable, LOW);
        double tension = valorSensor*3.33/4096;
        tension = tension*1000/0.638; // Este factor es para tener en cuenta el divisor de tensión y pasar la tensión a mV
        if(sensores[n].tipo == TEROS){
          humedad_sensor = 5.439e-10*pow(tension,3) -2.731e-6*pow(tension,2) +4.868e-3*tension -2.683;
          humedad[n] = round(humedad_sensor*100); // Se pasa a %, pues la fórmula lo da en unitarias
        }else{ // suponemos el Seed Studio
          tension = tension/1000.0; // En esta fórmula la tensión va en V
          humedad_sensor = 1281.605 - 1149.338 * tension + 348.9791 * tension * tension - 35.70235 * pow(tension, 3);
          humedad[n] = round(humedad_sensor); // La fórmula lo da ya en %
        }
        if(humedad[n] < 0){
          humedad[n] = 0;
        }else if(humedad[n] > 100){
          humedad[n] = 100;
        }
        Serial.print("Humedad sensor "); Serial.print(n); Serial.print("(%) = ");
        Serial.println(humedad[n]);
      }
      
      Serial.print("RTC: ");
      Serial.print(rtc.getHours());
      Serial.print(":");
      Serial.print(rtc.getMinutes());
      Serial.print(":");
      Serial.println(rtc.getSeconds());
      sprintf(mensaje,"%03d%03d%03d%03d", humedad[0], humedad[1], humedad[2], humedad[3]);
      sendMessage(mensaje, 12);
      
    }  
  }else{//recibo paquete despues del envio
    char rcv[64];
    //rcv[54] = 63;//pongo un valor aleatorio para luego comprobar que el paquete tiene la longitud necesaria
    int i = 0; //i tendra la longitud de la cadena recibida
    while (modem.available()) {
      rcv[i++] = (char)modem.read();
    }
    /*if(rcv[54] == 63){
      char msg[6] = "ERROR";//error de recepcion
      sendMessage(msg, 5);
      con_horario = 0;
    }*/
    Serial.print("Received: ");
    for (int j = 0; j < i; j++) {
      Serial.print(rcv[j] >> 4, HEX);
      Serial.print(rcv[j] & 0xF, HEX);
      Serial.print(" ");
    }
    Serial.println();
    indice_acc = 0; 
    manageSchedule(rcv);
    Serial.print("Numero de acciones recibidas: ");
    Serial.println(indice_acc);
    //poner alarmas etc
    if(indice_acc!=0){
      Serial.println("Poniendo alarmas...");
      //ponemos la primera alarma en funcionamiento
      rtc.setAlarmTime(acciones[0].hora.hour,acciones[0].hora.minute,acciones[0].hora.second);
      rtc.enableAlarm(rtc.MATCH_HHMMSS);
      rtc.attachInterrupt(alarma);
      Serial.println("Setup completo");
    }
  }
  
  
}

void sendMessage(char *message, int longitud){
  char *pt_msg = message;
  Serial.print("Sending:");
  for (int i = 0; i < longitud; i++) {
    Serial.print(*pt_msg >> 4, HEX);
    Serial.print(*pt_msg & 0xF, HEX);
    pt_msg++;
    Serial.print(" ");
  }
  Serial.println();
  int succ = 0;
  modem.beginPacket();
  while(!succ){
    modem.print(message);
    succ = modem.endPacket(true);
    if (succ > 0) {
      Serial.println("Message sent correctly!");
    } else {
      Serial.println("Error sending message :(");
    }
  }
  delay(1000);
}

void manageSchedule(char *paquete){

  char *esquema = paquete;
  struct PeripherialAction accion;
  char accionesInstantaneas = *esquema;
  esquema++;
  int *ptrVal = valvulas;
  int *ptrEn = enableValvula;
  //Serial.print("botones: ");
  //Serial.println(accionesInstantaneas, BIN);

  for(int i=0;i<8;i++){
    if(i%2==0 && i!=0){
      ptrVal+=2;
      ptrEn++;
    }
    if((accionesInstantaneas>>(7-i))&1){
      actuarElectrovalvula(ptrVal[0],ptrVal[1], ptrEn[0],!(i%2));//si i par es abrir sino cerrar
    }  
  }

  for(int i=0;i<4;i++){
    /*Serial.print("valor del puntero[0]: ");
    Serial.print(*esquema >> 4, HEX);
    Serial.println(*esquema & 0xF, HEX);*/
    if(*esquema==0){
      continue;
    }else{
      //hora,duracion,id_periferico,pinEnable
      accion.hora.hour = esquema[0];
      accion.hora.minute = 0;
      accion.hora.second = 0;
      accion.nextDay = 0;
      while(inAcciones(accion)){
        accion.hora.second += 10;
      }
      accion.gap = esquema[0];
      accion.id_periferico = i;
      accion.on_off = true;
      acciones[indice_acc] = accion;
      indice_acc++;

      //con la duracion creamos otra accion para cerrar la valvula
      accion.hora.hour = esquema[0];
      int horasRiego = esquema[1]/60;
      if(accion.hora.hour + horasRiego<24){
        accion.hora.hour += horasRiego;
        accion.nextDay = 0;
      }else{
        accion.hora.hour += horasRiego - 24;
        accion.nextDay = 1;
      }
      accion.hora.minute = esquema[1]%60;
      accion.hora.second = 0;
      while(inAcciones(accion)){
        accion.hora.second += 10;
      }
      accion.gap = esquema[0];
      accion.id_periferico = i;
      accion.on_off = false;
      acciones[indice_acc] = accion;
      indice_acc++;
    }
    
    esquema+=2;
  }

  Serial.println("Ordenando");
  sortActions();
  Serial.println("Terminado de ordenar");

  for(int j=0; j<indice_acc; j++){
    mostrarHorario(acciones[j]);
  }

  rtc.setTime(0,0,0);
  //PRUEBAS
  //rtc.setTime(0,59,0);
  
  return;
}

bool inAcciones(PeripherialAction accion){

    for(int i=0;i<indice_acc;i++){
      if(accion.hora.hour == acciones[i].hora.hour && accion.hora.minute == acciones[i].hora.minute && accion.hora.second == acciones[i].hora.second){
        return true;  
      }
    }
    return false;
}

void mostrarHorario(const PeripherialAction accion){

  Serial.print("Valvula: ");
  Serial.print(accion.id_periferico, DEC);
  Serial.print("\t");
  Serial.print("Hora: ");
  Serial.print(accion.hora.hour, DEC);
  Serial.print(":");
  Serial.print(accion.hora.minute, DEC);
  Serial.print(":");
  Serial.print(accion.hora.second, DEC);
  Serial.print(",nextDay: ");
  Serial.print(accion.nextDay);
  Serial.print(",gap: ");
  Serial.print(accion.gap, DEC);
  Serial.print(",on_off: ");
  Serial.println(accion.on_off);
  return;
}

void alarma(){
    Serial.println("Ejecutando alarma: ");
    mostrarHorario(acciones[0]);
    actuarElectrovalvula(valvulas[acciones[0].id_periferico*2], valvulas[(acciones[0].id_periferico*2)+1], enableValvula[acciones[0].id_periferico], acciones[0].on_off);
    PeripherialAction nextProgram;
    nextProgram = acciones[0];
    if(nextProgram.gap+rtc.getHours()<24){
      nextProgram.hora.hour = nextProgram.gap +rtc.getHours();
    }else{
      nextProgram.hora.hour = nextProgram.gap +rtc.getHours()-24;
      nextProgram.nextDay += 1;
    }
    while(inAcciones(nextProgram)){
        nextProgram.hora.second += 10;
    }
    acciones[0] = nextProgram;
    
    Serial.println("Ordenando");
    sortActions();
    Serial.println("Terminado de ordenar");

    for(int j=0; j<indice_acc; j++){
      mostrarHorario(acciones[j]);
    }
    rtc.setAlarmTime(acciones[0].hora.hour,acciones[0].hora.minute,acciones[0].hora.second);
    //PRUEBAS
    /*if(acciones[0].hora.minute !=0){
      rtc.setTime(acciones[0].hora.hour,acciones[0].hora.minute-1,acciones[0].hora.second);
    }else if(acciones[0].hora.hour != 0){
      rtc.setTime(acciones[0].hora.hour-1,59,acciones[0].hora.second);
    }*/
    
    return;
}

void sortActions(){

  for (int i=0; i<indice_acc-1;i++){
    for(int j=0; j<indice_acc-i-1; j++){
      if(!compare(acciones[j], acciones[j+1])){ //si acciones[j] es antes devolvera un 1 => no se cambia
        swap(&acciones[j], &acciones[j+1]);  
      }
    }
  }
  

  return;
}

bool compare(const PeripherialAction accion1, const PeripherialAction accion2){ 
  if(accion1.nextDay < accion2.nextDay){
    return true;
  }else if(accion1.nextDay == accion2.nextDay && accion1.hora.hour < accion2.hora.hour){ 
     return true; 
  }else if(accion1.nextDay == accion2.nextDay && accion1.hora.hour == accion2.hora.hour && accion1.hora.minute < accion2.hora.minute){
    return true;  
  }else if(accion1.nextDay == accion2.nextDay && accion1.hora.hour == accion2.hora.hour && accion1.hora.minute == accion2.hora.minute && accion1.hora.second < accion2.hora.second){
    return true;  
  }
  return false; 

}

void swap(PeripherialAction *xp, PeripherialAction *yp){
    struct PeripherialAction temp = *xp;
    *xp = *yp;
    *yp = temp;
    return;
}

void actuarElectrovalvula(int inp1, int inp2, int puertoEnable, bool on_off){
  //Logica para encender/apagar valvulas
  /*Serial.print("Argumentos para actuacion válvula:");
  Serial.print(inp1);
  Serial.print(",");
  Serial.print(inp2);
  Serial.print(",");
  Serial.print(puertoEnable);
  Serial.print(",");
  Serial.println(on_off);*/
  
  pinMode(puertoEnable, HIGH);
  if(on_off){
    Serial.println("Abriendo valvula en el puerto");
    digitalWrite(inp1, HIGH);
    digitalWrite(inp2, LOW);
    delay(20);//tiempo que tarde en abrirse/cerrarse
    digitalWrite(inp2, HIGH);
    
  }else{
    Serial.println("Cerrando valvula en el puerto");
    digitalWrite(inp1, LOW);
    digitalWrite(inp2, HIGH);
    delay(20);//timepo que tarde en abrirse/cerrarse
    digitalWrite(inp2, LOW);
  }
  pinMode(puertoEnable, LOW);
  
  return;
  }
