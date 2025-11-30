#include <windows.h>
#include <stdio.h>

#define PORTA_SERIAL "COM5"
#define BAUD_RATE 9600
#define OUTPUT_FILE "../front_end/airplane.json"

// Defina o tamanho mínimo de dados que indica "pacote completo"
#define MIN_PACKET_SIZE 237   // ajuste conforme necessário

int main() {

    HANDLE hSerial;
    DCB dcbSerialParams = {0};
    COMMTIMEOUTS timeouts = {0};
    DWORD bytesLidos;
    char buffer[512];

    /* Abre porta serial */
    hSerial = CreateFileA(
        PORTA_SERIAL,
        GENERIC_READ,
        0,
        NULL,
        OPEN_EXISTING,
        0,
        NULL
    );

    if (hSerial == INVALID_HANDLE_VALUE) {
        printf("Erro ao abrir %s\n", PORTA_SERIAL);
        return 1;
    }

    /* Configura porta serial */
    dcbSerialParams.DCBlength = sizeof(DCB);
    GetCommState(hSerial, &dcbSerialParams);

    dcbSerialParams.BaudRate = BAUD_RATE;
    dcbSerialParams.ByteSize = 8;
    dcbSerialParams.StopBits = ONESTOPBIT;
    dcbSerialParams.Parity   = NOPARITY;

    SetCommState(hSerial, &dcbSerialParams);

    /* Timeouts */
    timeouts.ReadIntervalTimeout         = 50;
    timeouts.ReadTotalTimeoutConstant    = 50;
    timeouts.ReadTotalTimeoutMultiplier  = 10;
    SetCommTimeouts(hSerial, &timeouts);

    printf("Lendo dados...\n");

    /* Loop principal */
    while (1) {

        if (ReadFile(hSerial, buffer, sizeof(buffer) - 1, &bytesLidos, NULL)) {

            if (bytesLidos > 0) {

                buffer[bytesLidos] = '\0'; // mantém tudo, inclusive colchetes

                /* Se atingiu o tamanho considerado "pacote completo" */
                if (bytesLidos >= MIN_PACKET_SIZE) {

                    FILE *fp = fopen(OUTPUT_FILE, "w"); // sobrescreve sempre

                    if (fp) {
                        fwrite(buffer, 1, bytesLidos, fp);
                        fclose(fp);
                    } else {
                        printf("Erro ao abrir %s\n", OUTPUT_FILE);
                    }
                }
            }
        }
    }

    CloseHandle(hSerial);
    return 0;
}
