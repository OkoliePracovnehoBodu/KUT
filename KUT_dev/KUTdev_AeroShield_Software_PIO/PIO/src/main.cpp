#include <AeroShield.h>

// -------------------------------
// Define Timer related macros, functions
// -------------------------------

#define CPUF 16000000UL                                      // CPU frequency for Arduino UNO
#define DIF(Tms) (1000.0f / Tms)                             // Frequency divider macro
#define CMR(PS, DIF) (static_cast<int>(CPUF / PS / DIF) - 1) // Compare match register value calculation macro
#define PS(CMR, DIR) ((CPUF / (CMR + 1)) / DIR)              // Prescaler value calculation macro
#define CHECK_TIMER(CMR) (CMR < 256)                         // Check if CMR value fits in 8-bit register
#define CURRENT_PS 1024 // Current prescaler value

// -------------------------------
// -------------------------------

// -------------------------------
// Built-in LED configs
// -------------------------------

const static int BUILT_IN_LED_PIN = 13; // PIN pre zabudovanu LED
const static unsigned long T_sample = 1000;
const static unsigned long LED_onTime = 15;
bool LED_on = false;

// -------------------------------
// -------------------------------


// -------------------------------
// Required variables and constexpr functions
// -------------------------------

byte Ts_user = 1; // sampling time in ms

constexpr float TS_INTERVAL_MIN(byte Ts)
{
    return (static_cast<float>(Ts) * 1000.0f) * 0.95f;
}

float uSig = 0.0f, ySig = 0.0f, potSig = 0.0f, dtoffset = 0.0f, dtoffset_interval = 0.0f; // control, output, reference, time offset

unsigned long currentTime, dt, lastTime;

// -------------------------------
// -------------------------------


// -------------------------------
// API calls
// -------------------------------

void updateOutput()
{
    ySig = AeroShield.sensorReadDegree();
}

void updatePotentiometer()
{
    potSig = AeroShield.referenceRead();
}

void updateControl(const float &u)
{
    uSig = u;
}

void writeControl()
{
    AeroShield.actuatorWrite(uSig);
}

// -------------------------------
// -------------------------------


// -------------------------------
// Write data into serial comms
// -------------------------------

void printData()
{
    dt = currentTime - lastTime;
    dtoffset = dtoffset_interval - dt;
    if (dtoffset > 0)
    {
        if (dtoffset > 1000)
        {
            dtoffset = static_cast<unsigned long>(floor(dtoffset / 1000)); // round to nearest 1ms
            delay(dtoffset);
        }
        else
        {
            dtoffset = static_cast<unsigned long>(floor(dtoffset / 100) * 100); // round to nearest 100us
            delayMicroseconds(dtoffset);
        }
        currentTime = micros();
        dt = currentTime - lastTime;
    }
    lastTime = currentTime;

    Serial.print(currentTime);
    Serial.print(" ");
    Serial.print(uSig);
    Serial.print(" ");
    Serial.print(ySig);
    Serial.print(" ");
    Serial.print(potSig);
    Serial.print(" ");
    Serial.print(dt);
    Serial.println();
}

// -------------------------------
// -------------------------------


// -------------------------------
// Read new values from serial com and inputs
// -------------------------------
void readData()
{
    updateOutput();
    updatePotentiometer();
}

int recvByte()
{
    if (Serial.available() >= 4)
    {
        Serial.readBytes((char *)&uSig, 4); // Read 4 bytes from Serial
        return 0;                           // Success
    }
    return 1; // No new data received
}

void processNewData()
{
    if (recvByte())
    {
        currentTime = micros();

        readData(); // Read the sensor and reference values

        writeControl(); // Write the control signal to the actuator

        printData();
    }
}


// -------------------------------
// -------------------------------


// -------------------------------
// Setup the Arduino board
// -------------------------------

void setup()
{
    Serial.begin(115200); // Initialize Serial communication at 115200 baud rate
    Serial.flush();
    pinMode(BUILT_IN_LED_PIN, OUTPUT); // for LED

    AeroShield.begin();
    AeroShield.calibrate();

    Serial.println("--- MCU config ---");
    while (!Serial.available())
    {
        delay(1); // Wait for user to open terminal
    }

    Ts_user = Serial.read(); // sampling time in ms

    if (Ts_user == 0)
    {
        Ts_user = 1; // minimum 1 ms
    }

    if (Ts_user > 10)
    {
        dtoffset_interval = static_cast<float>(Ts_user) * 1000.0f;
    }
    else
    {
        dtoffset_interval = TS_INTERVAL_MIN(Ts_user);
    }

    // Calculate the timers
    const int cmr = CMR(CURRENT_PS, DIF(T_sample));

    cli();

    // Timer1 for LED blink
    TCCR1A = 0; // Normal mode
    TCCR1B = 0;
    TCNT1 = 0;                           // Initialize counter value to 0
    OCR1A = cmr;                         // Set compare match register for desired timer count
    TCCR1B |= (1 << WGM12);              // CTC mode
    TCCR1B |= (1 << CS12) | (1 << CS10); // Set prescaler to 1024 and start the timer
    TIMSK1 |= (1 << OCIE1A);             // Enable timer compare interrupt

    sei();

    Serial.println("--- MCU starting [" + String(Ts_user) + "] ---");
    currentTime = micros();
    lastTime = currentTime - (Ts_user * 1000); // better for statistics

    // Initial reads and writes
    readData();
    updateControl(0.0f);
    writeControl();

    printData();
}

// -------------------------------
// -------------------------------


// -------------------------------
// Timer 1 callback function for when triggered
// -------------------------------

ISR(TIMER1_COMPA_vect)
{
    LED_on = !LED_on;
    digitalWrite(BUILT_IN_LED_PIN, LED_on);
}

// -------------------------------
// -------------------------------


void loop()
{
    processNewData();
}