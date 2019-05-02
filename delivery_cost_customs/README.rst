Customs cost in delivery
========================

This module allows to include in the shipping methods the cost of Customs when an export is made and exceeds an indicated amount. To meet this requirement, three fields were added:

- customs_requiere: To indicate if it is necessary to add the cost of customs.

- customs_cost: The value of the customs service.

- customs_amount: Amount of order from which the customs cost is charged.

For example: The customs cost must be included when the orders exceed $ 3000. Configuration in the image:

   .. image:: static/img/config.png
