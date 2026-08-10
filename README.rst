HR Hospital
===========

Hospital management addon for Odoo School.

Overview
--------

The ``hr_hospital`` addon provides a small hospital information system with:

* patient, doctor, visit, and disease/condition models,
* calendar, kanban, pivot, graph, list, search, and search panel views,
* visit reporting wizards and doctor PDF reports,
* hierarchical access rights for patients, interns, doctors, managers, and administrators,
* Ukrainian translations for the addon and disease classifier records.

Installation
------------

1. Add the addon to your Odoo addons path.
2. Update the applications list in Odoo.
3. Install ``HR Hospital`` from Apps.
4. Load demo data if you want to review the sample records.

Local upgrade helper
--------------------

A helper script is bundled in the addon folder for quick upgrades during development:

.. code-block:: bash

   cd /home/velk/odoo/addons/hr_hospital
   ./upgrade_addon.sh

Optional examples:

.. code-block:: bash

   ./upgrade_addon.sh --dry-run
   ./upgrade_addon.sh --db velk_dev
   ./upgrade_addon.sh --modules hr_hospital,another_module

Security
--------

The module includes a role hierarchy with record rules and access rights tailored for the hospital workflow:

* Patient — read only their own visits.
* Intern — read and write their own visits.
* Doctor — read and write their own visits and their interns' visits.
* Manager — read all visits.
* Administrator — can remove any module data where business logic allows it.

Support files
-------------

* ``static/description/index.html`` — Odoo Apps description page.
* ``changelog.rst`` — short version history for the addon.

