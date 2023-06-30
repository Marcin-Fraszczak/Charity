# 'Charity' app as a course project
Application for donating various items (available in Polish language, for now)
## Local version (best with Docker Compose)

1) Clone the repo:

    `git clone https://github.com/Marcin-Fraszczak/Charity.git`

2) Enter the main directory:

    `cd Charity/`

3) build and start the container:

    `docker compose up`
    
    It should take around 20 seconds and 120 MB of disk space. You can delete the container and the image later.
4) Objects populating database (along with users) will be displayed in the terminal.
5) Open your browser and visit:

    http://0.0.0.0:8000/
6) Use user credentials to log in:

    Username: `admin1@gmail.com`

    Password: `Testpass123`
7) Avoid using `Ctrl+C` inside the container for copying. If it happens, you can always restart the container:

    `docker restart <container_name>`
## Live version (pythonanywhere.com)
1) Visit this website:

    https://eurobyvelo.eu.pythonanywhere.com/
2) To log in use credentials:
    
    Username: `chrity.user@gmail.com`

    Password: `Testpass123`
3) Enjoy using the app.
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
