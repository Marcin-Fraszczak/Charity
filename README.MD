# 'Charity' app as a course project
Application for donating various items (available in Polish language, for now)

## Working app available at:
https://eurobyvelo.eu.pythonanywhere.com/

main focus of this project was to handle 5-step input form available at:

https://eurobyvelo.eu.pythonanywhere.com/add-donation/

You have to be logged in to see it work, test user credentials:

email:

chrity.user@gmail.com

password:

Testpass123

## Almost completely covered with tests:

<header>
    <div class="content">
        <h1>Coverage report:
            <span class="pc_cov">92%</span>
        </h1>
        <p class="text">
            <a class="nav" href="https://coverage.readthedocs.io">coverage.py v7.1.0</a>,
            created at 2023-01-26 15:28 +0100
        </p>
    </div>
</header>
<main id="index">
    <table class="index" data-sortable>
        <thead>
            <tr class="tablehead" title="Click to sort">
                <th class="name left" aria-sort="none" data-shortcut="n">Module</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="s">statements</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="m">missing</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="x">excluded</th>
                <th class="right" aria-sort="none" data-shortcut="c">coverage</th>
            </tr>
        </thead>
        <tbody>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_admin_py.html">app/admin.py</a></td>
                <td>52</td>
                <td>35</td>
                <td>0</td>
                <td class="right" data-ratio="17 52">33%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_apps_py.html">app/apps.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_forms_py.html">app/forms.py</a></td>
                <td>33</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="33 33">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_functions_py.html">app/functions.py</a></td>
                <td>22</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="22 22">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_models_py.html">app/models.py</a></td>
                <td>30</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="30 30">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_sendgrid_py.html">app/sendgrid.py</a></td>
                <td>12</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="12 12">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_urls_py.html">app/urls.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_5f5a17c013354698_views_py.html">app/views.py</a></td>
                <td>288</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="286 288">99%</td>
            </tr>
        </tbody>
        <tfoot>
            <tr class="total">
                <td class="name left">Total</td>
                <td>445</td>
                <td>37</td>
                <td>0</td>
                <td class="right" data-ratio="408 445">92%</td>
            </tr>
        </tfoot>
    </table>
</main>
<footer>
    <div class="content">
        <p>
            <a class="nav" href="https://coverage.readthedocs.io">coverage.py v7.1.0</a>,
            created at 2023-01-26 15:28 +0100
        </p>
    </div>
</footer>



# How to run it locally:
1. Fork the repository
2. Clone the repository to your local machine
3. Create and activate virtual environment
4. In the main folder, use command:
`pip install -r requirements.txt`
to install all needed packages
5. Go to config / settings.py and in `database` section uncomment option `3. SQLite`. Comment out both other options.
6. While in the main folder, run commands:
`python manage.py makemigrations`
`python manage.py migrate`
7. Use command `python manage.py runserver` to run development server
8. Optionally, you can use command: `python manage.py createsuperuser` to create admin entity and populate the database with example data