Approval of user sign up
========================

This module allows manage user sign up in the system.

When a user registers, a notification is sent to the managers and they can decide whether
to approve the registration or reject it.

  .. image:: static/description/user_message.png

  .. image:: static/description/view_user_status.png

If they approve it, the system sends the new user the link to enter your password, if it
is rejected you will be Notify that your request has not been approved.

A filter was added to find the pending approval users.

  .. image:: static/description/filter_user.png

*Installation*

- Install validate_email with pip install validate_email or equivalent.

*Configuration*

 To configure this module, you need to:

   - Properly configure your outgoing email server(s).

   - Go to Settings > General Settings -> Customer Account.
     Active the option *Free sign up (B2C)*
