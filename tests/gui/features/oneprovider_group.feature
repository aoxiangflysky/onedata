Feature: Oneprovider Group functionality
  Various operations on groups


  # assuming there is user1
  # assuming there is p1
  Background:
    Given user opens a Onezone URL in a web browser
    And user clicks on the "indigo" login button
    And user clicks on the "user1" link
    And user expands the "go to your files" Onezone sidebar panel
    And user clicks on the "p1" provider in Onezone providers sidebar panel
    And user clicks on the "Go to your files" button in provider popup
    And user clicks on the "groups" tab in main menu sidebar

  Scenario: User can add new group
    Given valid name string
    When user clicks on the "Create" button in groups sidebar
    And user sees that input box in "Create a new group" modal is active
    And user types given name on keyboard
    And user presses enter on keyboard
    Then user sees that the new item has appeared on the groups list

  # assuming there is group1
  Scenario: User can invite other user
    Given there is a "group1" item on the groups list
    When user clicks a settings icon displayed for "group1" item on the groups list
    And user sees a settings dropdown menu for "group1" item on the groups list
    And user clicks on the "INVITE USER" item in current settings dropdown
    And user sees that token box in "Invite user to the group" modal is active
    Then user sees non-empty token in active modal

  # assuming there is group1
  Scenario: User can invite group
    Given there is a "group1" item on the groups list
    When user clicks a settings icon displayed for "group1" item on the groups list
    And user sees a settings dropdown menu for "group1" item on the groups list
    And user clicks on the "INVITE GROUP" item in current settings dropdown
    And user sees that token box in "Invite group to the group" modal is active
    Then user sees non-empty token in active modal

  # assuming there is group1
  Scenario: User can request space creation
    Given there is a "group1" item on the groups list
    When user clicks a settings icon displayed for "group1" item on the groups list
    And user sees a settings dropdown menu for "group1" item on the groups list
    And user clicks on the "REQUEST SPACE CREATION" item in current settings dropdown
    And user sees that token box in "Request space creation for the group" modal is active
    Then user sees non-empty token in active modal

  # assuming there is group1
  Scenario: User can try to join space with incorrect token
    Given there is a "group1" item on the groups list
    When user clicks a settings icon displayed for "group1" item on the groups list
    And user sees a settings dropdown menu for "group1" item on the groups list
    And user clicks on the "JOIN SPACE" item in current settings dropdown
    And user sees that input box in "Join a space" modal is active
    And user types "helloworld" on keyboard
    And user presses enter on keyboard
    Then user sees an error notify with text matching to: .*join.*group1.*space.*

  # assuming there is group1
  Scenario: User can try to join as subgroup with incorrect token
    Given there is a "group1" item on the groups list
    When user clicks a settings icon displayed for "group1" item on the groups list
    And user sees a settings dropdown menu for "group1" item on the groups list
    And user clicks on the "JOIN AS SUBGROUP" item in current settings dropdown
    And user sees that input box in "Join a group to group" modal is active
    And user types "helloworld" on keyboard
    And user presses enter on keyboard
    Then user sees an error notify with text matching to: .*join.*group1.*subgroup.*

  Scenario: Try join to group with incorrect token
    When user clicks on the "Join" button in groups sidebar
    And user sees that input box in "Join a group" modal is active
    And user types "helloworld" on keyboard
    And user presses enter on keyboard
    Then user sees an error notify with text matching to: .*failed.*join.*group.*

  # assuming there is group1
  Scenario: User can rename existing group and then rename it back
    Given there is a "group1" item on the groups list
    When user clicks a settings icon displayed for "group1" item on the groups list
    And user sees a settings dropdown menu for "group1" item on the groups list
    And user clicks on the "RENAME" item in current settings dropdown
    And user sees that input box in "Rename a group" modal is active
    And user types "NewNameGroup" on keyboard
    And user presses enter on keyboard
    And user sees an info notify with text matching to: .*group1.*renamed.*NewNameGroup.*
    Then user sees that the "NewNameGroup" has appeared on the groups list
    And user should not see modal with title "Rename a group"
    And user clicks a settings icon displayed for "NewNameGroup" item on the groups list
    And user sees a settings dropdown menu for "NewNameGroup" item on the groups list
    And user clicks on the "RENAME" item in current settings dropdown
    And user sees that input box in "Rename a group" modal is active
    And user types "group1" on keyboard
    And user presses enter on keyboard
    And user sees an info notify with text matching to: .*NewNameGroup.*renamed.*group1.*

  # assuming there is group1
  Scenario: User can leave existing group and then create group with the same name
    Given there is a "group1" item on the groups list
    When user clicks a settings icon displayed for "group1" item on the groups list
    And user sees a settings dropdown menu for "group1" item on the groups list
    And user clicks on the "LEAVE THIS GROUP" item in current settings dropdown
    And user clicks "YES" confirmation button in displayed modal
    Then user sees an info notify with text matching to: .*group1.*left
    And user should not see modal with title "Leave the group"
    And user refreshes site
    And user clicks on the "Create" button in groups sidebar
    And user sees that input box in "Create a new group" modal is active
    And user types "group1" on keyboard
    And user presses enter on keyboard
    And user sees that the "group1" has appeared on the groups list
