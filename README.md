Table of contents
=================

   * [Description of the assigned task](#description-of-the-assigned-task)
   * [Usage](#usage)
      * [Installation](installation)

## Description of the ssigned task   
   
As a matter of proof, in this web application you can see <b>CRUD</b> pages developed with Django framework

## Task

You work for a restaurant chain, and your manager has asked you to create a small CMS for managing the information about their products.

## Database models

### Users

These are the users that will be authenticating inside the CMS for managing the data.

### Nutritional information

This table will hold the nutritional values that will be used for the products.

Fields:

*   Name
*   Unit

### Products

This table will hold the products.

Fields:

*   Name - name of the product
*   Description - description of the productName - name of the product
*   Nutritional values - each product can have multiple nutritional values (e.g. Proteins (g): 100.00 )
*   Status - Either ACTIVE or INACTIVE

## Requirements

*  Create the database models (and their related models)

  * Users (you can use the default Django model)
  * Nutritional information
  * Products

*  Create the login page for the users to authenticate inside the CMS
*  The users should not be able to manage the CMS data if they are not authenticated
*  Create the CRUD pages for the Nutritional Information

  *  List the nutritional informations 
  *  Create the nutritional informations
  *  Update the nutritional informations
  *  Delete the nutritional informations

*  Create the CRUD pages for the Products

  *  List the products
  *  Inside the list you should display the name of the product, as well as the nutritional values of that product
  *  Create the products
  *  Update the products
  *  Delete the products

*  Allow the user to filter the products

  *  This can be added on the page for listing the products
  *  The user should be able to filter the products by their name, as well as their status ( ACTIVE / INACTIVE )
  
## Usage 