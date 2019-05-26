Feature: Multi_regular_file_stat

  Background:
    Given environment is up
    And [u1, u2] start oneclients [client1, client2] in
      [/home/u1/onedata, /home/u2/onedata] on client_hosts
      [client-host1, client-host2] respectively,
      using [token, token]

  Scenario: Check file type when empty
    When u1 creates regular files [s1/file1] on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    Then u2 checks using shell stat if file type of s1/file1 is regular empty file on client2

  Scenario: Check file type when non-empty
    When u2 creates regular files [s1/file1] on client2
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    And u2 writes "TEST TEXT ONEDATA" to s1/file1 on client2
    Then file type of u1's s1/file1 is regular on client1

  Scenario: Check default access permissions
    When u1 creates regular files [s1/file1] on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    Then mode of u2's s1/file1 is 664 on client2

  Scenario: Change access permissions
    When u1 creates regular files [s1/file1] on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    And u1 changes s1/file1 mode to 211 on client1
    Then mode of u2's s1/file1 is 211 on client2

  Scenario: Increase regular file size
    # truncate
    When u1 creates regular files [s1/file1] on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    And u1 changes s1/file1 size to 1000000 bytes on client1
    Then size of u2's s1/file1 is 1000000 bytes on client2

  Scenario: Decrease regular file size
    # truncate
    When u1 creates regular files [s1/file1] on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    And u1 changes s1/file1 size to 1000000 bytes on client1
    And size of u2's s1/file1 is 1000000 bytes on client2
    And u1 changes s1/file1 size to 0 bytes on client1
    Then size of u2's s1/file1 is 0 bytes on client2

  Scenario: Truncate regular file without write permission
    When u1 creates directories [s1/dir1] on client1
    And u1 creates regular files [s1/dir1/file1] on client1
    And u1 sees [file1] in s1/dir1 on client1
    And u2 sees [file1] in s1/dir1 on client2
    And u1 changes s1/dir1/file1 mode to 644 on client1
    And mode of u2's s1/dir1/file1 is 644 on client2
    And u2 fails to change s1/dir1/file1 size to 1000000 bytes on client2

  Scenario: Timestamps at creation
    When u1 creates regular files [s1/file1] on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    Then modification time of u2's s1/file1 is equal to access time on client2
    And status-change time of u2's s1/file1 is equal to access time on client2

  Scenario: Update timestamps without write permission
    # touch dir1/file1
    When u1 creates directories [s1/dir1] on client1
    And u1 creates regular files [s1/dir1/file1] on client1
    And u1 sees [file1] in s1/dir1 on client1
    And u2 sees [file1] in s1/dir1 on client2
    And u1 changes s1/dir1/file1 mode to 644 on client1
    And mode of u2's s1/dir1/file1 is 644 on client2
    And u2 fails to update [s1/dir1/file1] timestamps on client2

  Scenario: Update timestamps with write permission
    # touch dir1/file1
    When u1 creates directories [s1/dir1] on client1
    And u1 creates regular files [s1/dir1/file1] on client1
    And u1 sees [file1] in s1/dir1 on client1
    And u2 sees [file1] in s1/dir1 on client2
    And u1 changes s1/dir1/file1 mode to 624 on client1
    And mode of u2's s1/dir1/file1 is 624 on client2
    And u2 updates [s1/dir1/file1] timestamps on client2
    Then modification time of u2's s1/dir1/file1 is equal to access time on client2

  Scenario: Access time
    When u1 writes "TEST TEXT ONEDATA" to s1/file1 on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    And u1 waits 2 second
    # call sleep, to be sure that time of write and read is different
    Then u1 reads "TEST TEXT ONEDATA" from file s1/file1 on client1
    And access time of u2's s1/file1 is greater than modification time on client2
    And access time of u2's s1/file1 is greater than status-change time on client2

  Scenario: Modification time
    When u1 creates regular files [s1/file1] on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    And u1 waits 2 second
    # call sleep, to be sure that time of above and below operations is different
    And u1 writes "TEST TEXT ONEDATA" to s1/file1 on client1
    Then modification time of u2's s1/file1 is greater than access time on client2
    And modification time of u2's s1/file1 is equal to status-change time on client2

  Scenario: Status-change time when changing mode
    When u1 creates regular files [s1/file1] on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    And u1 waits 2 second
    # call sleep, to be sure that time of above and below operations is different
    And u1 changes s1/file1 mode to 211 on client1
    Then mode of u2's s1/file1 is 211 on client2
    And status-change time of u2's s1/file1 is greater than modification time on client2
    And status-change time of u2's s1/file1 is greater than access time on client2

  Scenario: Status-change time when renaming on posix storage
    When u1 creates regular files [s1/file1] on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    And u2 records [s1/file1] stats on client2
    And u1 waits 2 second
    # call sleep, to be sure that time of above and below operations is different
    And u1 renames s1/file1 to s1/file2 on client1
    Then u2 sees [file2] in s1 on client2
    And access time of u2's s1/file2 is equal to recorded one of s1/file1
    And modification time of u2's s1/file2 is equal to access time on client2
    And status-change time of u2's s1/file2 is not less than access time on client2

  Scenario: Status-change time when renaming on nonposix storage
    When u1 creates regular files [s1/file1] on client1
    And u1 sees [file1] in s1 on client1
    And u2 sees [file1] in s1 on client2
    And u2 records [s1/file1] stats on client2
    And u1 waits 2 second
    # call sleep, to be sure that time of above and below operations is different
    And u1 renames s1/file1 to s1/file2 on client1
    Then u2 sees [file2] in s1 on client2
    And access time of u2's s1/file2 is greater than recorded one of s1/file1
    And modification time of u2's s1/file2 is equal to access time on client2
    And status-change time of u2's s1/file2 is not less than access time on client2
