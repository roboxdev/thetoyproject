## Quick start

1. Copy `cp .env.example .env` and fill your values
1. `make ssh`
1. `python manage.py loaddata dummy_data.json`
1. Go to the link: http://thetoyproject.lvh.me:8019/admin_thetoyproject/
1. Log in using login `root` and password `rootroot`
1. Go to `Groups` and edit the `Editors` group
1. Add permission `blogging | writer | Can change the status of articles`
1. Check the app using the `writer`/`rootroot` and `editor`/`rootroot` credentials