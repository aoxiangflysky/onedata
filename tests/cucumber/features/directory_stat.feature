Feature: Directory_stat

  Background:
    Given environment is defined in env.json
    Given environment is up
    Given u1 mounts onedata spaces in /root/onedata using token
    Given we are in space s1

  Scenario: Check file type
    When u1 creates directories [dir1]
    Then dir1 file type is directory
    Then clean succeeds

  Scenario: Check default access permissions
    When u1 creates directories [dir1]
    Then dir1 mode is 755
    Then clean succeeds

  Scenario: Change access permissions
    When u1 creates directories [dir1]
    When u1 changes dir1 mode to 211
    Then dir1 mode is 211
    Then clean succeeds

  Scenario: Timestamps at creation
    When u1 creates directories [dir1]
    Then modification time of dir1 is equal to access time
    Then status-change time of dir1 is equal to access time
    Then clean succeeds

  Scenario: Update timestamps
    When u1 creates directories [dir1]
    When sleep 1 seconds
    When u1 creates directories [dir1/dir2]
    When u1 updates [dir1] timestamps
    # aim of above step is to call touch on dir1
    # after creation of subdir access time and
    # modification time were different
    # after touch both will be updated to current time
    Then last operation succeeds
    Then modification time of dir1 is equal to access time
    Then clean succeeds

  Scenario: Access time
    When u1 creates directories [dir1]
    When sleep 1 seconds
    Then [dir] are not in ls dir1
    #aim of above step is to call ls
    Then access time of dir1 is greater than modification time
    Then access time of dir1 is greater than status-change time
    Then clean succeeds

  Scenario: Modification time
    When u1 creates directories [dir1]
    When sleep 1 seconds
    # call sleep, to be sure that time of above and below operations is different
    When u1 creates directories [dir1/dir2]
    Then modification time of dir1 is greater than access time
    Then modification time of dir1 is equal to status-change time
    Then clean succeeds

  Scenario: Status-change time when renaming
    When u1 creates directories [dir1]
    When sleep 1 seconds
    # call sleep, to be sure that time of above and below operations is different
    When u1 renames dir1 to dir2
    Then status-change time of dir2 is greater than modification time
    Then status-change time of dir2 is greater than access time
    Then clean succeeds

  Scenario: Status-change time when changing mode
    When u1 creates directories [dir1]
    When sleep 1 seconds
    # call sleep, to be sure that time of above and below operations is different
    When u1 changes dir1 mode to 211
    Then status-change time of dir1 is greater than modification time
    Then status-change time of dir1 is greater than access time
    Then clean succeeds
