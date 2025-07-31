@LOGIN
Feature: User Login
  As a customer
  I want to be able to login to the Magento e-commerce website
  So that I can access my account and make purchases

  @FUNCTIONAL @SMOKE
  Scenario: Successful login with valid credentials
    Given I navigate to the Magento login page
    When I login with valid credentials
    Then I should be redirected to the main page
    And I should see the logout button or username confirming active session 