@PRODUCT_BROWSING
Feature: Product Browse & Adding to Cart
  As a customer
  I want to browse products and add them to my shopping cart
  So that I can purchase items I'm interested in

  Background:
    Given I navigate to the Magento login page
    And I login with valid credentials

  @FUNCTIONAL @SMOKE
  Scenario: Add two different products to cart
    Given I remove all the products from the shopping cart if it is not empty
    And I select the "Women - Tops - Jackets" product category
    And I select the 1st product
    And I configure product options if needed
      | size | color | quantity |
      | M    | Any   | 1        |
    And I add the product to cart
    Then I should see a success message
    And the cart counter should be updated
    When I select the "Women - Bottoms - Pants" product category
    And I select the 2nd product
    And I configure product options if needed
      | size | color | quantity |
      | Any  | Any   | 1        |
    And I add the product to cart
    Then I should see a success message
    And the cart counter should show "2" items

  @FUNCTIONAL
  Scenario: Verify shopping cart contents
    Given I remove all the products from the shopping cart if it is not empty
    And I select the "Women - Tops - Jackets" product category
    And I select the 1st product
    And I configure product options if needed
      | size | color | quantity |
      | M    | Any   | 1        |
    And I add the product to cart
    When I select the "Women - Bottoms - Pants" product category
    And I select the 2nd product
    And I configure product options if needed
      | size | color | quantity |
      | Any  | Any   | 1        |
    And I add the product to cart
    And I navigate to the shopping cart page
    Then I should see the correct product names, quantities and prices in my cart
    And I should see the correct order total calculations 