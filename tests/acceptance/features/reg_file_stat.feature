Feature: Regular_file_stat

  Background:
    Given environment is up
    And u1 starts oneclient in /home/u1/onedata using token

  Scenario: Check file type when empty
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    Then u1 checks using shell stat if file type of s1/file1 is regular empty file

  Scenario: Check file type when non-empty
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    And u1 writes "TEST TEXT ONEDATA" to s1/file1
    Then file type of u1's s1/file1 is regular

  Scenario: Check default access permissions
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    Then mode of u1's s1/file1 is 664

  Scenario: Change access permissions
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    And u1 changes s1/file1 mode to 211
    Then mode of u1's s1/file1 is 211

  Scenario: Increase regular file size
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    And u1 changes s1/file1 size to 1000000 bytes
    Then size of u1's s1/file1 is 1000000 bytes

  Scenario: Decrease regular file size
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    And u1 changes s1/file1 size to 1000000 bytes
    And size of u1's s1/file1 is 1000000 bytes
    And u1 changes s1/file1 size to 0 bytes
    Then size of u1's s1/file1 is 0 bytes

  Scenario: Timestamps at creation
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    Then modification time of u1's s1/file1 is equal to access time
    And status-change time of u1's s1/file1 is equal to access time

  Scenario: Update timestamps
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    And u1 updates [s1/file1] timestamps
    Then modification time of u1's s1/file1 is equal to access time

  Scenario: Access time
    When u1 writes "TEST TEXT ONEDATA" to s1/file1
    And u1 sees file1 in s1
    And u1 waits 2 second
    # call sleep, to be sure that time of write and read is different
    Then u1 reads "TEST TEXT ONEDATA" from file s1/file1
    And access time of u1's s1/file1 is greater than modification time
    And access time of u1's s1/file1 is greater than status-change time

  Scenario: Modification time
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    And u1 waits 2 second
    # call sleep, to be sure that time of above and below operations is different
    And u1 writes "TEST TEXT ONEDATA" to s1/file1
    Then modification time of u1's s1/file1 is greater than access time
    And modification time of u1's s1/file1 is equal to status-change time

  Scenario: Status-change time when changing mode
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    And u1 waits 2 second
    # call sleep, to be sure that time of above and below operations is different
    And u1 changes s1/file1 mode to 711
    Then mode of u1's s1/file1 is 711
    And status-change time of u1's s1/file1 is greater than modification time
    And status-change time of u1's s1/file1 is greater than access time

  Scenario: Status-change time when renaming
    When u1 creates regular files [s1/file1]
    And u1 sees file1 in s1
    And u1 waits 2 second
    # call sleep, to be sure that time of above and below operations is different
    And u1 renames s1/file1 to s1/file2
    Then u1 sees file2 in s1
    And u1 doesn't see file1 in s1
    And u1 waits 2 second
    And status-change time of u1's s1/file2 is equal to modification time
    And status-change time of u1's s1/file2 is equal to access time
