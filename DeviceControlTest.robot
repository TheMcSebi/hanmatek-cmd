*** Settings ***
Documentation     Example use case for the library using the Robot Framework
Library           OperatingSystem
Library           HanmatekControl.py
Test Teardown     Set Status     ${False}

*** Keywords ***
Should Be
Voltage Should Be
    [Arguments]         ${voltage}
    ${cv}=              Get Voltage
    Should Be Equal     ${voltage}      ${cv}

Status Should Be
    [Arguments]         ${status}
    ${cs}=              Get Status
    Should Be Equal     ${status}       ${cs}

*** Test Cases ***
Test general device settings
    Set Voltage             7
    Set Status              ${True}
    Status Should Be        ${True}
    Set Voltage             4
    Sleep                   2
    Voltage Should Be       ${4.0}