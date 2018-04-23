Feature: Directory_CRUD

  Background:
    Given environment is up
    And u1 starts oneclient in /home/u1/onedata using token

  Scenario: Create directory
    When u1 creates directories [s1/dir1, s1/dir2, s1/dir3]
    Then u1 can stat [dir1, dir2, dir3] in s1
    Then u1 sees [dir1, dir2, dir3] in s1

  Scenario: Create directory in spaces directory
    Then u1 fails to create directories [dir]

  Scenario: Create space
    Then u1 fails to create directories [s1]

  Scenario: Rename directory
    When u1 creates directories [s1/dir1]
    And u1 renames s1/dir1 to s1/dir2
    Then u1 can stat [dir2] in s1
    And u1 can't stat [dir1] in s1
    And u1 sees [dir2] in s1
    And u1 doesn't see [dir1] in s1

  Scenario: Delete empty directory
    When u1 creates directories [s1/dir1]
    Then u1 can stat [dir1] in s1
    And u1 sees [dir1] in s1
    And u1 deletes empty directories [s1/dir1]
    And u1 can't stat [dir1] in s1
    And u1 doesn't see [dir1] in s1

  Scenario: Delete space
    When u1 deletes non-empty directories [s1]
    # space directory cannot be deleted
    Then u1 can list s1

  Scenario: Child directories
    When u1 creates directory and parents [s1/dir1/child1, s1/dir1/child2, s1/dir1/child3]
    Then u1 can stat [child1, child2, child3] in s1/dir1
    Then u1 sees [child1, child2, child3] in s1/dir1

  Scenario: Child directories 2
    When u1 creates directory and parents [s1/dir1/dir2/dir3/child1, s1/dir1/dir2/child1, s1/dir1/child1]
    Then u1 can stat [dir2, child1] in s1/dir1
    And u1 can stat [dir3, child1] in s1/dir1/dir2
    And u1 can stat [child1] in s1/dir1/dir2/dir3
    Then u1 sees [dir2, child1] in s1/dir1
    And u1 sees [dir3, child1] in s1/dir1/dir2
    And u1 sees [child1] in s1/dir1/dir2/dir3

  Scenario: Duplication
    When u1 creates directories [s1/dir1]
    Then u1 fails to create directories [s1/dir1]
    
  Scenario: Delete empty directory and parents
    #rmdir -p dir1/dir2/dir3
    When u1 creates directory and parents [s1/dir1/dir2/dir3]
    And u1 sees [dir1] in s1
    And u1 sees [dir2] in s1/dir1
    And u1 sees [dir3] in s1/dir1/dir2
    And u1 deletes empty directory and parents [s1/dir1/dir2/dir3]
    Then u1 can't stat [dir1] in s1
    Then u1 doesn't see [dir1] in s1

  Scenario: Delete non-empty directory in wrong way
    #wrong way means using rmdir instead of rm -rf
    When u1 creates directories [s1/dir1, s1/dir1/child1]
    And u1 sees [dir1] in s1
    And u1 sees [child1] in s1/dir1
    Then u1 fails to delete empty directories [s1/dir1]
    #dir1 is not empty, but we use step for empty dirs
    And u1 can stat [dir1] in s1
    And u1 can stat [child1] in s1/dir1
    And u1 sees [dir1] in s1
    And u1 sees [child1] in s1/dir1

  Scenario: Delete non-empty directory
    #rm -rf dir1 dir2
    When u1 creates directory and parents [s1/dir1/child1, s1/dir1/child2, s1/dir2/dir3/child1]
    And u1 sees [dir1, dir2] in s1
    And u1 sees [child1, child2] in s1/dir1
    And u1 sees [dir3] in s1/dir2
    And u1 sees [child1] in s1/dir2/dir3
    And u1 deletes non-empty directories [s1/dir1, s1/dir2]
    Then u1 can't stat [dir1, dir2] in s1
    Then u1 doesn't see [dir1, dir2] in s1

  Scenario: Move directory
    When u1 creates directory and parents [s1/dir1/dir2/dir3, s1/dir4/dir5]
    And u1 sees [dir1, dir4] in s1
    And u1 sees [dir2] in s1/dir1
    And u1 sees [dir3] in s1/dir1/dir2
    And u1 sees [dir5] in s1/dir4
    And u1 renames s1/dir4/dir5 to s1/dir1/dir2/dir3
    Then u1 can't stat [dir5] in s1/dir4
    Then u1 doesn't see [dir5] in s1/dir4
    And u1 can stat [dir1, dir4] in s1
    And u1 can stat [dir5] in s1/dir1/dir2/dir3
    And u1 sees [dir1, dir4] in s1
    And u1 sees [dir5] in s1/dir1/dir2/dir3

  Scenario: Copy directory
    When u1 creates directory and parents [s1/dir1/dir2/dir3, s1/dir4/dir5]
    And u1 sees [dir1, dir4] in s1
    And u1 sees [dir2] in s1/dir1
    And u1 sees [dir3] in s1/dir1/dir2
    And u1 sees [dir5] in s1/dir4
    And u1 copies directory s1/dir4 to s1/dir1/dir2/dir3
    Then u1 can stat [dir5] in s1/dir4
    And u1 can stat [dir5] in s1/dir1/dir2/dir3/dir4
    Then u1 sees [dir5] in s1/dir4
    And u1 sees [dir5] in s1/dir1/dir2/dir3/dir4

  Scenario: Move directory to itself
    When u1 creates directories [s1/dir1]
    And u1 sees [dir1] in s1
    Then u1 fails to move s1/dir1 to s1/dir1 using shell command
    And u1 can stat [dir1] in s1
    And u1 sees [dir1] in s1

  Scenario: Move directory to its subtree
    When u1 creates directory and parents [s1/dir1/dir2/dir3]
    And u1 sees [dir1] in s1
    And u1 sees [dir2] in s1/dir1
    And u1 sees [dir3] in s1/dir1/dir2
    And u1 fails to rename s1/dir1 to s1/dir1/dir2/dir3
    And u1 can stat [dir1] in s1
    And u1 sees [dir1] in s1
    And u1 can't stat [dir1] in s1/dir1/dir2/dir3
    And u1 doesn't see [dir1] in s1/dir1/dir2/dir3
