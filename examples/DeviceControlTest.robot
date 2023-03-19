*** Settings ***
Documentation     Example use case for the HanmatekControl library using the Robot Framework
...               Implementing a test to log drawn current for a set voltage range

Library           OperatingSystem
Library           HanmatekControl.py    /dev/ttyUSB0
Library           DateTime

Test Teardown     Power device off

*** Variables ***
${TEST_LOG_FILE}    testlog.csv
${MEASUREMENTS_PER_ITERATION}    5
${DELAY_BETWEEN_MEASUREMENTS}    0.5

*** Keywords ***
Voltage Should Be
    [Arguments]         ${voltage}
    ${cv}=              Get Voltage
    Should Be Equal     ${voltage}      ${cv}

Status Should Be
    [Arguments]         ${status}
    ${cs}=              Get Status
    Should Be Equal     ${status}       ${cs}

Power device on
    Set Status    ${True}

Power device off
    Set Status    ${False}


Run current draw test from ${initial_voltage} to ${voltage_limit} step ${voltage_iteration_step}
    [Documentation]    Iterates through the given voltage range and logs all results to the log file defined above as CSV
    ...
    ...                File Format: 
    ...                Timestamp (YYYY-MM-DD HH:MM:SS), Voltage (Volts), Current (Ampere), Power (Watts)
    ...
    ...
    Create File        ${TEST_LOG_FILE}    timestamp,voltage,current,power\n

    ${begin_time}=     Get Time
    Log To Console     \nTest begin time: ${begin_time}\nInitial Voltage: ${initial_voltage}\nLimit: ${voltage_limit}\nStep: ${voltage_iteration_step}\n

    Set Voltage        0
    Power device on

    FOR    ${voltage}    IN RANGE    ${initial_voltage}    ${voltage_limit}+${voltage_iteration_step}    ${voltage_iteration_step}
        Set Voltage    ${voltage}
        
        FOR    ${j}    IN RANGE    0    ${MEASUREMENTS_PER_ITERATION}    1
            Sleep    ${DELAY_BETWEEN_MEASUREMENTS}
            ${timestamp}=  Get Time
            Sync Device
            ${voltage}=    Get Voltage    ${True}
            ${current}=    Get Current    ${True}
            ${power}=      Get Power      ${True}

            Append To File    ${TEST_LOG_FILE}    ${timestamp},${voltage},${current},${power}\n
            Log To Console    ${timestamp}: ${voltage} V, ${current} A (${power} W)
        END
    END

    ${end_time}=    Get Time
    ${duration}=    Subtract Date From Date    ${end_time}    ${begin_time}
    Log To Console    Test Finished\nTime elapsed: ${duration} seconds

*** Test Cases ***
#Test general device settings
#    Set Voltage             7
#    Set Status              ${True}
#    Status Should Be        ${True}
#    Set Voltage             4
#    Sleep                   2
#    Voltage Should Be       ${4.0}

Run a basic current draw test
    #Run current draw test from 1 to 2 step 0.3
    #Sync Device
    Run current draw test from 0 to 12 step 0.1