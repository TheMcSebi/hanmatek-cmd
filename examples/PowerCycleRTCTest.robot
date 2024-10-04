*** Settings ***
Documentation     Example use case for the HanmatekControl library using the Robot Framework
...               Implementing a test to log device rtc time over a series of power losses

Library           OperatingSystem
Library           ../HanmatekControl.py    COM9
Library           ../ServiceControl.py    127.0.0.1     8080
Library           DateTime

Test Teardown     Power device on

*** Variables ***
${BOOT_WAIT_TIME}    8s
${CYCLE_COUNT}    30
${REPEAT_WAIT_TIME}   3s

*** Keywords ***
Power device on
    Set Status    ${True}

Power device off
    Set Status    ${False}

Get Device Time Difference
    ${system_time}=     Get System Time
    ${current_date}=    Get Current Date
    ${difference}=	    Subtract Date From Date     ${system_time}     ${current_date}
    [Return]    ${difference}

*** Test Cases ***

Test RTC System Time During Power Cycles
    [Documentation]    Power cycles the device and retrieves its time every on every reboot
    [Tags]      robot:skip

    ${begin_time}=     Get Time
    Log To Console     \nTest begin time: ${begin_time}\n

    Power device on
    Sleep   ${BOOT_WAIT_TIME}
    Send Service Command     signin 10
    Set System Time

    FOR    ${i}    IN RANGE    ${CYCLE_COUNT}
        Power device on
        Sleep   ${BOOT_WAIT_TIME}
        ${difference1}=     Get Device Time Difference
        Log     ${difference1}
        Sleep   ${REPEAT_WAIT_TIME}
        ${difference2}=     Get Device Time Difference
        Log     ${difference2}
        Sleep   ${REPEAT_WAIT_TIME}
        ${difference3}=     Get Device Time Difference
        Log     ${difference3}
        ${system_time}=     Get System Time
        Log     ${system_time}
        ${Average}=     Evaluate       (${difference1}+${difference2}+${difference3})/3
        Log     ${i}
        Log     ${system_time}
        Log     ${Average}
        Log To Console     ${i}. Cycle: ${Average} seconds
        Power device off
        Sleep   2s
    END

    ${end_time}=    Get Time
    ${duration}=    Subtract Date From Date    ${end_time}    ${begin_time}
    Log To Console    Test Finished\nTime elapsed: ${duration} seconds

Test RTC System Time Repeatedly
    [Documentation]    Retrieves system time offset repeatedly

    ${begin_time}=     Get Time
    Log To Console     \nTest begin time: ${begin_time}\n

    Power device on
    Sleep   ${BOOT_WAIT_TIME}
    Send Service Command     signin 10
    Set System Time

    FOR    ${i}    IN RANGE    ${CYCLE_COUNT}
        ${difference1}=     Get Device Time Difference
        Log     ${difference1}
        Sleep   ${REPEAT_WAIT_TIME}
        ${difference2}=     Get Device Time Difference
        Log     ${difference2}
        Sleep   ${REPEAT_WAIT_TIME}
        ${difference3}=     Get Device Time Difference
        Log     ${difference3}
        ${system_time}=     Get System Time
        Log     ${system_time}
        ${Average}=     Evaluate       (${difference1}+${difference2}+${difference3})/3
        Log     ${i}
        Log     ${system_time}
        Log     ${Average}
        Log To Console     ${i}. Cycle: ${Average} seconds
        Sleep   2s
    END

    ${end_time}=    Get Time
    ${duration}=    Subtract Date From Date    ${end_time}    ${begin_time}
    Log To Console    Test Finished\nTime elapsed: ${duration} seconds


Test RTC System Time With Reboots
    [Documentation]    Retrieves system time offset after repeated reboots


    ${begin_time}=     Get Time
    Log To Console     \nTest begin time: ${begin_time}\n

    Power device on
    Sleep   ${BOOT_WAIT_TIME}
    Send Service Command     signin 10
    Set System Time

    FOR    ${i}    IN RANGE    ${CYCLE_COUNT}
        ${difference1}=     Get Device Time Difference
        Log     ${difference1}
        Sleep   ${REPEAT_WAIT_TIME}
        ${difference2}=     Get Device Time Difference
        Log     ${difference2}
        Sleep   ${REPEAT_WAIT_TIME}
        ${difference3}=     Get Device Time Difference
        Log     ${difference3}
        ${system_time}=     Get System Time
        Log     ${system_time}
        ${Average}=     Evaluate       (${difference1}+${difference2}+${difference3})/3
        Log     ${i}
        Log     ${system_time}
        Log     ${Average}
        Log To Console     ${i}. Cycle: ${Average} seconds
        Send Service Command     restart 10
        Sleep   ${BOOT_WAIT_TIME}
    END

    ${end_time}=    Get Time
    ${duration}=    Subtract Date From Date    ${end_time}    ${begin_time}
    Log To Console    Test Finished\nTime elapsed: ${duration} seconds

