@CHECKOUT
Feature: Checkout Process (Happy Path)
  As a customer
  I want to complete the checkout process
  So that I can purchase products from my shopping cart

  Background:
    Given I navigate to the Magento login page
    And I login with valid credentials

  @FUNCTIONAL @SMOKE @RUN
  Scenario: Complete checkout process with dummy data
    Given I select the "Men - Tops - Tanks" product category
    And I select the 4th product
    And I configure product options if needed
      | size | color | quantity |
      | L    | Any   | 1        |    
    And I add the product to cart
    And I select the "Men - Bottoms - Shorts" product category
    And I select the 3nd product
    And I configure product options if needed
      | size | color | quantity |
      | Any  | Any   | 3        |
    And I add the product to cart
    And I am on the shopping cart page
    When I proceed to checkout
    And I fill out all required shipping information with dummy data if no address is already filled
    And I select a shipping method
    And I continue to payment section
    And I select a payment method
    And I place the order
    Then I should see the order confirmation page
    And I should see the order number displayed 